#!/bin/bash

# AI文本检测器一键部署脚本

set -e

echo "🚀 AI文本检测器部署脚本"
echo "==========================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose 未安装，请先安装 docker-compose"
    exit 1
fi

# 检查环境变量文件
if [ ! -f "backend/.env" ]; then
    echo "⚠️  检测到未配置环境变量文件"

    if [ -f "backend/.env.example" ]; then
        cp backend/.env.example backend/.env
        echo "✅ 已从模板创建 .env 文件"
        echo "⚠️  请编辑 backend/.env 文件，添加 DASHSCOPE_API_KEY"
        echo "   nano backend/.env  # 或使用其他编辑器"
        exit 1
    else
        echo "❌ 找不到环境变量模板文件"
        exit 1
    fi
fi

# 检查API Key是否配置
if ! grep -q "DASHSCOPE_API_KEY=sk-" backend/.env; then
    echo "⚠️  DASHSCOPE_API_KEY 似乎未正确配置"
    echo "   请确保 backend/.env 中的 DASHSCOPE_API_KEY 以 'sk-' 开头"
    exit 1
fi

echo "📦 构建和启动服务..."
docker-compose down 2>/dev/null || true
docker-compose build --no-cache
docker-compose up -d

echo "⏳ 等待服务启动..."
sleep 10

# 健康检查
echo "🏥 执行健康检查..."
if curl -f http://localhost:8000/api/health &>/dev/null; then
    echo "✅ 后端服务启动成功"
else
    echo "❌ 后端服务启动失败"
    echo "   查看日志: docker-compose logs backend"
    exit 1
fi

echo ""
echo "🎉 部署完成！"
echo "==============="
echo "🌐 前端应用: http://localhost:5173"
echo "🔌 后端API:   http://localhost:8000"
echo "📊 API文档:   http://localhost:8000/docs"
echo ""
echo "常用命令:"
echo "  docker-compose logs -f          # 查看实时日志"
echo "  docker-compose down             # 停止服务"
echo "  docker-compose restart          # 重启服务"
echo ""
echo "如需停止服务，请运行: docker-compose down"
