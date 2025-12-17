import oracledb

ORACLE_CONFIG = {
    "user": "SYSTEM",
    "password": "system",
    "dsn": "localhost:1521/XEPDB1",
}

def get_connection():
    return oracledb.connect(**ORACLE_CONFIG)

def get_pending_by_customer_id(customer_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT PENDING_AMOUNT FROM CUSTOMER_LOAN_DATA WHERE CUSTOMER_ID = :1",
        [customer_id],
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None

def get_pending_by_account_no(account_no: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT PENDING_AMOUNT FROM CUSTOMER_LOAN_DATA WHERE ACCOUNT_NO = :1",
        [account_no],
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None
