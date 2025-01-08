import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gradio as gr

def create_plot(csv_file):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Convert _time to datetime
        df['_time'] = pd.to_datetime(df['_time'])
        
        # Get unique forecast groups
        forecast_groups = df['forecastGroup'].unique()
        
        # Create figure with subplots for each forecast group
        fig = make_subplots(
            rows=len(forecast_groups), 
            cols=1,
            subplot_titles=[f"Forecast Group: {fg}" for fg in forecast_groups],
            specs=[[{"secondary_y": True}] for _ in forecast_groups],
            vertical_spacing=0.1,
            height=400 * len(forecast_groups)  # Adjust height based on number of groups
        )
        
        # Color mapping for consistency
        colors = {
            'ocw': '#1f77b4',
            'asaTarget': '#2ca02c',
            'interactionsWaiting': '#ff7f0e'
        }
        
        # Add traces for each forecast group
        for i, fg in enumerate(forecast_groups, 1):
            fg_data = df[df['forecastGroup'] == fg]
            
            fig.add_trace(
                go.Scatter(
                    x=fg_data['_time'],
                    y=fg_data['ocw'],
                    name=f"OCW",
                    line=dict(color=colors['ocw']),
                    showlegend=(i==1)  # Show legend only for first subplot
                ),
                row=i, col=1, secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=fg_data['_time'],
                    y=fg_data['asaTarget'],
                    name=f"ASA Target",
                    line=dict(color=colors['asaTarget']),
                    showlegend=(i==1)
                ),
                row=i, col=1, secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=fg_data['_time'],
                    y=fg_data['interactionsWaiting'],
                    name=f"Interactions Waiting",
                    line=dict(color=colors['interactionsWaiting']),
                    showlegend=(i==1)
                ),
                row=i, col=1, secondary_y=True
            )
            
            # Update axes titles for each subplot
            fig.update_yaxes(title_text="OCW & ASA Target", row=i, col=1, secondary_y=False)
            fig.update_yaxes(title_text="Interactions Waiting", row=i, col=1, secondary_y=True)
        
        # Update layout
        fig.update_layout(
            title="Time Series Analysis by Forecast Group",
            xaxis_title="Time",
            hovermode='x unified',
            showlegend=True,
            template="plotly_white"
        )
        
        return fig
    
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
iface = gr.Interface(
    fn=create_plot,
    inputs=[
        gr.File(
            label="Upload CSV file",
            file_types=[".csv"],
            type="filepath"
        )
    ],
    outputs=gr.Plot(),
    title="Time Series Visualization",
    description="Upload a CSV file with columns: _time, ocw, asaTarget, interactionsWaiting, and forecastGroup"
)

if __name__ == "__main__":
    iface.launch() 