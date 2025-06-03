import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json
from datetime import date, timedelta

def download_data(api_key, output_folder):

    # Dates
    today = date.today()
    yesterday = today - timedelta(days=1)
    before_create_time = f"{yesterday}T00:00:00+00:00"
    since_create_time = "2025-01-01T00:00:00"

    try:
        client = MailchimpMarketing.Client()
        client.set_config({"api_key": api_key})

        # Fetch all campaigns in a single call
        response = client.campaigns.list(
            count=1000, 
            before_create_time=before_create_time,
            since_create_time=since_create_time
        )
        campaigns = response.get('campaigns', [])

        # Output each campaign to its own file
        for campaign in campaigns:
            campaign_id = campaign.get('id')
            if campaign_id:
                filename = os.path.join(output_folder, f"campaign_{campaign_id}.json")
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(campaign, f, indent=2)
                print(f"✅ Saved campaign {campaign_id} to {filename}")

        print("\n" + "="*60)
        print(f"✅ Successfully saved {len(campaigns)} campaigns to individual files!")
        print("="*60 + "\n")

    except ApiClientError as error:
        print("Error: {}".format(error.text))
