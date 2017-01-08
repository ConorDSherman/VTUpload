'''CODE OUTLINE
1. Open the CSV
2. Extract the HASH into an Array (?)
Loop
3. Check the HASH with VT
4. Store the Respone 'HASH : Verdict"
5. Add the HASH to a 'Checked List'
6. Close loop and print report
    http://stackoverflow.com/questions/23113231/write-dictionary-values-in-an-excel-file'''

# Import Libraries
import requests #Needed For the GET request
import openpyxl #Needed to Open the Excel files
import time #Needed for the sleep time as to not violate the VT T&C
import xlsxwriter #Needed to write to Excel

#Open Remotely Stored API Key
API_FILE = open('/Users/conorsherman/Desktop/VT_API_KEY.txt', 'r') #This is Unique to You
API_KEY = API_FILE.read().rstrip('\n') #Because, you know... text is "simple"
#
#Open and assign the Excel
input_workbook = openpyxl.load_workbook('/Users/conorsherman/Desktop/Tanium_Hash_One_Column.xlsx')
input_sheet = input_workbook.get_sheet_by_name("Sheet1")

# Prepare Export
# Open the Files to Write To Excel
output_workbook = xlsxwriter.Workbook('/Users/conorsherman/Desktop/Tanium_Hash_Output.xlsx')
output_worksheet = output_workbook.add_worksheet()
output_row = 0
output_col = 0

#Initialize counter user to select value out of the input Excel
input_row = 1

# Temp Dictionary to hold the results
hash_report = {}

for hash in range(0, 60): #CHANGE ME TO THE MAX

    #Get Value of the Cell
    hash_value=input_sheet.cell(row=input_row, column=1).value

    #Send Hash to VT
    params = {'apikey': API_KEY, 'resource': hash_value}
    headers = {"Accept-Encoding": "gzip, deflate", "User-Agent": "gzip,  ConorSherman"}
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
    json_response = response.json()

    #Update the Report
    #I had to cast to STR so that i could loop through the dictionary during the write to Excel function
    if json_response.get('positives') == None:
        hash_report.update({json_response.get('resource'): "No Results"})
    else:
        hash_report.update({json_response.get('resource'): json_response.get('positives')})

    print hash_report

    # Move to the next HASH
    input_row += 1

    #Time Delay for Rate Limit
    time.sleep(15)

#Grab the results from the Dictionary
for key, value in hash_report.items():
    #print hash_report.items()
    #print hash_report
    output_worksheet.write(output_row, output_col, key) #Write the Hash
    output_worksheet.write(output_row, output_col + 1, hash_report[key]) #Write the Result
    #Position for next Output
    output_row += 1

# Close Excel to keep it clean
output_workbook.close()