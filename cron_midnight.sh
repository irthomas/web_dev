#!/bin/sh
# cron jobs to be run at midnight
# add line to crontab -e as follows:
# 0 0 * * * /var/www/web_dev/cron_midnight.sh /var/www/cron.log 2>&1
$(which python3) /var/www/web_dev/djdownloader/downloader/update.py
$(which python3) /var/www/web_dev/fl/articles/update.py
$(which python3) /var/www/web_dev/fl/nomad_orders/update.py
