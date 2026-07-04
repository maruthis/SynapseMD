"""Unit tests for Kafka audit sink."""

import sys
from unittest.mock import MagicMock, patch

from synapsemd_platform.audit.kafka_sink import KafkaAuditSink


def test_kafka_sink_publish() -> None:
    sink = KafkaAuditSink("localhost:9092", "synapsemd.audit.events")
    mock_producer = MagicMock()
    with patch.object(sink, "_get_producer", return_value=mock_producer):
        sink.publish({"event_type": "test", "tenant_id": "t1"})
    mock_producer.send.assert_called_once()
    mock_producer.flush.assert_called_once()


def test_kafka_sink_lazy_producer() -> None:
    sink = KafkaAuditSink("localhost:9092", "audit")
    mock_producer = MagicMock()
    mock_kafka = MagicMock()
    mock_kafka.KafkaProducer.return_value = mock_producer
    with patch.dict(sys.modules, {"kafka": mock_kafka}):
        producer = sink._get_producer()
        assert producer is mock_producer
        assert sink._get_producer() is mock_producer
    mock_kafka.KafkaProducer.assert_called_once()
