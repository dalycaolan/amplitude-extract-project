# Amplitude Extract Project

## Introduction

This project aims to walk through extraction of data from an Amplitude API and loading of this into local storage.

There are two python scripts to write in order to extract, one is the primary ingestion script and the other defines a function that we will call in the ingestion script.

### 1. Defining Endpoint and Parameters

Documentation for this API can be found here: https://amplitude.com/docs/apis/analytics/export

To call this API we need our endpoint URL and parameters, in particular start and end datetimes to define a range.
