import requests

base_url = "http://localhost:8080/predict"

headers = {
    "accept": "application/json",
}

def categorize(param):
    query_param = {"url": param}
    response = requests.post(base_url, headers=headers, data="", params=query_param)

    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.json() if response.headers.get("Content-Type") == "application/json" else response.text)
