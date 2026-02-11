// Dashboard JavaScript Utilities

class DashboardUtils {
    static formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }
    
    static formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    static formatUptime(seconds) {
        const days = Math.floor(seconds / 86400);
        const hours = Math.floor((seconds % 86400) / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        
        if (days > 0) {
            return `${days}d ${hours}h ${minutes}m`;
        } else if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else {
            return `${minutes}m`;
        }
    }
    
    static getSeverityColor(severity) {
        const colors = {
            'critical': '#ef4444',
            'high': '#f59e0b',
            'medium': '#3b82f6',
            'low': '#10b981',
            'info': '#6b7280'
        };
        return colors[severity.toLowerCase()] || colors.info;
    }
    
    static getStatusColor(status) {
        return status ? '#10b981' : '#ef4444';
    }
    
    static animateValue(element, start, end, duration) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            element.textContent = this.formatNumber(Math.floor(current));
            
            if (current >= end) {
                clearInterval(timer);
            }
        }, 16);
    }
    
    static createNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.css = {
            'top': '20px',
            'right': '20px',
            'z-index': '9999',
            'min-width': '300px',
            'box-shadow': '0 4px 12px rgba(0,0,0,0.15)',
            'border-radius': '8px',
            'backdrop-filter': 'blur(10px)'
        };
        notification.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <span>${message}</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert">
                    <span>&times;</span>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after duration
        setTimeout(() => {
            notification.remove();
        }, duration);
    }
    
    static showLoading(element, message = 'Loading...') {
        element.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">${message}</span>
                </div>
                <p class="mt-2 text-muted">${message}</p>
            </div>
        `;
    }
    
    static hideLoading(element) {
        element.innerHTML = '';
    }
    
    static copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.createNotification('Copied to clipboard!', 'success', 2000);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    }
    
    static exportToCSV(data, filename) {
        const csv = this.convertToCSV(data);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }
    
    static convertToCSV(data) {
        if (!data.length) return '';
        
        const headers = Object.keys(data[0]);
        const csvHeaders = headers.join(',');
        const csvRows = data.map(row => 
            headers.map(header => `"${row[header] || ''}"`).join(',')
        );
        
        return [csvHeaders, ...csvRows].join('\n');
    }
    
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    func(...args);
                }, wait);
            };
            if (!timeout) {
                executedFunction(...args);
            } else {
                clearTimeout(timeout);
                timeout = later();
            }
        };
    }
    
    static throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// Chart utilities
class ChartUtils {
    static createGradient(ctx, color1, color2) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, color1);
        gradient.addColorStop(1, color2);
        return gradient;
    }
    
    static defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    font: {
                        size: 12,
                        weight: '500'
                    }
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: '#ddd',
                borderWidth: 1,
                cornerRadius: 4,
                displayColors: false,
                intersect: false,
                mode: 'index',
                position: 'nearest'
            }
        },
        scales: {
            x: {
                grid: {
                    display: true,
                    color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.7)'
                }
            },
            y: {
                grid: {
                    display: true,
                    color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.7)'
                }
            }
        }
    };
    
    static lineChartOptions = {
        ...this.defaultOptions,
        elements: {
            line: {
                tension: 0.4
            },
            point: {
                radius: 4,
                hoverRadius: 6
            }
        }
    };
    
    static barChartOptions = {
        ...this.defaultOptions,
        elements: {
            bar: {
                borderRadius: 6,
                borderWidth: 2
            }
        }
    };
}

// Performance monitoring
class PerformanceMonitor {
    constructor() {
        this.metrics = {
            pageLoadTime: performance.now(),
            domContentLoaded: false,
            renderTime: 0,
            networkLatency: 0,
            memoryUsage: 0
        };
        
        this.init();
    }
    
    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.metrics.domContentLoaded = true;
                this.metrics.pageLoadTime = performance.now();
            });
        }
        
        // Monitor network performance
        this.monitorNetworkPerformance();
        
        // Monitor memory usage (if available)
        this.monitorMemoryUsage();
        
        // Report performance metrics
        this.reportPerformance();
    }
    
    monitorNetworkPerformance() {
        if (window.performance && window.performance.getEntriesByType) {
            const navigationEntries = performance.getEntriesByType('navigation');
            if (navigationEntries.length > 0) {
                const navTiming = navigationEntries[0];
                this.metrics.networkLatency = navTiming.responseStart - navTiming.requestStart;
                this.metrics.renderTime = navTiming.loadEventEnd - navTiming.loadEventStart;
            }
        }
    }
    
    monitorMemoryUsage() {
        if (performance.memory) {
            this.metrics.memoryUsage = performance.memory.usedJSHeapSize;
        }
    }
    
    reportPerformance() {
        const metrics = this.metrics;
        const renderTime = metrics.renderTime || (performance.now() - metrics.pageLoadTime);
        
        console.log('Performance Metrics:', {
            pageLoadTime: metrics.pageLoadTime.toFixed(2) + 'ms',
            domContentLoaded: metrics.domContentLoaded,
            renderTime: renderTime.toFixed(2) + 'ms',
            networkLatency: metrics.networkLatency.toFixed(2) + 'ms',
            memoryUsage: DashboardUtils.formatBytes(metrics.memoryUsage)
        });
        
        // Show performance warning if slow
        if (renderTime > 3000) {
            DashboardUtils.createNotification('Page load time is slow. Consider optimizing assets.', 'warning');
        }
    }
}

// Initialize performance monitoring
const performanceMonitor = new PerformanceMonitor();

// Global error handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    DashboardUtils.createNotification('An unexpected error occurred. Please refresh the page.', 'danger');
});

// Global unhandled promise rejection handling
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    DashboardUtils.createNotification('An unexpected error occurred. Please refresh the page.', 'danger');
});

// Export utilities for global use
window.DashboardUtils = DashboardUtils;
window.ChartUtils = ChartUtils;
window.PerformanceMonitor = PerformanceMonitor;
