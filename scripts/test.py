import requests
import csv
import time

API_URL = "http://localhost:8000/api/query"

QUERIES = []
with open("../reference.csv", 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        QUERIES.append({
            "type": row["type"],
            "text": row["text"],
        })
print(f"{len(QUERIES)} sorgu başarıyla yüklendi.")

results = []

i=1
for query in QUERIES:
    payload = {"question": query["text"]}
    
    start_time = time.time()
    response = requests.post(API_URL, json=payload, timeout=100)
    end_time = time.time()
    
    
    if response.status_code == 200:
        data = response.json()
        latency = data.get("latency_ms", {})
        retrieval_time = latency.get("retrieval", "N/A")
        generation_time = latency.get("generation", "N/A")
        
        results.append({
            "Query": query["text"],
            "Query_Length": query["type"],
            "Retrieval_Time_MS": retrieval_time,
            "Generation_Time_MS": generation_time,
            "Total_Time_MS": retrieval_time+generation_time
        })
        print(f"Sorgu{i} başarılı Toplam süre: {retrieval_time+generation_time} ms")
    else:
        print(f"Sorgu{i} başarısız-> {response.status_code}")
        results.append({
            "Query": query["text"],
            "Query_Length": query["type"],
            "Retrieval_Time_MS": "",
            "Generation_Time_MS": "",
            "Total_Time_MS": f" {response.status_code}"
        })
    i+=1

output_file = "../performance_results.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["Query", "Query_Length", "Retrieval_Time_MS", "Generation_Time_MS", "Total_Time_MS"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)
    
print(f"\n*******  Test tamamlandı  *******")