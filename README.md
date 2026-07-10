# 基于 Django + Vue 的物业管理系统

这是一个前后端分离的物业管理系统，后端使用 Django REST Framework 提供 API，前端使用 Vue 3 + Vite + Element Plus 构建管理端页面。项目覆盖社区基础资料、业主房屋、车辆车位、收费缴费、报修派单、访客登记、公告投诉、客服消息、角色权限和系统日志等物业业务，可作为毕业设计、课程设计、作品集或面试展示项目。

## 在线信息

- GitHub 仓库：https://github.com/N-04/PropertyManagementSystem
- 当前公网 IP：`123.57.75.124`
- 后端 API 本地默认地址：`http://127.0.0.1:8000/api`
- 前端本地默认地址：`http://127.0.0.1:5173`
- 初始化数据：`wyglxx2026.sql`

> 公网 IP 可用于云服务器部署、数据库白名单、接口访问白名单或面试 Demo 环境说明。正式上线时建议绑定域名并启用 HTTPS。

## 项目重点

- 前后端分离架构：Django 负责业务接口和权限控制，Vue 负责管理端交互与数据展示。
- RESTful API 设计：按业务模块拆分接口，前端通过 Axios 统一请求后端 API。
- JWT 登录认证：使用 Simple JWT 实现访问令牌、刷新令牌和登录状态维护。
- RBAC 权限模型：支持用户、角色、菜单和权限管理，适合后台管理系统场景。
- 完整物业业务闭环：从房屋业主档案，到缴费、报修、投诉、访客、公告和消息通知。
- 数据可视化仪表盘：通过 ECharts 展示房屋、费用、报修等关键指标。
- 生产部署适配：支持环境变量配置密钥、数据库、跨域、Allowed Hosts、HTTPS 和 Gunicorn。
- 初始化数据完整：提供 MySQL SQL 文件，便于快速恢复演示数据和本地调试。

## 主要功能

- 登录认证：验证码、登录、JWT 鉴权、Token 刷新、个人信息维护。
- 权限管理：用户管理、角色管理、菜单管理、权限分配。
- 社区基础数据：小区、楼栋、单元、房屋信息管理。
- 业主管理：业主列表、搜索筛选、详情查看、资料编辑、关联房屋。
- 车辆车位：车辆信息、车位信息、车位购买和绑定业主。
- 财务收费：物业费用记录、缴费状态、费用统计和收费管理。
- 报修管理：报修登记、维修派单、处理结果、状态流转和评价反馈。
- 访客管理：访客登记、审批、访问记录维护。
- 公告投诉：公告发布、投诉建议、处理记录。
- 客服消息：站内客服会话、消息中心、业务反馈提醒。
- 文件上传：图片和附件上传，支持报修、头像等业务场景。
- 日志审计：登录日志、操作日志，便于后台追踪系统行为。
- 数据看板：统计卡片、趋势图表、待办事项和业务概览。

## 技术栈

### 后端

- Python 3.11+
- Django 5.2
- Django REST Framework
- djangorestframework-simplejwt
- django-cors-headers
- django-extensions
- MySQL
- PyMySQL
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

### 工程与部署

- 前端构建：Vite
- 后端服务：Django + Gunicorn
- 反向代理：Nginx
- 数据库：MySQL
- 推荐部署：Vercel / Netlify + Render / Railway，或云服务器 Nginx + Gunicorn + MySQL

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
│   ├── logs/             # 日志
│   ├── menu/             # 菜单权限
│   ├── notice/           # 公告
│   ├── owners/           # 业主
│   ├── parking/          # 车位
│   ├── repairs/          # 报修
│   ├── upload/           # 文件上传
│   ├── users/            # 用户角色
│   └── visitors/         # 访客
├── common/               # 后端公共模块
├── config/               # Django 配置
├── manage.py             # Django 入口
├── requirements.txt      # 后端依赖
├── web/                  # Vue 3 前端
├── DEPLOYMENT.md         # 部署说明
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

创建 MySQL 数据库，并导入初始化数据：

```sh
mysql -u root -p -e "CREATE DATABASE property_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p property_management < wyglxx2026.sql
```

后端数据库配置优先读取环境变量：

```env
MYSQL_DATABASE=property_management
MYSQL_USER=root
MYSQL_PASSWORD=你的数据库密码
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

后端默认访问地址：

```text
http://127.0.0.1:8000/api
```

### 3. 启动前端

```sh
cd web
npm install
npm run dev
```

前端默认访问地址：

```text
http://127.0.0.1:5173
```

前端可通过环境变量指定后端 API：

```env
VITE_API_ORIGIN=http://127.0.0.1:8000
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 部署方案

### 方案一：前后端分离云平台部署

适合简历展示和面试 Demo，维护成本较低。

```text
用户浏览器
    |
    v
Vercel / Netlify 托管 Vue 前端
    |
    v
Render / Railway / Fly.io 托管 Django API
    |
    v
云 MySQL
```

前端部署：

- Root Directory：`web`
- Build Command：`npm run build`
- Output Directory：`dist`
- 环境变量：`VITE_API_ORIGIN`、`VITE_API_BASE_URL`

后端部署：

- Build Command：`pip install -r requirements.txt`
- Start Command：`gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
- 环境变量：`DJANGO_DEBUG=false`、`DJANGO_SECRET_KEY`、`DJANGO_ALLOWED_HOSTS`、`DJANGO_CORS_ALLOWED_ORIGINS`、MySQL 连接信息

### 方案二：云服务器一体化部署

适合已有云服务器的情况，可使用当前公网 IP `123.57.75.124` 作为部署入口，后续再绑定域名。

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

部署后建议检查：

- `http://123.57.75.124` 能打开前端页面。
- `http://123.57.75.124/api/auth/captcha/` 能访问后端接口。
- 登录、列表、详情、上传、报修、缴费等核心流程正常。
- 正式域名和 HTTPS 配好后，将环境变量中的 IP 替换为域名。

更完整的部署步骤见 [DEPLOYMENT.md](./DEPLOYMENT.md)。

## 生产安全配置

- 生产环境必须设置 `DJANGO_DEBUG=false`。
- 生产环境必须设置强随机 `DJANGO_SECRET_KEY`。
- `DJANGO_ALLOWED_HOSTS` 只填写真实 IP 或域名。
- `DJANGO_CORS_ALLOWED_ORIGINS` 只填写前端访问地址。
- HTTPS 部署后建议开启 `DJANGO_SECURE_SSL_REDIRECT=true`。
- 不要提交 `.env`、数据库密码、服务器私钥、上传目录和构建产物。

## 数据说明

- `wyglxx2026.sql` 包含初始化表结构和演示数据。
- 导入数据前请确认目标数据库字符集为 `utf8mb4`。
- 如果使用云 MySQL，请将公网 IP `123.57.75.124` 或服务器出口 IP 加入数据库白名单。

## 推荐演示路径

1. 登录系统，展示验证码、JWT 登录和动态菜单。
2. 进入首页仪表盘，展示业务统计卡片和 ECharts 图表。
3. 进入业主管理，展示搜索、列表、详情和编辑。
4. 进入房屋、楼栋、单元模块，展示基础数据关联关系。
5. 进入收费管理，展示费用记录和缴费状态。
6. 进入报修管理，展示创建、派单、处理和评价闭环。
7. 进入公告、投诉、访客、消息模块，展示物业日常业务完整度。
8. 进入用户、角色、菜单模块，展示后台权限设计。

## 构建检查

```sh
cd web
npm run build
```

```sh
python manage.py check
```
