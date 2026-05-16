from fastapi import APIRouter
from database import (
    accounts_collection,
    transactions_collection
)
from datetime import datetime

router = APIRouter()


@router.post("/transfer")
def transfer(data: dict):

    sender = data["sender"]
    receiver = data["receiver"]
    amount = float(data["amount"])

    sender_acc = accounts_collection.find_one(
        {"account_number": sender}
    )

    receiver_acc = accounts_collection.find_one(
        {"account_number": receiver}
    )

    if not sender_acc or not receiver_acc:

        return {
            "message":
            "Invalid account"
        }

    if sender_acc["balance"] < amount:

        return {
            "message":
            "Insufficient balance"
        }

    accounts_collection.update_one(
        {"account_number": sender},
        {
            "$set": {
                "balance":
                sender_acc["balance"] - amount
            }
        }
    )

    accounts_collection.update_one(
        {"account_number": receiver},
        {
            "$set": {
                "balance":
                receiver_acc["balance"] + amount
            }
        }
    )

    transactions_collection.insert_one({

        "account_number": sender,

        "type": "transfer_sent",

        "amount": amount,

        "date": datetime.now().isoformat()
    })

    transactions_collection.insert_one({

        "account_number": receiver,

        "type": "transfer_received",

        "amount": amount,

        "date": datetime.now().isoformat()
    })

    return {
        "message":
        "Transfer successful"
    }