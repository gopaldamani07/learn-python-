import requests


post_id = 1

url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

updated_post = {
    "id": post_id,
    "title": "update...",
    "body": "This is upadted",
    "userId": 1
}

response = requests.put(
    url,
    json=updated_post
)

print("Status Code:", response.status_code)
print("Response:", response.json())