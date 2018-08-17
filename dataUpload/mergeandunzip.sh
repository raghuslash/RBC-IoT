#!/bin/bash
cd /home/raghu/


ls esparts
if [ $? -neq 0 ]
then
	echo "esparts doesn't exist... exiting"
    exit 1
fi


cd esparts

cat esbackup.zip* > backup.zip
unzip backup.zip

if [ $? -eq 0 ]
then
	echo "Successfully unzipped /esbackup folder."     
    rm -rf ../esbackup/*    
    mv esbackup/* ../esbackup/
    
    cd ..
    rm -rf esparts
    	
    exit 0
else
	echo "Could not unzip /esbackup folder." 
	exit 2
fi
