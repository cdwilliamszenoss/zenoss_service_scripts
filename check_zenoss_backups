#!/bin/bash

#
# Important: Create data source and data point with the name checkbackups
# Create Map and add checkbackups data point to graph
# Use the comand syntax in Command Template:  /usr/bin/env bash -c /home/zenoss/checkbackups.sh
#

count=$(find /opt/serviced/var/backups -type f  -mtime -7 | wc -l)

if [ "$count" -le 7 ]; then
echo '{"values": {"": {"checkbackups": '$count'}}, "events": [{"eventClass": "/App/Info", "severity": 4, "summary": "Backups under threshold: '$count'"}]}'
else
# This line reports the number of backups and genrates clearing event
echo '{"values": {"": {"checkbackups": '$count'}}, "events": [{"eventClass": "/App/Info", "severity": 0, "summary": "OK"}]}'
# This line only reports the number of backups. Does not generate clearing event
# echo '{"values": {"": {"checkbackups": '$count'}}, "events": []}'
fi
