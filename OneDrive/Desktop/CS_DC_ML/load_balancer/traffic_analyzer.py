"""
Traffic Feature Analyzer
Extracts features from HTTP requests for AI-based intrusion detection
"""

import time
import hashlib
import re
from typing import Dict, Any
from urllib.parse import urlparse, parse_qs
import ipaddress

class TrafficFeatureExtractor:
    def __init__(self):
        self.request_count = 0
        self.ip_request_counts = {}
        self.last_reset_time = time.time()
        
    def extract_features(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract NSL-KDD style features from HTTP request"""
        features = {}
        
        # Basic connection features
        features['duration'] = 0  # HTTP is stateless, duration is typically 0
        features['protocol_type'] = 'tcp'  # HTTP uses TCP
        features['service'] = 'http'  # HTTP service
        
        # Extract flag based on request characteristics
        features['flag'] = self._extract_flag(request_data)
        
        # Byte transfer features
        features['src_bytes'] = len(str(request_data.get('body', '')))
        features['dst_bytes'] = 0  # Will be updated after response
        
        # Basic TCP flags (simplified for HTTP)
        features['land'] = 0  # Land attack detection
        features['wrong_fragment'] = 0
        features['urgent'] = 0
        
        # Hot indicators
        features['hot'] = self._calculate_hot_indicators(request_data)
        
        # Failed login attempts
        features['num_failed_logins'] = self._count_failed_logins(request_data)
        
        # Login status
        features['logged_in'] = self._check_login_status(request_data)
        
        # Compromised conditions
        features['num_compromised'] = 0
        features['root_shell'] = 0
        features['su_attempted'] = 0
        features['num_root'] = 0
        
        # File access indicators
        features['num_file_creations'] = self._count_file_operations(request_data, 'create')
        features['num_shells'] = 0
        features['num_access_files'] = self._count_file_operations(request_data, 'access')
        features['num_outbound_cmds'] = 0
        
        # Host login indicators
        features['is_host_login'] = 0
        features['is_guest_login'] = self._check_guest_login(request_data)
        
        # Network-level statistics (simulated)
        client_ip = request_data.get('client_ip', '127.0.0.1')
        features.update(self._calculate_network_stats(client_ip))
        
        # Host-level statistics (simulated)
        features.update(self._calculate_host_stats(client_ip))
        
        return features
    
    def _extract_flag(self, request_data: Dict[str, Any]) -> str:
        """Extract connection flag based on request characteristics"""
        method = request_data.get('method', 'GET')
        status_code = request_data.get('status_code', 200)
        headers = request_data.get('headers', {})
        
        # Check for suspicious patterns
        user_agent = headers.get('user-agent', '').lower()
        suspicious_patterns = ['bot', 'crawler', 'scanner', 'sqlmap', 'nikto']
        
        if any(pattern in user_agent for pattern in suspicious_patterns):
            return 'REJ'  # Rejected
        
        if status_code >= 400:
            return 'RSTR'  # Connection reset
            
        if method in ['GET', 'POST', 'PUT', 'DELETE']:
            return 'SF'  # Normal connection
        
        return 'SF'  # Default to normal
    
    def _calculate_hot_indicators(self, request_data: Dict[str, Any]) -> int:
        """Calculate hot indicators (suspicious activities)"""
        hot_count = 0
        
        # Check for SQL injection patterns
        body = str(request_data.get('body', '')).lower()
        sql_patterns = ['union select', 'drop table', 'insert into', 'delete from', 'exec(']
        if any(pattern in body for pattern in sql_patterns):
            hot_count += 1
        
        # Check for XSS patterns
        xss_patterns = ['<script', 'javascript:', 'onerror=', 'onload=']
        if any(pattern in body for pattern in xss_patterns):
            hot_count += 1
        
        # Check for path traversal
        path = request_data.get('path', '').lower()
        traversal_patterns = ['../', '..\\', '%2e%2e%2f', '%2e%2e\\']
        if any(pattern in path for pattern in traversal_patterns):
            hot_count += 1
        
        # Check for command injection
        cmd_patterns = ['; cat', '; ls', '| whoami', '`id`', '$()']
        if any(pattern in body for pattern in cmd_patterns):
            hot_count += 1
        
        return hot_count
    
    def _count_failed_logins(self, request_data: Dict[str, Any]) -> int:
        """Count failed login attempts (simplified)"""
        path = request_data.get('path', '').lower()
        status_code = request_data.get('status_code', 200)
        
        # Check if this is a login endpoint and failed
        if 'login' in path and status_code == 401:
            return 1
        
        return 0
    
    def _check_login_status(self, request_data: Dict[str, Any]) -> int:
        """Check if user is logged in"""
        headers = request_data.get('headers', {})
        auth_header = headers.get('authorization', '')
        
        # Simple check for presence of authorization
        if auth_header:
            return 1
        
        # Check for session cookie
        cookies = headers.get('cookie', '')
        if 'session' in cookies.lower() or 'token' in cookies.lower():
            return 1
        
        return 0
    
    def _count_file_operations(self, request_data: Dict[str, Any], operation: str) -> int:
        """Count file operations in request"""
        path = request_data.get('path', '').lower()
        body = str(request_data.get('body', '')).lower()
        
        file_operations = {
            'create': ['upload', 'create', 'write', 'save'],
            'access': ['download', 'read', 'open', 'view']
        }
        
        count = 0
        for op in file_operations.get(operation, []):
            count += path.count(op)
            count += body.count(op)
        
        return min(count, 5)  # Cap at 5 to avoid extreme values
    
    def _check_guest_login(self, request_data: Dict[str, Any]) -> int:
        """Check if guest login is being used"""
        headers = request_data.get('headers', {})
        user_agent = headers.get('user-agent', '').lower()
        
        guest_indicators = ['guest', 'anonymous', 'public']
        if any(indicator in user_agent for indicator in guest_indicators):
            return 1
        
        return 0
    
    def _calculate_network_stats(self, client_ip: str) -> Dict[str, float]:
        """Calculate network-level statistics"""
        current_time = time.time()
        
        # Update request counts
        self.request_count += 1
        self.ip_request_counts[client_ip] = self.ip_request_counts.get(client_ip, 0) + 1
        
        # Reset counters periodically
        if current_time - self.last_reset_time > 60:  # Reset every minute
            self.ip_request_counts.clear()
            self.last_reset_time = current_time
        
        # Calculate statistics
        ip_requests = self.ip_request_counts.get(client_ip, 0)
        total_ips = len(self.ip_request_counts)
        
        # Simulate network statistics
        features = {}
        
        # Connection counts
        features['count'] = min(ip_requests, 100)  # Cap to prevent extreme values
        features['srv_count'] = min(ip_requests // 2, 50)
        
        # Error rates (simulated based on request patterns)
        features['serror_rate'] = 0.1 if ip_requests > 20 else 0.05
        features['srv_serror_rate'] = features['serror_rate']
        features['rerror_rate'] = 0.05 if ip_requests > 30 else 0.02
        features['srv_rerror_rate'] = features['rerror_rate']
        
        # Service distribution
        features['same_srv_rate'] = 0.8 if ip_requests < 10 else 0.6
        features['diff_srv_rate'] = 1 - features['same_srv_rate']
        features['srv_diff_host_rate'] = 0.1 if total_ips > 5 else 0.05
        
        return features
    
    def _calculate_host_stats(self, client_ip: str) -> Dict[str, float]:
        """Calculate host-level statistics"""
        ip_requests = self.ip_request_counts.get(client_ip, 0)
        total_ips = len(self.ip_request_counts)
        
        features = {}
        
        # Host connection counts
        features['dst_host_count'] = min(total_ips * 2, 200)
        features['dst_host_srv_count'] = min(ip_requests, 100)
        
        # Host service distribution
        features['dst_host_same_srv_rate'] = 0.7 if ip_requests < 15 else 0.5
        features['dst_host_diff_srv_rate'] = 1 - features['dst_host_same_srv_rate']
        features['dst_host_same_src_port_rate'] = 0.9  # HTTP typically uses port 80/443
        features['dst_host_srv_diff_host_rate'] = 0.2 if total_ips > 3 else 0.1
        
        # Host error rates
        features['dst_host_serror_rate'] = 0.08 if ip_requests > 25 else 0.04
        features['dst_host_srv_serror_rate'] = features['dst_host_serror_rate']
        features['dst_host_rerror_rate'] = 0.06 if ip_requests > 35 else 0.03
        features['dst_host_srv_rerror_rate'] = features['dst_host_rerror_rate']
        
        return features
    
    def reset_counters(self):
        """Reset internal counters"""
        self.request_count = 0
        self.ip_request_counts.clear()
        self.last_reset_time = time.time()
