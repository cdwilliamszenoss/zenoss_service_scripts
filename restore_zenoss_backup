#!/bin/bash

BACKUP_FILE_TO_RESTORE="/opt/serviced/var/backups/backup-2018-10-01-192849.tgz"


while true; do

if [[ -n $(egrep -o "started|stopping|pending_start|pending_stop|starting|pulling" <(/usr/bin/serviced service status)) ]]; then
 echo  "Waiting for services to stop"
 /usr/bin/serviced service stop resmgr
 sleep 100
else
 echo "Services stopped";
 break
fi

done

echo -n "Remove Application Template: "
/usr/bin/serviced service remove resmgr
sleep 10
echo "Restore Backup: $BACKUP_FILE_TO_RESTORE"
serviced restore $BACKUP_FILE_TO_RESTORE
