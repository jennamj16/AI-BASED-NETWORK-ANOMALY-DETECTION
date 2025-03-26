from flask import Blueprint, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import traceback

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    try:
        # Check if file exists
        if not os.path.exists('data/network_logs_with_anomalies.csv'):
            return "<h2>No data file found. Waiting for data collection...</h2>"

        # Read the anomaly data
        df = pd.read_csv('data/network_logs_with_anomalies.csv')
        
        if df.empty:
            return "<h2>No data available. Please ensure the system is capturing traffic.</h2>"

        # Ensure columns exist
        required_columns = ['ip_address', 'bytes_sent', 'bytes_received', 'connections', 'anomaly']
        if not all(col in df.columns for col in required_columns):
            return "<h2>Data format incorrect. Missing required columns.</h2>"

        # Configure the static plot layout
        static_layout = dict(
            dragmode=False,
            showlegend=True,
            modebar_remove=[
                'zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
                'hoverCompareCartesian', 'toggleSpikelines', 'toImage'
            ]
        )

        # 1. Anomaly Distribution
        fig1 = px.pie(values=[sum(df['anomaly'] == 1), sum(df['anomaly'] == -1)],
                     names=['Normal', 'Anomaly'],
                     title='Anomaly Distribution')
        fig1.update_layout(**static_layout)

        # 2. Traffic Volume
        fig2 = px.histogram(df, x='bytes_sent',
                          title='Traffic Volume Distribution')
        fig2.update_layout(**static_layout)

        # Create stats summary
        stats = {
            'Total Packets': len(df),
            'Anomalies Detected': sum(df['anomaly'] == -1),
            'Average Bytes Sent': f"{df['bytes_sent'].mean():.2f}"
        }

        return render_template('dashboard.html', 
                             plot1=fig1.to_html(full_html=False, config={'displayModeBar': False}),
                             plot2=fig2.to_html(full_html=False, config={'displayModeBar': False}),
                             stats=stats)

    except Exception as e:
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return f"<pre>An error occurred:\n{error_msg}</pre>" 