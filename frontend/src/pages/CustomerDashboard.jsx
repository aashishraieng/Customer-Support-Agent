import { useEffect, useState } from "react"
import API from "../services/api"
import { useNavigate } from "react-router-dom"

function CustomerDashboard() {

    const navigate = useNavigate()

    const [data, setData] = useState(null)

    const [receiver, setReceiver] = useState("")
    const [amount, setAmount] = useState("")


    const fetchProfile = async () => {

        try {

            const accountNumber =
                localStorage.getItem(
                    "accountNumber"
                )

            const response =
                await API.get(

                    `/customer-profile/${accountNumber}`

                )

            setData(
                response.data
            )

        }

        catch (err) {

            console.log(err)

        }

    }


    useEffect(() => {

        fetchProfile()

    }, [])



    const logout = () => {

        localStorage.removeItem(
            "accountNumber"
        )

        navigate("/login")

    }



    const transferMoney =
        async () => {

            try {

                await API.post(

                    "/transfer",

                    {

                        sender:
                            data.account_number,

                        receiver,

                        amount

                    }

                )


                alert(
                    "Transfer Successful"
                )


                setReceiver("")
                setAmount("")

                fetchProfile()

            }

            catch {

                alert(
                    "Transfer Failed"
                )

            }

        }



    if (!data) {

        return <h1>
            Loading...
        </h1>

    }



    return (

        <div className="
min-h-screen
bg-sky-50
p-8
">

            <div className="
max-w-6xl
mx-auto
">


                <div className="
flex
justify-between
items-center
mb-8
">

                    <div>

                        <h1 className="
text-3xl
font-bold
">

                            Welcome,
                            {data.name}

                        </h1>

                    </div>


                    <button

                        onClick={logout}

                        className="
bg-red-500
text-white
px-4
py-2
rounded-lg
"

                    >

                        Logout

                    </button>

                </div>



                <div className="
grid
md:grid-cols-3
gap-5
">

                    <div className="
bg-white
p-6
rounded-xl
">

                        Balance

                        <h2 className="
text-2xl
font-bold
">

                            ₹ {data.balance}

                        </h2>

                    </div>



                    <div className="
bg-white
p-6
rounded-xl
">

                        Account Number

                        <h2>

                            {
                                data.account_number
                            }

                        </h2>

                    </div>



                    <div className="
bg-white
p-6
rounded-xl
">

                        Debit Card

                        <h2>

                            {
                                data.card_number
                            }

                        </h2>

                    </div>

                </div>




                {/* Transfer */}

                <div className="
bg-white
p-6
rounded-xl
mt-8
">

                    <h2 className="
text-xl
font-semibold
mb-4
">

                        Transfer Money

                    </h2>



                    <input

                        placeholder="
Receiver Account Number
"

                        value={receiver}

                        onChange={(e) =>

                            setReceiver(
                                e.target.value
                            )

                        }

                        className="
border
p-3
rounded-lg
w-full
mb-3
"

                    />



                    <input

                        placeholder="
Amount
"

                        value={amount}

                        onChange={(e) =>

                            setAmount(
                                e.target.value
                            )

                        }

                        className="
border
p-3
rounded-lg
w-full
mb-3
"

                    />



                    <button

                        onClick={
                            transferMoney
                        }

                        className="
bg-black
text-white
px-5
py-3
rounded-lg
"

                    >

                        Transfer

                    </button>

                </div>




                {/* Transactions */}

                <div className="
bg-white
p-6
rounded-xl
mt-8
">

                    <h2 className="
mb-4
text-xl
font-semibold
">

                        Transactions

                    </h2>



                    {

                        data.transactions.map(

                            (txn, index) => (

                                <div
                                    key={index}
                                    className="
border-b
py-2
"
                                >

                                    {txn.type}

                                    -

                                    ₹{txn.amount}

                                </div>

                            )

                        )

                    }

                </div>


            </div>

        </div>

    )

}

export default CustomerDashboard