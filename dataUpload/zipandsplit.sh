#!/bin/bash
cd /home/raghu

zip -r esbackup.zip esbackup

mkdir -p esparts
rm -rf esparts/*

echo "Now starting split... Please wait."
split --bytes=100MB esbackup.zip esparts/esbackup.zip_

if [ $? -eq 0 ]; then
	echo "Successfully completed split."
    #add index name file to paths folder	
    rm esbackup.zip
	exit 0
else
	echo "Could not split." 
	rm esbackup.zip
	rm -rf esparts
	exit 1
fi


