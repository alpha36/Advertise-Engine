import requests
from bs4 import BeautifulSoup
import re


def extract_relevant_content(url):
    """
    Fetch the webpage at `url` and extract text relevant for keyword searches:
      - Meta tags (keywords, description, possibly Open Graph)
      - Headings (h1-h4)
      - Paragraphs (p)

    Returns a dictionary with:
      {
        "url": ...,
        "title": ...,
        "meta_keywords": ...,
        "meta_description": ...,
        "headings": [...],
        "paragraphs": [...]
      }
    """

    # 1. Fetch the page
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raises HTTPError if the status is 4xx or 5xx

    # 2. Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # 3. Remove unwanted elements (scripts, styles, nav, etc.)
    for tag in soup(["script", "style", "nav", "header", "footer", "form", "aside"]):
        tag.extract()

    # 4. Extract meta tags
    #    (Note: Some sites may not have these, or might use alternate metadata conventions)

    # Meta keywords
    meta_keywords_tag = soup.find("meta", attrs={"name": re.compile("^keywords$", re.I)})
    meta_keywords = meta_keywords_tag["content"] if meta_keywords_tag and "content" in meta_keywords_tag.attrs else ""

    # Meta description
    meta_description_tag = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    meta_description = meta_description_tag[
        "content"] if meta_description_tag and "content" in meta_description_tag.attrs else ""

    # 5. Extract headings (h1, h2, h3, h4, etc.)
    #    Adjust as needed: h5, h6, or other tags if you want more detail
    headings = []
    for heading_tag in soup.find_all(["h1", "h2", "h3", "h4"]):
        heading_text = heading_tag.get_text(separator=" ", strip=True)
        if heading_text:
            headings.append(heading_text)

    # 6. Extract paragraphs
    paragraphs = []
    for p_tag in soup.find_all("p"):
        p_text = p_tag.get_text(separator=" ", strip=True)
        if p_text:
            paragraphs.append(p_text)

    # 7. (Optional) You might also want to extract title from <title> tag
    page_title_tag = soup.find("title")
    page_title = page_title_tag.get_text(strip=True) if page_title_tag else ""

    # 8. Package the results in a dictionary
    content_data = {
        "url": url,
        "title": page_title,
        "meta_keywords": meta_keywords,
        "meta_description": meta_description,
        "headings": headings,
        "paragraphs": paragraphs
    }

    return content_data


def preprocess_text(raw_text):
    """
    Lowercase the text, remove punctuation (except letters, numbers, spaces),
    and split into a list of words (tokens).
    """
    text = raw_text.lower()                          # Convert to lowercase
    text = re.sub(r'[^a-z0-9\s]', '', text)          # Remove punctuation
    words = text.split()                             # Split into tokens
    return words

def categorize_text(words, category_keywords):
    """
    Dictionary-based categorization:
      - Each category has a list of keywords
      - We count how many times category keywords appear in the text
      - Return (best_category, category_scores_dict)
    """
    category_scores = {}
    for category, keywords in category_keywords.items():
        score = 0
        for kw in keywords:
            score += words.count(kw)
        category_scores[category] = score

    # Pick the category with the highest score
    best_category = max(category_scores, key=category_scores.get)
    return best_category, category_scores