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
        
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add traces
        fig.add_trace(
            go.Scatter(
                x=df['_time'],
                y=df['ocw'],
                name="OCW",
                line=dict(color='#1f77b4')
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['_time'],
                y=df['asaTarget'],
                name="ASA Target",
                line=dict(color='#2ca02c')
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['_time'],
                y=df['interactionsWaiting'],
                name="Interactions Waiting",
                line=dict(color='#ff7f0e')
            ),
            secondary_y=True
        )
        
        # Update layout
        fig.update_layout(
            title="Time Series Analysis",
            xaxis_title="Time",
            yaxis_title="OCW & ASA Target",
            yaxis2_title="Interactions Waiting",
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
    description="Upload a CSV file with columns: _time, ocw, asaTarget, and interactionsWaiting",
    examples=[],
    cache_examples=False
)

if __name__ == "__main__":
    iface.launch() 