import { Link } from "react-router-dom"

function DashboardLayout({ children }) {
    return (
        <div className="min-h-screen bg-white">

            {/* Navbar */}
            <nav className="bg-sky-100 border-b border-sky-200 px-6 py-3 flex justify-between items-center">

                {/* Logo */}
                <h1 className="text-lg font-semibold text-black tracking-wide">
                    Aaam Aadami Bank
                </h1>

                {/* Navigation */}
                <div className="flex gap-6 text-sm font-medium text-black">

                    <Link
                        to="/dashboard"
                        className="hover:text-blue-700 transition"
                    >
                        Dashboard
                    </Link>

                    <Link
                        to="/users"
                        className="hover:text-blue-700 transition"
                    >
                        Customers
                    </Link>

                    <Link
                        to="/create-user"
                        className="hover:text-blue-700 transition"
                    >
                        Create User
                    </Link>

                </div>

                {/* Logout */}
                <button className="bg-black text-white text-sm px-3 py-1.5 rounded-md hover:bg-gray-800 transition">
                    Logout
                </button>

            </nav>

            {/* Main Content */}
            <main className="p-6">
                {children}
            </main>

        </div>
    )
}

export default DashboardLayout