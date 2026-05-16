from fastapi import APIRouter
from database import (
    accounts_collection,
    transactions_collection
)
from datetime import datetime

router = APIRouter()


@router.post("/withdraw")
def withdraw(data: dict):

    account_number = data["account_number"]
    amount = float(data["amount"])

    account = accounts_collection.find_one({
        "account_number": account_number
    })

    if not account:

        return {
            "message": "Account not found"
        }

    if account["balance"] < amount:

        return {
            "message": "Insufficient balance"
        }

    new_balance = account["balance"] - amount

    accounts_collection.update_one(
        {"account_number": account_number},
        {"$set": {"balance": new_balance}}
    )

    transaction = {
        "account_number": account_number,
        "type": "withdraw",
        "amount": amount,
        "created_at": datetime.now().isoformat()
    }

    transactions_collection.insert_one(
        transaction
    )

    return {
        "message": "Withdrawal successful",
        "withdrawn amount": amount
    }