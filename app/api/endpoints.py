import random

from fastapi import APIRouter
from app.models.request import RecommendBody
from app.urlcategorizer.urlcategorizer import extract_relevant_content, preprocess_text, categorize_text
from app.models.db_schema import categories_keywords, category_map

router = APIRouter()

@router.post("/advertise-recommendation")
def advertise_recommendation(request: RecommendBody):
    content = extract_relevant_content(request.url)

    combined_text = " ".join([
        content["meta_keywords"],
        content["meta_description"],
        content["title"],
        " ".join(content["headings"]),
        " ".join(content["paragraphs"])
    ])

    tokens = preprocess_text(combined_text)

    best_category, _ = categorize_text(tokens, categories_keywords)

    random_key = random.choice(list(category_map[best_category].keys()))
    random_value = category_map[best_category][random_key]
    print(random_key, " ", random_value)

    return {
        "imageUrl": random_value,
        "linkUrl": "https://upb.ro/",
        "type": random_key
    }