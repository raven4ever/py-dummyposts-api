from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models
from . import schemas
from . import utils
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def root():
    return {
        "message": "Wazzzaaa!!!"
    }


@app.get('/posts', response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    saved_post = models.Post(**new_post.dict())
    db.add(saved_post)
    db.commit()
    db.refresh(saved_post)

    return saved_post


@app.get('/posts/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")

    return post


@app.delete('/posts/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    delete_query = db.query(models.Post).filter(models.Post.id == id)

    if not delete_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")

    update_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return update_query.first()


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)

    saved_user = models.User(**user.dict())
    db.add(saved_user)
    db.commit()
    db.refresh(saved_user)

    return saved_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} was not found!")

    return user
