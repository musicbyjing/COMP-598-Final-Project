import requests
import json
import os
from datetime import datetime
import time

# CONSTANTS
num_posts = 333
subs = ['politics', 'conservative']
categories = ['hot', 'top', 'controversial']
output_dir = 'data'
current_time = datetime.now().strftime("%Y-%m-%d")

# then conservative hot

"""
Pull data from Reddit API, given:
    subreddit
    category (e.g. Top)
    output file
    filter function
    output file for filtered data
    after marker
Returns the next after
"""
def hit_api(sub_name, category, output_file, filter_func, filtered_output, after):
    data = requests.get(f'https://api.reddit.com/r/{sub_name}/{category}/?t=day&limit=100&after={after}', 
        headers={'User-Agent': 'macos: requests (by /u/school_reddit_acc)'})
    content = data.json()['data']
    posts = content['children'] # type list
    with open(output_file, 'a') as f: # append each post to the output file
        with open(filtered_output, 'a') as g:
            for post in posts:
                data = post['data']
                json.dump(data, f)
                f.write('\n')
                if(filter_func(data)):
                    json.dump(data, g)
                    g.write('\n')

    return content['after'] # for the next iteration

"""
Input: post in dictionary form
Output: True if post mentions Biden or Trump, case-insensitive, False otherwise
"""
def mentions(data):
    title = data['title']
    return True if 'trump' in title.lower() or 'biden' in title.lower() else False

def main():
    after = ""
    for i in range(num_posts//100 + 1):
        # iteration i uses `after` returned in iteration i-1
        for sub_name in subs:
            for category in categories:
                filename = f'{current_time}_{sub_name}_{category}'
                output_file = os.path.join(os.getcwd(), output_dir, filename, '.json')
                filtered_output = os.path.join(os.getcwd(), output_dir, filename, '_filtered.json')
                after = hit_api(sub_name, category, output_file, mentions, filtered_output, after)
            time.sleep(61) # sleep to avoid hitting API access limit

if __name__ == '__main__':
    main()