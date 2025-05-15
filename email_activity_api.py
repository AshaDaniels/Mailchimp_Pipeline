from dotenv import load_dotenv
import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json
from datetime import datetime, timedelta, timezone  # For working with dates and time deltasC

# Load environment variables
load_dotenv()
api_key = os.getenv('MAILCHIMP_API_KEY')

# Dates
now = datetime.now(timezone.utc)
# One hour ago
one_hour_ago = now - timedelta(hours=1)

# Create date-time strings for API query filters
since = "2025-01-01T00:00:00"

# Load campaign IDs from file
with open("mailchimp_campaigns.json", "r", encoding="utf-8") as f:
    campaigns_data = json.load(f)

campaign_ids = [c['id'] for c in campaigns_data]

count = 1000
all_email_activities = []

try:
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,
    })

    for campaign_id in campaign_ids:
        offset = 0
        while True:
            response = client.reports.get_email_activity_for_campaign(
                campaign_id,
                count=count,
                offset=offset,
                since = since
            )
            emails = response.get('emails', [])

            if len(emails) < count:
                break
            offset += count

    print(f"\nTotal emails fetched across all campaigns: {len(all_email_activities)}")

    # Write to JSON file
    output_filename = "mailchimp_email_activity.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_email_activities, f, indent=2)

    print("\n" + "="*60)
    print(f"✅ Successfully fetched {len(all_email_activities)} emails across {len(campaign_ids)} campaigns!")
    print(f"📄 Full email info saved to: {output_filename}")
    print("="*60 + "\n")

except ApiClientError as error:
    print("Error: {}".format(error.text))
