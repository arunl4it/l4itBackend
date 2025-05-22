from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import SessionLocal
from app.blog.schemas.blog import BlogCreate, BlogUpdate, BlogOut
from app.blog.crud import create_blog, get_blog, get_blogs, update_blog, delete_blog
import os
import shutil
from app.auth.dependencies import get_current_user
from app.auth.models.user import User
from fastapi.responses import JSONResponse

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BlogOut, status_code=status.HTTP_201_CREATED)
async def create(
    heading: str = Form(...),
    short_description: str = Form(...),
    content: str = Form(...),
    meta_title: Optional[str] = Form(None),
    meta_description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_path = None
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format. Allowed: jpg, png, gif, webp")
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = f"/{file_location.replace(os.sep, '/')}"
    blog_data = BlogCreate(
        heading=heading,
        short_description=short_description,
        content=content,
        meta_title=meta_title,
        meta_description=meta_description,
        image=image_path
    )
    return create_blog(db, blog_data)

@router.get("/", response_model=List[BlogOut])
def read_blogs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_blogs(db, skip=skip, limit=limit)

@router.get("/{blog_id}", response_model=BlogOut)
def read_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/{blog_id}", response_model=BlogOut)
async def update(
    blog_id: int,
    heading: str = Form(...),
    short_description: str = Form(...),
    content: str = Form(...),
    meta_title: Optional[str] = Form(None),
    meta_description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_path = None
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format. Allowed: jpg, png, gif, webp")
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = f"/{file_location.replace(os.sep, '/')}"
    blog_data = BlogUpdate(
        heading=heading,
        short_description=short_description,
        content=content,
        meta_title=meta_title,
        meta_description=meta_description,
        image=image_path
    )
    updated = update_blog(db, blog_id, blog_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Blog not found")
    return updated

@router.delete("/{blog_id}", status_code=status.HTTP_200_OK)
def delete(blog_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = delete_blog(db, blog_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blog not found")
    return JSONResponse(content={"detail": "Blog deleted successfully."}, status_code=200) 