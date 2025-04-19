#!/bin/bash

# 等待MySQL服务启动
echo "等待MySQL服务启动..."
sleep 10

# 执行数据库迁移
echo "执行数据库迁移..."
python manage.py migrate

# 启动Django应用
echo "启动Django应用..."
# 确保使用绝对路径调用gunicorn或使用python -m
python -m gunicorn WPF_Backend.wsgi:application --bind 0.0.0.0:8000 