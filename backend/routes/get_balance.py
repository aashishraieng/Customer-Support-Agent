from fastapi import APIRouter
from database import accounts_collection

router = APIRouter()


@router.get("/balance/{account_number}")
def get_balance(account_number: str):

    account = accounts_collection.find_one({
        "account_number": account_number
    })

    if not account:

        return {
            "message": "Account not found"
        }

    return {

        "account_number":
        account["account_number"],

        "balance":
        account["balance"]

    }