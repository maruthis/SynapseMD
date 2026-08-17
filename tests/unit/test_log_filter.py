import logging

from synapsemd_platform.observability.log_filter import (
    PhiLogFilter,
    install_phi_log_filter,
    redact_log_message,
)


PLANTED = (
    "Patient Dr. Jane Smith MRN:ABC12345 glucose 126 mg/dL "
    "email john.doe@example.com phone 555-123-4567"
)


def test_redact_log_message_strips_planted_phi() -> None:
    redacted = redact_log_message(PLANTED)
    assert "Jane Smith" not in redacted
    assert "john.doe@example.com" not in redacted
    assert "555-123-4567" not in redacted
    assert "ABC12345" not in redacted
    assert "126 mg/dL" not in redacted
    assert "[REDACTED]" in redacted


def test_phi_log_filter_redacts_args() -> None:
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="contact %s",
        args=("john.doe@example.com",),
        exc_info=None,
    )
    assert PhiLogFilter().filter(record) is True
    assert "john.doe@example.com" not in record.getMessage()


def test_phi_log_filter_redacts_dict_args_and_non_strings() -> None:
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="contact %(email)s %(n)s",
        args={"email": "john.doe@example.com", "n": 3},
        exc_info=None,
    )
    assert PhiLogFilter().filter(record) is True
    assert "john.doe@example.com" not in record.getMessage()


def test_phi_log_filter_fail_closed() -> None:
    class Boom:
        def __str__(self) -> str:
            raise RuntimeError("cannot stringify")

    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="ok",
        args=(),
        exc_info=None,
    )
    record.msg = Boom()  # type: ignore[assignment]
    assert PhiLogFilter().filter(record) is True
    assert record.msg == "[REDACTED]"


def test_install_phi_log_filter_is_idempotent() -> None:
    logger = logging.getLogger("synapsemd.test.phi.filter")
    first = install_phi_log_filter(logger)
    second = install_phi_log_filter(logger)
    assert first is not second
    assert sum(isinstance(item, PhiLogFilter) for item in logger.filters) == 1
