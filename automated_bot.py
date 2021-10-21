import requests
import random


def get_token(username, password):
    url = 'http://127.0.0.1:8000/get_token'
    credentials = {
        'username': username,
        'password': password,
    }
    response = requests.post(url, data=credentials).json()
    return response['access']


def create_user(headers, username, password):
    url = 'http://127.0.0.1:8000/users'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def create_post(headers, title, content):
    url = 'http://127.0.0.1:8000/posts'
    data = {
        'title': title,
        'content': content
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def get_all_users(headers):
    url = 'http://127.0.0.1:8000/users'
    response = requests.get(url, headers=headers)
    return response.json()


def get_all_posts(headers):
    url = 'http://127.0.0.1:8000/posts'
    response = requests.get(url, headers=headers)
    return response.json()


def like_post(headers, post_id):
    url = f'http://127.0.0.1:8000/smash_like_button/{post_id}'
    response = requests.post(url, headers=headers)
    return response.json()


def get_config_file_data():
    with open('config.txt', 'r') as f:
        data = f.read()
    first_line, second_line, third_line = data.split('\n')
    return int(first_line.split('=')[1]), int(second_line.split('=')[1]), int(third_line.split('=')[1])


# get data from config file
number_of_users, max_posts_per_user, max_likes_per_user = get_config_file_data()

admin_token = get_token('admin', 'admin')
admin_headers = {'Authorization': f"Bearer {admin_token}"}

# signing up users
for i in range(1, number_of_users + 1):
    create_user(admin_headers, f"user{i}", f"user1")

# each user creates random number of posts (max = max_posts_per_user)
users = get_all_users(admin_headers)
for user in users:
    if user['username'] == 'admin':
        continue
    user_token = get_token(user['username'], 'user1')
    user_headers = {'Authorization': f"Bearer {user_token}"}
    for i in range(1, random.randint(1, max_posts_per_user) + 1):
        create_post(user_headers, f"title#{i} by user {user['username']}", f"content#{i} by user {user['username']}")

# liking posts randomly (max = max_likes_per_user)
posts = get_all_posts(admin_headers)
for user in users:
    if user['username'] == 'admin':
        continue
    user_token = get_token(user['username'], 'user1')
    user_headers = {'Authorization': f"Bearer {user_token}"}
    for post in posts:
        if random.random() > 0.4:
            print(user_headers, post['id'])
            print(like_post(user_headers, post['id']))
