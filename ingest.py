import json
import os
import uuid
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()
pc_api = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=pc_api)

index = pc.Index("ragtest")

with open("data/deeplearning_batch_301_to_305.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

records = []
for article in articles:
    records.append({
        "_id": str(uuid.uuid4()),
        "text": article["text"],  
        "title": article["title"],
        "image_url": article["image_url"],
        "link": article["link"]
    })

index.upsert_records("__default__", records)
    
print(f"Inserted {len(records)} articles into Pinecone.")
