import json, requests,datetime
a = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
print(a)
# lat = '25.667'
# long = "ammar"
# data1= '{"lat": '+lat+',"long": '+long+'}'
# print(data1)
# data2= '{"lat": 27.8854,"long": 69.866,"speed": 24.0,"time": 20221024,"cabin": 1,"front": 1,"rear": 0,"left": 0,"right": 0}'
# fdata1 = json.loads(data1)
# fdata2 = json.loads(data1)
# ds = [fdata1,fdata2]
# hubid = "29"

# url = {
#   "deviceId": hubid,
#   "data": [ds]
# }

# api = 'https://monitstage-core-srvc.peekaboo.guru/heartbeats'
# x=requests.post(api,json=url)
# print(x.status_code)
# print(x.json())