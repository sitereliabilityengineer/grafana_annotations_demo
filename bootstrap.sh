#!/bin/sh

### Modify password in All the Files
echo -n "Please Input the New Password to Access MySQL and InfluxDb: "
read new_pass
egrep -lRZ 'DemoPassw0rd1234' . | xargs -0 -l sed -i -e "s/DemoPassw0rd1234/$new_pass/g"

# Install requirements inside venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

# Volume creation
echo -e "Docker volume Creation!"
docker volume create grafana-dashboards
docker volume create grafana-datasources
docker volume create grafana-plugins
docker volume create grafana-volume
docker volume create mysqlvol-01
#

# Start everything
echo -e "Starting docker containers with docker-compose. It will take approx 70s"
docker-compose -f docker-compose.yml.all up -d
sleep 90

# Populate MySQL
echo -e "Populate MySQL"
python3 populate_mysql.py
# Populate Influxdb
echo -e "Populating InfluxDB"
python3 populate_influxdb.py
