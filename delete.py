import requests


post_id = 1

url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

response = requests.delete(url)

print("Status Code:", response.status_code)

if response.status_code == 200:
    print("Post deleted successfully")
else:
    print("Something went wrong")