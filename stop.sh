#!/bin/bash
# PyPI Repository Stop Script

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 停止监控
stop_monitor() {
    log_info "Stopping monitor..."
    
    if [ -f "monitor.pid" ]; then
        MONITOR_PID=$(cat monitor.pid)
        if kill -0 $MONITOR_PID 2>/dev/null; then
            kill $MONITOR_PID
            log_success "Monitor stopped (PID: $MONITOR_PID)"
        else
            log_warning "Monitor process not found (PID: $MONITOR_PID)"
        fi
        rm -f monitor.pid
    else
        log_warning "Monitor PID file not found"
    fi
}

# 停止服务
stop_service() {
    log_info "Stopping PyPI repository service..."
    
    if [ -f "app.pid" ]; then
        SERVICE_PID=$(cat app.pid)
        if kill -0 $SERVICE_PID 2>/dev/null; then
            kill $SERVICE_PID
            log_success "Service stopped (PID: $SERVICE_PID)"
        else
            log_warning "Service process not found (PID: $SERVICE_PID)"
        fi
        rm -f app.pid
    else
        log_warning "Service PID file not found"
    fi
}

# 清理进程
cleanup_processes() {
    log_info "Cleaning up processes..."
    
    # 查找并停止相关的Python进程
    PIDS=$(pgrep -f "python3.*app.py\|python3.*monitor.py" || true)
    if [ ! -z "$PIDS" ]; then
        for pid in $PIDS; do
            log_info "Stopping process $pid"
            kill $pid 2>/dev/null || true
        done
        log_success "Process cleanup completed"
    else
        log_info "No related processes found"
    fi
}

# 清理文件
cleanup_files() {
    log_info "Cleaning up temporary files..."
    
    # 删除PID文件
    rm -f app.pid
    rm -f monitor.pid
    
    log_success "File cleanup completed"
}

# 显示状态
show_status() {
    log_info "Current Status:"
    
    # 检查服务状态
    if [ -f "app.pid" ]; then
        SERVICE_PID=$(cat app.pid)
        if kill -0 $SERVICE_PID 2>/dev/null; then
            if curl -s http://localhost:8385/health > /dev/null 2>&1; then
                echo "  - Service: Running (PID: $SERVICE_PID)"
            else
                echo "  - Service: Process running but not responding"
            fi
        else
            echo "  - Service: Stopped"
        fi
    else
        echo "  - Service: Not running"
    fi
    
    # 检查监控状态
    if [ -f "monitor.pid" ]; then
        MONITOR_PID=$(cat monitor.pid)
        if kill -0 $MONITOR_PID 2>/dev/null; then
            echo "  - Monitor: Running (PID: $MONITOR_PID)"
        else
            echo "  - Monitor: Stopped"
        fi
    else
        echo "  - Monitor: Not running"
    fi
}

# 主函数
main() {
    echo "=========================================="
    echo "    PyPI Repository Stop Script"
    echo "=========================================="
    echo ""
    
    # 显示当前状态
    show_status
    echo ""
    
    # 停止服务
    stop_monitor
    stop_service
    cleanup_processes
    cleanup_files
    
    echo ""
    log_success "PyPI repository service stopped successfully!"
    echo ""
    log_info "To start the service again, run: ./start.sh"
}

# 运行主函数
main "$@" 