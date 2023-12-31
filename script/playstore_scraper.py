import json
import pandas as pd
from tqdm import tqdm
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from google_play_scraper import Sort, reviews, app, reviews_all
from re import sub
from time import sleep
from google.cloud import storage

storage_client = storage.Client()

bucket = storage_client.get_bucket("intern_cicle")
output_file_path = "scraping_result"

app_packages = [
    'com.Slack',
    'com.microsoft.teams',
    'com.asana.app',
    'com.basecamp.bc3',
    'com.trello',
    'com.atlassian.android.jira.core',
    'com.monday.monday',
    'com.wrike',
    'com.smartsheet.android',
    'com.zoho.projects',
    'io.quire.app',
    'com.todoist',
    'com.meisterlabs.meistertask.native',
    'com.proofhub'
]

def print_json(json_object):
    json_str = json.dumps(
        json_object,
        indent=4,
        sort_keys=False,
        default=str
    )
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))

app_reviews_mr = []

for ap in tqdm(app_packages):
    rvsa, _ = reviews(
        ap,
        lang='en',
        country='us',
        sort=Sort.MOST_RELEVANT,
        count= 200000, #if score == 3 else 100,
    )
    for r in rvsa:
#         r['sortOrder'] = 'newest' #if sort_order == Sort.MOST_RELEVANT else 'newest'
        r['appId'] = ap
        r['source'] = 'playstore'
    app_reviews_mr.extend(rvsa)
    sleep(5)

app_reviews_df = pd.DataFrame(app_reviews_mr)
app_reviews_df["content"] = app_reviews_df["content"].str.replace('\n', ' ')
app_reviews_df["content"] = app_reviews_df["content"].str.replace('\'', '')
app_reviews_df["replyContent"] = app_reviews_df["replyContent"].str.replace('\n', ' ')
app_reviews_df["replyContent"] = app_reviews_df["replyContent"].str.replace('\'', ' ')

app_reviews_df.to_csv('/tmp/relevant_play_store_reviews.csv', index=None, header=True)

output_bucket = storage_client.get_bucket(bucket_name)
output_blob = output_bucket.blob(output_file_path)
output_blob.upload_from_filename('/tmp/relevant_play_store_reviews.csv')

os.remove('/tmp/relevant_play_store_reviews.csv')