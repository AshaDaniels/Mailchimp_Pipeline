from dotenv import load_dotenv
import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json
from datetime import date, timedelta

# Load environment variables
load_dotenv()
api_key = os.getenv('MAILCHIMP_API_KEY')

# Dates
today = date.today()
yesterday = today - timedelta(days=1)
yesterday_str = str(yesterday) + "T00:00:00+00:00"
before_create_time = yesterday_str

# Pagination setup
count = 1000
offset = 0
all_campaigns = []

try:
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,
    })

    # Fetch campaigns in a loop, handling pagination
    while True:
        response = client.campaigns.list(
            count=count,
            offset=offset,
            before_create_time=before_create_time
        )
        campaigns = response.get('campaigns', [])
        all_campaigns.extend(campaigns)
        print(f"Fetched {len(campaigns)} campaigns at offset {offset}")
        
        if len(campaigns) < count:
            break
        offset += count

    print(f"Total campaigns fetched: {len(all_campaigns)}")

    # Write to JSON file
    output_filename = "mailchimp_campaigns.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_campaigns, f, indent=2)

    print("\n" + "="*60)
    print(f"✅ Successfully fetched {len(all_campaigns)} campaigns!")
    print(f"📄 Full campaign info saved to: {output_filename}")
    print("="*60 + "\n")

except ApiClientError as error:
    print("Error: {}".format(error.text))
