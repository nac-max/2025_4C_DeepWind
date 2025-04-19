FROM python:3.10

WORKDIR /app

COPY requirements.txt .

# 升级pip并配置国内镜像源
RUN pip install --upgrade pip && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 安装依赖
RUN pip install -r requirements.txt

# 确保gunicorn已安装
RUN pip install gunicorn==21.2.0

COPY . .

# 添加可执行权限到entrypoint.sh
RUN chmod +x entrypoint.sh

EXPOSE 8000

# 使用entrypoint.sh作为入口点
ENTRYPOINT ["/app/entrypoint.sh"] 