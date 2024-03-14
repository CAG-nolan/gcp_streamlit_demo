"""
This is a wrapper for the NPD data agent. The NPD data agent uses google query to fetch data form a google GCP
bucket. This data can come in as a variety of types, but it is indexed and analyzed through the google indexer.
The data that is collected from these data sources is the basis for the content generation and contextualization.

This wrapper will find the target age demographic for a specific category, as well as the most desirable prep time
for that food item. From there, the application will return the result as either a JSON or a text object, which can
then be used to generate novel and exciting food creations.

These will then be sent to the generation service which will create the content and images based on the data provided 
from within this wrapper
"""

from google.cloud import bigquery

class NPDWrapper:
    PROJECT_ID = "gcp-atcbld0004344"
    BQ_DATASET = "food"
    BQ_TABLE = "iri_handhelds_upc_data"
    BQ_FULLTABLE = PROJECT_ID + "." + BQ_DATASET + "." + BQ_TABLE
    QUERY = f"CALL {BQ_DATASET}.npd_search('','','')"
    CLIENT = bigquery.Client()

    def return_dataframe(self):
        query_job = self.CLIENT.query(self.QUERY)
        return query_job.to_dataframe()

    def return_json(self):
        query_job = self.return_dataframe()
        return query_job.to_json(orient='records')
