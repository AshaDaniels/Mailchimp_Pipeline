# Load libraries
from dotenv import load_dotenv  # For loading environment variables from a .env file
import os  # For accessing environment variables and file system operations
import mailchimp_marketing as MailchimpMarketing  # For interacting with the Mailchimp API
from mailchimp_marketing.api_client import ApiClientError  # For handling Mailchimp API errors
import json  # For working with JSON data
from datetime import date, timedelta  # For working with dates and time deltas

# Load environment variables
load_dotenv()  # Reads key-value pairs from a .env file and loads them into environment variables
api_key = os.getenv('MAILCHIMP_API_KEY')  # Retrieves the Mailchimp API key from the environment variables

# Dates
today = date.today()  # Gets today's date
yesterday = today - timedelta(days=1)  # Calculates yesterday's date by subtracting one day

# Create date-time strings for API query filters
since_create_time = str(yesterday) + "T00:00:00+00:00"  # Start of yesterday in UTC format
before_create_time = str(yesterday) + "T23:59:59+00:00"  # End of yesterday in UTC format

# Construct API call with pagination and date filter
try:
    client = MailchimpMarketing.Client()  # Initializes the Mailchimp client
    client.set_config({
        "api_key": api_key,  # Configures the client with the API key
    })
    response = client.campaigns.list( 
        since_create_time=since_create_time,  # Filter campaigns created after this date-time
        before_create_time=before_create_time  # Filter campaigns created before this date-time
    )
    campaigns = response.get('campaigns', [])  # Extract the list of campaigns from the response; default to empty list if key not found

    if len(campaigns) == 0:
        print("No campaigns found for yesterday. The file has not been altered.")  # Message if no campaigns were returned
    else:
        print(f"Total campaigns from yesterday: {len(campaigns)}")  # Print the number of campaigns found
        output_filename = "mailchimp_campaigns.json"  # Define the output file name
        with open(output_filename, "w", encoding="utf-8") as f:  # Open the file in write mode with UTF-8 encoding
            json.dump(campaigns, f, indent=2)  # Write the campaigns data to the file in JSON format, indented for readability

except ApiClientError as error:
    print("Error: {}".format(error.text))  # Print error message if an API exception occurs
