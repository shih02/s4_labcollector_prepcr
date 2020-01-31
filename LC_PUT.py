import requests
import re
from openpyxl import load_workbook, workbook

#API header for labcollector
headers = {
  'Accept': 'application/json;odata.metadata=full',
  'X-LC-APP-Auth': 'b970d14af941f18aa1417c874e0f414db437fa6b277bf4c7ec196a189fc9f0c5',
  'Host': '10.95.2.101',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}

#parse column A for sample IDs
samplelist = ""
wb = load_workbook(filename = 'Book1.xlsx')
ws = wb['Sheet1']
for x in range(1, ws.max_row+1):
  id = ws.cell(row = x, column = 1).value
  concentration = ws.cell(row = x, column = 2).value
  url = "http://10.95.2.101/lab/webservice/v1/samples?label=" + id
  response = requests.request("GET", url, headers=headers)
  res_split = re.split(r'[,:""]',response.text)
  count = res_split[4]
  payload = {'comments': 'API testing' + str(x),'origin': concentration,'volume': concentration}
  print(id+count+str(concentration))
  put_url = "http://10.95.2.101/lab/webservice/v1/samples/" + count
  put_response = requests.request("PUT", put_url, headers=headers, data = payload)


# get below
# url = "http://10.95.2.101/lab/webservice/v1/samples?label=" + name
# response_text = requests.request("GET", url, headers=headers).text








