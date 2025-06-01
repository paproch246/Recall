import subprocess
import time
import os
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import ConnectionError


def start_elasticsearch():
    elasticsearch_home = "C:/Users/papro/Documents/Recall/elasticsearch-9.0.0"
    elasticsearch_bat = os.path.join(elasticsearch_home, "bin", "elasticsearch.bat")
    
    if os.path.exists(elasticsearch_bat):
        print("Starting Elasticsearch...")
        try:
            # Change to Elasticsearch directory first
            original_dir = os.getcwd()
            os.chdir(elasticsearch_home)
            
            # Start Elasticsearch without redirecting output so we can see what's happening
            process = subprocess.Popen(
                f'"{elasticsearch_bat}"',
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            # Change back to original directory
            os.chdir(original_dir)
            
            # Wait for Elasticsearch to start
            es = None
            for attempt in range(60):  # Try for 60 seconds instead of 30
                try:
                    print(f"Attempting to connect (attempt {attempt + 1}/60)...")
                    es = Elasticsearch(
                        "https://localhost:9200",
                        basic_auth=("elastic", "vqF+dCROd1r=vtqeowzx"),
                        ca_certs=os.path.join(elasticsearch_home, "config", "certs", "http_ca.crt"),
                        verify_certs=True
                    )
                    if es.ping():
                        print("Successfully connected to Elasticsearch!")
                        return es
                except Exception as e:
                    print(f"Connection attempt failed: {str(e)}")
                    time.sleep(1)
                    
                    # Check if process is still running
                    if process.poll() is not None:
                        print("Elasticsearch process has stopped!")
                        break
            
            raise Exception("Failed to start Elasticsearch after 60 seconds")
        except Exception as e:
            print(f"Error starting Elasticsearch: {str(e)}")
            raise
    else:
        raise FileNotFoundError(f"Elasticsearch not found at: {elasticsearch_bat}")

# Try to connect to Elasticsearch first
print("Attempting to connect to existing Elasticsearch instance...")
try:
    es = Elasticsearch(
        "https://localhost:9200",
        basic_auth=("elastic", "vqF+dCROd1r=vtqeowzx"),
        ca_certs="C:/Users/papro/Documents/elasticsearch-9.0.0/config/certs/http_ca.crt",
        verify_certs=True
    )
    if es.ping():
        print("Successfully connected to existing Elasticsearch instance!")
    else:
        raise ConnectionError("Ping failed")
except Exception as e:
    print(f"Could not connect to existing instance: {str(e)}")
    print("Attempting to start Elasticsearch...")
    es = start_elasticsearch()

# Index name
index_name = "screenshots"

# 1. Define mapping and create index if not exists
mapping = {
    "mappings": {
        "properties": {
            "filename": {"type": "keyword"},
            "text": {"type": "text"},
            "timestamp": {"type": "date"}
        }
    }
}

# Delete existing index to start fresh
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"Deleted existing index: {index_name}")

# Create new index
es.indices.create(index=index_name, body=mapping)
print(f"Created index: {index_name}")

# 2. Sample documents to index
docs = [
    {
        "_index": index_name,
        "_source": {
            "filename": "screenshot_001.png",
            "text": "This is an invoice for April April 2025.",
            "timestamp": datetime.now().isoformat()
        }
    },
    {
        "_index": index_name,
        "_source": {
            "filename": "screenshot_002.png",
            "text": "Meeting notes: discuss Q2 planning. april",
            "timestamp": datetime.now().isoformat()
        }
    },
    {
        "_index": index_name,
        "_source": {
            "filename": "screenshot_003.png",
            "text": "Your Amazon order has been shipped.",
            "timestamp": datetime.now().isoformat()
        }
    },
]

# 3. Bulk insert
success, failed = bulk(es, docs, stats_only=True)
print(f"Indexed {success} documents successfully. {failed} documents failed.")

# Refresh the index to make sure all documents are searchable
es.indices.refresh(index=index_name)

# 4. First, let's see all documents in the index
print("\nAll documents in the index:")
results = es.search(index=index_name, body={"query": {"match_all": {}}})
print(f"Total documents found: {results['hits']['total']['value']}")
for hit in results["hits"]["hits"]:
    print(f"{hit['_source']['filename']} -> {hit['_source']['text']}")

# 5. Now search for the keyword
keyword = "april"
query = {
    "query": {
        "match": {
            "text": keyword
        }
    }
}
print(f"\nSearch results for keyword: '{keyword}'\n")
results = es.search(index=index_name, body=query)
print(f"Total matches found: {results['hits']['total']['value']}")
for hit in results["hits"]["hits"]:
    print(f"{hit['_source']['filename']} -> {hit['_source']['text']}")