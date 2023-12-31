import json
import pandas as pd
from re import sub
import ast
storage_client = storage.Client()

bucket = storage_client.get_bucket("intern_cicle")
input_file_path = "scraping_result"
output_file_path = "cleaned_data"

blob = bucket.blob(input_file_path)
blob.download_to_filename('/tmp/relevant_play_store_reviews.csv')

df1 = pd.read_csv('/tmp/relevant_play_store_reviews.csv')

rename_dict = {'com.Slack':'slack',
    'com.microsoft.teams':'microsoft teams',
    'com.asana.app':'asana',
    'com.basecamp.bc3':'basecamp',
    'com.trello':'trello',
    'com.atlassian.android.jira.core':'jira cloud',
    'com.monday.monday':'monday.com',
    'com.wrike':'wrike',
    'com.smartsheet.android':'smartsheet',
    'com.zoho.projects':'zoho projects',
    'io.quire.app':'quire',
    'com.todoist':'todoist',
    'com.meisterlabs.meistertask.native':'meistertask',
    'com.proofhub':'proofhub'}
df1['appId']=df1['appId'].replace(rename_dict)

df1['review_date'] = pd.to_datetime(df1['at'])

df1['title']=None
df1['edited']=None
df1=df1.drop(['userImage','repliedAt','at','appVersion'], axis=1)

rename_column={'reviewId':'id',
               'userName':'username',
               'content':'review',
               'thumbsUpCount':'thumbs_up_count',
               'reviewCreatedVersion':'app_version',
               'replyContent':'reply',
               'appId':'app_name',
               'score':'rating'
              }
df1=df1.rename(columns=rename_column)
df1_final=df1[['id',
              'username',
              'rating',
              'title',
              'review',
              'review_date',
              'app_version',
              'thumbs_up_count',
              'edited',
              'reply',
              'app_name',
              'source']]

df2 = pd.read_csv('/tmp/app_store_reviews.csv')

df2['review_date'] = pd.to_datetime(df2['date'])

df2['reply'] = df2['developerResponse']\
                .apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else None)
df2['reply'] = df2['reply'].apply(lambda x: x['body'] if pd.notnull(x) else None)
df2["reply"] = df2["reply"].str.replace('\n', ' ')
df2["reply"] = df2["reply"].str.replace('\'', '')

df2['id']=None
df2['thumbs_up_count']=None
df2['app_version']=None
df2['source'] = 'appstore'
df2=df2.drop(['date','developerResponse'], axis=1)

rename_dict = {'microsoft-teams':'microsoft teams'}
df2['app_name']=df2['app_name'].replace(rename_dict)

rename_column={'isEdited':'edited',
               'userName':'username'
              }
df2=df2.rename(columns=rename_column)
df2_final=df2[['id',
              'username',
              'rating',
              'title',
              'review',
              'review_date',
              'app_version',
              'thumbs_up_count',
              'edited',
              'reply',
              'app_name',
              'source'
              ]]

df1_final = df1_final.append(df2_final, ignore_index=True)

df1_final["username"] = df1_final["username"].str.replace('\n', ' ')
df1_final["username"] = df1_final["username"].str.replace('\'', '')
df1_final["username"] = df1_final["username"].str.replace(';', ' ')

df1_final["title"] = df1_final["title"].astype(str)
df1_final["title"] = df1_final["title"].apply(lambda x: sub('[^\w\s]', ' ', x))
df1_final["title"] = df1_final["title"].replace(r'\s+', ' ', regex=True)
df1_final["title"] = df1_final["title"].str.strip()
df1_final['title'] = df1_final['title'].str.lower()
df1_final['title'] = df1_final["title"]\
                            .apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))

df1_final["review"] = df1_final["review"].astype(str)
df1_final["review"] = df1_final["review"].apply(lambda x: sub('[^\w\s]', ' ', x))
df1_final["review"] = df1_final["review"].replace(r'\s+', ' ', regex=True)
df1_final["review"] = df1_final["review"].str.strip()
df1_final['review'] = df1_final['review'].str.lower()
df1_final['review'] = df1_final["review"]\
                            .apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))

df1_final["reply"] = df1_final["reply"].astype(str)
df1_final["reply"] = df1_final["reply"].apply(lambda x: sub('[^\w\s]', ' ', x))
df1_final["reply"] = df1_final["reply"].replace(r'\s+', ' ', regex=True)
df1_final["reply"] = df1_final["reply"].str.strip()
df1_final['reply'] = df1_final['reply'].str.lower()
df1_final['reply'] = df1_final["reply"]\
                            .apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))

df1_final.to_csv('all_app_reviews.csv', index=None, header=True)

output_bucket = storage_client.get_bucket(bucket_name)
output_blob = output_bucket.blob(output_file_path)
output_blob.upload_from_filename('/tmp/all_app_reviews.csv')

os.remove('/tmp/relevant_play_store_reviews.csv')
os.remove('/tmp/app_store_reviews.csv')
os.remove('/tmp/all_app_reviews.csv')