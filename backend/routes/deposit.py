from fastapi import APIRouter
from database import (
    accounts_collection,
    transactions_collection
)
from datetime import datetime

router = APIRouter()


@router.post("/deposit")
def deposit(data: dict):

    account_number = data["account_number"]
    amount = float(data["amount"])

    account = accounts_collection.find_one({
        "account_number": account_number
    })

    if not account:

        return {
            "message": "Account not found"
        }

    new_balance = account["balance"] + amount

    accounts_collection.update_one(
        {
            "account_number": account_number
        },
        {
            "$set": {
                "balance": new_balance
            }
        }
    )

    transaction_data = {
        "account_number": account_number,
        "type": "deposit",
        "amount": amount,
        "created_at": datetime.now().isoformat()
    }

    transactions_collection.insert_one(transaction_data)

    return {
        "message": "Deposit successful",
        "balance Deposit": amount
    }