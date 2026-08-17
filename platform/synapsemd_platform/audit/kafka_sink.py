"""Optional Kafka/SIEM copy of audit events. Postgres is the system of record (C-9)."""

import json
from typing import Any


class KafkaAuditSink:
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self._producer = None

    def _get_producer(self) -> Any:
        if self._producer is None:
            from kafka import KafkaProducer

            self._producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
            )
        return self._producer

    def publish(self, record: dict[str, Any]) -> None:
        producer = self._get_producer()
        producer.send(self.topic, record)
        producer.flush()
