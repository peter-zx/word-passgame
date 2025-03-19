# 使用官方 Python 镜像作为基础
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖清单并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露 Flask 默认端口
EXPOSE 5000

# 运行应用
CMD ["python", "main.py"]