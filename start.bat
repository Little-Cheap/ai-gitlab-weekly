@echo off
echo ========================================
echo   AI GitLab 周报助手 启动脚本
echo ========================================
echo.

cd backend

if not exist "venv" (
    echo 正在创建虚拟环境...
    python -m venv venv
)

echo 正在激活虚拟环境...
call venv\Scripts\activate

echo 正在安装依赖...
pip install -r requirements.txt

echo.
echo ========================================
echo   服务启动中...
echo   访问地址: http://localhost:8000
echo ========================================
echo.

python main.py

pause
