from dotenv import load_dotenv
import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json
from datetime import date, timedelta

# Load environment variables from a .env file
load_dotenv()
api_key = os.getenv('MAILCHIMP_API_KEY')

# Set up date variables for filtering campaigns
today = date.today()  # Get today's date
yesterday = today - timedelta(days=1)  # Calculate yesterday's date
yesterday_str = str(yesterday) + "T00:00:00+00:00"  # Format yesterday's date as a string
before_create_time = yesterday_str  # Set the 'before_create_time' parameter for API filtering

# Initialize pagination and data storage variables
count = 1000  # Number of campaigns to fetch per API call
offset = 0  # Starting offset for pagination
all_campaigns = []  # List to store all fetched campaigns

try:
    # Initialize Mailchimp client
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,  # Set the API key for authentication
    })

    # Loop to fetch campaigns, handling pagination
    while True:
        # Fetch campaigns using the Mailchimp API
        response = client.campaigns.list(
            count=count,  # Number of campaigns to fetch in this batch
            offset=offset,  # Offset for pagination
            before_create_time=before_create_time  # Filter campaigns created before yesterday
        )
        campaigns = response.get('campaigns', [])  # Extract the campaigns list from the response
        all_campaigns.extend(campaigns)  # Add the fetched campaigns to the list
        print(f"Fetched {len(campaigns)} campaigns at offset {offset}")  # Log the number of campaigns fetched
        
        # Break the loop if there are no more campaigns to fetch
        if len(campaigns) < count:
            break
        offset += count  # Increment the offset for the next API call

    print(f"Total campaigns fetched: {len(all_campaigns)}")  # Log the total number of campaigns fetched

    # Save the fetched campaigns to a JSON file
    output_filename = "mailchimp_campaigns.json"  # Name of the output file
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_campaigns, f, indent=2)  # Write campaigns data to the file in JSON format

    # Print a success message with details
    print("\n" + "="*60)
    print(f"✅ Successfully fetched {len(all_campaigns)} campaigns!")
    print(f"📄 Full campaign info saved to: {output_filename}")
    print("="*60 + "\n")

except ApiClientError as error:
    # Handle API errors and print the error message
    print("Error: {}".format(error.text))
