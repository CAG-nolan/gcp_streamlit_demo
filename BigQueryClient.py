from google.cloud import bigquery

class BigQueryClient:
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
        query_job = self.CLIENT.query(self.QUERY)
        return query_job.to_json()

client = BigQueryClient()
print(client.return_json)
