<img width="1728" height="1002" alt="image" src="https://github.com/user-attachments/assets/59af417b-897e-4f39-bac7-922baff4b5a8" /># 物业管理系统

物业管理系统统一仓库，包含 Django 后端接口服务和 Vue 前端 Web 管理界面，支持用户、房产、缴费、报修、公告、消息等物业业务管理，可作为计算机相关专业毕业设计项目参考使用。

## 项目简介

本项目面向物业管理业务场景，后端基于 Django 和 Django REST Framework 开发，前端基于 Vue 3、Vite、TypeScript 和 Element Plus 开发。系统覆盖用户认证、角色权限、社区楼栋、房屋业主、车位车辆、收费缴费、报修处理、访客登记、公告通知、投诉建议、站内消息和操作日志等能力，功能结构完整，可用作毕业设计、课程设计或物业管理系统实践项目参考。

## 目录结构

```text
.
├── apps/             # Django 业务应用
├── common/           # 后端公共模块
├── config/           # Django 项目配置
├── manage.py         # 后端启动入口
├── requirements.txt  # 后端依赖
├── web/              # 前端 Vue 管理端
└── wyglxx2026.sql    # 初始化数据
```

## 主要功能

- 用户登录、角色权限和菜单管理
- 小区、楼栋、单元、房屋基础信息管理
- 业主、车辆、车位和停车信息管理
- 物业费用、缴费状态和收费记录管理
- 报修、投诉、访客、公告等日常物业业务
- 站内客服会话、消息发送和会话状态维护
- 文件上传、登录日志和系统操作记录

- 业主
- 

## 技术栈

### 后端

- Python 3.11
- Django 5
- Django REST Framework
- Simple JWT
- MySQL / PyMySQL

### 前端

- Vue 3
- Vite
- TypeScript
- Element Plus
- Pinia
- Vue Router
- Axios
- ECharts

## 后端运行

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 前端运行

```sh
cd web
npm install
npm run dev
```

## 前端构建

```sh
cd web
npm run build
```

## 数据说明

仓库中包含 `wyglxx2026.sql`，可按本地数据库环境导入初始化数据。数据库连接参数请根据本机 MySQL 配置在 Django settings 中调整。
