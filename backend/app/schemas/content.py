from pydantic import BaseModel, Field
from enum import Enum
from typing import List


class BusinessGoal(str, Enum):
    leads = "Leads"
    branding = "Branding"
    sales = "Sales"
    engagement = "Engagement"


class ToneType(str, Enum):
    professional = "Professional"
    friendly = "Friendly"
    bold = "Bold"
    educational = "Educational"


class ContentRequest(BaseModel):
    business_name: str
    industry: str
    target_audience: str
    location: str
    business_goal: BusinessGoal
    tone: ToneType
    number_of_posts: int = Field(default=5, ge=1, le=30)


class PlatformVariations(BaseModel):
    instagram: str
    linkedin: str
    facebook: str


class CreativeType(str, Enum):
    carousel = "Carousel"
    reel = "Reel"
    static_post = "Static Post"


class PostResponse(BaseModel):
    post_number: int
    post_topic: str
    caption: str  # platform-neutral
    platform_variations: PlatformVariations
    hashtags: list[str]
    cta: str
    # Image/creative suggestions (no actual image generated)
    ai_image_prompt: str  # for DALL·E / Midjourney / Stable Diffusion
    suggested_creative_type: CreativeType
    text_overlay_suggestion: str
    color_theme_suggestion: str


class ContentResponse(BaseModel):
    business_name: str
    generated_posts: List[PostResponse]
