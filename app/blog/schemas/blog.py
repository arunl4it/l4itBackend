from pydantic import BaseModel, ConfigDict
from typing import Optional

class BlogBase(BaseModel):
    image: Optional[str] = None
    heading: str
    short_description: str
    content: str
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
