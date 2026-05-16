import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "../pages/Login"
import Dashboard from "../pages/Dashboard"
import CreateUser from "../pages/CreateUser"
import Users from "../pages/Users"
import CustomerDashboard from "../pages/CustomerDashboard"
function AppRoutes() {
    return (
        <BrowserRouter>

            <Routes>

                <Route path="/" element={<Login />} />

                <Route path="/login" element={<Login />} />

                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/create-user" element={<CreateUser />} />
                <Route path="/users" element={<Users />} />
                <Route
                    path="/customer-dashboard"
                    element={<CustomerDashboard />}
                />
            </Routes>

        </BrowserRouter>
    )
}

export default AppRoutes