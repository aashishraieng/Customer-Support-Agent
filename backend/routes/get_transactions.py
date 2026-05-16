from fastapi import APIRouter
from database import transactions_collection

router = APIRouter()


@router.get("/transactions/{account_number}")
def get_transactions(account_number: str):

    transactions = []

    data = transactions_collection.find(
        {
            "account_number": account_number
        }
    )

    for txn in data:

        transactions.append({

            "type":
            txn["type"],

            "amount":
            txn["amount"],

            "date":
            txn.get(
                "created_at",
                txn.get("date", "N/A")
            )

        })

    return {
        "transactions":
        transactions
    }