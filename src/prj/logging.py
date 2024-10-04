import logging, os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client



class InfluxDBHandler(logging.Handler):
    def __init__(self, client):
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        point = (
            Point("django_logs")
            .tag("level", record.levelname)
            .tag("module", record.module)
            .field("message", log_entry)
        )
        
        token = os.environ.get("INFLUXDB_TOKEN")
        org = os.environ.get("INFLUXDB_ORG")
        url = os.environ.get("INFLUXDB_URL")
        write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        write_api = write_client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=os.environ.get("INFLUXDB_DB"), org="canilgu.dev", record=point)