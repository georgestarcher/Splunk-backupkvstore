# Splunk KVStore Backup 


Author: George Starcher (starcher)
Email: george@georgestarcher.com

This code is presented **AS IS** under MIT license.

##Summary:

This Python script backs up KVStore collections via the REST API.

##Requirements:

* Splunk Admin role level credentials 

* Make a subfolder called backup

##Usage:

* Optional: make a different subfolder to backup to. Update the field backup_folder in the kvstore.conf

1. Edit the target splunk server in kvstore.conf

    splunk_server = localhost

2. Execute the script

    python backupkvstore.py

