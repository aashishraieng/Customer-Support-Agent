from fastapi import APIRouter
from database import (
    users_collection,
    accounts_collection,
    cards_collection
)

router = APIRouter()


@router.get("/users")
def get_users():

    users = []

    for user in users_collection.find():

        user_id = str(user["_id"])

        account = accounts_collection.find_one({
            "user_id": str(user["_id"])
        })

        card = cards_collection.find_one({
            "user_id": str(user["_id"])
        })

        users.append({

            "id": user_id,

            "name": user["name"],

            "email": user["email"],

            "phone": user["phone"],

            "balance": (
                account["balance"]
                if account else 0
            ),

            "account_number": (
                account["account_number"]
                if account else "N/A"
            ),

            "card_number": (
                card["card_number"]
                if card else "N/A"
            )

        })

    return {
        "users": users
    }