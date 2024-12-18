from pydantic import BaseModel

class RecommendBody(BaseModel):
    url: str