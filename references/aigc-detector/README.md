# AI 文本检测助手

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://hub.docker.com)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

类似朱雀AI的检测助手，使用 Qwen 大模型进行文本来源判别和AI痕迹分析。支持详细的检测报告和交互式痕迹标记。

## 功能
- **AI文本检测**：输入文本，调用 Qwen 模型进行全面AI生成分析
  - 输出标签（人类/AI/不确定）、置信度、判断置信度级别
  - **详细分析报告**：提供多维度分析（语言模式、内容结构、写作风格、统计特征）
  - **关键指标识别**：列出最重要的AI判断依据
  - **方法论说明**：解释使用的检测算法和判断流程
  - **自动标记AI痕迹**：检测完成后自动分析并高亮显示AI特征
- **AI痕迹标记**：独立分析文本，标记出潜在的AI生成特征
  - **逐行分析**：保持原始文本格式，对每行分别进行AI痕迹检测
  - **交互式详情**：点击标记可查看详细的AI判定理由和解释
  - 支持多种痕迹类型：词语重复、过长行、正式表达、复杂句式等
- **Web 前端展示**：现代化的 Ant Design 界面，支持标签页切换

## 运行

### 后端
1. 安装依赖：`pip install -r backend/requirements.txt`
2. 配置环境变量：复制 `backend/.env.example` 为 `.env`，填入 DashScope API Key
3. 运行：`uvicorn app.main:app --reload --port 8000`

### 前端
1. 安装依赖：`npm install`
2. 配置环境变量：复制 `frontend/.env.example` 为 `.env`
3. 开发：`npm run dev`（代理到后端）
4. 构建：`npm run build`

## API 接口

### 检测接口
```
POST /api/detect
Content-Type: application/json

{
  "text": "要检测的文本内容"
}
```
返回全面的AI检测分析结果，包含：
- 基本判断（标签、分数、置信度）
- 详细分析报告（多维度特征分析）
- 关键指标列表
- 判断方法论说明
- 自动标记的AI痕迹

**返回示例**：
```json
{
  "result": {
    "label": "ai",
    "score": 0.85,
    "confidence": "high",
    "rationale": "文本表现出典型的AI生成特征",
    "detailed_analysis": "详细的分析报告...",
    "key_indicators": ["特征1", "特征2"],
    "methodology": "基于多维度特征分析的AI检测算法"
  }
}
```


### 标记AI痕迹接口
```
POST /api/mark-traces
Content-Type: application/json

{
  "text": "需要标记AI痕迹的文本"
}
```
返回带有HTML标记的文本和痕迹详情。

## 注意
- 需配置 DashScope API Key
- 文本长度限制 8000 字符
- 检测温度设为 0.2 以提高一致性
- AI模型返回严格的JSON格式，确保解析稳定性
- 包含7个标准字段：label、score、confidence、rationale、detailed_analysis、key_indicators、methodology
- AI痕迹标记基于规则引擎，不需要API调用，响应速度快
- 标记功能保持原始文本格式，逐行进行AI痕迹检测
- 标记的痕迹类型包括：词语重复、过长行、正式表达、复杂句式等

## 🚀 部署选项

### Docker 快速启动
```bash
# 克隆项目
git clone https://github.com/hoyo0210/aigc-detector.git
cd aigc-detector

# 配置环境变量
cp backend/.env.example backend/.env
# 编辑 .env 文件添加 DASHSCOPE_API_KEY

# Docker Compose 启动
docker-compose up -d

# 访问应用
# 前端: http://localhost:5173
# 后端API: http://localhost:8000
```

### 云平台部署
- **Vercel**: 前端静态部署
- **Railway**: 全栈应用部署
- **Render**: Web服务 + 静态站点
- **Fly.io**: 全球分布式部署
- **AWS EC2**: 自托管服务器

📖 详细部署指南：[DEPLOYMENT.md](DEPLOYMENT.md)

