# 物业管理系统｜Django + Vue 前后端分离项目

面向物业公司日常管理场景开发的后台管理系统，覆盖小区房产、业主档案、车辆车位、物业收费、报修工单、访客登记、公告投诉、客服消息、角色权限和日志审计等核心业务。项目采用 Django REST Framework + Vue 3 前后端分离架构，适合作为 Python/Web 后端或全栈方向面试作品展示。

## 快速入口

- 项目公网地址：http://123.57.75.124
- 公网 API 根地址：http://123.57.75.124/api
- GitHub 仓库：https://github.com/N-04/PropertyManagementSystem
- 公网 IP：`123.57.75.124`
- 初始化数据：`wyglxx2026.sql`

> 公开仓库不直接放置可登录密码，避免演示环境被外部修改；

## 演示账号

| 角色 | 用户名 | 密码 |
| --- | --- | --- |
| 物业管理员 | `property_admin_demo` |  |
| 财务人员 | `finance_demo` |  |
| 维修员 | `repairer_demo` |  |
| 业主 | `owner_dem` |  |

## 项目亮点

- 前后端分离：后端提供 REST API，前端通过 Axios 统一调用，方便独立部署和联调。
- 认证与权限完整：支持验证码登录、JWT 鉴权、Token 刷新、用户角色、菜单权限和 RBAC 管理。
- 业务模块覆盖广：从基础房产资料到缴费、报修、访客、投诉、公告、消息，形成物业管理闭环。
- 数据看板可视化：首页使用统计卡片和 ECharts 图表展示房屋、收费、报修等运营指标。
- 部署友好：支持环境变量配置数据库、密钥、跨域、Allowed Hosts、HTTPS 和 Gunicorn。
- 演示数据可恢复：提供 MySQL 初始化 SQL，便于本地部署、云服务器部署和面试现场演示。
- 工程结构清晰：Django 按业务 app 拆分，Vue 按 api、views、components、router、stores 分层。

## 技术栈

### 后端

- Python 3.11+
- Django 5.2
- Django REST Framework
- Simple JWT
- django-cors-headers
- django-extensions
- MySQL / PyMySQL
- Pillow
- Gunicorn

### 前端

- Vue 3
- Vite 8
- TypeScript
- Element Plus
- Pinia
- Vue Router
- Axios
- ECharts
- ESLint / Oxlint

### 部署

- Nginx：静态资源服务和反向代理
- Gunicorn：Django WSGI 服务
- MySQL：业务数据存储
- 可选云平台：Vercel / Netlify + Render / Railway / Fly.io

## 核心功能

| 模块 | 功能说明 |
| --- | --- |
| 登录认证 | 验证码、账号登录、JWT 鉴权、Token 刷新、个人信息维护 |
| 权限管理 | 用户管理、角色管理、菜单管理、权限分配 |
| 小区房产 | 小区、楼栋、单元、房屋基础数据维护 |
| 业主管理 | 业主列表、搜索筛选、详情查看、资料编辑、关联房屋 |
| 车辆车位 | 车辆资料、车位资料、车位购买、业主绑定 |
| 财务收费 | 费用账单、缴费状态、收费记录、费用统计 |
| 报修工单 | 报修登记、维修派单、处理结果、状态流转、评价反馈 |
| 访客管理 | 访客登记、审批处理、访问记录 |
| 公告投诉 | 公告发布、投诉建议、处理记录 |
| 客服消息 | 站内会话、消息中心、业务反馈提醒 |
| 文件上传 | 图片和附件上传，支持头像、报修等业务场景 |
| 日志审计 | 登录日志、操作日志，便于追踪后台行为 |
| 数据看板 | 统计卡片、趋势图表、待办事项和业务概览 |

## 系统架构

```text
浏览器 / 管理端用户
        |
        v
Vue 3 + Vite + Element Plus
        |
        v
Axios 请求 /api/*
        |
        v
Django REST Framework + Simple JWT
        |
        v
MySQL
```

## 目录结构

```text
PropertyManagementSystem/
├── apps/                 # Django 业务应用
│   ├── auth/             # 登录认证
│   ├── cars/             # 车辆管理
│   ├── chat/             # 客服消息
│   ├── community/        # 小区、楼栋、单元、房屋
│   ├── complaints/       # 投诉建议
│   ├── dashboard/        # 首页看板
│   ├── finance/          # 财务收费
│   ├── logs/             # 日志审计
│   ├── menu/             # 菜单权限
│   ├── notice/           # 公告通知
│   ├── owners/           # 业主管理
│   ├── parking/          # 车位管理
│   ├── repairs/          # 报修工单
│   ├── upload/           # 文件上传
│   ├── users/            # 用户角色
│   └── visitors/         # 访客管理
├── common/               # 后端公共模块
├── config/               # Django 配置
├── manage.py             # Django 入口
├── requirements.txt      # 后端依赖
├── web/                  # Vue 3 前端
└── wyglxx2026.sql        # 初始化数据
```

## 页面预览

### 业主管理

<img width="1728" height="1002" alt="业主管理页面" src="https://github.com/user-attachments/assets/59af417b-897e-4f39-bac7-922baff4b5a8" />

### 维修管理

<img width="1727" height="999" alt="维修管理页面" src="https://github.com/user-attachments/assets/880dc38e-4b1a-47e6-8c1d-43ce66e509e9" />

### 财务管理

<img width="1728" height="1000" alt="财务管理页面" src="https://github.com/user-attachments/assets/9a78a009-0ca8-4b73-993d-864ab751f9a3" />

## 本地运行

### 1. 准备数据库

```sh
mysql -u root -p -e "CREATE DATABASE property_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p property_management < wyglxx2026.sql
```

后端数据库配置优先读取环境变量：

```env
MYSQL_DATABASE=property_management
MYSQL_USER=root
MYSQL_PASSWORD=数据库密码
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

### 2. 启动后端

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

后端默认地址：

```text
http://127.0.0.1:8000/api
```

### 3. 启动前端

```sh
cd web
npm install
npm run dev
```

前端默认地址：

```text
http://127.0.0.1:5173
```

前端环境变量示例：

```env
VITE_API_ORIGIN=http://127.0.0.1:8000
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 部署方案

### 方案一：云服务器一体化部署

适合面试作品展示，可直接使用公网 IP `123.57.75.124` 作为访问入口，后续再绑定域名和 HTTPS。

```text
Nginx
├── /        -> web/dist 前端静态文件
├── /api/    -> 反向代理到 Django Gunicorn
├── /admin/  -> 反向代理到 Django Gunicorn
└── /media/  -> 上传文件目录

Gunicorn
└── config.wsgi:application

MySQL
└── property_management
```

后端生产环境变量示例：

```env
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=请替换为至少50位的随机字符串
DJANGO_ALLOWED_HOSTS=123.57.75.124,你的域名
DJANGO_CORS_ALLOWED_ORIGINS=http://123.57.75.124,https://你的域名
DJANGO_SECURE_SSL_REDIRECT=false

MYSQL_DATABASE=property_management
MYSQL_USER=你的数据库用户名
MYSQL_PASSWORD=你的数据库密码
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

前端生产环境变量示例：

```env
VITE_API_ORIGIN=http://123.57.75.124
VITE_API_BASE_URL=http://123.57.75.124/api
```

部署后检查：

- `http://123.57.75.124` 能打开前端页面。
- `http://123.57.75.124/api` 能返回 API 状态。
- 登录、业主列表、费用账单、报修工单、文件上传等核心流程可用。

### 方案二：前后端分离云平台部署

适合低成本 Demo 托管：

- 前端：Vercel / Netlify，Root Directory 设置为 `web`，构建命令为 `npm run build`。
- 后端：Render / Railway / Fly.io，启动命令为 `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`。
- 数据库：云 MySQL，导入 `wyglxx2026.sql`。
- 前端环境变量：`VITE_API_ORIGIN`、`VITE_API_BASE_URL`。
- 后端环境变量：`DJANGO_DEBUG`、`DJANGO_SECRET_KEY`、`DJANGO_ALLOWED_HOSTS`、`DJANGO_CORS_ALLOWED_ORIGINS`、MySQL 连接信息。

## 安全配置

- 生产环境设置 `DJANGO_DEBUG=false`。
- 生产环境必须配置强随机 `DJANGO_SECRET_KEY`。
- `DJANGO_ALLOWED_HOSTS` 只填写真实 IP 或域名。
- `DJANGO_CORS_ALLOWED_ORIGINS` 只填写前端访问地址。
- HTTPS 部署后建议开启 `DJANGO_SECURE_SSL_REDIRECT=true`。
- 不提交 `.env`、数据库密码、服务器私钥、上传目录和构建产物。
- 测试账号密码不直接公开在仓库中，避免演示环境被修改。

## 面试演示路径

1. 打开公网地址，说明项目采用前后端分离架构。
2. 登录系统，展示验证码、JWT 登录和动态菜单。
3. 进入首页看板，说明统计卡片和 ECharts 图表的数据来源。
4. 进入业主管理，演示列表搜索、详情查看、资料编辑和房屋关联。
5. 进入小区、楼栋、单元、房屋模块，说明基础数据层级关系。
6. 进入收费管理，演示账单、缴费状态和费用统计。
7. 进入报修管理，演示报修创建、派单、处理和评价闭环。
8. 进入访客、公告、投诉、消息模块，展示物业日常业务完整度。
9. 进入用户、角色、菜单模块，说明 RBAC 权限设计。
10. 结合部署方案说明 Nginx、Gunicorn、MySQL 和环境变量配置。

## 构建检查

```sh
cd web
npm run build
```

```sh
python manage.py check
```
