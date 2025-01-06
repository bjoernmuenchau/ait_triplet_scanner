import requests, json, time, os

openwebif = 'http://192.168.2.10'
output = time.strftime('%y%m%d_%H%M%S')+'_Astra_Overview.tsv'
aitdelay = 3

getservices = requests.get(openwebif+'/api/getservices?sRef=1:7:1:0:0:0:0:0:0:0:')
getservices_json = getservices.json() if getservices and getservices.status_code == 200 else None
srefs = []
for i in getservices_json['services']:
    srefs.append(i['servicereference'])

for i in srefs:
    zap = requests.get(openwebif+'/api/zap?sRef='+i)
    time.sleep(aitdelay)
    getcurrent = requests.get(openwebif+'/api/getcurrent') if zap and zap.status_code == 200 else None
    getcurrent_json = getcurrent.json() if getcurrent and getcurrent.status_code == 200 else None
    with open(os.path.dirname(os.path.realpath(__file__))+'/'+output, 'a', errors='ignore') as f:
        f.write(getcurrent_json['info']['name']+'\t'+getcurrent_json['info']['provider']+'\t'+str(getcurrent_json['info']['onid'])+'.'+str(getcurrent_json['info']['tsid'])+'.'+str(getcurrent_json['info']['sid'])+'\t'+getcurrent_json['info']['hbbtvurl']+ '\n')
