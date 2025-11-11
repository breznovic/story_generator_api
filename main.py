from fastapi import FastAPI, Query, Depends
from schemas import StoryRequest
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from models import Story
from database import engine, Base, get_db
from utils import generate_childhood, generate_historical_conflict, generate_historical_context, generate_profession


app = FastAPI(
    title="Medieval Stories API",
    description="Generate historical medieval stories based on social class",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to medieval stories generator!"}


@app.post("/generate-story")
def generate_story(
    request: StoryRequest,
    db: Session = Depends(get_db)
):
    period_context = generate_historical_context()
    base_story = f"You were born into a {request.social_class.value} family in {request.region} {period_context}. "
    base_story += generate_childhood(request.social_class)
    base_story += " " + generate_profession(request.social_class)

    if request.include_conflict:
        base_story += " " + generate_historical_conflict(request.social_class)

    db_story = Story(
        social_class=request.social_class.value,
        region=request.region,
        story_text=base_story
    )

    db.add(db_story)
    db.commit()
    db.refresh(db_story)

    return {
        "id": db_story.id,
        "story": base_story,
        "created_at": db_story.created_at
    }


@app.get("/stories/")
def read_stories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    stories = db.query(Story).offset(skip).limit(limit).all()
    total = db.query(Story).count()

    return {
        "items": stories,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@app.delete("/stories/{story_id}")
def delete_story(
    story_id: int,
    db: Session = Depends(get_db)
):

    story = db.query(Story).filter(Story.id == story_id).first()

    db.delete(story)
    db.commit()

    return {
        "deleted_id": story_id
    }
