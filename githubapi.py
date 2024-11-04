import requests
import csv


search_url = 'https://api.github.com/search/users'
params = {
    'q': 'location:Beijing followers:>500',
    'per_page': 100,
    'page': 1
}

TOKEN = 'INSERT_TOKEN_HERE'
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


def extract_repo_details(repo, owner_login):
    return {
        'login': owner_login,
        'full_name': repo.get('full_name'),
        'created_at': repo.get('created_at'),
        'stargazers_count': repo.get('stargazers_count'),
        'watchers_count': repo.get('watchers_count'),
        'language': repo.get('language'),
        'has_projects': repo.get('has_projects'),
        'has_wiki': repo.get('has_wiki'),
        'license_name': repo.get('license', {}).get('name') if repo.get('license') else None
    }

all_repo_details = []

for user in users:
    username = user['login']
    print(f'Fetching repositories for user: {username}')
    repos = fetch_user_repos(username)
    for repo in repos:
        repo_details = extract_repo_details(repo, username)
        all_repo_details.append(repo_details)

fieldnames = [
    'login',
    'full_name',
    'created_at',
    'stargazers_count',
    'watchers_count',
    'language',
    'has_projects',
    'has_wiki',
    'license_name'
]

with open('repositories_raw.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for repo_info in all_repo_details:
        writer.writerow(repo_info)



# ------------------------------------------------------------------------------------
# QUESTIONS AND ANALYSIS
# ------------------------------------------------------------------------------------

users_dataset = pd.read_csv('users_raw.csv')
repos_dataset = pd.read_csv('repositories_raw.csv')

# Clean data
users_dataset = users_dataset.applymap(lambda x: 'true' if x is True else 'false' if x is False else '' if pd.isnull(x) else x)
users_dataset.to_csv('users.csv')

repos_dataset = repos_dataset.applymap(lambda x: 'true' if x is True else 'false' if x is False else '' if pd.isnull(x) else x)
repos_dataset.to_csv('repositories.csv')


# Question 1
users_dataset.sort_values(by='followers', ascending=False)[:5].login

# Question 2
users_dataset.sort_values(by='created_at')[:5].login

# Question 3
repos_dataset.groupby('license_name').count().sort_values(by='login', ascending=False)[:3]

# Question 4
users_dataset.groupby('company').count().sort_values(by='login', ascending=False)[:1]

# Question 5
repos_dataset.groupby('language').count().sort_values(by='login', ascending=False)[:3]

# Question 6
users_dataset['year_joined'] = users_dataset.created_at.str[:4].astype(int)
post2020 = users_dataset[users_dataset['year_joined'] > 2019]['login']
filtered_repos_dataset = repos_dataset[repos_dataset['login'].isin(post2020)]

filtered_repos_dataset.groupby('language').count().sort_values(by='login', ascending=False)[:3]

# Question 7
repos_dataset.groupby('language')['stargazers_count'].mean().sort_values(ascending=False)[:5]

# Question 8
users_dataset['leader_strength'] = users_dataset['followers'] / (1 + users_dataset['following'])
users_dataset.sort_values(by='leader_strength', ascending=False)[:6]

# Question 9
users_dataset['followers'].corr(users_dataset['public_repos'])

# Question 10
from sklearn.linear_model import LinearRegression

X = users_dataset[['public_repos']]
y = users_dataset['followers']
model = LinearRegression()
model.fit(X, y)
model.coef_[0]

# Question 11
repos_dataset['has_projects'].corr(repos_dataset['has_wiki'])

# Question 12
hireable = users_dataset[users_dataset['hireable']==True]
not_hireable = users_dataset[users_dataset['hireable']!=True]

hireable['following'].mean() - not_hireable['following'].mean()

# Question 13
users_dataset['word_count'] = users_dataset['bio'].str.split().str.len()
bio_followers = users_dataset[['word_count','followers']].dropna(how='any')
X = bio_followers[['word_count']]
y = bio_followers['followers']
model = LinearRegression()
model.fit(X, y)
model.coef_[0]

# Question 14
repos_dataset['created_at'] = pd.to_datetime(repos_dataset['created_at'])
weekend_repos = repos_dataset[repos_dataset['created_at'].dt.dayofweek >= 5]
weekend_repos['login'].value_counts().sort_values(ascending=False)[:6]

# Question 15
(len(hireable['email'].dropna(how='any')) / len(hireable['email'])) - ((len(not_hireable['email'].dropna(how='any')) / len(not_hireable['email'])))

# Question 16
users_dataset['second_name'] = users_dataset['name'].str.split().str[1]
users_dataset.groupby('second_name').count().sort_values(by='login', ascending=False)[:6]


# Analysis
repos_dataset['year_created'] = repos_dataset.created_at.dt.year
year_language_data = repos_dataset[['stargazers_count', 'year_created', 'language']]

year_language_data.groupby('language').mean().sort_values(by='stargazers_count', ascending=False)[:5][['stargazers_count']]

popular_languages = ['Jinja', 'Solidity', 'VBScript', 'Lex', 'TeX']
year_language_data[year_language_data['language'].isin(popular_languages)]

year_language_data.groupby(['year_created','language']).mean()
