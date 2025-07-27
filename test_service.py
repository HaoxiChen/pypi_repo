#!/usr/bin/env python3
"""
PyPI Repository Service Test Script
"""

import requests
import time
import json
import sys
from pathlib import Path

def test_health_check(base_url):
    """测试健康检查"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data.get('status')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_stats(base_url):
    """测试统计信息"""
    print("📊 Testing stats endpoint...")
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Stats retrieved:")
            print(f"   - Packages: {data.get('packages_count')}")
            print(f"   - Files: {data.get('files_count')}")
            print(f"   - Total Size: {data.get('total_size_mb')} MB")
            print(f"   - Uptime: {data.get('uptime_hours', 0):.1f} hours")
            return True
        else:
            print(f"❌ Stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Stats error: {e}")
        return False

def test_main_page(base_url):
    """测试主页面"""
    print("🏠 Testing main page...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Main page accessible")
            return True
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main page error: {e}")
        return False

def test_package_page(base_url, package_name):
    """测试包页面"""
    print(f"📦 Testing package page for {package_name}...")
    try:
        response = requests.get(f"{base_url}/{package_name}/", timeout=10)
        if response.status_code == 200:
            print(f"✅ Package page for {package_name} accessible")
            return True
        else:
            print(f"❌ Package page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Package page error: {e}")
        return False

def test_package_download(base_url, package_name, filename):
    """测试包文件下载"""
    print(f"⬇️ Testing package download: {filename}...")
    try:
        response = requests.get(f"{base_url}/{package_name}/{filename}", timeout=30)
        if response.status_code == 200:
            content_length = len(response.content)
            print(f"✅ Package download successful: {content_length} bytes")
            return True
        else:
            print(f"❌ Package download failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Package download error: {e}")
        return False

def test_pip_compatibility(base_url):
    """测试pip兼容性"""
    print("🐍 Testing pip compatibility...")
    try:
        # 测试Simple Repository API格式
        response = requests.get(f"{base_url}/simple/", timeout=10)
        if response.status_code == 200:
            print("✅ Simple Repository API accessible")
            return True
        else:
            print(f"❌ Simple Repository API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Simple Repository API error: {e}")
        return False

def main():
    """主测试函数"""
    base_url = "http://localhost:8385"
    
    print("🚀 Starting PyPI Repository Service Tests")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ Waiting for service to start...")
    time.sleep(5)
    
    tests = []
    
    # 运行测试
    tests.append(test_health_check(base_url))
    tests.append(test_stats(base_url))
    tests.append(test_main_page(base_url))
    tests.append(test_package_page(base_url, "payo-cli"))
    
    # 测试包文件下载
    package_files = [
        "payo_cli-1.0.0-py3-none-any.whl",
        "payo_cli-1.0.0.tar.gz"
    ]
    
    for filename in package_files:
        tests.append(test_package_download(base_url, "payo-cli", filename))
    
    tests.append(test_pip_compatibility(base_url))
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("📋 Test Results Summary")
    print("=" * 50)
    
    passed = sum(tests)
    total = len(tests)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Service is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the service logs.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 