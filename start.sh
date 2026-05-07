#!/bin/bash

echo "========================================"
echo "  AI GitLab 周报助手 启动脚本"
echo "========================================"
echo

cd backend

if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python3 -m venv venv
fi

echo "正在激活虚拟环境..."
source venv/bin/activate

echo "正在安装依赖..."
pip install -r requirements.txt

echo
echo "========================================"
echo "  服务启动中..."
echo "  访问地址: http://localhost:8000"
echo "========================================"
echo

python main.py
