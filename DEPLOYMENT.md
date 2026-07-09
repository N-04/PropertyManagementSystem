# 物业管理系统部署方案

本文档面向“让面试官和 HR 不用本地部署也能查看项目效果”的场景，推荐把项目部署成一个可公开访问的 Demo：

- 前端：Vercel 或 Netlify 静态托管 `web/`
- 后端：Render、Railway、Fly.io 或云服务器部署 Django API
- 数据库：云 MySQL，导入 `wyglxx2026.sql`
- README/简历：放在线预览地址、演示账号、截图和演示视频

## 一、当前项目部署结论

当前项目是前后端分离结构：

```text
PropertyManagementSystem/
├── apps/                 # Django 业务应用
├── config/               # Django 配置
├── manage.py             # 后端入口
├── requirements.txt      # 后端依赖
├── web/                  # Vue 3 + Vite 前端
└── wyglxx2026.sql        # 初始化数据
```

后端已经支持通过环境变量配置生产环境，包括：

- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CORS_ALLOWED_ORIGINS`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`

前端已经支持通过环境变量配置后端地址：

- `VITE_API_ORIGIN`
- `VITE_API_BASE_URL`

因此推荐方案是：**前端单独部署，后端单独部署，前端通过 HTTPS API 地址访问后端。**

## 二、推荐部署架构

```text
HR / 面试官浏览器
        |
        v
前端 Demo 地址
Vercel / Netlify
https://property-demo.vercel.app
        |
        v
后端 API 地址
Render / Railway / 云服务器
https://property-api.onrender.com/api
        |
        v
云 MySQL
property_management
```

## 三、最推荐方案：Vercel + Render/Railway + 云 MySQL

这个方案适合简历展示，维护成本低，不需要面试官安装 Python、Node、MySQL。

### 1. 准备代码仓库

建议把 `PropertyManagementSystem` 作为一个完整仓库提交到 GitHub。

确认仓库里包含：

```text
apps/
config/
manage.py
requirements.txt
web/
wyglxx2026.sql
```

不要提交：

```text
.env
.venv/
web/node_modules/
web/dist/
media/
```

### 2. 准备云 MySQL

可选平台：

- Railway MySQL
- 阿里云 RDS MySQL
- 腾讯云 MySQL
- PlanetScale 或其他兼容 MySQL 服务

创建数据库后，记录这些信息：

```text
MYSQL_DATABASE=property_management
MYSQL_USER=你的数据库用户名
MYSQL_PASSWORD=你的数据库密码
MYSQL_HOST=你的数据库公网地址
MYSQL_PORT=3306
```

导入初始化数据：

```sh
mysql -h MYSQL_HOST -P 3306 -u MYSQL_USER -p MYSQL_DATABASE < wyglxx2026.sql
```

如果云平台提供 Web 控制台，也可以直接在控制台导入 `wyglxx2026.sql`。

### 3. 部署后端 Django

推荐平台：Render 或 Railway。

后端服务配置：

```text
Root Directory: .
Build Command: pip install -r requirements.txt
Start Command: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
Python Version: 3.11 或 3.12
```

注意：当前 `requirements.txt` 里没有 `gunicorn`。部署前需要补充：

```sh
pip install gunicorn
pip freeze > requirements.txt
```

或者手动在 `requirements.txt` 增加：

```text
gunicorn
```

后端环境变量示例：

```env
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=请换成至少50位的随机字符串
DJANGO_ALLOWED_HOSTS=property-api.onrender.com
DJANGO_CORS_ALLOWED_ORIGINS=https://property-demo.vercel.app
DJANGO_SECURE_SSL_REDIRECT=false

MYSQL_DATABASE=property_management
MYSQL_USER=你的数据库用户名
MYSQL_PASSWORD=你的数据库密码
MYSQL_HOST=你的数据库公网地址
MYSQL_PORT=3306
```

说明：

- 如果 Render/Railway 已经在外层处理 HTTPS，`DJANGO_SECURE_SSL_REDIRECT=false` 更稳，避免代理环境下反复跳转。
- 后端域名确定后，把它写入 `DJANGO_ALLOWED_HOSTS`。
- 前端域名确定后，把它写入 `DJANGO_CORS_ALLOWED_ORIGINS`。

后端部署完成后，浏览器访问：

```text
https://property-api.onrender.com/api/auth/captcha/
```

如果能返回接口响应，说明 API 服务可访问。

### 4. 部署前端 Vue

推荐平台：Vercel。

Vercel 项目配置：

```text
Framework Preset: Vite
Root Directory: web
Build Command: npm run build
Output Directory: dist
Install Command: npm install
Node Version: 20 或 22
```

前端环境变量：

```env
VITE_API_ORIGIN=https://property-api.onrender.com
VITE_API_BASE_URL=https://property-api.onrender.com/api
```

部署完成后，访问：

```text
https://property-demo.vercel.app
```

如果登录、列表、详情、上传等功能能正常请求后端接口，说明前后端联通成功。

## 四、云服务器部署方案

如果你有阿里云、腾讯云或轻量服务器，也可以部署成一台服务器承载全部服务。

推荐结构：

```text
Nginx
├── /              -> 前端 web/dist 静态文件
├── /api/          -> 反向代理到 Django gunicorn
├── /admin/        -> 反向代理到 Django gunicorn
└── /media/        -> Django 上传文件目录

Gunicorn
└── Django config.wsgi:application

MySQL
└── property_management
```

服务器安装依赖：

```sh
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nodejs npm nginx mysql-server
```

后端启动：

```sh
cd /var/www/PropertyManagementSystem
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
python manage.py migrate
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

前端构建：

```sh
cd /var/www/PropertyManagementSystem/web
npm install
npm run build
```

前端生产环境变量：

```env
VITE_API_ORIGIN=https://你的域名
VITE_API_BASE_URL=https://你的域名/api
```

## 五、上线前检查清单

后端：

- `DJANGO_DEBUG=false`
- `DJANGO_SECRET_KEY` 已替换为强随机字符串
- `DJANGO_ALLOWED_HOSTS` 包含后端域名
- `DJANGO_CORS_ALLOWED_ORIGINS` 包含前端域名
- MySQL 环境变量配置正确
- `requirements.txt` 包含 `gunicorn`
- 数据库已导入 `wyglxx2026.sql`
- 登录、刷新 token、上传、列表接口正常

前端：

- `VITE_API_ORIGIN` 指向后端域名
- `VITE_API_BASE_URL` 指向后端 `/api`
- `npm run build` 可以成功
- 访问前端域名后没有空白页
- 登录后页面刷新不会丢失路由

展示：

- README 顶部放在线 Demo 链接
- README 放演示账号
- README 放核心截图
- 准备 1 到 3 分钟演示视频

## 六、给 HR 和面试官看的 README 模板

可以把下面内容放到 `README.md` 顶部：

```md
## 在线预览

- 前端 Demo：https://property-demo.vercel.app
- 后端 API：https://property-api.onrender.com/api
- 演示账号：admin
- 演示密码：123456
- 演示视频：https://你的演示视频链接

> Demo 使用云端 MySQL 初始化数据，面试官无需本地部署即可体验用户、房屋、业主、缴费、报修、公告、访客、投诉、消息和权限管理等核心功能。
```

## 七、推荐演示路径

给面试官演示时，可以按这个顺序：

1. 登录系统，展示 JWT 登录和权限菜单。
2. 进入首页仪表盘，展示统计卡片和图表。
3. 进入业主管理，展示列表、搜索、详情、编辑。
4. 进入房屋/楼栋/单元模块，展示基础数据关系。
5. 进入缴费管理，展示费用记录和状态。
6. 进入报修管理，展示创建、派单、处理闭环。
7. 进入公告/投诉/访客/消息模块，展示业务完整度。
8. 进入角色和菜单管理，展示 RBAC 权限设计。

## 八、最小可用 Demo 方案

如果暂时不想部署完整后端，可以先做一个“可展示版本”：

- 前端部署到 Vercel
- 后端部署到 Render 免费实例
- 数据库使用 Railway MySQL
- README 放截图和演示视频兜底

这样 HR 打开链接即可看到项目效果，面试官也能继续查看源码、接口和数据库设计。
