#!/bin/bash
if [[ "${1}" == "celery" ]]; then
  celery -A app.worker worker --loglevel=info --logfile=logs/celery.log
elif [[ "${1}" == "flower" ]]; then
  celery -A app.worker flower --basic-auth=user:pswd
elif [[ "${1}" == "beat" ]]; then
  celery -A app.worker beat -l INFO
 fi