from pydantic import BaseModel

class RecommendBody(BaseModel):
    data: str