from fastapi import APIRouter
from database import (
    accounts_collection,
    cards_collection,
    transactions_collection,
    users_collection
)

router = APIRouter()


@router.get(
"/customer-profile/{account_number}"
)
def customer_profile(
    account_number: str
):

    account = accounts_collection.find_one({

        "account_number":
        account_number

    })


    if not account:

        return {
            "message":
            "Customer not found"
        }


    user = users_collection.find_one({

        "_id":
        account["user_id"]

    })


    card = cards_collection.find_one({

        "user_id":
        account["user_id"]

    })


    transactions = []

    for txn in transactions_collection.find({

        "account_number":
        account_number

    }):

        transactions.append({

            "type":
            txn["type"],

            "amount":
            txn["amount"]

        })


    return {

        "name":
        user["name"]
        if user else "Customer",

        "balance":
        account["balance"],

        "account_number":
        account["account_number"],

        "card_number":
        card["card_number"]
        if card else "N/A",

        "transactions":
        transactions

    }