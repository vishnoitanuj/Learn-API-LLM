import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gradio as gr

def create_plot(csv_file, forecast_group):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Convert _time to datetime
        df['_time'] = pd.to_datetime(df['_time'])
        
        # Filter data for selected forecast group
        df = df[df['primaryWorkgroup'] == forecast_group]
        
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Color mapping for consistency
        colors = {
            'ocw': '#1f77b4',
            'asaTarget': '#2ca02c',
            'interactionsWaiting': '#ff7f0e'
        }
        
        # Add traces
        fig.add_trace(
            go.Scatter(
                x=df['_time'],
                y=df['ocw'],
                name="OCW",
                line=dict(color=colors['ocw'])
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['_time'],
                y=df['asaTarget'],
                name="ASA Target",
                line=dict(color=colors['asaTarget'])
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['_time'],
                y=df['interactionsWaiting'],
                name="Interactions Waiting",
                line=dict(color=colors['interactionsWaiting'])
            ),
            secondary_y=True
        )
        
        # Update layout
        fig.update_layout(
            title=f"Time Series Analysis - {forecast_group}",
            xaxis_title="Time",
            yaxis_title="OCW & ASA Target",
            yaxis2_title="Interactions Waiting",
            hovermode='x unified',
            showlegend=True,
            template="plotly_white",
            height=600
        )
        
        return fig
    
    except Exception as e:
        return f"Error: {str(e)}"

def get_forecast_groups(csv_file):
    try:
        df = pd.read_csv(csv_file)
        return list(df['primaryWorkgroup'].unique())
    except:
        return []

# Create Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("# Time Series Visualization")
    gr.Markdown("Select a forecast group to view its metrics")
    
    with gr.Row():
        file_input = gr.File(
            label="Upload CSV file",
            file_types=[".csv"],
            type="filepath"
        )
        forecast_group = gr.Dropdown(
            label="Forecast Group",
            choices=[],
            interactive=True
        )
    
    plot_output = gr.Plot(label="Visualization")
    
    def update_forecast_groups(csv_file):
        groups = get_forecast_groups(csv_file)
        return gr.Dropdown(choices=groups, value=groups[0] if groups else None)
    
    file_input.change(
        fn=update_forecast_groups,
        inputs=[file_input],
        outputs=[forecast_group]
    )
    
    forecast_group.change(
        fn=create_plot,
        inputs=[file_input, forecast_group],
        outputs=[plot_output]
    )

if __name__ == "__main__":
    iface.launch() 