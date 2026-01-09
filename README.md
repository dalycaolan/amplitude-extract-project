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

## Contributions 📔

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (git switch -c feature/NewFeatureLetsGo)
3. Commit your Changes (git commit -m 'Added new stuff')
4. Push to the Branch (git push origin feature/NewFeatureLetsGo)
5. Open a Pull Request

## License 🪪

Distributed under the MIT License. See LICENSE for more information.
