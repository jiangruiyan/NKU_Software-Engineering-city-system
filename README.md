# 智能城市生成系统

南开大学《软件工程》课程期末团队作业其一（原型系统）。

团队作业其二（Blender 插件）仓库：

## 技术栈

| 层 | 技术 |
|---|------|
| 后端 | Python · FastAPI · SQLAlchemy · JWT |
| 前端 | 原生 HTML/CSS/JS · Chart.js |
| 数据库 | MySQL |
| 认证 | JWT (python-jose) · bcrypt |

## 快速开始

### 1. 环境准备

- Python 3.10+
- MySQL 8.0+

### 2. 安装依赖

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS / Linux

pip install -r requirements.txt
```

### 3. 配置数据库

编辑 `backend/database.py`，修改数据库连接信息：

```python
DATABASE_URL = "mysql+pymysql://用户名:密码@localhost/city_system"
```

确保 MySQL 中已创建数据库 `city_system`。

### 4. 初始化数据

```bash
cd backend
python init_data.py
```

这会创建默认用户和测试资产。

### 5. 启动服务

```bash
cd backend
uvicorn main:app --reload --port 8000
```

浏览器打开 `http://localhost:8000`，自动跳转登录页。

### 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| `admin01` | `password123` | 系统管理员 |
| `analyst01` | `password123` | 行业分析师 |
| `modeler01` | `password123` | 场景建模师 |


## 项目结构

```text
├── backend/
│   ├── main.py          # FastAPI 入口 & 路由
│   ├── models.py        # SQLAlchemy 数据模型
│   ├── schemas.py       # Pydantic 请求模型
│   ├── database.py      # 数据库连接配置
│   ├── auth.py          # JWT & 密码哈希
│   └── init_data.py     # 初始数据脚本
├── frontend/
│   ├── login.html       # 登录页
│   ├── admin.html       # 管理员控制台
│   ├── analyst.html     # 分析师工作台
│   ├── modeler.html     # 建模师工作台
│   ├── common.js        # 公共 JS（API、鉴权、弹窗）
│   └── style.css        # 全局样式
├── requirements.txt
└── README.md
```

## 角色与权限

| 功能 | 管理员 | 分析师 | 建模师 |
|------|:---:|:---:|:---:|
| 用户管理（增删改查） | ✅ | — | — |
| 重置用户密码 | ✅ | — | — |
| 资产审核 | ✅ | — | — |
| 数据看板 & 图表 | ✅ | ✅ | — |
| 生成分析报告 | — | ✅ | — |
| 场景模板管理 | — | — | ✅ |
| 提交资产 | — | — | ✅ |
| 修改自己的密码 | ✅ | ✅ | ✅ |

---


