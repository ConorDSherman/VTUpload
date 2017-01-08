# VTUpload
The objective of this script is to take the "Running Proccess with HASH" from Tanium and check with VirusTotal to see if any of the running processes match the HASH of a known piece of malware.

Remember that VirusTotal has not seen everything so at times the scipt will call for the verdict of a HASH and VirusTotal will simply return "No Results" in this case that process requires further investigation.

## Library Dependencies
import requests #Needed For the GET request

import openpyxl #Needed to Open the Excel files

import time #Needed for the sleep time as to not violate the VirusTotal T&C

import xlsxwriter #Needed to write to Excel

import csv #Needed to manipulate the raw data

## Known Issues
* No Resilience: If something goes wrong with one check the script exits without writing the previous results to excel
* Unable to handle whitespace: If you have whitespace at the end of your input file the script will attempt to read that value and check with VT and this will cause an error.
