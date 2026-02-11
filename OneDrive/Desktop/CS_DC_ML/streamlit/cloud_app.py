import streamlit as st
import time
import random
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="🚀 AI-Powered Secure Load Balancer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
        margin-bottom: 1rem;
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
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for persistent data
if 'metrics' not in st.session_state:
    st.session_state.metrics = {
        'total_requests': 15234,
        'threats_blocked': 52,
        'avg_response_time': 118,
        'active_servers': 3,
        'total_servers': 3
    }

if 'traffic_history' not in st.session_state:
    st.session_state.traffic_history = []
    # Generate initial historical data
    for i in range(24):
        timestamp = datetime.now() - timedelta(hours=23-i)
        st.session_state.traffic_history.append({
            'timestamp': timestamp,
            'requests': random.randint(800, 1200),
            'response_time': random.uniform(80, 150),
            'threats': random.randint(0, 5)
        })

if 'security_events' not in st.session_state:
    st.session_state.security_events = [
        {"time": "2 mins ago", "type": "SQL Injection", "status": "BLOCKED", "severity": "High", "source": "192.168.1.105"},
        {"time": "5 mins ago", "type": "XSS Attack", "status": "BLOCKED", "severity": "Medium", "source": "10.0.0.15"},
        {"time": "8 mins ago", "type": "Path Traversal", "status": "BLOCKED", "severity": "High", "source": "172.16.0.8"},
        {"time": "12 mins ago", "type": "DoS Attack", "status": "BLOCKED", "severity": "Critical", "source": "203.0.113.5"},
        {"time": "15 mins ago", "type": "Command Injection", "status": "BLOCKED", "severity": "High", "source": "198.51.100.12"}
    ]

if 'servers' not in st.session_state:
    st.session_state.servers = [
        {"name": "Server 1", "status": "healthy", "port": 8001, "active_connections": 45, "cpu": 67, "memory": 54, "uptime": "2d 14h 32m"},
        {"name": "Server 2", "status": "healthy", "port": 8002, "active_connections": 38, "cpu": 45, "memory": 62, "uptime": "2d 14h 28m"},
        {"name": "Server 3", "status": "healthy", "port": 8003, "active_connections": 52, "cpu": 78, "memory": 71, "uptime": "2d 14h 35m"}
    ]

def simulate_normal_traffic():
    """Simulate normal traffic generation"""
    endpoints = ['/api/users', '/api/products', '/api/orders', '/api/dashboard', '/api/search']
    
    for i in range(20):
        endpoint = random.choice(endpoints)
        response_time = random.uniform(50, 200)
        status_code = 200
        
        # Update metrics
        st.session_state.metrics['total_requests'] += 1
        st.session_state.metrics['avg_response_time'] = int(
            (st.session_state.metrics['avg_response_time'] + response_time) / 2
        )
        
        # Add to history
        current_time = datetime.now()
        if len(st.session_state.traffic_history) > 0:
            last_entry = st.session_state.traffic_history[-1]
            if (current_time - last_entry['timestamp']).seconds < 300:  # Within 5 minutes
                last_entry['requests'] += 1
                last_entry['response_time'] = (last_entry['response_time'] + response_time) / 2
            else:
                st.session_state.traffic_history.append({
                    'timestamp': current_time,
                    'requests': 1,
                    'response_time': response_time,
                    'threats': 0
                })
        else:
            st.session_state.traffic_history.append({
                'timestamp': current_time,
                'requests': 1,
                'response_time': response_time,
                'threats': 0
            })
        
        # Update server connections
        server = random.choice(st.session_state.servers)
        server['active_connections'] = max(0, server['active_connections'] + random.randint(-2, 3))
        server['cpu'] = min(100, max(20, server['cpu'] + random.randint(-5, 8)))
        server['memory'] = min(100, max(30, server['memory'] + random.randint(-3, 6)))

def simulate_attack_traffic():
    """Simulate attack traffic"""
    attacks = [
        {'type': 'SQL Injection', 'pattern': '/api/users?id=1\' OR \'1\'=\'1', 'severity': 'High'},
        {'type': 'XSS Attack', 'pattern': '/api/search?q=<script>alert(1)</script>', 'severity': 'Medium'},
        {'type': 'Path Traversal', 'pattern': '/api/files/../../../etc/passwd', 'severity': 'High'},
        {'type': 'Command Injection', 'pattern': '/api/ping;rm -rf /', 'severity': 'High'},
        {'type': 'DoS Attack', 'pattern': '/api/heavy?size=1000000', 'severity': 'Critical'}
    ]
    
    for i, attack in enumerate(attacks):
        # Simulate attack detection
        blocked = random.random() > 0.1  # 90% block rate
        
        if blocked:
            st.session_state.metrics['threats_blocked'] += 1
            status = "BLOCKED"
        else:
            status = "ALLOWED"
        
        # Add to security events
        source_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        st.session_state.security_events.insert(0, {
            "time": f"{i+1} min ago",
            "type": attack['type'],
            "status": status,
            "severity": attack['severity'],
            "source": source_ip
        })
        
        # Keep only last 10 events
        st.session_state.security_events = st.session_state.security_events[:10]

def create_traffic_chart():
    """Create traffic visualization"""
    if not st.session_state.traffic_history:
        return None
    
    # Create simple bar chart data
    recent_data = st.session_state.traffic_history[-12:]  # Last 12 entries
    times = [entry['timestamp'].strftime('%H:%M') for entry in recent_data]
    requests = [entry['requests'] for entry in recent_data]
    
    # Create chart using st.bar_chart
    chart_data = {
        'Time': times,
        'Requests': requests
    }
    
    return chart_data

def main():
    # Header with live indicator
    st.markdown("""
    <div class="main-header">
        <span class="live-indicator"></span>
        🛡️ AI-Powered Secure Load Balancer - Live Demo
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # System Status
        st.subheader("📊 System Status")
        
        if st.button("🔄 Refresh Dashboard", type="primary"):
            st.rerun()
        
        if st.button("🚀 Generate Normal Traffic", type="secondary"):
            with st.spinner("Generating normal traffic..."):
                simulate_normal_traffic()
                st.success("Normal traffic generated successfully!")
                time.sleep(1)
                st.rerun()
        
        if st.button("🔥 Simulate Attacks", type="secondary"):
            with st.spinner("Simulating security attacks..."):
                simulate_attack_traffic()
                st.success("Attack simulation completed!")
                time.sleep(1)
                st.rerun()
        
        st.divider()
        
        # Quick Links
        st.subheader("🔗 Quick Links")
        st.markdown(f"""
        **🌐 Live Dashboard**: This Streamlit App
        **📚 GitHub**: [Repository](https://github.com/Aaditya-jx/loadbalancing)
        **📖 Documentation**: [README](https://github.com/Aaditya-jx/loadbalancing/blob/main/README.md)
        **🚀 Deploy**: [Streamlit Cloud](https://share.streamlit.io/)
        """)
        
        st.divider()
        
        # Settings
        st.subheader("⚙️ Settings")
        auto_refresh = st.checkbox("🔄 Auto-refresh (10s)", value=False)
        
        if auto_refresh:
            st.session_state.auto_refresh = True
        else:
            st.session_state.auto_refresh = False
        
        st.divider()
        
        # System Info
        st.subheader("ℹ️ System Info")
        st.markdown(f"""
        **Platform**: Streamlit Cloud  
        **Status**: 🟢 Production Ready  
        **Version**: 2.0.0  
        **Last Update**: {datetime.now().strftime('%H:%M:%S')}
        """)
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌐 Total Requests</h3>
            <h1 style="color: #667eea;">{st.session_state.metrics['total_requests']:,}</h1>
            <p style="color: #64748b;">↑ {random.randint(8, 20)}% from last hour</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🛡️ Threats Blocked</h3>
            <h1 style="color: #ef4444;">{st.session_state.metrics['threats_blocked']}</h1>
            <p style="color: #64748b;">AI Security Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚡ Avg Response Time</h3>
            <h1 style="color: #10b981;">{st.session_state.metrics['avg_response_time']}ms</h1>
            <p style="color: #64748b;">Optimal performance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🖥️ Active Servers</h3>
            <h1 style="color: #3b82f6;">{st.session_state.metrics['active_servers']}/{st.session_state.metrics['total_servers']}</h1>
            <p style="color: #64748b;">All healthy</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Server Health Section
    st.markdown("---")
    st.header("🖥️ Server Health Monitoring")
    
    server_cols = st.columns(3)
    for i, server in enumerate(st.session_state.servers):
        with server_cols[i]:
            status_color = {
                "healthy": "#10b981",
                "unhealthy": "#f59e0b", 
                "unreachable": "#ef4444"
            }.get(server["status"], "#6b7280")
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>🖥️ {server['name']}</h4>
                <p class="status-healthy">Status: {server['status'].upper()}</p>
                <p>Port: {server['port']}</p>
                <p>Connections: {server['active_connections']}</p>
                <p>CPU: {server['cpu']}%</p>
                <p>Memory: {server['memory']}%</p>
                <p>Uptime: {server['uptime']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Traffic Analytics Section
    st.markdown("---")
    st.header("📈 Traffic Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📊 Traffic Volume", "⚡ Response Times", "🛡️ Security Events"])
    
    with tab1:
        st.subheader("📊 Request Volume Over Time")
        chart_data = create_traffic_chart()
        if chart_data:
            st.bar_chart(chart_data, x="Time", y="Requests")
        else:
            st.info("No traffic data available yet. Generate some traffic to see charts!")
    
    with tab2:
        st.subheader("⚡ Response Time Trends")
        if st.session_state.traffic_history:
            recent_data = st.session_state.traffic_history[-12:]
            times = [entry['timestamp'].strftime('%H:%M') for entry in recent_data]
            response_times = [entry['response_time'] for entry in recent_data]
            
            response_chart = {
                'Time': times,
                'Response Time (ms)': response_times
            }
            st.line_chart(response_chart, x="Time", y="Response Time (ms)")
        else:
            st.info("No response time data available yet!")
    
    with tab3:
        st.subheader("🛡️ Recent Security Events")
        
        for event in st.session_state.security_events:
            severity_color = {
                "High": "#ef4444",
                "Medium": "#f59e0b",
                "Critical": "#991b1b",
                "Low": "#10b981"
            }.get(event["severity"], "#6b7280")
            
            status_color = "#ef4444" if event["status"] == "BLOCKED" else "#f59e0b"
            
            st.markdown(f"""
            <div style="padding: 0.5rem; border-left: 4px solid {severity_color}; margin-bottom: 0.5rem; background: #f8fafc; border-radius: 5px;">
                <strong>{event['time']}</strong> - {event['type']}<br>
                <span style="color: {status_color}; font-weight: bold;">{event['status']}</span>
                <span style="float: right; color: #64748b;">Source: {event['source']}</span>
                <span style="float: right; color: {severity_color}; font-weight: bold; margin-right: 1rem;">Severity: {event['severity']}</span>
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
            <p>Status: 🟢 Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    with info_col2:
        st.markdown("""
        <div class="metric-card">
            <h4>⚖️ Load Balancing</h4>
            <p><strong>Algorithm:</strong> Least Connections</p>
            <p><strong>Health Check:</strong> 30s interval</p>
            <p><strong>Failover:</strong> Automatic</p>
            <p><strong>Strategy:</strong> Round Robin</p>
        </div>
        """, unsafe_allow_html=True)
    
    with info_col3:
        st.markdown("""
        <div class="metric-card">
            <h4>🌐 Deployment</h4>
            <p><strong>Platform:</strong> Streamlit Cloud</p>
            <p><strong>Services:</strong> 5 running</p>
            <p><strong>Status:</strong> Production Ready</p>
            <p><strong>Access:</strong> Worldwide</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #64748b;'>
        <strong>🚀 AI-Powered Secure Load Balancer - Cloud Dashboard</strong><br>
        Professional Real-time Monitoring & Security System<br>
        <small>Built with ❤️ using Streamlit Cloud - Accessible Worldwide</small><br>
        <small>🌍 This demo runs entirely in the cloud - no local setup required!</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh functionality
    if hasattr(st.session_state, 'auto_refresh') and st.session_state.auto_refresh:
        time.sleep(10)
        st.rerun()

if __name__ == "__main__":
    main()
