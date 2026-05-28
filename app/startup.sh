#!/bin/bash
source /home/site/wwwroot/antenv/bin/activate
cd /home/site/wwwroot/src
gunicorn --bind=0.0.0.0:8000 --timeout=600 --workers=2 main:app
