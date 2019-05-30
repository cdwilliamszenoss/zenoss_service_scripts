import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#-- Set varibles:
username = ''
password = ''
url = 'https://zenoss5.server.com'

#-- Specific a single device or device class
devices_path = '/zport/dmd/Devices/Server/SSH'
dst_collector = 'localhost'


router = '/zport/dmd/device_router'
device_data = {}
device_list = []

getDevices_payload = {"action":"DeviceRouter","method":"getDevices","data":[{"uid":devices_path}],\
                    "type":"rpc","tid":1}
device_request = requests.post(url+router,auth=(username,password),json=getDevices_payload,verify=False)

try:
    if device_request.status_code != 200:
        print "Check status_code"
        exit()
    else:
        device_data = device_request.json()
except Exception as e:
    print("\n*** No data recieved. Check connection information ***\n" + str(e))
    exit()

if (len(device_data["result"]["devices"]) != int(device_data["result"]["hash"])):
    print "Hashcheck failed"
    exit()
else:
    print "Move collector"
    for i in device_data["result"]["devices"]:
        device_list.append(i["uid"])

device_list = [x.encode("ascii","ignore") for x in device_list]


# -------- Set Collector ---------

setCollector_payload = {"action":"DeviceRouter","method":"setCollector","data":[{"uids":device_list,\
            "asynchronous":"false","collector":dst_collector,"hashcheck":""}],"type":"rpc","tid":2}

collect_request = requests.post(url+router,auth=(username,password),json=setCollector_payload,verify=False)

try:
    if collect_request.status_code != 200:
        print "Check status_code"
        exit()
    else:
        collect_data = collect_request.json()
except Exception as e:
    print("\n*** No data recieved. Check connection information ***\n" + str(e))
    exit()

collect_list = collect_data["result"]["new_jobs"]["description"]
print collect_list
