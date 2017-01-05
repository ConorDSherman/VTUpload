'''CODE OUTLINE
1. Open the CSV
2. Extract the HASH into an Array (?)
Loop
3. Check the HASH with VT
4. Store the Respone 'HASH : Verdict"
5. Add the HASH to a 'Checked List'
6. Close loop and print report
    http://stackoverflow.com/questions/23113231/write-dictionary-values-in-an-excel-file'''

import requests
import openpyxl
import time
import xlsxwriter

#Open Remotely Stored API Key
API_FILE = open('/Users/conorsherman/Desktop/VT_API_KEY.txt', 'r')
API_KEY = API_FILE.read().rstrip('\n')

#Temporary Dictionary
hash_report = {}

#Final Excel Output
output_workbook = xlsxwriter.Workbook('/Users/conorsherman/Desktop/Tanium_Hash_Output.xlsx')
output_worksheet = output_workbook.add_worksheet()
output_row = 0
output_col = 0


#Open and assign the Excel
wb = openpyxl.load_workbook('/Users/conorsherman/Desktop/Tanium_Hash_One_Column.xlsx')
sheet = wb.get_sheet_by_name("Sheet1")

#Initialize the counter
count = 1
for hash in range(0, 7):
    #Get Value of the Cell
    hash_value=sheet.cell(row=count, column=1).value
    count += 1

    #Send Hash to VT
    params = {'apikey': API_KEY, 'resource': hash_value}
    #print params
    headers = {"Accept-Encoding": "gzip, deflate", "User-Agent": "gzip,  ConorSherman"}
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
    #print response
    json_response = response.json()
    #print json_response

    #Update the Report
    hash_report.update({json_response.get('resource'): json_response.get('positives')})
    print hash_report

    #Write to Excel
    for key in hash_report.keys():
        print hash_report.keys()
        output_row += 1
        print output_row
        output_col = 0
        print output_col
        output_worksheet.write(output_row, output_col, key)
        for item in hash_report[key]:
            print key
            print item
         #   output_worksheet.write(output_row, output_col + 1, item)
          #  output_row += 1


    #Time Delay for Rate Limit
    time.sleep(20)

#Cleanup
output_workbook.close()