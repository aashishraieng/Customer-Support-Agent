import { useState } from "react"
import { useNavigate } from "react-router-dom"

function Login() {

    const navigate = useNavigate()

    const [role, setRole] = useState("customer")

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")


    const handleLogin = (e) => {

        e.preventDefault()


        // Employee login

        if (

            role === "employee"

            &&

            username.toLowerCase() ===
            "ashish rai"

            &&

            password ===
            "ashishrai@123"

        ) {

            navigate("/dashboard")

            return
        }



        // Customer demo login

        if (

            role === "customer"

            &&

            password === "1234"

        ) {

            localStorage.setItem(
                "accountNumber",
                username
            )

            navigate(
                "/customer-dashboard"
            )

            return
        }


        alert(
            "Invalid credentials"
        )

    }



    return (

        <div className="min-h-screen bg-sky-50 flex items-center justify-center">

            <div className="bg-white p-8 rounded-2xl shadow w-full max-w-md">

                <h1 className="text-2xl font-bold text-center mb-2">

                    Aaam Aadami Bank

                </h1>

                <p className="text-center text-gray-500 mb-8">

                    Login Portal

                </p>


                <form
                    onSubmit={handleLogin}
                    className="space-y-5"
                >


                    <select

                        value={role}

                        onChange={(e) =>
                            setRole(
                                e.target.value
                            )
                        }

                        className="w-full border p-3 rounded-lg"
                    >

                        <option value="customer">

                            Customer

                        </option>

                        <option value="employee">

                            Employee

                        </option>

                    </select>



                    <input

                        type="text"

                        value={username}

                        onChange={(e) =>
                            setUsername(
                                e.target.value
                            )
                        }

                        placeholder={

                            role === "employee"

                                ?

                                "Employee Name"

                                :

                                "Account Number"

                        }

                        className="w-full border p-3 rounded-lg"

                    />



                    <input

                        type="password"

                        value={password}

                        onChange={(e) =>
                            setPassword(
                                e.target.value
                            )
                        }

                        placeholder="Password"

                        className="w-full border p-3 rounded-lg"

                    />


                    <button

                        className="
                        w-full
                        bg-black
                        text-white
                        py-3
                        rounded-lg
                        "

                    >

                        Login

                    </button>


                </form>

            </div>

        </div>
    )
}

export default Login