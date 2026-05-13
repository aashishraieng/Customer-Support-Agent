import { useState } from "react"
import API from "../services/api"

function CreateUser() {

    const [formData, setFormData] = useState({
        name: "",
        email: "",
        phone: ""
    })

    const handleChange = (e) => {

        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        })
    }

    const handleSubmit = async (e) => {

        e.preventDefault()

        try {

            const response = await API.post(
                "/create-user",
                formData
            )

            console.log(response.data)

            alert("User Created Successfully")

        } catch (error) {

            console.log(error)

            alert("Failed to create user")
        }
    }

    return (
        <div className="min-h-screen bg-sky-50 p-8">

            <div className="max-w-xl mx-auto bg-white p-8 rounded-2xl shadow-sm border border-gray-200">

                <h1 className="text-2xl font-semibold text-black mb-6">
                    Create Bank User
                </h1>

                <form
                    className="space-y-5"
                    onSubmit={handleSubmit}
                >

                    {/* Name */}
                    <div>

                        <label className="block text-sm font-medium mb-2">
                            Full Name
                        </label>

                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            placeholder="Enter full name"
                            className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm"
                        />

                    </div>

                    {/* Email */}
                    <div>

                        <label className="block text-sm font-medium mb-2">
                            Email
                        </label>

                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="Enter email"
                            className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm"
                        />

                    </div>

                    {/* Phone */}
                    <div>

                        <label className="block text-sm font-medium mb-2">
                            Phone Number
                        </label>

                        <input
                            type="text"
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            placeholder="Enter phone number"
                            className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm"
                        />

                    </div>

                    {/* Button */}
                    <button
                        type="submit"
                        className="w-full bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
                    >
                        Create User
                    </button>

                </form>

            </div>

        </div>
    )
}

export default CreateUser