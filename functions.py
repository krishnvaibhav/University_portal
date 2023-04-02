import os
import json
from serpapi import GoogleSearch

search_term = input("Enter search term: ")

params = {
    "engine": "duckduckgo",
    "q": f"{search_term} tutorial",
    "sort_by": "rating",
    "sort_order": "desc",
    "num": 10,
    "api_key": "50c1f2cb977b3a7e2f8cc9f4a11e7cdebdeb1bf6345078cd1875a59399509204",
}

search = GoogleSearch(params)
results = search.get_dict()

links = []

for result in results["organic_results"]:
    links.append(result)

