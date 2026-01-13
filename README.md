# Amplitude Extract Project

## Introduction 👋

This project aims to walk through extraction of data from an Amplitude API and loading of this into local storage.

There are two python scripts to write in order to extract, one is the primary ingestion script and the other defines a function that we will call in the ingestion script.

### 1. Defining Endpoint and Parameters 📅

Documentation for this API can be found here:
<br/><br/>
`https://amplitude.com/docs/apis/analytics/export`

<br/>
The request URL for the EU can be found below:
<br/><br/>

`https://analytics.eu.amplitude.com/api/2/export`

Our request will be in the following format:

`'https://amplitude.com/api/2/export?start=\<starttime>&end=<endtime>' \
-u '{api_key}:{secret_key}'`

To call this API we need our endpoint URL and parameters, in particular start and end datetimes to define a range. In this example I have used datetimenow to grab yesterday's date and then roll back a week to define the start and end dates.

We use the requests package to get our API request.

### 2. Calling the API ☎️

Make sure you have you Amplitude credentials saved in a .env file and install the dotenv Python package. You will call in your API key and secret to authorise the API request.

Use the datetime package to define the start and end datetimes of your request and convert this into the correct string format using strftime.

If the request is successful, we will download the data as a ZIP file and then try to unzip this to find the JSONs stored within it.

### 3. Unzipping and Storing 🧰

Define a separate modules.py script in order to keep our extraction script concise. Please follow this script to see how the function is defined. We will create a directory to unzip and store our JSON files. In order to do this, we will create a temporary directory to initially unzip our file, and then from there unzip it again to find our event data JSONs and put them in the correct folder.

# Data Pipeline: AWS to Snowflake Integration

This project outlines a robust data engineering pipeline designed to ingest JSON data into an AWS S3 bucket via Python and integrate it seamlessly into a Snowflake data warehouse using Storage Integrations.

---

## 🏗️ 4. AWS Configuration

The foundation of the pipeline requires a secure and well-permissioned AWS environment.

- **KMS & S3 Setup**
  - Create a specialized **KMS Key** for encryption.
  - Provision an **S3 Bucket** with strict security:
    - Block Public Access
    - Disable ACLs
    - Encrypt with KMS
- **IAM Policies**
  - **For Load:** Create Policy, Create User, Attach Policy to user, and record Access ID/Secret.
  - **For Storage Integration:** Create Role and Attach Policy to Role.

---

## 🐍 5. Python Loading Process

This stage handles local data orchestration and transfer to the cloud.

- **Set Up Credentials**
  - Create a `.env` file to store `aws_key`, `secret`, `region`, and `bucket_name`.
- **Write Load Function**
  - **Folder Traversal:** Walk through `json_data` folder using nested for-loops to look in subfolders.
  - **Path Management:** Create full file paths and parse destination file paths for S3.

---

## ❄️ 6. Snowflake Integration

Connecting the S3 data lake to the Snowflake warehouse for analysis.

- **Schema & Storage Integration**
  - Create Schema.
  - **Storage Integration Setup:** \* Create Role and Policy in AWS.
    - Create Storage Integration object in Snowflake and note key details.
    - Update the AWS Role **Trust Relationship**.
- **Data Ingestion**
  - Create **External Stage**.
  - Create target **Table**.
  - Execute **Load into table**.

---

## 🚀 Further Developments

### 🔄 Incremental Refresh

_Goal: Fill in gaps to make data more recent._

1.  Create a list of JSONs and convert to **datetime**.
2.  Find the **most recent datetime**.
3.  Set this as the **start time** for the API call.
4.  Unzip and store as normal.

### 🔍 Fill In Missing Gaps

_Goal: Ensure data completeness._

1.  Generate a list of files currently in the S3 bucket.
2.  After unzipping gzips, iterate through:
    - **If file already there:** Don't extract into `json_data` folder.
    - **If file not there:** Load in.

## Contributions 📔

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (git switch -c feature/NewFeatureLetsGo)
3. Commit your Changes (git commit -m 'Added new stuff')
4. Push to the Branch (git push origin feature/NewFeatureLetsGo)
5. Open a Pull Request

## License 🪪

Distributed under the MIT License. See LICENSE for more information.
