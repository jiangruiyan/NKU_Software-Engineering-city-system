"""
运行一次即可：初始化用户密码 + 写入测试资产数据
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, engine
import models
from auth import hash_password

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ── 用户 ──
accounts = [
    ("admin01",   "password123", "admin"),
    ("analyst01", "password123", "analyst"),
    ("modeler01", "password123", "modeler"),
]
for username, password, role in accounts:
    u = db.query(models.User).filter(models.User.username == username).first()
    if u:
        u.hashed_password = hash_password(password)
        print(f"  更新密码: {username}")
    else:
        db.add(models.User(username=username, hashed_password=hash_password(password), role=role))
        print(f"  创建用户: {username} ({role})")

# ── 测试资产 ──
test_assets = [
    ("路灯-现代款", "model",   "pending",  "modeler01", "适用于城市主干道的现代路灯3D模型"),
    ("沥青路面贴图", "texture", "pending",  "modeler01", "高精度沥青路面PBR贴图"),
    ("城市植被插件", "plugin",  "approved", "modeler01", "自动生成行道树的Blender插件"),
    ("公交站台模型", "model",   "rejected", "modeler01", "标准公交站台3D模型"),
]
for name, type_, status, submitted_by, desc in test_assets:
    if not db.query(models.Asset).filter(models.Asset.name == name).first():
        db.add(models.Asset(name=name, type=type_, status=status, submitted_by=submitted_by, description=desc))
        print(f"  添加资产: {name}")

db.commit()
db.close()
print("\n✅ 初始化完成")
