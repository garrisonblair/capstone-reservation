#!/bin/bash

USER=`whoami`
BACKUP_DIR="/home/$USER/capstone_backups"
LATEST_BACKUP=`ls -t $BACKUP_DIR | head -1`
FILE_NAME="db.json"
VIRTUAL_ENV="/home/$USER/venv/CapstoneReservation"

cp $BACKUP_DIR/$LATEST_BACKUP .
tar -zxvf $LATEST_BACKUP

FOLDER_NAME=${LATEST_BACKUP%.*}
cd $FOLDER_NAME

# Restore old DB
source $VIRTUAL_ENV/bin/activate
cd ..
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata $FOLDER_NAME/$FILE_NAME

# Clean up
rm -rf $FOLDER_NAME
rm $LATEST_BACKUP
