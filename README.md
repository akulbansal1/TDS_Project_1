- I used GitHub API to query data from GitHub on users (and their 500 latest repositories) in Beijing with more than 500 followers.
-	Even though the most popular language (when looked at the entire dataset) is by a wide margin Jinja, further investigation reveals other languages are also just as popular.
-	Developers could look at which languages are the most popular in practice but are not very popular on GitHub and create projects in those languages.

# TDS_Project_1
Quiz ID: Beijing:500
## Data
The script `githubapi.py` collects raw data using the [GitHub API](https://docs.github.com/en/rest?apiVersion=2022-11-28) and searches for users located in **Beijing** with more than **500** followers and iterated through up to 50 pages to compile a list of users. The parameters can be changed by editing the python dictionary `params`.
```python
search_url = 'https://api.github.com/search/users'

params = {
'q': 'location:Beijing followers:>500',
'per_page': 100,
'page': 1
}
```
To enable the script for larger data extraction, GitHub TOKEN is used for authorisation.
```python
TOKEN = 'INSERT_TOKEN_HERE'
HEADERS = {'Authorization': f'token {TOKEN}'}
```
The script then iterates through all the users and stores the details of each user to `users_raw.csv`. Then, it fetches up to 500 latest repositories for each user, extracts relevant details and saves this data to `repositories_raw.csv`. The data is then cleaned by replacing `NaN` values with empty strings and Boolean values as 'true' and 'false'. The cleaned data, stored in `users.csv` and `repositories.csv`, is then used for further analysis.

## Findings
```python
import pandas as pd

repos_dataset = pd.read_csv('repositories.csv')
repos_dataset['year_created'] = repos_dataset.created_at.dt.year
year_language_data = repos_dataset[['stargazers_count', 'year_created', 'language']]
```
5 most popular language by average `stargazers_count`
```python
year_language_data.groupby('language').mean().sort_values(by='stargazers_count', ascending=False)[:5][['stargazers_count']]
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>stargazers_count</th>
    </tr>
    <tr>
      <th>language</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Jinja</th>
      <td>3430.00</td>
    </tr>
    <tr>
      <th>Solidity</th>
      <td>1289.44</td>
    </tr>
    <tr>
      <th>VBScript</th>
      <td>699.00</td>
    </tr>
    <tr>
      <th>Lex</th>
      <td>482.50</td>
    </tr>
    <tr>
      <th>TeX</th>
      <td>294.51</td>
    </tr>
  </tbody>
</table>

```python
popular_languages = ['Jinja', 'Solidity', 'VBScript', 'Lex', 'TeX']
pop_lang_data = year_language_data[year_language_data['language'].isin(popular_languages)]
pop_lang_data.groupby(['year_created','language']).mean().sort_values(by=['language', 'year_created'])
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>stargazers_count</th>
    </tr>
    <tr>
      <th>year_created</th>
      <th>language</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020</th>
      <th>Jinja</th>
      <td>3430.00</td>
    </tr>
    <tr>
      <th>2014</th>
      <th>Lex</th>
      <td>948.00</td>
    </tr>
    <tr>
      <th>2016</th>
      <th>Lex</th>
      <td>982.00</td>
    </tr>
    <tr>
      <th>2018</th>
      <th>Lex</th>
      <td>0.00</td>
    </tr>
    <tr>
      <th>2019</th>
      <th>Lex</th>
      <td>0.00</td>
    </tr>
    <tr>
      <th>2021</th>
      <th>Solidity</th>
      <td>2.00</td>
    </tr>
    <tr>
      <th>2022</th>
      <th>Solidity</th>
      <td>2311.80</td>
    </tr>
    <tr>
      <th>2023</th>
      <th>Solidity</th>
      <td>15.00</td>
    </tr>
    <tr>
      <th>2024</th>
      <th>Solidity</th>
      <td>14.00</td>
    </tr>
    <tr>
      <th>2011</th>
      <th>TeX</th>
      <td>5328.00</td>
    </tr>
    <tr>
      <th>2013</th>
      <th>TeX</th>
      <td>16.00</td>
    </tr>
    <tr>
      <th>2014</th>
      <th>TeX</th>
      <td>221.67</td>
    </tr>
    <tr>
      <th>2015</th>
      <th>TeX</th>
      <td>92.80</td>
    </tr>
    <tr>
      <th>2016</th>
      <th>TeX</th>
      <td>13.40</td>
    </tr>
    <tr>
      <th>2017</th>
      <th>TeX</th>
      <td>392.60</td>
    </tr>
    <tr>
      <th>2018</th>
      <th>TeX</th>
      <td>408.85</td>
    </tr>
    <tr>
      <th>2019</th>
      <th>TeX</th>
      <td>10.12</td>
    </tr>
    <tr>
      <th>2020</th>
      <th>TeX</th>
      <td>104.25</td>
    </tr>
    <tr>
      <th>2021</th>
      <th>TeX</th>
      <td>16.50</td>
    </tr>
    <tr>
      <th>2022</th>
      <th>TeX</th>
      <td>0.00</td>
    </tr>
    <tr>
      <th>2023</th>
      <th>TeX</th>
      <td>1.67</td>
    </tr>
    <tr>
      <th>2024</th>
      <th>TeX</th>
      <td>28.00</td>
    </tr>
    <tr>
      <th>2020</th>
      <th>VBScript</th>
      <td>699.00</td>
    </tr>
  </tbody>
</table>

Even though Jinja is the most popular language (among the top contributors in Beijing) based on average `stargazers_count`, all the repositories that use *Jinja* were, surprisingly, only created in 2020. On the other hand, other languages like *Tex*, *Lex*, *Solidity* have been used for longer periods and also have more consistency in being placed high on average stargazers_count. In fact, *Tex* even has the highest average stargazers_count when looked at on a 'per year' basis, which was otherwise hidden if the data is looked at in aggregate.

## Recommendation
Looking at the popularity of each language on GitHub and the general popularity of those languages in the industry, developers could create repositories in the languages that are widely used in practice but are not very popular on GitHub. Doing this will provide help to a lot of other developers who might be just starting to use those languages. A good way to start is to look at existing popular projects in the most popular language and then replicate those projects in other languages.

A straightforward extension of the analysis is if the reader relaxes the search criteria. Since we are only looking at the data of the most popular contributors **today**, the data has a 'survivorship bias' due to the simple fact that the popular contributors today will not be the same as the popular contributors two, three, etc. years ago. The search criteria could be relaxed. Unfortunately, GitHub API does not support point-in-time data querying. A possible workaround is to filter the users by relaxing the minimum followers to 'greater than 50'. Another workaround could be using [GitHub Archive](https://www.gharchive.org/) to query point-in-time data.
