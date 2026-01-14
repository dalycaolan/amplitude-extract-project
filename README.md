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

## 🏗️ Orchestration with Kestra

While the Python scripts handle the core logic of **Extracting** from Amplitude and **Loading** to AWS S3, we use **Kestra** to orchestrate the entire lifecycle. This ensures the pipeline is scheduled, observable, and handles environment dependencies automatically.

### Workflow Architecture

The orchestration flow (`amplitude.yaml`) manages the following lifecycle within a unified `WorkingDirectory`:

1. **Environment Setup**: Clones the specific branch (`modularising-script`) from GitHub.
2. **Dependency Management**: Dynamically installs required libraries via `pip`.
3. **Execution**: Passes secure credentials from Kestra's KV store into the Python environment.
4. **Logging**: Captures stdout/stderr for real-time monitoring of the ETL process.

### Required Secrets (KV Store)

To run this pipeline, the following keys must be configured in your Kestra namespace (`des.amplitude`). This prevents sensitive credentials from being hardcoded in the source code:

| Category      | Key                                | Description                            |
| :------------ | :--------------------------------- | :------------------------------------- |
| **GitHub**    | `github_user`, `github_token`      | Authentication for repository cloning. |
| **Amplitude** | `AMP_API_KEY`, `AMP_SECRET_KEY`    | API credentials for data extraction.   |
| **AWS**       | `AWS_ACCESS_KEY`, `AWS_SECRET_KEY` | Credentials for S3 loading.            |
| **Storage**   | `BUCKET_NAME`                      | The target S3 bucket for data uploads. |

### The Workflow Definition

The following YAML defines the orchestration logic. It is stored within Kestra and can be triggered manually or via the built-in scheduler.

```yaml
id: amplitude
namespace: des.amplitude

tasks:
  - id: wdir
    type: io.kestra.plugin.core.flow.WorkingDirectory
    tasks:
      - id: hello
        type: io.kestra.plugin.core.log.Log
        message: "Starting Amplitude Extraction Pipeline... 🚀"

      - id: clone
        type: io.kestra.plugin.git.Clone
        url: [https://github.com/dalycaolan/amplitude-extract-project](https://github.com/dalycaolan/amplitude-extract-project)
        branch: modularising-script
        username: "{{ kv('github_user')}}"
        password: "{{ kv('github_token')}}"

      - id: python_scripts
        type: io.kestra.plugin.scripts.python.Commands
        env:
          AMP_API_KEY: "{{kv('AMP_API_KEY')}}"
          AMP_SECRET_KEY: "{{kv('AMP_SECRET_KEY')}}"
          AWS_ACCESS_KEY: "{{kv('AWS_ACCESS_KEY')}}"
          AWS_SECRET_KEY: "{{kv('AWS_SECRET_KEY')}}"
          BUCKET_NAME: "{{kv('BUCKET_NAME')}}"
        beforeCommands:
          - pip install -r requirements.txt
        commands:
          - echo "Packages installed, starting main script ☘️"
          - python main.py
          - echo "Files uploaded successfully ☘️☘️☘️"
```

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

---

## Contributions 📔

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (git switch -c feature/NewFeatureLetsGo)
3. Commit your Changes (git commit -m 'Added new stuff')
4. Push to the Branch (git push origin feature/NewFeatureLetsGo)
5. Open a Pull Request

## License 🪪

Distributed under the MIT License. See LICENSE for more information.
