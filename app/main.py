from fastapi import FastAPI, Depends, HTTPException, Response, status
from pydantic import BaseModel

from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
# models.Base.metadata.create_all(bind=engine) //no need if using alembic

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def index():
    your_name = "Vikesh Singh"
    about = (
        "Hello! I'm Vikesh Singh, a backend developer with over 8 years of experience in creating scalable, "
        "secure, and high-performance web applications. I specialize in building robust APIs and "
        "optimizing databases using technologies like **FastAPI**, **Laravel**, **PostgreSQL**, **MySQL**, "
        "**Redis**, **SQLAlchemy**, and **Celery**.\n\n"
        
        "My passion lies in writing clean, maintainable code and solving complex problems that drive business growth. "
        "I am experienced in designing systems that handle high traffic with efficiency and reliability.\n\n"
        
        "If you're seeking a dedicated developer skilled in **API development**, **database optimization**, and "
        "**cloud infrastructure**, who can deliver results beyond expectations, "
        "let's connect! I'm excited to contribute to innovative projects and help your company succeed."
    )
    linkedin_url = "https://linkedin.com/in/developervikeshsingh"
    github_url = "https://github.com/vikeshsingh/fastapi-socialmedia-sample"
    demo_url = "/docs"
    html_content = f"""
    <html>
        <head>
            <title>Vikesh Singh - Backend Developer</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: auto;
                    padding: 20px;
                    line-height: 1.6;
                    background-color: #f9f9f9;
                    color: #333;
                }}
                h1 {{
                    color: #2c3e50;
                }}
                b {{
                    color: #000;
                }}
                a {{
                    color: #0077b5;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .links {{
                    margin-top: 15px;
                }}
                .links a {{
                    margin-right: 15px;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h1>Hello! I'm Vikesh Singh</h1>
            <p>
                I am a backend developer with over 8 years of experience in creating scalable, secure, 
                and high-performance web applications. I specialize in building robust APIs and optimizing databases 
                using technologies like <b>FastAPI</b>, <b>Laravel</b>, <b>PostgreSQL</b>, <b>MySQL</b>, 
                <b>Redis</b>, <b>SQLAlchemy</b>, and <b>Docker</b>.
            </p>
            <p>
                My passion lies in writing clean, maintainable code and solving complex problems that drive business growth. 
                I am experienced in designing systems that handle high traffic with efficiency and reliability.
            </p>
            <p>
                If you're seeking a dedicated developer skilled in <b>API development</b>, 
                <b>database optimization</b>, and <b>cloud infrastructure</b> 
                who can deliver results beyond expectations — let's connect! 
                I'm excited to contribute to innovative projects and help your company succeed.
            </p>
            <div class="links">
                <a href="{linkedin_url}" target="_blank">LinkedIn</a>
                <a href="{github_url}" target="_blank">GitHub</a>
                <a href="mailto:vikesh121singh@gmail.com">Email</a>
                <a href="{demo_url}" target="_blank">Demo API</a>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)