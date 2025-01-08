import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gradio as gr
import os

# Define the path to your CSV file
CSV_PATH = "data.csv"  # Update this path to your CSV file location

def create_plot(forecast_group):
    try:
        # Read the CSV file from local path
        df = pd.read_csv(CSV_PATH)
        
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

def get_forecast_groups():
    try:
        df = pd.read_csv(CSV_PATH)
        return list(df['primaryWorkgroup'].unique())
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return []

# Create Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("# Time Series Visualization")
    gr.Markdown("Select a forecast group to view its metrics")
    
    # Get forecast groups once
    groups = get_forecast_groups()
    default_group = groups[0] if groups else None
    
    forecast_group = gr.Dropdown(
        label="Forecast Group",
        choices=groups,
        value=default_group,
        interactive=True
    )
    
    plot_output = gr.Plot(label="Visualization", value=create_plot(default_group) if default_group else None)
    
    forecast_group.change(
        fn=create_plot,
        inputs=forecast_group,
        outputs=plot_output
    )

if __name__ == "__main__":
    # Verify CSV file exists
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        print("Please update the CSV_PATH variable with the correct path to your CSV file")
    else:
        iface.launch() 