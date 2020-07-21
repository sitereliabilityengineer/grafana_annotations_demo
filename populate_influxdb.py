#!venv/bin/python3
# -*- coding: utf-8 -*-
import time, datetime, pytz, random, sys
from influxdb import InfluxDBClient
#
utc = pytz.utc
#


def get_epoch_ms_now():
        epoch_ms_now = int(utc.localize((datetime.datetime.now()),is_dst=False).strftime('%s'))
        return epoch_ms_now

#
def create_mets():
    populate = []
    time_now = get_epoch_ms_now()
    for i in range(1, 361):
        met = random.randint(100,300)
        populate.append({"measurement": "metrics",
                        "time": time_now,
                        "fields": {
                            "resp_time": met
                            }
                        })
        time_now = time_now - 60
    return populate

def create_annotation(time, text, tags):
    annotation = {"measurement": "annotations",
                "time": time,
                "fields": {
                    "text": text
                    },
                "tags": {
                    "tag1": tags
                    }
                }
    return annotation


populate_list = create_mets()

### Save index for later use, to create annotations
tmp_annot1 = random.choice(populate_list)
annot1_idx = populate_list.index(tmp_annot1)
tmp_annot2 = random.choice(populate_list)
annot2_idx = populate_list.index(tmp_annot2)
# Modify to elements of the list, changing response time to 1000 and 800
populate_list[annot1_idx]['fields']['resp_time'] = 1000
populate_list[annot2_idx]['fields']['resp_time'] = 800
###

### Insert metrics
client = InfluxDBClient(host='localhost', port=8086, username='metrics', password='DemoPassw0rd1234')
client.switch_database('grafana')
client.write_points(populate_list, time_precision='s')

### Insert annotations
annotation_list = []
annotation1_time = populate_list[annot1_idx]['time']
annotation1_text = '<p>Patching servers on data-center-1</p> <a href=https://www.google.com>CHANGE-ID-9271</a>'
annotation1_tags = ['data-center-1', 'data-center-EU-1', 'CHANGE-ID-9271']
annotation1 = create_annotation(annotation1_time, annotation1_text, annotation1_tags)
annotation_list.append(annotation1)

annotation2_time = populate_list[annot2_idx]['time']
annotation2_text = '<p>Running Query on Database DB1-EU-1</p> <a href=https://www.google.com>CHANGE-ID-9371</a>'
annotation2_tags = ['data-center-EU-1', 'CHANGE-ID-9371']
annotation2 = create_annotation(annotation2_time, annotation2_text, annotation2_tags)
annotation_list.append(annotation2)
# Writing data into Influxdb
client.write_points(annotation_list, time_precision='s')
