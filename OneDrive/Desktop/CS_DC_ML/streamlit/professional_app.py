import streamlit as st
import time
import random
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="🛡️ AI-Powered Secure Load Balancer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS
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
    .server-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .server-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    .attack-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 4px solid #ef4444;
        margin-bottom: 0.5rem;
    }
    .status-healthy { color: #10b981; font-weight: bold; }
    .status-warning { color: #f59e0b; font-weight: bold; }
    .status-error { color: #ef4444; font-weight: bold; }
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    .gradient-bg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'metrics' not in st.session_state:
    st.session_state.metrics = {
        'total_requests': 15234,
        'threats_blocked': 52,
        'avg_response_time': 118,
        'active_servers': 3,
        'total_servers': 3,
        'cpu_usage': 67,
        'memory_usage': 54,
        'network_throughput': 2.4,
        'uptime': '2d 14h 32m'
    }

if 'servers' not in st.session_state:
    st.session_state.servers = [
        {"name": "Server 1", "status": "healthy", "port": 8001, "active_connections": 45, "cpu": 67, "memory": 54, "uptime": "2d 14h 32m", "response_time": 95, "requests": 5234},
        {"name": "Server 2", "status": "healthy", "port": 8002, "active_connections": 38, "cpu": 45, "memory": 62, "uptime": "2d 14h 28m", "response_time": 112, "requests": 4891},
        {"name": "Server 3", "status": "healthy", "port": 8003, "active_connections": 52, "cpu": 78, "memory": 71, "uptime": "2d 14h 35m", "response_time": 87, "requests": 5109}
    ]

if 'security_events' not in st.session_state:
    st.session_state.security_events = [
        {"time": datetime.now() - timedelta(minutes=2), "type": "SQL Injection", "status": "BLOCKED", "severity": "High", "source": "192.168.1.105", "target": "/api/users"},
        {"time": datetime.now() - timedelta(minutes=5), "type": "XSS Attack", "status": "BLOCKED", "severity": "Medium", "source": "10.0.0.15", "target": "/api/search"},
        {"time": datetime.now() - timedelta(minutes=8), "type": "Path Traversal", "status": "BLOCKED", "severity": "High", "source": "172.16.0.8", "target": "/api/files"},
        {"time": datetime.now() - timedelta(minutes=12), "type": "DoS Attack", "status": "BLOCKED", "severity": "Critical", "source": "203.0.113.5", "target": "/api/health"},
        {"time": datetime.now() - timedelta(minutes=15), "type": "Command Injection", "status": "BLOCKED", "severity": "High", "source": "198.51.100.12", "target": "/api/ping"}
    ]

if 'traffic_data' not in st.session_state:
    st.session_state.traffic_data = []
    for i in range(24):
        timestamp = datetime.now() - timedelta(hours=23-i)
        st.session_state.traffic_data.append({
            'timestamp': timestamp,
            'requests': random.randint(800, 1200),
            'response_time': random.uniform(80, 150),
            'cpu_usage': random.randint(40, 80),
            'memory_usage': random.randint(50, 75)
        })

def simulate_attack():
    """Simulate various attack types"""
    attacks = [
        {"type": "SQL Injection", "pattern": "/api/users?id=1' OR '1'='1", "severity": "High"},
        {"type": "XSS Attack", "pattern": "/api/search?q=<script>alert(1)</script>", "severity": "Medium"},
        {"type": "Path Traversal", "pattern": "/api/files/../../../etc/passwd", "severity": "High"},
        {"type": "Command Injection", "pattern": "/api/ping;rm -rf /", "severity": "High"},
        {"type": "DoS Attack", "pattern": "/api/flood?size=1000000", "severity": "Critical"},
        {"type": "Brute Force", "pattern": "/api/login (multiple attempts)", "severity": "Medium"},
        {"type": "CSRF Attack", "pattern": "/api/transfer?to=attacker&amount=1000", "severity": "High"}
    ]
    
    attack = random.choice(attacks)
    blocked = random.random() > 0.05  # 95% block rate
    
    if blocked:
        st.session_state.metrics['threats_blocked'] += 1
        status = "BLOCKED"
    else:
        status = "ALLOWED"
    
    source_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    
    st.session_state.security_events.insert(0, {
        "time": datetime.now(),
        "type": attack["type"],
        "status": status,
        "severity": attack["severity"],
        "source": source_ip,
        "target": attack["pattern"][:50] + "..." if len(attack["pattern"]) > 50 else attack["pattern"]
    })
    
    st.session_state.security_events = st.session_state.security_events[:15]
    return blocked

def generate_traffic():
    """Generate normal traffic"""
    endpoints = ['/api/users', '/api/products', '/api/orders', '/api/dashboard', '/api/search', '/api/analytics']
    
    for i in range(10):
        endpoint = random.choice(endpoints)
        response_time = random.uniform(50, 200)
        
        st.session_state.metrics['total_requests'] += 1
        st.session_state.metrics['avg_response_time'] = int((st.session_state.metrics['avg_response_time'] + response_time) / 2)
        
        # Update random server
        server = random.choice(st.session_state.servers)
        server['active_connections'] = max(0, server['active_connections'] + random.randint(-2, 3))
        server['cpu'] = min(100, max(20, server['cpu'] + random.randint(-5, 8)))
        server['memory'] = min(100, max(30, server['memory'] + random.randint(-3, 6)))
        server['requests'] += 1

def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 2rem;'>
            <h2>🛡️ Control Panel</h2>
            <p>AI-Powered Load Balancer</p>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.selectbox("📊 Navigate", [
            "🏠 Dashboard", 
            "🖥️ Servers", 
            "🛡️ Security", 
            "📈 Analytics",
            "⚙️ Settings"
        ])
        
        st.markdown("---")
        
        # Quick Actions
        st.subheader("🚀 Quick Actions")
        
        if st.button("🌐 Generate Traffic", type="primary"):
            with st.spinner("Generating traffic..."):
                generate_traffic()
                st.success("Traffic generated!")
                time.sleep(1)
                st.rerun()
        
        if st.button("🔥 Simulate Attack", type="secondary"):
            with st.spinner("Simulating attack..."):
                blocked = simulate_attack()
                if blocked:
                    st.success("Attack blocked by AI! 🛡️")
                else:
                    st.error("Attack bypassed security! ⚠️")
                time.sleep(1)
                st.rerun()
        
        if st.button("🔄 Refresh All", type="secondary"):
            st.rerun()
        
        st.markdown("---")
        
        # System Info
        st.subheader("ℹ️ System Info")
        st.markdown(f"""
        **Status**: 🟢 Online  
        **Uptime**: {st.session_state.metrics['uptime']}  
        **Version**: 2.0.0  
        **Last Update**: {datetime.now().strftime('%H:%M:%S')}
        """)
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        st.markdown('<div class="main-header">🏠 Real-Time Dashboard</div>', unsafe_allow_html=True)
        
        # Key Metrics
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
        
        # System Performance
        st.markdown("---")
        st.header("📊 System Performance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="gradient-bg">
                <h4>💻 CPU Usage</h4>
                <h2>{st.session_state.metrics['cpu_usage']}%</h2>
                <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 10px; margin-top: 1rem;">
                    <div style="background: white; width: {st.session_state.metrics['cpu_usage']}%; height: 10px; border-radius: 10px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="gradient-bg">
                <h4>🧠 Memory Usage</h4>
                <h2>{st.session_state.metrics['memory_usage']}%</h2>
                <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 10px; margin-top: 1rem;">
                    <div style="background: white; width: {st.session_state.metrics['memory_usage']}%; height: 10px; border-radius: 10px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="gradient-bg">
                <h4>🌐 Network Throughput</h4>
                <h2>{st.session_state.metrics['network_throughput']} GB/s</h2>
                <p>Peak: 3.2 GB/s</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent Activity
        st.markdown("---")
        st.header("📈 Recent Activity")
        
        if st.session_state.traffic_data:
            recent_data = st.session_state.traffic_data[-8:]
            times = [entry['timestamp'].strftime('%H:%M') for entry in recent_data]
            requests = [entry['requests'] for entry in recent_data]
            
            chart_data = {
                'Time': times,
                'Requests': requests
            }
            st.bar_chart(chart_data, x="Time", y="Requests")
    
    elif page == "🖥️ Servers":
        st.markdown('<div class="main-header">🖥️ Server Management</div>', unsafe_allow_html=True)
        
        # Server Overview
        st.header("📊 Server Overview")
        
        server_cols = st.columns(3)
        for i, server in enumerate(st.session_state.servers):
            with server_cols[i]:
                status_color = "#10b981" if server["status"] == "healthy" else "#ef4444"
                
                st.markdown(f"""
                <div class="server-card">
                    <h3>🖥️ {server['name']}</h3>
                    <p class="status-healthy">Status: {server['status'].upper()}</p>
                    <p>Port: {server['port']}</p>
                    <p>Connections: {server['active_connections']}</p>
                    <p>CPU: {server['cpu']}%</p>
                    <p>Memory: {server['memory']}%</p>
                    <p>Response Time: {server['response_time']}ms</p>
                    <p>Requests: {server['requests']:,}</p>
                    <p>Uptime: {server['uptime']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Server Performance
        st.markdown("---")
        st.header("📈 Performance Metrics")
        
        performance_data = {
            'Server': [s['name'] for s in st.session_state.servers],
            'CPU Usage': [s['cpu'] for s in st.session_state.servers],
            'Memory Usage': [s['memory'] for s in st.session_state.servers],
            'Response Time': [s['response_time'] for s in st.session_state.servers]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💻 CPU & Memory Usage")
            cpu_mem_data = {
                'Server': [s['name'] for s in st.session_state.servers],
                'CPU': [s['cpu'] for s in st.session_state.servers],
                'Memory': [s['memory'] for s in st.session_state.servers]
            }
            st.bar_chart(cpu_mem_data, x="Server", y=["CPU", "Memory"])
        
        with col2:
            st.subheader("⚡ Response Times")
            response_data = {
                'Server': [s['name'] for s in st.session_state.servers],
                'Response Time (ms)': [s['response_time'] for s in st.session_state.servers]
            }
            st.bar_chart(response_data, x="Server", y="Response Time (ms)")
    
    elif page == "🛡️ Security":
        st.markdown('<div class="main-header">🛡️ Security Center</div>', unsafe_allow_html=True)
        
        # Security Overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🛡️ Threats Blocked", st.session_state.metrics['threats_blocked'], "↑ 12%")
        
        with col2:
            st.metric("🔥 Active Attacks", random.randint(0, 3), "Real-time")
        
        with col3:
            st.metric("📊 Security Score", "94.7%", "Excellent")
        
        with col4:
            st.metric("🚨 Critical Events", random.randint(0, 2), "Last 24h")
        
        # Recent Security Events
        st.markdown("---")
        st.header("🚨 Recent Security Events")
        
        for event in st.session_state.security_events:
            severity_color = {
                "High": "#ef4444",
                "Medium": "#f59e0b",
                "Critical": "#991b1b",
                "Low": "#10b981"
            }.get(event["severity"], "#6b7280")
            
            status_color = "#ef4444" if event["status"] == "BLOCKED" else "#f59e0b"
            time_str = event["time"].strftime('%H:%M:%S') if isinstance(event["time"], datetime) else event["time"]
            
            st.markdown(f"""
            <div class="attack-card">
                <strong>{time_str}</strong> - {event['type']}<br>
                <span style="color: {status_color}; font-weight: bold;">{event['status']}</span>
                <span style="float: right; color: {severity_color}; font-weight: bold;">Severity: {event['severity']}</span><br>
                <span style="color: #64748b;">Source: {event['source']}</span>
                <span style="float: right; color: #64748b;">Target: {event['target']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "📈 Analytics":
        st.markdown('<div class="main-header">📈 Traffic Analytics</div>', unsafe_allow_html=True)
        
        # Traffic Trends
        st.header("📊 Traffic Trends")
        
        if st.session_state.traffic_data:
            recent_data = st.session_state.traffic_data[-24:]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🌐 Request Volume")
                times = [entry['timestamp'].strftime('%H:%M') for entry in recent_data]
                requests = [entry['requests'] for entry in recent_data]
                
                traffic_chart = {
                    'Time': times,
                    'Requests': requests
                }
                st.line_chart(traffic_chart, x="Time", y="Requests")
            
            with col2:
                st.subheader("⚡ Response Times")
                response_times = [entry['response_time'] for entry in recent_data]
                
                response_chart = {
                    'Time': times,
                    'Response Time (ms)': response_times
                }
                st.line_chart(response_chart, x="Time", y="Response Time (ms)")
        
        # Performance Analytics
        st.markdown("---")
        st.header("💻 Performance Analytics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📈 Peak Requests", "1,247", "Today")
            st.metric("📉 Avg Response", "118ms", "Optimal")
            st.metric("🎯 Success Rate", "99.7%", "Excellent")
        
        with col2:
            st.metric("💾 Bandwidth Used", "2.4 GB/s", "75% capacity")
            st.metric("🔄 Cache Hit Rate", "87.3%", "Good")
            st.metric("📊 Error Rate", "0.3%", "Low")
        
        with col3:
            st.metric("🌍 Active Users", "1,234", "Live now")
            st.metric("📱 Mobile Traffic", "34%", "Growing")
            st.metric("🖥️ Desktop Traffic", "66%", "Stable")
    
    elif page == "⚙️ Settings":
        st.markdown('<div class="main-header">⚙️ System Settings</div>', unsafe_allow_html=True)
        
        st.header("🔧 Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🛡️ Security Settings")
            ai_security = st.checkbox("🤖 AI Security", value=True)
            auto_block = st.checkbox("🚫 Auto-block Threats", value=True)
            log_level = st.selectbox("📝 Log Level", ["INFO", "WARNING", "ERROR", "CRITICAL"])
            
            st.subheader("⚖️ Load Balancing")
            algorithm = st.selectbox("🔄 Algorithm", ["Round Robin", "Least Connections", "IP Hash", "Weighted"])
            health_check = st.slider("🏥 Health Check Interval", 10, 300, 30)
        
        with col2:
            st.subheader("📊 Monitoring")
            auto_refresh = st.checkbox("🔄 Auto-refresh", value=False)
            refresh_interval = st.slider("⏱️ Refresh Interval", 5, 60, 10)
            enable_alerts = st.checkbox("🚨 Enable Alerts", value=True)
            
            st.subheader("🌐 Network")
            max_connections = st.slider("🔗 Max Connections", 100, 10000, 1000)
            timeout = st.slider("⏰ Request Timeout", 1, 60, 5)
        
        if st.button("💾 Save Settings", type="primary"):
            st.success("Settings saved successfully!")
            time.sleep(1)
            st.rerun()

if __name__ == "__main__":
    main()
