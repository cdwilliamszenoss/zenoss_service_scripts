# Generate Events for Services using above mem threshold
# Graph datapoint to see trend.

# Required Modules:
# pip install wmi
# pip install json
# 
# May have to install pypiwin32 for the wmi module
# pip install pypiwin32

try:
  import json
except ImportError:
	print ("\nError: Use the command to install the module.   pip install json\n")
        exit()
try:
 import wmi
except ImportError:
       print ("\nError: Use the command to install the module.     pip install wmi\n")
       exit()



#Use the exact name of the running service 
service_name = 'WinRM'


#Change to 0 to test event or to the number of GB
#Set the Memory Threshold: 
threshold_value_GB = 0

service_dict = {}
threshold_bytes_to_gig = 1073741824 * threshold_value_GB

c = wmi.WMI()

for www_srv in c.Win32_Service(Name=service_name):
    for process in c.Win32_Process(ProcessId=www_srv.ProcessId):
       
	   
        if long(process.WorkingSetSize) > long(threshold_bytes_to_gig):
            service_dict = {"values": {"": {
                service_name: process.WorkingSetSize}},
                "events": [{"severity": 4, "eventClass":'/Perf/Memory', "summary": str(service_name) + " over threshold " + process.WorkingSetSize }]}
        else:
            service_dict = {"values": {"": {
                service_name: process.WorkingSetSize}},
                "events": []}
print json.dumps(service_dict)
