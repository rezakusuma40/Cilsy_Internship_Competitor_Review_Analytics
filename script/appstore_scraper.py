from app_store_scraper import AppStore
import pandas as pd
from re import sub
from time import sleep
from google.cloud import storage

storage_client = storage.Client()

bucket = storage_client.get_bucket("intern_cicle")
output_file_path = "scraping_result"

app_reviews=[]

# Specify the app IDs or app names you want to scrape
app_names = ['slack', 'trello', 'asana', 'microsoft-teams', \
             'basecamp', 'monday.com', 'jira cloud', 'wrike', \
             'smartsheet', 'zoho projects', 'quire', 'todoist', \
             'meistertask', 'proofhub']
# Scrape the app details, ratings, and reviews for each app
for name in app_names:
    try:
        app = AppStore(country="us", app_name=name)
        app.review(how_many=2000)
        reviews = app.reviews
        for review in reviews:
            review['app_name']=name
            review['source']='appstore'
    #     print(app.reviews)
        app_reviews.extend(app.reviews)
        sleep(60)
    except:
        continue

app_reviews_df = pd.DataFrame(app_reviews)
app_reviews_df["review"] = app_reviews_df["review"].str.replace('\n', ' ')
app_reviews_df["review"] = app_reviews_df["review"].str.replace('\'', '')
app_reviews_df["title"] = app_reviews_df["title"].str.replace('\n', ' ')
app_reviews_df["title"] = app_reviews_df["title"].str.replace('\'', '')

app_reviews_df.to_csv('/tmp/app_store_reviews.csv', index=None, header=True)

output_bucket = storage_client.get_bucket(bucket_name)
output_blob = output_bucket.blob(output_file_path)
output_blob.upload_from_filename('/tmp/app_store_reviews.csv')

os.remove('/tmp/app_store_reviews.csv')