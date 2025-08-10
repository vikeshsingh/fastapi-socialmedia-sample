from fastapi import FastAPI, Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]  #only for swagger
)

@router.get("/",response_model=List[schemas.PostOut])
def test_post(db: Session = Depends(get_db), user_id:int = Depends(oauth2.get_current_user),limit: int = 10):
    # posts = db.query(models.Post).limit(limit).all() // without join
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("vote")).join(models.Vote,models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).limit(limit).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    # new_post = models.Post(title=post.title,content=post.content,published=post.published) // this will also work
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id:int,db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id==id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return posts

@router.delete("/{id}")
def delete_post(id:int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostCreate,db: Session = Depends(get_db)):
    post_data = db.query(models.Post).filter(models.Post.id==id)
    if post_data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    post_data.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_data.first() 