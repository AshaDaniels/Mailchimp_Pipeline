# Project 1: 📧 Mailchimp Campaign Data Extractor

## Overview
Scripts to extract Mailchimp campaign data using the Mailchimp Marketing API. This project includes two distinct scripts:
- 📦 **Full Load:** Extract all historical campaign data
- 🕒 **Incremental Load:** Extract only campaigns created on the previous day

---

## 1. Setting Up the Environment

### Objective
Configure the necessary environment and retrieve API keys to connect to the Mailchimp Marketing API.

### Steps
1. Install required Python dependencies:
   - `requests`
   - `python-dotenv`
2. Load environment variables using the `dotenv` library to retrieve the API key and other credentials.
3. Set up the Mailchimp client using the loaded API key.

---

## 2. Full Campaign Data Extraction

### Objective
Fetch all campaign data up to the current date and save it to a JSON file.

### Steps
1. Define a date boundary (`yesterday`) to limit the scope of the data.
2. Use the Mailchimp API to retrieve campaigns:
   - 🔄 Implement pagination logic to fetch all campaigns in batches.
   - ➕ Append data across pages until all campaigns are retrieved.
3. Save the resulting data to a JSON file (`mailchimp_campaigns.json`).

---

## 3. Incremental Campaign Data Extraction

### Objective
Fetch only campaigns created on the previous day for daily updates.

### Steps
1. Define the date range (`since` and `before`) for the previous day.
2. Fetch campaigns matching the date range using the Mailchimp API.
3. Save the incremental data to the existing JSON file (`mailchimp_campaigns.json`), appending if necessary.
4. If no campaigns are found, log an appropriate message.

---

## 4. Error Handling and Logging

### Objective
Ensure the script handles errors gracefully and provides clear feedback.

### Steps
1. Wrap API requests in `try/except` blocks to catch errors.
2. Log errors and print summaries of successful or failed actions.

---

## Output

- `mailchimp_campaigns.json` 📄: A JSON file containing the extracted campaign data.

---

## Scripts

- **`mailchimp_api.py`** 🧹: Fetches all historical campaigns before yesterday (for full data loads).
- **`mailchimp_api_incremental.py`** 🔁: Fetches campaigns created on the previous day (to be run daily).


# Project 2: 📧 Mailchimp Loading Plan via Python

## Overview
This README outlines the steps required to set up, modify, and test a Mailchimp data loading plan using Python and AWS S3.

---

## 1. Setting Up in S3

### Objective
Prepare the necessary permissions and folder structure to practice loading data into S3 using Python.

### Steps

#### a. Create a Folder in S3
1. In the S3 bucket, create a folder named `python-import`.

#### b. Create a User for Python
1. Navigate to **IAM** and create a new user (e.g., `mailchimp-python-user`).
2. Attach policies directly to this user:
   - Use a policy document to define granular permissions.
   - Allow actions like `s3:PutObject`, `s3:GetObject`, and KMS decryption for the `python-import` folder.
   - Update policies with the correct bucket name and KMS ARN.
   - Save the policy with a clear name (e.g., `mailchimp-python-upload-policy`).
3. Add tags for easier management (e.g., `Key: project`, `Value: mailchimp`).

#### c. Generate Keys for the Python User
1. Generate an **Access Key and Secret Key** for the user.
2. Save these keys securely and update the `.env` file with:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `BUCKET_NAME`
   - `BUCKET_FILE_PATH`

---

## 2. Adjust Existing Script

### Objective
Modify the existing script to meet the current project requirements.

### Steps

#### a. Create a New Git Branch
1. Create a new branch in Git for the changes (e.g., `mailchimp-integration`).

#### b. Remove Pagination Logic
1. Remove the loop handling pagination (`while True`) since only campaigns created in 2025 are required.

---

## 3. Split Output Data into Multiple Files

### Objective
Save campaigns data into multiple JSON files instead of one large file.

### Steps

#### a. Create an Output Directory
1. Use Python’s `os` module to create a directory called `campaign_data`.
2. Set `exist_ok=True` to avoid errors if the directory already exists.

#### b. Save Each Campaign to a Separate File
1. Iterate through the fetched campaigns and save each to a separate JSON file.
2. Include error handling to manage any issues during file writing.

---

## 4. Test File Upload to S3

### Objective
Verify that a single campaign JSON file can be uploaded successfully to the S3 bucket.

### Steps

#### a. Select a File for Upload
1. Choose a JSON file created in the previous step (e.g., `campaign_1.json`).

#### b. Write a Python Script to Upload the File
1. Use the Python `boto3` library to upload the file to the S3 bucket.
2. Ensure the correct bucket name and folder path are used (`<bucket-name>/python-import/`).

#### c. Verify the Upload in S3
1. Navigate to the S3 console.
2. Confirm that the test file is visible in the `python-import` folder.

---

## 5. Automate and Test Bulk Upload

### Objective
Upload all campaign JSON files to S3 and create a reusable function for the process.

### Steps

#### a. Write a Bulk Upload Function
1. Create a function that accepts a directory path and uploads all JSON files within it to S3.
2. Maintain the appropriate folder structure in S3.

#### b. Add Logging
1. Include logs to track successful file uploads.

#### c. Test the Function
1. Verify that all files in the directory are uploaded correctly and appear in the S3 bucket.
