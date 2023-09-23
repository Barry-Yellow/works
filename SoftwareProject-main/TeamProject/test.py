import json
import requests

url = 'http://localhost:5000/select_class'
url2 = 'http://localhost:5000/get_data'
data = {'courses[]': ['软件工程', '生物学原理', 'Python程序设计基础', '数学分析II']}
req = requests.get(url, params=data)
r2 = json.loads(requests.get(url2).text)
r = json.loads(req.text)
print()
