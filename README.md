# AI GitLab 周报助手

一个基于 FastAPI + Kimi AI 的智能周报生成工具，能够自动从 GitLab 获取代码提交记录，并通过 AI 生成结构化、专业的工作周报。

## 功能特性

- **自动获取提交记录**：连接 GitLab API，按时间范围获取指定项目的代码提交
- **AI 智能分析**：调用 Kimi AI 将零散的 commit 信息归纳为完整的工作内容
- **结构化周报输出**：生成包含工作总结、技术亮点、下周计划的专业周报
- **Web 服务接口**：提供 HTTP API，方便前端或其他工具集成
- **跨域支持**：内置 CORS 中间件，支持前端页面直接调用

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 服务器 | Uvicorn |
| HTTP 客户端 | httpx |
| AI 服务 | Kimi (Moonshot) |
| 环境管理 | python-dotenv |

## 项目结构

```
GitWeekly/
├── backend/
│   ├── main.py          # FastAPI 应用入口
│   ├── gitlab_api.py    # GitLab API 封装
│   ├── kimi_api.py      # Kimi AI 调用
│   ├── config.py        # 配置读取
│   ├── requirements.txt # Python 依赖
│   └── test_kimi.py     # 测试脚本
├── .env.example         # 环境变量示例
├── .gitignore           # Git 忽略规则
└── README.md            # 项目说明
```

## 快速开始

### 1. 克隆仓库

```bash
git clone <repository-url>
cd GitWeekly
```

### 2. 创建虚拟环境

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 4. 配置环境变量

复制示例文件并根据实际情况修改：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
KIMI_API_KEY=your-kimi-api-key
KIMI_API_URL=https://api.kimi.com/coding/v1

GITLAB_URL=https://your-gitlab-instance.com
GITLAB_TOKEN=your-gitlab-private-token
```

> **注意**：
> - `KIMI_API_KEY` 请从 [Moonshot 开放平台](https://platform.moonshot.cn) 获取
> - `GITLAB_TOKEN` 请从 GitLab 个人设置 → Access Tokens 中创建

### 5. 启动服务

```bash
python main.py
```

服务默认运行在 [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API 接口

### 生成周报

```http
POST /api/generate-report
Content-Type: application/json
```

**请求参数：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| gitlab_url | string | 是 | GitLab 实例地址 |
| gitlab_token | string | 是 | GitLab Private Token |
| project_ids | array | 是 | 项目 ID 列表 |
| author_email | string | 否 | 提交者邮箱筛选 |
| start_date | string | 是 | 开始日期 (YYYY-MM-DD) |
| end_date | string | 是 | 结束日期 (YYYY-MM-DD) |
| kimi_api_key | string | 是 | Kimi API Key |
| kimi_api_url | string | 否 | 自定义 Kimi API 地址 |

**请求示例：**

```json
{
  "gitlab_url": "https://gitlab.example.com",
  "gitlab_token": "glpat-xxxxxxxx",
  "project_ids": ["123", "456"],
  "author_email": "developer@example.com",
  "start_date": "2024-01-01",
  "end_date": "2024-01-07",
  "kimi_api_key": "sk-kimi-xxxxxxxx"
}
```

**响应示例：**

```json
{
  "success": true,
  "report": "## 本周工作总结\n\n### 项目名称\n- 完成了 xxx 功能开发\n- 修复了 xxx 问题\n...",
  "commits_count": 15,
  "message": "周报生成成功"
}
```

### 健康检查

```http
GET /api/health
```

## 隐私与安全

本项目已采取以下措施保护敏感信息：

- **环境变量隔离**：所有敏感配置（API Key、Token、URL）均通过 `.env` 文件管理
- **Git 忽略**：`.env` 文件已加入 `.gitignore`，不会提交到版本控制
- **示例文件**：提供 `.env.example` 作为配置模板，不含真实凭据

> **警告**：请勿将真实的 API Key、Token 等敏感信息直接硬编码在代码中或提交到仓库。

## 获取凭据指南

### Kimi API Key

1. 访问 [Moonshot 开放平台](https://platform.moonshot.cn)
2. 注册或登录账号
3. 进入「API Key 管理」页面
4. 创建新的 API Key 并复制

### GitLab Access Token

1. 登录你的 GitLab 实例
2. 点击右上角头像 → 「编辑个人资料」
3. 左侧菜单选择「Access Tokens」
4. 填写名称、过期时间，勾选 `read_api` 和 `read_repository` 权限
5. 点击创建并复制生成的 Token

### GitLab Project ID

1. 进入目标项目主页
2. 项目名称下方或设置页面中可看到 Project ID
3. 多个项目用逗号分隔传入

## 许可证

[MIT](LICENSE)
