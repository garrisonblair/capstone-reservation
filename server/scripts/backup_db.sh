#!/bin/bash

APP_NAME="capstone"
TIMESTAMP=`date +%F-%H%M`
BACKUP_NAME="$APP_NAME-$TIMESTAMP"
OUTPUT_DIR="dump"
JSON_FILE_NAME="db.json"
USER=`whoami`
BACKUP_DIR="/home/$USER/capstone_backups"
VIRTUAL_ENV="/home/$USER/venv/CapstoneReservation"

source $VIRTUAL_ENV/bin/activate
mkdir $OUTPUT_DIR
python manage.py dumpdata --exclude contenttypes > $OUTPUT_DIR/$JSON_FILE_NAME
mv $OUTPUT_DIR $BACKUP_NAME
tar -zcvf $BACKUP_NAME.tgz $BACKUP_NAME
mv $BACKUP_NAME.tgz $BACKUP_DIR
rm -rf $BACKUP_NAME
