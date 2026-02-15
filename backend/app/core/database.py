import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:admin@localhost:5432/social_media"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    business_name = Column(String(255), nullable=False)
    industry = Column(String(255), nullable=False)
    goal = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class GeneratedPost(Base):
    __tablename__ = "generated_posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    post_number = Column(Integer, nullable=False)
    caption = Column(String(2000), nullable=False)
    linkedin_version = Column(String(2000), nullable=False)
    instagram_version = Column(String(2000), nullable=False)
    hashtags = Column(JSON, nullable=False)  # list of strings
    cta = Column(String(500), nullable=False)
    image_prompt = Column(String(2000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
