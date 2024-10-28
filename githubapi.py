import requests
import csv


search_url = 'https://api.github.com/search/users'
params = {
    'q': 'location:Beijing followers:>500',
    'per_page': 100,
    'page': 1
}

TOKEN = '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'
HEADERS = {'Authorization': f'token {TOKEN}'}


# ------------------------------------------------------------------------------------
# FETCH USERS
# ------------------------------------------------------------------------------------

users = []
max_pages = 50

for page in range(1, max_pages+1):
    params['page'] = page
    response = requests.get(search_url, headers= HEADERS, params=params)

    if response.status_code != 200:
        print(f'Error fetching page {page}: {response.status_code}')
        break

    data = response.json()
    users.extend(data.get('items', []))

    if 'next' not in response.links:
        break

# Get User Details
# ------------------------------------------------------------------------------------
user_details = []

for user in users:
    username = user['login']
    user_url = f'https://api.github.com/users/{username}'
    user_response = requests.get(user_url, headers=HEADERS)

    if user_response.status_code != 200:
        print(f'Error fetching details for {username}: {user_response.status_code}')
        continue

    user_data = user_response.json()

    user_info = {
        'login': user_data.get('login'),
        'name': user_data.get('name'),
        'company': user_data.get('company'),
        'location': user_data.get('location'),
        'email': user_data.get('email'),
        'hireable': user_data.get('hireable'),
        'bio': user_data.get('bio'),
        'public_repos': user_data.get('public_repos'),
        'followers': user_data.get('followers'),
        'following': user_data.get('following'),
        'created_at': user_data.get('created_at'),
    }

    if user_info['company']:
        company = user_info['company'].strip()
        company = company.lstrip('@')
        company = company.upper()
        user_info['company'] = company
    else:
        user_info['company'] = None
    
    user_details.append(user_info)


fieldnames = [
    'login', 'name', 'company', 'location', 'email',
    'hireable', 'bio', 'public_repos', 'followers',
    'following', 'created_at'
]

with open('users.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for user_info in user_details:
        writer.writerow(user_info)



# ------------------------------------------------------------------------------------
# FETCH REPOSITORIES
# ------------------------------------------------------------------------------------

# for user in users:
#     username = user['login']
#     repos_url = f'https://api.github.com/users/{username}/repos'
#     repos = []

#     for page in range(1, 500):
#         repo_params = {
#             'per_page': 100,
#             'page': page
#         }
#         repo_response = requests.get(repos_url, params=repo_params)

#         if repo_response.status_code != 200:
#             print(f'Error fetching repos for {username}: {repo_response.status_code}')
#             break

#         repo_data = repo_response.json()
#         repos.extend(repo_data)

#         if len(repo_data) < 100:
#             break

#     repo_names = [repo['name'] for repo in repos]
#     print(f'Users: {username}, Repositiries: {repo_names}')

def fetch_user_repos(
        username,
        max_repos=500
):
    repos = []
    page = 1
    per_page = 100

    while len(repos) < max_repos:
        repo_url = f'https://api.github.com/users/{username}/repos'
        params = {
            'per_page' : per_page,
            'page' : page,
            'sort' : 'created',
            'direction' : 'desc'
        }
        repo_response = requests.get(repo_url, headers=HEADERS, params=params)
        if repo_response.status_code != 200:
            print(f'Error fetching for {username}: {repo_response.status_code}')
            break

        data = repo_response.json()
        if not data:
            break

        repos.extend(data)
        if len(data) < per_page:
            break

        page += 1

    return repos[:max_repos]