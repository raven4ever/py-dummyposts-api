import time
from typing import Optional

import psycopg2
from fastapi import FastAPI, Response, status, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='example123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connected to DB!')
        break
    except Exception as err:
        print('Connection to DB failed!')
        print(err)
        time.sleep(3)

app = FastAPI()


@app.get('/')
def root():
    return {
        "message": "Wazzzaaa!!!"
    }


@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (new_post.title, new_post.content, new_post.published))
    saved_post = cursor.fetchone()

    conn.commit()

    return {"data": saved_post}


@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))

    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")

    return {"post_details": post}


@app.delete('/posts/{id}')
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))

    deleted_post = cursor.fetchone()

    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, id))

    updated_post = cursor.fetchone()

    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")

    return {"data": updated_post}
