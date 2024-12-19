# This part of the script is functioning and can be deleted once integrated into the main topicmodel.py script
from google.cloud import bigquery
import os

#Pull data from the BigQuery table and save transcripts as .txt files. Adjust the column name in the SELECT statement and the table name in the FROM statement to match your data.
client = bigquery.Client()
query = """
SELECT full_transcript
FROM `talkiq-data.vidata_q42024.Lex_FY2025_HR_Stratified`
"""

query_job = client.query(query)
results = query_job.result()

output_dir = "transcript_text_files"
os.makedirs(output_dir, exist_ok=True)

for i, row in enumerate(results):
    text_content = row['full_transcript']
    file_path = os.path.join(output_dir, f"text_{i}.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text_content)

print(f"Saved {i+1} text files in the '{output_dir}' directory.")