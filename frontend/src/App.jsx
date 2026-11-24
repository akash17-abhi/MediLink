import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";

import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import VerifyEmail from "./pages/auth/VerifyEmail";
import LoginOtp from "./pages/auth/LoginOtp";


function App() {

    return (

        <BrowserRouter>

            <AuthProvider>

                <Routes>


                    {/* =========================================
                        PUBLIC
                    ========================================= */}

                    <Route
                        path="/login"
                        element={<Login />}
                    />


                    <Route
                        path="/login-otp"
                        element={<LoginOtp />}
                    />


                    <Route
                        path="/register"
                        element={<Register />}
                    />


                    <Route
                        path="/verify-email"
                        element={<VerifyEmail />}
                    />


                    {/* =========================================
                        HOMEPAGE & DASHBOARDS
                    ========================================= */}

                    <Route
                        path="/"
                        element={<Dashboard />}
                    />

                    <Route
                        path="/dashboard"
                        element={<Dashboard />}
                    />


                    {/* =========================================
                        404
                    ========================================= */}

                    <Route
                        path="*"
                        element={
                            <Navigate
                                to="/dashboard"
                                replace
                            />
                        }
                    />

                </Routes>

            </AuthProvider>

        </BrowserRouter>
    );
}


export default App;