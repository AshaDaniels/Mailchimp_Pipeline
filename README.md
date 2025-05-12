project: 📧 Mailchimp Campaign Data Extractor

description: >
  Scripts to extract Mailchimp campaign data using the Mailchimp Marketing API.
  Two separate scripts are included:
  - 📦 One for a full historical load of all campaigns
  - 🕒 One for daily incremental loads based on the previous day's date

steps:
  - 🔐 Load environment variables using dotenv to retrieve the API key
  - ⚙️ Set up the Mailchimp client with the API key
  - 📅 Define date boundaries for campaign filtering
  - 📥 For the full load:
      - 🔄 Use pagination to retrieve all campaigns before a given date (yesterday)
      - ➕ Append campaigns across pages and write the result to a JSON file
  - 📈 For the incremental load:
      - ⏱️ Fetch only campaigns created on the previous day using since/before timestamps
      - 💾 Save the filtered results to the same JSON file if campaigns are found
  - 📊 Print summaries of actions taken or if no campaigns were found
  - ❌ Catch and print errors from the Mailchimp API

scripts:
  - `mailchimp_api.py` 🧹: Fetches all campaigns prior to yesterday (for full data loads)
  - `mailchimp_api_incremental.py` 🔁: Fetches campaigns created only yesterday (to be run daily)

output:
  - `mailchimp_campaigns.json` 📄: JSON file containing campaign data retrieved from the API
