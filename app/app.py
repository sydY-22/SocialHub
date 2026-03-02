from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from app.images import upload_image
from app.images import upload_options
import shutil
import os
import tempfile


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(""),
        session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None
    # create temp file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splittext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
        # upload the temp file
        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=upload_options(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )
        # check the response
        if upload_result.response.http_status_code == 200:
            post = Post(
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@app.get("/feed")
async def get_feed(
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()] # get post one by one

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
    return {"posts": posts_data}


text_posts = {}


# @app.get("/posts")
# def get_all_posts(limit: int = None):
#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts
#
#
# @app.get("/posts/{id}")
# def get_post(id: int) -> PostResponse:
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return text_posts.get(id)
#
#
# @app.post("/posts")
# def create_post(post: PostCreate) -> PostResponse:
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[max(text_posts.keys()) + 1] = new_post
#     return new_post
