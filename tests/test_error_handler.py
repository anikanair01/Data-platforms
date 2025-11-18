import sqlite3
import pytest
from unittest.mock import Mock

from utils.error_handler import Apperror, handle_errors

# --- Fixtures ---------------------------------------------------------------

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE accounts(id INTEGER PRIMARY KEY, balance INTEGER)")
    cur.executemany("INSERT INTO accounts(id, balance) VALUES (?, ?)", [(1, 100), (2, 50)])
    conn.commit()
    yield conn
    conn.close()

# --- Helper (harder) function under test ----------------------------------

def transfer_funds(conn, from_id, to_id, amount):
    """Transfer amount between accounts with simple checks.

    Raises Apperror with status_code 404 when source account not found,
    and 400 when insufficient funds.
    """
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,))
    row = cur.fetchone()
    if row is None:
        raise Apperror("source account not found", status_code=404)
    if row[0] < amount:
        raise Apperror("insufficient funds", status_code=400)

    cur.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
    conn.commit()
    return True

# --- Tests -----------------------------------------------------------------

def test_transfer_funds_success(db_conn):
    assert transfer_funds(db_conn, 1, 2, 30) is True
    cur = db_conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id = 1")
    assert cur.fetchone()[0] == 70
    cur.execute("SELECT balance FROM accounts WHERE id = 2")
    assert cur.fetchone()[0] == 80


def test_transfer_funds_insufficient(db_conn):
    with pytest.raises(Apperror) as exc:
        transfer_funds(db_conn, 2, 1, 500)
    assert exc.value.status_code == 400


def test_transfer_funds_source_not_found(db_conn):
    with pytest.raises(Apperror) as exc:
        transfer_funds(db_conn, 999, 1, 10)  # non-existent source account
    assert exc.value.status_code == 404
    assert "source account" in str(exc.value).lower()


# Tests for the decorator behavior (unit-level)
def test_handle_errors_success_and_apperror():
    logger = Mock()

    @handle_errors(logger)
    def succeed(a, b):
        return a + b

    @handle_errors(logger)
    def fail_with_apperror():
        raise Apperror("bad things", status_code=422)

    assert succeed(1, 2) == 3
    resp = fail_with_apperror()
    assert isinstance(resp, dict)
    assert resp["error"] == "bad things"
    assert resp["status_code"] == 422
    logger.error.assert_called()


def test_handle_errors_unexpected_exception_logs_and_returns_500():
    logger = Mock()

    @handle_errors(logger)
    def blow_up():
        raise ValueError("boom")

    resp = blow_up()
    assert resp["status_code"] == 500
    assert "unexpected" in resp["error"].lower()
    logger.error.assert_called()

