import requests
import json

token = "PUT_TOKEN_HERE"  # we can get the error structure from DRF even without a valid token if permissions are strict
res = requests.post("http://127.0.0.1:8000/posts/posts/", data={"title": "Test", "description": "Desc"})
print(res.status_code)
print(res.text)
