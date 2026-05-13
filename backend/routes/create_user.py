from fastapi import APIRouter
from database import (
    users_collection,
    accounts_collection,
    cards_collection
)
import random

router = APIRouter()


def generate_account_number():
    return str(random.randint(10000000, 99999999))


def generate_card_number():

    parts = []

    for _ in range(4):
        parts.append(str(random.randint(1000, 9999)))

    return "-".join(parts)


@router.post("/create-user")
def create_user(data: dict):

    # USER
    user_data = {
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"]
    }

    user_result = users_collection.insert_one(user_data)

    user_id = str(user_result.inserted_id)

    # ACCOUNT
    account_data = {
        "user_id": user_id,
        "account_number": generate_account_number(),
        "balance": 0,
        "account_type": "savings"
    }

    account_result = accounts_collection.insert_one(account_data)

    # CARD
    card_data = {
        "user_id": user_id,
        "card_number": generate_card_number(),
        "card_type": "debit",
        "status": "active"
    }

    card_result = cards_collection.insert_one(card_data)

    # RESPONSE
    return {
        "message": "User created successfully",

        "user": {
            "id": user_id,
            "name": user_data["name"],
            "email": user_data["email"],
            "phone": user_data["phone"]
        },

        "account": {
            "id": str(account_result.inserted_id),
            "account_number": account_data["account_number"],
            "balance": account_data["balance"],
            "account_type": account_data["account_type"]
        },

        "card": {
            "id": str(card_result.inserted_id),
            "card_number": card_data["card_number"],
            "card_type": card_data["card_type"],
            "status": card_data["status"]
        }
    }