import logging
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDBHandler(logging.Handler):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def emit(self, record):
        log_entry = self.format(record)
        point = (
            Point("django_logs")
            .tag("level", record.levelname)
            .tag("module", record.module)
            .field("message", log_entry)
            .time(record.created, WritePrecision.NS)  # Write timestamp
        )
        write_api = self.client.WriteApi(influxdb_client=self.client, write_options=SYNCHRONOUS)
        write_api.write(bucket=self.client.bucket, org=self.client.org, record=point)
