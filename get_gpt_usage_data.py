import os, openai


with open('open_ai_key', 'r', encoding='utf-8') as f:
    openai.api_key = os.getenv(f.read())


from datetime import datetime, timedelta
start_date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
end_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

usage = openai.usage.list(
    start_date=start_date,
    end_date=end_date
)

for item in usage["data"]:
    print(item)
