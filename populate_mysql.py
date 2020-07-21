#!venv/bin/python3
# -*- coding: utf-8 -*-
import time, datetime, pytz, random, sys
import pymysql
#
utc = pytz.utc
#
def check_args():
    arguments = len(sys.argv)
    if arguments == 2:
        password = sys.argv[1]
        return password
    else:
        print ('Please pass the password to the script as command line argument')


def con_mysql(password):
    connection = pymysql.connect(host='localhost', user='metrics', password=password,
                                db='grafana')
    return connection


def get_epoch_ms_now():
        epoch_ms_now = int(utc.localize((datetime.datetime.now()),is_dst=False).strftime('%s'))
        return epoch_ms_now

#
def create_mets():
    metrics = []
    for i in range(1, 358):
        metrics.append(random.randint(100,300))
    idx800 = random.choice(range(1,200))
    idx1000 = random.choice(range(250,300))
    metrics.insert(idx800, 800)
    metrics.insert(idx1000, 1000)
    #
    met_with_timestamp = []
    time_now = get_epoch_ms_now()
    for met in metrics:
        met_with_timestamp.append((time_now, met))
        time_now = time_now - 60
    time_1000 = met_with_timestamp[idx1000][0]
    time_800 = met_with_timestamp[idx800][0]
    return (met_with_timestamp, time_1000, time_800)
#
metrics, time_1000, time_800 = create_mets()

### Insert metrics
conn = con_mysql('DemoPassw0rd1234')
try:
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE Metrics")
    conn.commit()
    for met in metrics:
        ts = met[0]
        data = met[1]
        insert_metric = f"INSERT INTO Metrics(metric_name,timestamp_in_s, metric_data) VALUES ('response_time', {ts}, {data})"
        cursor.execute(insert_metric)
    conn.commit()
except Exception as e:
    print (e)
finally:
    conn.close()

### Insert Annotations
conn = con_mysql('DemoPassw0rd1234')
try:
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE annotations")
    conn.commit()
    annot1 = f"INSERT INTO annotations(timestamp_in_s, timeEnd, text, tags) VALUES({time_1000}, {time_1000+600},'<p>Running an application update</p><a href=https://www.google.es>More info here...</a>', 'server1, v2.3.4')"
    annot2 = f"INSERT INTO annotations(timestamp_in_s, timeEnd, text, tags) VALUES({time_800}, {time_800+800},'<p>Updating OS</p><a href=https://www.google.es>Open the URI</a>', 'db-host01, tag2')"
    cursor.execute(annot1)
    cursor.execute(annot2)
    conn.commit()
except Exception as e:
    print (e)
finally:
    conn.close()
