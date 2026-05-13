import DashboardLayout from "../layouts/DashboardLayout"

function Dashboard() {
    return (
        <DashboardLayout>

            {/* Heading */}
            <div className="mb-8">
                <h1 className="text-2xl font-semibold text-black mb-2">
                    Welcome User
                </h1>

                <p className="text-gray-600 text-sm">
                    Manage your banking activities securely.
                </p>
            </div>

            {/* Dashboard Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">

                {/* Balance Card */}
                <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
                    <p className="text-sm text-gray-500 mb-2">
                        Current Balance
                    </p>

                    <h2 className="text-2xl font-bold text-black">
                        ₹45,000
                    </h2>
                </div>

                {/* Transactions */}
                <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
                    <p className="text-sm text-gray-500 mb-2">
                        Transactions
                    </p>

                    <h2 className="text-2xl font-bold text-black">
                        128
                    </h2>
                </div>

                {/* Transfers */}
                <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
                    <p className="text-sm text-gray-500 mb-2">
                        Money Transfers
                    </p>

                    <h2 className="text-2xl font-bold text-black">
                        24
                    </h2>
                </div>

                {/* Support */}
                <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
                    <p className="text-sm text-gray-500 mb-2">
                        Support Requests
                    </p>

                    <h2 className="text-2xl font-bold text-black">
                        3
                    </h2>
                </div>

            </div>
            {/* Recent Transactions */}
            <div className="mt-10">

                <div className="flex justify-between items-center mb-4">

                    <h2 className="text-xl font-semibold text-black">
                        Recent Transactions
                    </h2>

                    <button className="text-sm text-blue-600 hover:underline">
                        View All
                    </button>

                </div>

                <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">

                    <table className="w-full">

                        <thead className="bg-sky-50 text-left">

                            <tr>

                                <th className="p-4 text-sm font-semibold text-black">
                                    Name
                                </th>

                                <th className="p-4 text-sm font-semibold text-black">
                                    Type
                                </th>

                                <th className="p-4 text-sm font-semibold text-black">
                                    Amount
                                </th>

                                <th className="p-4 text-sm font-semibold text-black">
                                    Status
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            <tr className="border-t">

                                <td className="p-4 text-sm">
                                    Rahul Sharma
                                </td>

                                <td className="p-4 text-sm">
                                    Transfer
                                </td>

                                <td className="p-4 text-sm font-medium">
                                    ₹2,000
                                </td>

                                <td className="p-4 text-sm text-green-600">
                                    Success
                                </td>

                            </tr>

                            <tr className="border-t">

                                <td className="p-4 text-sm">
                                    Netflix
                                </td>

                                <td className="p-4 text-sm">
                                    Subscription
                                </td>

                                <td className="p-4 text-sm font-medium">
                                    ₹799
                                </td>

                                <td className="p-4 text-sm text-green-600">
                                    Paid
                                </td>

                            </tr>

                            <tr className="border-t">

                                <td className="p-4 text-sm">
                                    Amazon
                                </td>

                                <td className="p-4 text-sm">
                                    Shopping
                                </td>

                                <td className="p-4 text-sm font-medium">
                                    ₹4,500
                                </td>

                                <td className="p-4 text-sm text-red-500">
                                    Pending
                                </td>

                            </tr>

                        </tbody>

                    </table>

                </div>

            </div>

        </DashboardLayout>
    )
}

export default Dashboard