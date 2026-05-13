import { useNavigate } from "react-router-dom"

function Login() {

    const navigate = useNavigate()

    return (
        <div className="min-h-screen bg-sky-50 flex items-center justify-center px-4">

            <div className="bg-white w-full max-w-md p-8 rounded-2xl shadow-sm border border-gray-200">

                {/* Heading */}
                <div className="mb-8 text-center">

                    <h1 className="text-2xl font-semibold text-black mb-2">
                        Aaam Aadami Bank
                    </h1>

                    <p className="text-sm text-gray-500">
                        Secure Banking Login
                    </p>

                </div>

                {/* Form */}
                <form
                    className="space-y-5"
                    onSubmit={(e) => {
                        e.preventDefault()
                        navigate("/dashboard")
                    }}
                >

                    {/* Email */}
                    <div>

                        <label className="block text-sm font-medium text-black mb-2">
                            Email
                        </label>

                        <input
                            type="email"
                            placeholder="Enter your email"
                            className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-sky-400"
                        />

                    </div>

                    {/* Password */}
                    <div>

                        <label className="block text-sm font-medium text-black mb-2">
                            Password
                        </label>

                        <input
                            type="password"
                            placeholder="Enter your password"
                            className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm outline-none focus:border-sky-400"
                        />

                    </div>

                    {/* Login Button */}
                    <button
                        type="submit"
                        className="w-full bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
                    >
                        Login
                    </button>

                </form>

            </div>

        </div>
    )
}

export default Login