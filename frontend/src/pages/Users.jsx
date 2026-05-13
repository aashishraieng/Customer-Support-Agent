import { useEffect, useState } from "react"
import API from "../services/api"

function Users() {

    const [users, setUsers] = useState([])

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
                                        Account Number
                                    </th>

                                    <th className="p-4 text-sm font-semibold">
                                        Debit Card
                                    </th>

                                </tr>

                            </thead>

                            <tbody>

                                {users.map((user) => (

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