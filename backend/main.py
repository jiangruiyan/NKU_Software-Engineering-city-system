from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db, engine
import models
from auth import verify_password, create_token, decode_token, hash_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路径跳转登录页
@app.get("/")
def root():
    return RedirectResponse(url="/frontend/login.html")

# html_only=True 禁止目录列表
app.mount("/frontend", StaticFiles(directory="../frontend", html=True), name="frontend")

# ── 依赖：解析 token ──────────────────────────────────────────────
def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="未授权")

# ── 登录 ─────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_token({"sub": user.username, "role": user.role})
    return {"token": token, "role": user.role, "username": user.username}

# ── 修改密码 ──────────────────────────────────────────────────────
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

@app.post("/api/change-password")
def change_password(req: ChangePasswordRequest, current=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == current["sub"]).first()
    if not verify_password(req.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="原密码错误")
    user.hashed_password = hash_password(req.new_password)
    db.commit()
    return {"message": "密码修改成功"}

# ── 用户管理（管理员） ────────────────────────────────────────────
@app.get("/api/users")
def list_users(role: Optional[str] = None, current=Depends(get_current_user), db: Session = Depends(get_db)):
    if current["role"] != "admin":
        raise HTTPException(status_code=403, detail="无权限")
    query = db.query(models.User)
    if role:
        query = query.filter(models.User.role == role)
    users = query.all()
    return [{"id": u.id, "username": u.username, "role": u.role,
             "created_at": str(u.created_at)} for u in users]

class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str

@app.post("/api/users")
def create_user(req: CreateUserRequest, current=Depends(get_current_user), db: Session = Depends(get_db)):
    if current["role"] != "admin":
        raise HTTPException(status_code=403, detail="无权限")
    if db.query(models.User).filter(models.User.username == req.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = models.User(username=req.username, hashed_password=hash_password(req.password), role=req.role)
    db.add(user)
    db.commit()
    return {"message": "创建成功"}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, current=Depends(get_current_user), db: Session = Depends(get_db)):
    if current["role"] != "admin":
        raise HTTPException(status_code=403, detail="无权限")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.commit()
    return {"message": "删除成功"}

class UpdateUserRequest(BaseModel):
    role: str

@app.put("/api/users/{user_id}")
def update_user(user_id: int, req: UpdateUserRequest, current=Depends(get_current_user), db: Session = Depends(get_db)):
    if current["role"] != "admin":
        raise HTTPException(status_code=403, detail="无权限")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.role = req.role
    db.commit()
    return {"message": "更新成功"}

class ResetPasswordRequest(BaseModel):
    new_password: str

@app.put("/api/users/{user_id}/reset-password")
def reset_user_password(user_id: int, req: ResetPasswordRequest, current=Depends(get_current_user), db: Session = Depends(get_db)):
    if current["role"] != "admin":
        raise HTTPException(status_code=403, detail="无权限")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.role == "admin":
        raise HTTPException(status_code=403, detail="不能重置管理员的密码")
    if len(req.new_password) < 4:
        raise HTTPException(status_code=400, detail="密码至少需要4个字符")
    user.hashed_password = hash_password(req.new_password)
    db.commit()
    return {"message": "密码重置成功"}

# ── 资产审核（管理员） ────────────────────────────────────────────
@app.get("/api/assets")
def list_assets(status: Optional[str] = None, current=Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(models.Asset)
    if status:
        query = query.filter(models.Asset.status == status)
    assets = query.all()
    return [{"id": a.id, "name": a.name, "type": a.type, "status": a.status,
             "submitted_by": a.submitted_by, "description": a.description,
             "created_at": str(a.created_at)} for a in assets]

class AssetStatusRequest(BaseModel):
    status: str

@app.put("/api/assets/{asset_id}/status")
def update_asset_status(asset_id: int, req: AssetStatusRequest, current=Depends(get_current_user), db: Session = Depends(get_db)):
    if current["role"] != "admin":
        raise HTTPException(status_code=403, detail="无权限")
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    asset.status = req.status
    db.commit()
    return {"message": "状态已更新"}

# ── 统计数据（分析师） ────────────────────────────────────────────
@app.get("/api/stats")
def get_stats(current=Depends(get_current_user), db: Session = Depends(get_db)):
    total_users = db.query(models.User).count()
    admin_count = db.query(models.User).filter(models.User.role == 'admin').count()
    analyst_count = db.query(models.User).filter(models.User.role == 'analyst').count()
    modeler_count = db.query(models.User).filter(models.User.role == 'modeler').count()
    total_assets = db.query(models.Asset).count()
    pending_assets = db.query(models.Asset).filter(models.Asset.status == 'pending').count()
    approved_assets = db.query(models.Asset).filter(models.Asset.status == 'approved').count()
    rejected_assets = db.query(models.Asset).filter(models.Asset.status == 'rejected').count()
    total_templates = db.query(models.SceneTemplate).count()
    return {
        "users": {"total": total_users, "admin": admin_count, "analyst": analyst_count, "modeler": modeler_count},
        "assets": {"total": total_assets, "pending": pending_assets, "approved": approved_assets, "rejected": rejected_assets},
        "templates": {"total": total_templates}
    }

# ── 场景模板（建模师） ────────────────────────────────────────────
@app.get("/api/templates")
def list_templates(current=Depends(get_current_user), db: Session = Depends(get_db)):
    templates = db.query(models.SceneTemplate).all()
    return [{"id": t.id, "name": t.name, "template_no": t.template_no,
             "tree_count": t.tree_count, "road_type": t.road_type,
             "seat_count": t.seat_count, "description": t.description,
             "created_by": t.created_by, "created_at": str(t.created_at)} for t in templates]

class CreateTemplateRequest(BaseModel):
    name: str
    template_no: int
    tree_count: int
    road_type: str
    seat_count: int
    description: Optional[str] = ""

@app.post("/api/templates")
def create_template(req: CreateTemplateRequest, current=Depends(get_current_user), db: Session = Depends(get_db)):
    if current["role"] != "modeler":
        raise HTTPException(status_code=403, detail="无权限")
    if db.query(models.SceneTemplate).filter(models.SceneTemplate.template_no == req.template_no).first():
        raise HTTPException(status_code=400, detail="模板编号已存在")
    t = models.SceneTemplate(**req.dict(), created_by=current["sub"])
    db.add(t)
    db.commit()
    return {"message": "模板创建成功"}

@app.delete("/api/templates/{template_id}")
def delete_template(template_id: int, current=Depends(get_current_user), db: Session = Depends(get_db)):
    if current["role"] != "modeler":
        raise HTTPException(status_code=403, detail="无权限")
    t = db.query(models.SceneTemplate).filter(models.SceneTemplate.id == template_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="模板不存在")
    db.delete(t)
    db.commit()
    return {"message": "删除成功"}

# ── 提交资产（建模师提交，管理员审核） ───────────────────────────
class SubmitAssetRequest(BaseModel):
    name: str
    type: str
    description: Optional[str] = ""

@app.post("/api/assets")
def submit_asset(req: SubmitAssetRequest, current=Depends(get_current_user), db: Session = Depends(get_db)):
    asset = models.Asset(name=req.name, type=req.type, description=req.description,
                         submitted_by=current["sub"], status="pending")
    db.add(asset)
    db.commit()
    return {"message": "提交成功，等待审核"}
