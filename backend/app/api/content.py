from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.content import (
    ContentRequest,
    ContentResponse,
    PostResponse,
    PlatformVariations,
    CreativeType,
)
from app.core.database import get_db, Project, GeneratedPost
from app.core.gemini import generate_posts_with_ai

router = APIRouter()


def _parse_creative_type(value: str | None) -> CreativeType:
    """Parse creative type from API response; default to Static Post."""
    if not value:
        return CreativeType.static_post
    v = str(value).strip().lower()
    if "carousel" in v:
        return CreativeType.carousel
    if "reel" in v:
        return CreativeType.reel
    return CreativeType.static_post


def _normalize_post(raw: dict, post_number: int) -> PostResponse:
    """Map Gemini response item to PostResponse."""
    pv = raw.get("platform_variations") or {}
    hashtags = raw.get("hashtags")
    if isinstance(hashtags, str):
        hashtags = [h.strip() for h in hashtags.replace("#", "").split() if h.strip()]
    elif not isinstance(hashtags, list):
        hashtags = []
    return PostResponse(
        post_number=post_number,
        post_topic=raw.get("post_topic", ""),
        caption=raw.get("caption", ""),
        platform_variations=PlatformVariations(
            instagram=pv.get("instagram", ""),
            linkedin=pv.get("linkedin", ""),
            facebook=pv.get("facebook", ""),
        ),
        hashtags=hashtags,
        cta=raw.get("cta", ""),
        ai_image_prompt=raw.get("ai_image_prompt", ""),
        suggested_creative_type=_parse_creative_type(raw.get("suggested_creative_type")),
        text_overlay_suggestion=raw.get("text_overlay_suggestion", ""),
        color_theme_suggestion=raw.get("color_theme_suggestion", ""),
    )


@router.post("/", response_model=ContentResponse)
def generate_content(request: ContentRequest, db: Session = Depends(get_db)):
    # 1. Save input to PostgreSQL projects table
    project = Project(
        business_name=request.business_name,
        industry=request.industry,
        goal=request.business_goal.value,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # 2. Call Gemini API for structured post generation
    try:
        raw_posts = generate_posts_with_ai(request)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI generation failed: {getattr(e, 'message', str(e))}",
        )

    posts = [
        _normalize_post(p, i) for i, p in enumerate(raw_posts[: request.number_of_posts], start=1)
    ]

    # 3. Save generated posts to database
    for p in posts:
        db.add(
            GeneratedPost(
                project_id=project.id,
                post_number=p.post_number,
                caption=p.caption,
                linkedin_version=p.platform_variations.linkedin,
                instagram_version=p.platform_variations.instagram,
                hashtags=p.hashtags,
                cta=p.cta,
                image_prompt=p.ai_image_prompt,
            )
        )
    db.commit()

    return ContentResponse(
        business_name=request.business_name,
        generated_posts=posts,
    )
