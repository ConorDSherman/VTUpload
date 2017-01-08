# Import Libraries
import requests #Needed For the GET request
import openpyxl #Needed to Open the Excel files
import time #Needed for the sleep time as to not violate the VirusTotal T&C
import xlsxwriter #Needed to write to Excel

#Open Remotely Stored API Key
API_FILE = open('/Users/conorsherman/Desktop/VT_API_KEY.txt', 'r') #This is Unique to You
API_KEY = API_FILE.read().rstrip('\n') #Because, you know... text is "simple"

#Open and assign the Excel
input_workbook = openpyxl.load_workbook('/Users/conorsherman/Desktop/Tanium_Process_Hash.xlsx')
input_sheet = input_workbook.worksheets[0]

#Initialize counter user to select value out of the input Excel
input_row = 2

# Temp Dictionary to hold the results
hash_report = {}
# Temo Dictionary to hold the process name
hash_process_name = {}

for hash in range(1, input_sheet.max_row): #Needs to Start at 1 due to the headers
    #Populating the HASH and process name
    hash_process_name.update({input_sheet.cell(row=input_row, column=2).value : input_sheet.cell(row=input_row, column=1).value})
    print hash_process_name

    #Get Value of the Cell
    hash_value=input_sheet.cell(row=input_row, column=2).value
    print hash_value

    #Send Hash to VT
    params = {'apikey': API_KEY, 'resource': hash_value}
    headers = {"Accept-Encoding": "gzip, deflate", "User-Agent": "gzip,  ConorSherman"}
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
    json_response = response.json()

    #Update the Report
    if json_response.get('positives') == None:
        hash_report.update({json_response.get('resource'): "No Results"})
    else:
        hash_report.update({json_response.get('resource'): json_response.get('positives')})

    print hash_report

    # Move to the next HASH
    input_row += 1

    #Time Delay for Rate Limit
    time.sleep(15)


# Prepare Export
# Open the Files to Write To Excel
output_workbook = xlsxwriter.Workbook('/Users/conorsherman/Desktop/Tanium_Hash_Output.xlsx')
output_worksheet = output_workbook.add_worksheet()
name_col = 0
hash_col = 1
result_col = 2
output_row = 0

#Write Headers
output_worksheet.write(output_row, name_col, "Process Name")
output_worksheet.write(output_row, hash_col, "Process HASH")
output_worksheet.write(output_row, result_col, "VirusTotal Results")
output_row +=1 #Move to the next row

#Grab the results from the Dictionary
for key, value in hash_report.items():
    output_worksheet.write(output_row, name_col, hash_process_name[key] )
    output_worksheet.write(output_row, hash_col, key) #Write the Hash
    output_worksheet.write(output_row, result_col, hash_report[key]) #Write the Result
    #Position for next Output
    output_row += 1

# Close Excel to keep it clean
output_workbook.close()
