import { useEffect, useState } from "react"
import API from "../services/api"

function Users() {

    const [users, setUsers] = useState([])
    const [search, setSearch] = useState("")

    const fetchUsers = async () => {

        try {

            const response = await API.get("/users")

            setUsers(response.data.users)

        } catch (error) {

            console.log(error)
        }
    }

    useEffect(() => {
        fetchUsers()
    }, [])

    return (

        <div className="min-h-screen bg-sky-50 p-8">

            <div className="max-w-6xl mx-auto">

                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">

                    <div className="flex items-center justify-between mb-6">

                        <h1 className="text-2xl font-semibold text-black">
                            Bank Customers
                        </h1>
                        <p className="text-sm text-gray-500">
                            Total Customers: {users.length}
                        </p>

                    </div>
                    <div className="mb-5">

                        <input
                            type="text"
                            placeholder="Search by account number..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            className="border border-gray-300 rounded-lg px-4 py-2 text-sm w-72"
                        />

                    </div>

                    <div className="overflow-x-auto">

                        <table className="w-full border-collapse">

                            <thead>

                                <tr className="bg-sky-100 text-left">

                                    <th className="p-4 text-sm font-semibold">
                                        Name
                                    </th>

                                    <th className="p-4 text-sm font-semibold">
                                        Email
                                    </th>

                                    <th className="p-4 text-sm font-semibold">
                                        Phone
                                    </th>
                                    <th className="p-4 text-sm font-semibold">
                                        Balance
                                    </th>
                                    <th className="p-4 text-sm font-semibold">
                                        Account Number
                                    </th>

                                    <th className="p-4 text-sm font-semibold">
                                        Debit Card
                                    </th>

                                </tr>

                            </thead>

                            <tbody>

                                {users
                                    .filter(user =>
                                        (user.account_number || "")
                                            .toString()
                                            .includes(search.trim())
                                    )
                                    .map((user) => (

                                        <tr
                                            key={user.id}
                                            className="border-b border-gray-200"
                                        >

                                            <td className="p-4 text-sm">
                                                {user.name}
                                            </td>

                                            <td className="p-4 text-sm">
                                                {user.email}
                                            </td>

                                            <td className="p-4 text-sm">
                                                {user.phone}
                                            </td>
                                            <td className="p-4 text-sm">
                                                ₹ {user.balance}
                                            </td>
                                            <td className="p-4 text-sm">
                                                {user.account_number}
                                            </td>

                                            <td className="p-4 text-sm">
                                                {user.card_number}
                                            </td>

                                        </tr>
                                    ))}

                            </tbody>

                        </table>

                    </div>

                </div>

            </div>

        </div>
    )
}

export default Users