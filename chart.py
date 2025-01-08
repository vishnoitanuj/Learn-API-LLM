import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gradio as gr
import requests
from datetime import datetime, timedelta
import time

def fetch_data(forecast_group):
    try:
        # Replace with your actual endpoint
        response = requests.get(f"http://localhost:8000/metrics/{forecast_group}")
        return pd.DataFrame(response.json())
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None

def create_plots(forecast_group):
    try:
        # Fetch data from endpoint
        df = fetch_data(forecast_group)
        if df is None:
            return None
        
        # Convert _time to datetime
        df['_time'] = pd.to_datetime(df['_time'])
        
        # Sort by time and get the latest 3 time periods
        df = df.sort_values('_time', ascending=False)
        latest_times = df['_time'].unique()[:3]
        df = df[df['_time'].isin(latest_times)].copy()
        
        # Create figure with three subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=[f"Time Period: {time}" for time in latest_times],
            specs=[[{"secondary_y": True}] for _ in range(3)],
            vertical_spacing=0.12,
            height=900
        )
        
        colors = {
            'ocw': '#1f77b4',
            'asaTarget': '#2ca02c',
            'interactionsWaiting': '#ff7f0e'
        }
        
        # Add traces for each time period
        for i, time in enumerate(latest_times, 1):
            time_data = df[df['_time'] == time]
            
            fig.add_trace(
                go.Scatter(
                    x=[time],
                    y=[time_data['ocw'].iloc[0]],
                    name=f"OCW - {time.strftime('%Y-%m-%d %H:%M')}",
                    line=dict(color=colors['ocw']),
                    showlegend=(i==1)
                ),
                row=i, col=1, secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=[time],
                    y=[time_data['asaTarget'].iloc[0]],
                    name=f"ASA Target - {time.strftime('%Y-%m-%d %H:%M')}",
                    line=dict(color=colors['asaTarget']),
                    showlegend=(i==1)
                ),
                row=i, col=1, secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(
                    x=[time],
                    y=[time_data['interactionsWaiting'].iloc[0]],
                    name=f"Interactions Waiting - {time.strftime('%Y-%m-%d %H:%M')}",
                    line=dict(color=colors['interactionsWaiting']),
                    showlegend=(i==1)
                ),
                row=i, col=1, secondary_y=True
            )
        
        # Update layout
        fig.update_layout(
            title=f"Latest Metrics - {forecast_group}",
            template="plotly_white",
            showlegend=True,
            height=900
        )
        
        # Update y-axes titles
        for i in range(1, 4):
            fig.update_yaxes(title_text="OCW & ASA Target", row=i, col=1, secondary_y=False)
            fig.update_yaxes(title_text="Interactions Waiting", row=i, col=1, secondary_y=True)
        
        return fig
    
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# Real-time Metrics Visualization")
    gr.Markdown("View the latest 3 time periods of metrics for a specific forecast group")
    
    with gr.Row():
        forecast_group = gr.Textbox(
            label="Forecast Group",
            placeholder="Enter forecast group name"
        )
        refresh_btn = gr.Button("Refresh")
    
    plot = gr.Plot()
    
    def update():
        if forecast_group.value:
            return create_plots(forecast_group.value)
        return None
    
    forecast_group.change(fn=create_plots, inputs=forecast_group, outputs=plot)
    refresh_btn.click(fn=update, outputs=plot)
    
    # Auto refresh using interval
    demo.load(fn=update, outputs=plot)

if __name__ == "__main__":
    demo.queue().launch() 