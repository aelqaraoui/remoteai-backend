import os
import re
import json
from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient('mongodb+srv://amineelqaraoui:bHDVb1BW0lzWdnx4@jobs.47twkjx.mongodb.net/?retryWrites=true&w=majority')
db = client['JOBS']
collection = db['listings']

valid_jsons = []

# Loop through all the JSON files in the "jobs" folder
folder = 'jobs'
for filename in os.listdir(folder):
    with open(os.path.join(folder, filename), 'r') as f:
        job_data = json.load(f)

        # Insert the job_data into the MongoDB database
        collection.insert_one(job_data)
        print(f"Processed and stored {filename}")
        
        # Check if there are any numerical values in the 'salary' field
        salary = job_data['salary']
        if re.search(r'\d', salary) and 'remote' in job_data['location'].lower():
            valid_jsons.append(job_data)

import json
import os
from sentence_transformers import SentenceTransformer
import pinecone
import numpy as np

model = SentenceTransformer('distilbert-base-nli-mean-tokens')

pinecone.init(api_key="cb3fb340-7ed6-439b-905f-fa1b7a8b08d1", environment='us-east4-gcp')

print(pinecone.list_indexes())

index_name = pinecone.list_indexes()[0]

index = pinecone.Index(index_name=index_name)

import pandas as pd
df = pd.DataFrame.from_records(valid_jsons)

from typing import Iterator

class BatchGenerator:
    """ Models a simple batch generator that make chunks out of an input DataFrame. """
    
    def __init__(self, batch_size: int = 10) -> None:
        self.batch_size = batch_size
    
    def to_batches(self, df: pd.DataFrame) -> Iterator[pd.DataFrame]:
        """ Makes chunks out of an input DataFrame. """
        splits = self.splits_num(df.shape[0])
        if splits <= 1:
            yield df
        else:
            for chunk in np.array_split(df, splits):
                yield chunk
    
    def splits_num(self, elements: int) -> int:
        """ Determines how many chunks DataFrame contians. """
        return round(elements / self.batch_size)
    
    __call__ = to_batches

df_batcher = BatchGenerator(300)

print(df.columns)

for column in df.columns:
    if column in ['title', 'location', 'jobType', 'jobLevel', 'salary', 'company', 'description']:
        print(f'Encoding {column}s...')
        encoded_titles = model.encode(df[column].tolist(), show_progress_bar=True)
        df[column + '_vector'] = encoded_titles.tolist()

        df['vector_id'] = df['hash']
        df['vector_id'] = df['vector_id'].apply(str)

        # Upsert title vectors in title namespace
        print(f"Uploading vectors to {column} namespace..")
        for batch_df in df_batcher(df):
            index.upsert(vectors=zip(batch_df['vector_id'], batch_df[column + '_vector']), namespace=column)
            