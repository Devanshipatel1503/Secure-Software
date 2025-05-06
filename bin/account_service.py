import sqlite3

# Database file path (can be centralized for easier updates/testing)
DB_PATH = 'bank.db'

def get_balance(account_number, owner):
    """
    Retrieves the balance for a given account number belonging to a specific owner.
    
    Args:
        account_number (str): The ID of the account.
        owner (str): The username or identifier of the account owner.
    
    Returns:
        float or None: The account balance, or None if the account doesn't exist or mismatches the owner.
    """
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute(
            "SELECT balance FROM accounts WHERE id=? AND owner=?",
            (account_number, owner)
        )
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        con.close()

def do_transfer(source, target, amount):
    """
    Transfers a specified amount from the source account to the target account.

    Args:
        source (str): ID of the source account.
        target (str): ID of the destination account.
        amount (float): The amount to transfer.

    Returns:
        bool: True if the transfer succeeded, False if the target account doesn't exist.
    """
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        # Ensure the target account exists before attempting a transfer
        cur.execute("SELECT id FROM accounts WHERE id=?", (target,))
        if cur.fetchone() is None:
            return False

        # Deduct from source
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, source))

        # Add to target
        cur.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, target))

        con.commit()
        return True
    finally:
        con.close()
