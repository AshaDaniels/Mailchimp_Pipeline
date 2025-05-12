# Load libraries
from dotenv import load_dotenv  # For loading environment variables from a .env file
import os  # For accessing environment variables and file system operations
import mailchimp_marketing as MailchimpMarketing  # For interacting with the Mailchimp API
from mailchimp_marketing.api_client import ApiClientError  # For handling Mailchimp API errors
import json  # For working with JSON data

# Load environment variables
load_dotenv()  # Reads key-value pairs from a .env file and loads them into environment variables
api_key = os.getenv('MAILCHIMP_API_KEY')  # Retrieves the Mailchimp API key from the environment variables

# === STATIC DATES ===
# This script will only collect dates statitcally, another script will be run to add new daily info
today_str = "2025-05-12"
start_of_year_str = "2025-01-01"

# Create date-time strings for API query filters
since_create_time = start_of_year_str + "T00:00:00+00:00"
before_create_time = today_str + "T23:59:59+00:00"

# # UNNECESSARY Pagination setup
# count = 1000  # Number of campaigns to fetch per API call
# offset = 0  # Starting point for pagination
# all_campaigns = []  # List to store all fetched campaigns

# Construct API call with pagination and date filter
try:
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key,
    })

    # Fetch campaigns in a loop, handling pagination
    # while True:
    response = client.campaigns.list( 
        # count=count,  # Number of campaigns to retrieve in this call
        # offset=offset,  # Offset to fetch the next batch of campaigns
        since_create_time=since_create_time,  # Filter campaigns created after this date
        before_create_time=before_create_time  # Filter campaigns created before this date
    )
    campaigns = response.get('campaigns', [])  # Extract the list of campaigns from the response
    #     all_campaigns.extend(campaigns)  # Add the fetched campaigns to the main list
    #     print(f"Fetched {len(campaigns)} campaigns at offset {offset}")  # Log the number of campaigns fetched
        
    #     if len(campaigns) < count:  # Check if fewer campaigns were fetched than requested
    #         break  # Exit the loop if there are no more campaigns to fetch
    #     offset += count  # Increment the offset for the next API call

    print(f"Total campaigns from this year: {len(campaigns)}")  # Log the total number of campaigns fetched

    # === Write to JSON file instead of printing ===
    output_filename = "mailchimp_campaigns_from_2025.json"  # Define the output file name
    with open(output_filename, "w", encoding="utf-8") as f:  # Open the file in write mode with UTF-8 encoding
        json.dump(campaigns, f, indent=2)  # Write the campaigns list to the file in JSON format

    # Log success message
    print("\n" + "="*60)
    print(f"✅ Successfully fetched {len(campaigns)} campaigns from 2025-01-01 to 2025-05-12!")
    print(f"📄 Full campaign info saved to: {output_filename}")
    print("="*60 + "\n")

except ApiClientError as error:  # Catch exceptions related to Mailchimp API errors
    print("Error: {}".format(error.text))  # Log the error message
