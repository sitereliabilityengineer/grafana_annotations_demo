#!/bin/sh

## Stop all containers
docker-compose -f docker-compose.yml.all down

# Delete previous created volumes
docker volume rm grafana-dashboards grafana-datasources grafana-plugins grafana-volume mysqlvol-01

## Delete all images
docker images | grep -E -i "grafana|mysql|influxdb" | awk '{print $3}' | xargs docker rmi --force

# Remove venv
rm -rf $(pwd)/venv

## remove data files inside influxdb
echo -e "\nPlease remove Manually the directories inside $(pwd)/influxdb/data/*"
