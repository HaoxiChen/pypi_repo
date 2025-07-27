#!/bin/bash
# PyPI Repository Startup Script

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

# 检查依赖
check_dependencies() {
    log_info "Checking dependencies..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 is not installed"
        exit 1
    fi
    
    # 检查pip
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3 is not installed"
        exit 1
    fi
    
    # 检查supervisor
if ! command -v supervisord &> /dev/null; then
    log_warning "Supervisor is not installed, installing..."
    # 使用系统包管理器安装supervisor
    if command -v apt &> /dev/null; then
        sudo apt install supervisor -y
    elif command -v yum &> /dev/null; then
        sudo yum install supervisor -y
    else
        log_error "Cannot install supervisor automatically. Please install it manually."
        exit 1
    fi
fi
    
    log_success "Dependencies check completed"
}

# 安装Python依赖
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        # 检查虚拟环境是否存在
        if [ -d "venv" ]; then
            log_info "Using existing virtual environment"
            source venv/bin/activate
            pip install -r requirements.txt
            log_success "Python dependencies installed in virtual environment"
        else
            log_info "Creating new virtual environment"
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
            log_success "Python dependencies installed in new virtual environment"
        fi
    else
        log_warning "requirements.txt not found, skipping Python dependencies installation"
    fi
}

# 创建必要的目录和文件
setup_directories() {
    log_info "Setting up directories and files..."
    
    # 创建日志目录
    mkdir -p logs
    
    # 创建包目录（如果不存在）
    mkdir -p packages
    
    # 设置文件权限
    chmod +x app.py
    chmod +x monitor.py
    
    log_success "Directories and files setup completed"
}

# 检查服务状态
check_service_status() {
    log_info "Checking service status..."
    
    if [ -f "app.pid" ]; then
        SERVICE_PID=$(cat app.pid)
        if kill -0 $SERVICE_PID 2>/dev/null; then
            if curl -s http://localhost:8385/health > /dev/null 2>&1; then
                log_success "Service is already running (PID: $SERVICE_PID)"
                return 0
            else
                log_warning "Service process exists but not responding"
                return 1
            fi
        else
            log_warning "Service process not found"
            return 1
        fi
    else
        log_info "Service is not running"
        return 1
    fi
}

# 启动服务
start_service() {
    log_info "Starting PyPI repository service..."
    
    # 激活虚拟环境并启动服务
    if [ -d "venv" ]; then
        source venv/bin/activate
        log_info "Starting service with virtual environment..."
        
        # 启动Flask应用（模块化架构）
        log_info "Starting with modular architecture (app.py)"
        nohup python app.py > pypi_repo.log 2>&1 &
        SERVICE_PID=$!
        echo $SERVICE_PID > app.pid
        
        # 等待服务启动
        sleep 3
        
        # 检查服务状态
        if curl -s http://localhost:8385/health > /dev/null 2>&1; then
            log_success "Service started successfully (PID: $SERVICE_PID)"
        else
            log_error "Service failed to start"
            exit 1
        fi
    else
        log_error "Virtual environment not found"
        exit 1
    fi
}

# 启动监控
start_monitor() {
    log_info "Starting monitor in background..."
    
    # 创建日志目录
    mkdir -p logs
    
    # 激活虚拟环境并启动监控脚本
    if [ -d "venv" ]; then
        source venv/bin/activate
        nohup python monitor.py > logs/monitor.log 2>&1 &
        MONITOR_PID=$!
        echo $MONITOR_PID > monitor.pid
        
        log_success "Monitor started with PID: $MONITOR_PID"
    else
        log_warning "Virtual environment not found, skipping monitor"
    fi
}

# 显示服务信息
show_service_info() {
    log_info "Service Information:"
    echo "  - Repository URL: http://localhost:8385"
    echo "  - Health Check: http://localhost:8385/health"
    echo "  - Statistics: http://localhost:8385/stats"
    echo ""
    log_info "Management Commands:"
    echo "  - Check status: ps aux | grep app.py"
    echo "  - Restart service: ./stop.sh && ./start.sh"
    echo "  - Stop service: ./stop.sh"
    echo "  - View logs: tail -f pypi_repo.log"
    echo "  - View monitor logs: tail -f logs/monitor.log"
    echo "  - Architecture: Modular (app.py)"
    echo ""
    log_info "To stop the service, run: ./stop.sh"
}

# 主函数
main() {
    echo "=========================================="
    echo "    PyPI Repository Startup Script"
    echo "=========================================="
    echo ""
    
    # 检查是否已经运行
    if check_service_status; then
        log_warning "Service is already running"
        show_service_info
        exit 0
    fi
    
    # 执行启动步骤
    check_dependencies
    install_python_deps
    setup_directories
    start_service
    start_monitor
    
    echo ""
    log_success "PyPI repository service started successfully!"
    echo ""
    show_service_info
}

# 运行主函数
main "$@" 