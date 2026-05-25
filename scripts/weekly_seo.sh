#!/bin/bash
# Haftalık SEO raporu — her Pazartesi 09:00

export GA4_PROPERTY_ID=504367222
cd /root/projects/yakinimdakideprem.com
/usr/bin/python3 scripts/seo_report.py --days 7 >> reports/cron.log 2>&1
echo "[$(date -Iseconds)] Rapor üretildi" >> reports/cron.log

# Sitemap lastmod güncelleme
bash "$(dirname "$0")/update-sitemap-lastmod.sh" >> reports/cron.log 2>&1
echo "[$(date -Iseconds)] Sitemap lastmod güncellendi" >> reports/cron.log
