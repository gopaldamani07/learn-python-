import requests


url = "https://jsonplaceholder.typicode.com/posts"

new_post = {
    "title": "helo rg",
    "body": "I am fvd",
    "userId": 1
}

response = requests.post(
    url,
    json=new_post
)

print("Status Code:", response.status_code)
print("Response:", response.json())