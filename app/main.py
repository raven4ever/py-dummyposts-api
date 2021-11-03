from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from . import models
from .database import engine, get_db


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def root():
    return {
        "message": "Wazzzaaa!!!"
    }


@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post, db: Session = Depends(get_db)):
    saved_post = models.Post(**new_post.dict())
    db.add(saved_post)
    db.commit()
    db.refresh(saved_post)

    return {"data": saved_post}


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")

    return {"post_details": post}


@app.delete('/posts/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_query = db.query(models.Post).filter(models.Post.id == id)

    if not delete_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")

    update_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"data": update_query.first()}
