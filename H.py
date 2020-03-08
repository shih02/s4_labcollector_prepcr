#API headers and URL
headers = {
  'Accept': 'application/json;odata.metadata=full',
  'X-LC-APP-Auth': 'b970d14af941f18aa1417c874e0f414db437fa6b277bf4c7ec196a189fc9f0c5',
  'Host': '10.95.2.101',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}

url = "http://10.95.2.101/lab/webservice/v1/samples?label="

url_v2 = "http://10.95.2.101/lab/webservice/index.php?v=2&action=tube_sorter&record_name="

put_url = "http://10.95.2.101/lab/webservice/v1/samples/"

con = "http://10.95.2.101/lab/webservice/v1/samples?label=TEST200801"