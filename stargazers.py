
# coding: utf-8

# # Install Python Pandas and Request Library.
# To do so run the below command on your Terminal or Command line

$ pip install requests
$ pip install pandas   


# # Retrieve starred date and stargazers of most starred repository
# stargazers are the users who starred the repository.
# Github provides a api to get as many public repositories with their owners, which will be userd in next api call to retreive starred_date and stargazers information
# We will retreive most starred repositories in decending order with below api call.
# url - https://api.github.com/repositories?&sort=stars&order=desc
# Github provides a api to get all users who starred a given repository
# url - https://api.github.com/repos/:owner/:repo name/stargazers


# # Let's Code

# In[63]:


import pandas as pd
import requests
from datetime import datetime

def openGitApi():
    # Making a list for 10 iterations and to avoid "while" loop, as while loop is slower compared to "for" loop.
    pages = [1,2,3,4,5,6,7,8,9,10]

    # Data frame to store starred repositories with their owners.
    df_repos = pd.DataFrame(columns=['repository_name','owner'])

    # Data frame to store final output of repositories with the day when it was starred along with stargazers.
    df_stars = pd.DataFrame(columns=['repository_name','owner_name','starred_date',  'stargazer_name'])

    # url variable for getting most starred repository in descending order
    base_url_1 = 'https://api.github.com/repositories?&sort=stars&order=desc%page='

    #url for getting the starred_date and stargazer of repositories.
    base_url_2 = 'https://api.github.com/repos/'

    # Git hub provides only 60 api requests per hour, to do more requests you have to go with authentication token.
    git_username = ' paste you git username'
    git_token = 'paste your git token for autherization'
    # loop to retrieve most starred public repositories.
    for page in pages:
        url = ''.join([base_url_1, str(page)])
        response = requests.get(
            url,auth=(git_username,git_token)
        )
        json_response = response.json()
        #print(json_response)
        for repos in json_response:
            d_tmp = {'repository_name': repos['name'],
                     'owner': repos['owner']['login']
                        }
            df_repos = df_repos.append(d_tmp, ignore_index=True)

    #loop for retrieve the starred_date and stargazer of repositories receieved from above code        
    for value in df_repos.iterrows():    
        url = ''.join([base_url_2,value[1]['owner'],'/',value[1]['repository_name'],'/','stargazers' ])
        response = requests.get(url,
        params={'q': 'requests+language:python'},
        headers={'Accept': 'application/vnd.github.v3.star+json'},
        auth=(git_username,git_token),                        
        )
        json_response = response.json()
        for user in json_response:
            d_tmp = {'repository_name': value[1]['repository_name'],
                        'owner_name': value[1]['owner'],
                        'starred_date': datetime.strptime(user['starred_at'],'%Y-%m-%dT%H:%M:%SZ'),
                        'stargazer_name': user['user']['login']
                    }
            df_stars = df_stars.append(d_tmp, ignore_index=True)
    df_stars.to_csv('/Users/rohitthapliyal/Downloads/repo_starred.csv', index = False)    

#change path as per your machine directory to save the dataframe to csv
if __name__ == "__main__": 
    openGitApi()

