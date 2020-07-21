FROM grafana/grafana:6.6.2-ubuntu
USER root
RUN apt-get update && apt-get install -y bash inetutils-ping
RUN mkdir -p /data/grafana/plugins
RUN mkdir -p /data/grafana/provisioning/datasources
RUN mkdir /data/grafana/provisioning/dashboards
COPY grafana/datasource.yml /data/grafana/provisioning/datasources
COPY grafana/dashboard.yml /data/grafana/provisioning/dashboards
COPY grafana/mysql-dashboard.json /data/grafana/provisioning/dashboards
COPY grafana/influxdb-dashboard.json /data/grafana/provisioning/dashboards
RUN chown -R grafana:grafana /data/grafana/
