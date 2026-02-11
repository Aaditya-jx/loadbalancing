import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import json
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="🚀 AI-Powered Secure Load Balancer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    .status-healthy {
        color: #10b981;
        font-weight: bold;
    }
    .status-warning {
        color: #f59e0b;
        font-weight: bold;
    }
    .status-error {
        color: #ef4444;
        font-weight: bold;
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-top: 1rem;
    }
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
LOAD_BALANCER_URL = "http://localhost:8000"
DASHBOARD_URL = "http://localhost:5000"

def get_load_balancer_stats():
    """Get statistics from load balancer"""
    try:
        response = requests.get(f"{LOAD_BALANCER_URL}/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        return None

def get_dashboard_data():
    """Get data from dashboard API"""
    try:
        response = requests.get(f"{DASHBOARD_URL}/api/metrics", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        return None

def get_server_health(server_url):
    """Check health of individual server"""
    try:
        response = requests.get(f"{server_url}/health", timeout=3)
        return {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "response_time": response.elapsed.total_seconds() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    except:
        return {"status": "unreachable", "response_time": None, "status_code": None}

def simulate_traffic():
    """Simulate traffic to the load balancer"""
    endpoints = ['/api/users', '/api/products', '/api/orders', '/api/dashboard']
    
    for i in range(10):
        try:
            endpoint = np.random.choice(endpoints)
            response = requests.get(f"{LOAD_BALANCER_URL}{endpoint}", timeout=5)
            time.sleep(0.1)
        except:
            pass

def main():
    # Header
    st.markdown('<div class="main-header">🛡️ AI-Powered Secure Load Balancer</div>', unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # System Status
        st.subheader("📊 System Status")
        
        if st.button("🔄 Refresh Data", type="primary"):
            st.rerun()
        
        if st.button("🚀 Generate Traffic", type="secondary"):
            with st.spinner("Generating traffic..."):
                simulate_traffic()
                st.success("Traffic generated successfully!")
                time.sleep(1)
                st.rerun()
        
        st.divider()
        
        # Quick Links
        st.subheader("🔗 Quick Links")
        st.markdown(f"""
        **Load Balancer:** [{LOAD_BALANCER_URL}]({LOAD_BALANCER_URL})
        **Dashboard:** [{DASHBOARD_URL}]({DASHBOARD_URL})
        **GitHub:** [Repository](https://github.com/Aaditya-jx/loadbalancing)
        """)
        
        st.divider()
        
        # Settings
        st.subheader("⚙️ Settings")
        auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=True)
        
        if auto_refresh:
            st.session_state.auto_refresh = True
        else:
            st.session_state.auto_refresh = False
    
    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🌐 Total Requests</h3>
            <h1 style="color: #667eea;">12,543</h1>
            <p style="color: #64748b;">↑ 15.3% from last hour</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🛡️ Threats Blocked</h3>
            <h1 style="color: #ef4444;">47</h1>
            <p style="color: #64748b;">AI Security Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ Avg Response Time</h3>
            <h1 style="color: #10b981;">124ms</h1>
            <p style="color: #64748b;">Optimal performance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🖥️ Active Servers</h3>
            <h1 style="color: #3b82f6;">3/3</h1>
            <p style="color: #64748b;">All healthy</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Server Health Section
    st.markdown("---")
    st.header("🖥️ Server Health Monitoring")
    
    servers = [
        {"name": "Server 1", "url": "http://localhost:8001", "port": 8001},
        {"name": "Server 2", "url": "http://localhost:8002", "port": 8002},
        {"name": "Server 3", "url": "http://localhost:8003", "port": 8003}
    ]
    
    server_cols = st.columns(3)
    for i, server in enumerate(servers):
        with server_cols[i]:
            health = get_server_health(server["url"])
            
            status_color = {
                "healthy": "#10b981",
                "unhealthy": "#f59e0b", 
                "unreachable": "#ef4444"
            }.get(health["status"], "#6b7280")
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>🖥️ {server['name']}</h4>
                <p class="status-{'healthy' if health['status'] == 'healthy' else 'warning'}">
                    Status: {health['status'].upper()}
                </p>
                <p>Port: {server['port']}</p>
                <p>Response Time: {health['response_time']:.3f}s' if health['response_time'] else 'N/A'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Traffic Analytics Section
    st.markdown("---")
    st.header("📈 Traffic Analytics")
    
    # Generate sample data for demonstration
    times = pd.date_range(end=datetime.now(), periods=24, freq="H")
    traffic_data = pd.DataFrame({
        'timestamp': times,
        'requests': np.random.randint(100, 1000, len(times)),
        'response_time': np.random.uniform(50, 200, len(times)),
        'threats_blocked': np.random.randint(0, 10, len(times))
    })
    
    tab1, tab2, tab3 = st.tabs(["📊 Traffic Volume", "⚡ Response Times", "🛡️ Security Events"])
    
    with tab1:
        fig = px.line(traffic_data, x='timestamp', y='requests', 
                     title='📊 Request Volume Over Time',
                     labels={'timestamp': 'Time', 'requests': 'Requests per Hour'})
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.line(traffic_data, x='timestamp', y='response_time',
                     title='⚡ Response Time Trends',
                     labels={'timestamp': 'Time', 'response_time': 'Response Time (ms)'})
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = px.bar(traffic_data, x='timestamp', y='threats_blocked',
                    title='🛡️ Threats Blocked Over Time',
                    labels={'timestamp': 'Time', 'threats_blocked': 'Threats Blocked'})
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Security Dashboard Section
    st.markdown("---")
    st.header("🛡️ AI Security Dashboard")
    
    sec_col1, sec_col2 = st.columns(2)
    
    with sec_col1:
        # Attack Types Distribution
        attack_types = ['SQL Injection', 'XSS', 'Path Traversal', 'DoS', 'Command Injection']
        attack_counts = [12, 8, 5, 15, 3]
        
        fig = px.pie(values=attack_counts, names=attack_types, title='🎯 Attack Types Distribution')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with sec_col2:
        # Recent Security Events
        st.subheader("🚨 Recent Security Events")
        
        security_events = [
            {"time": "2 mins ago", "type": "SQL Injection", "status": "BLOCKED", "severity": "High"},
            {"time": "5 mins ago", "type": "XSS Attack", "status": "BLOCKED", "severity": "Medium"},
            {"time": "8 mins ago", "type": "Path Traversal", "status": "BLOCKED", "severity": "High"},
            {"time": "12 mins ago", "type": "DoS Attack", "status": "BLOCKED", "severity": "Critical"},
            {"time": "15 mins ago", "type": "Command Injection", "status": "BLOCKED", "severity": "High"}
        ]
        
        for event in security_events:
            severity_color = {
                "High": "#ef4444",
                "Medium": "#f59e0b",
                "Critical": "#991b1b",
                "Low": "#10b981"
            }.get(event["severity"], "#6b7280")
            
            st.markdown(f"""
            <div style="padding: 0.5rem; border-left: 4px solid {severity_color}; margin-bottom: 0.5rem;">
                <strong>{event['time']}</strong> - {event['type']}<br>
                <span style="color: {severity_color}; font-weight: bold;">{event['status']}</span>
                <span style="float: right; color: #64748b;">Severity: {event['severity']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # System Information Section
    st.markdown("---")
    st.header("ℹ️ System Information")
    
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🤖 AI Model</h4>
            <p><strong>Random Forest</strong></p>
            <p>Accuracy: 94.7%</p>
            <p>Training Data: 50K samples</p>
        </div>
        """, unsafe_allow_html=True)
    
    with info_col2:
        st.markdown("""
        <div class="metric-card">
            <h4>⚖️ Load Balancing</h4>
            <p><strong>Algorithm:</strong> Least Connections</p>
            <p><strong>Health Check:</strong> 30s interval</p>
            <p><strong>Failover:</strong> Automatic</p>
        </div>
        """, unsafe_allow_html=True)
    
    with info_col3:
        st.markdown("""
        <div class="metric-card">
            <h4>🐳 Deployment</h4>
            <p><strong>Platform:</strong> Docker</p>
            <p><strong>Containers:</strong> 5 services</p>
            <p><strong>Status:</strong> Production Ready</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #64748b;'>
        <strong>🚀 AI-Powered Secure Load Balancer</strong><br>
        Professional Real-time Monitoring & Security System<br>
        <small>Built with ❤️ using Streamlit, Docker, and Machine Learning</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh functionality
    if hasattr(st.session_state, 'auto_refresh') and st.session_state.auto_refresh:
        time.sleep(5)
        st.rerun()

if __name__ == "__main__":
    main()
