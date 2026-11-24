import { useState } from "react";

import {
    HeartPulse,
    Mail,
    Lock,
    Eye,
    EyeOff,
    Loader2,
} from "lucide-react";

import {
    Link,
    useNavigate,
    useLocation,
} from "react-router-dom";

import AuthLayout from "../layouts/AuthLayout";

import { useAuth } from "../context/AuthContext";


const Login = () => {

    const navigate = useNavigate();

    const location = useLocation();

    const {
        login,
    } = useAuth();


    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [showPassword, setShowPassword] =
        useState(false);

    const [error, setError] =
        useState("");

    const [loading, setLoading] =
        useState(false);


    // =========================================================
    // SUCCESS MESSAGE
    // =========================================================

    const verificationMessage =
        location.state?.message || "";


    // =========================================================
    // LOGIN
    // =========================================================

    const handleSubmit = async (event) => {

        event.preventDefault();

        setError("");


        // -----------------------------------------------------
        // VALIDATION
        // -----------------------------------------------------

        if (!email.trim()) {

            setError(
                "Please enter your email."
            );

            return;
        }


        if (!password) {

            setError(
                "Please enter your password."
            );

            return;
        }


        try {

            setLoading(true);


            // -------------------------------------------------
            // STEP 1
            // Email + Password
            // -------------------------------------------------

            const response =
                await login(
                    email.trim(),
                    password
                );


            // -------------------------------------------------
            // DEBUG
            // -------------------------------------------------

            console.log(
                "LOGIN RESPONSE:",
                response
            );


            // -------------------------------------------------
            // STEP 2
            // Backend requires Login OTP
            // -------------------------------------------------

            // Direct login (No OTP required)
            navigate(
                "/dashboard",
                {
                    replace: true,
                }
            );

            return;


            // -------------------------------------------------
            // UNEXPECTED RESPONSE
            // -------------------------------------------------

            console.error(
                "Unexpected login response:",
                response
            );


            setError(
                response?.message ||
                "Unexpected response from the server."
            );


        } catch (error) {

            // =================================================
            // IMPORTANT DEBUG INFORMATION
            // =================================================

            console.error(
                "Login error:",
                error
            );


            console.error(
                "Login HTTP status:",
                error.response?.status
            );


            console.error(
                "Login backend response:",
                error.response?.data
            );


            console.error(
                "Login backend message:",
                error.response?.data?.message
            );


            // -------------------------------------------------
            // Get actual backend message
            // -------------------------------------------------

            let message =
                error.response?.data?.message;


            // -------------------------------------------------
            // Handle different backend responses
            // -------------------------------------------------

            if (!message) {

                if (
                    error.response?.status === 401
                ) {

                    message =
                        "Login was rejected by the server. Please check your email, password, and email verification status.";

                } else {

                    message =
                        error.message ||
                        "Unable to login. Please try again.";
                }
            }


            setError(message);


        } finally {

            setLoading(false);

        }
    };


    return (
        <AuthLayout>

            {/* =================================================
                MOBILE LOGO
            ================================================= */}

            <div className="lg:hidden flex items-center justify-center gap-2 mb-8">

                <div className="w-10 h-10 bg-blue-600 text-white rounded-xl flex items-center justify-center">

                    <HeartPulse size={23} />

                </div>

                <div>

                    <h1 className="text-xl font-bold text-slate-900">
                        MediLink
                    </h1>

                    <p className="text-xs text-slate-500">
                        Smart Healthcare
                    </p>

                </div>

            </div>


            {/* =================================================
                LOGIN CARD
            ================================================= */}

            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8">


                {/* =================================================
                    HEADER
                ================================================= */}

                <div className="mb-8">

                    <h2 className="text-2xl font-bold text-slate-900">
                        Welcome back
                    </h2>

                    <p className="text-slate-500 mt-2">
                        Sign in to your MediLink account.
                    </p>

                </div>


                {/* =================================================
                    EMAIL VERIFICATION SUCCESS MESSAGE
                ================================================= */}

                {verificationMessage && (

                    <div className="mb-5 rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">

                        {verificationMessage}

                    </div>

                )}


                {/* =================================================
                    ERROR MESSAGE
                ================================================= */}

                {error && (

                    <div className="mb-5 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">

                        {error}

                    </div>

                )}


                {/* =================================================
                    LOGIN FORM
                ================================================= */}
                <form
                    onSubmit={handleSubmit}
                    className="space-y-5"
                >


                    {/* =================================================
                        EMAIL
                    ================================================= */}

                    <div>

                        <label className="block text-sm font-medium text-slate-700 mb-2">
                            Email address
                        </label>


                        <div className="relative">

                            <Mail
                                size={19}
                                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                            />


                            <input
                                type="email"
                                value={email}
                                onChange={(event) =>
                                    setEmail(
                                        event.target.value
                                    )
                                }
                                placeholder="you@example.com"
                                className="w-full rounded-lg border border-slate-300 bg-white py-3 pl-10 pr-4 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                                autoComplete="email"
                                disabled={loading}
                            />

                        </div>

                    </div>


                    {/* =================================================
                        PASSWORD
                    ================================================= */}

                    <div>

                        <div className="flex items-center justify-between mb-2">

                            <label className="block text-sm font-medium text-slate-700">
                                Password
                            </label>


                            <Link
                                to="/forgot-password"
                                className="text-sm font-medium text-blue-600 hover:text-blue-700"
                            >
                                Forgot password?
                            </Link>

                        </div>


                        <div className="relative">

                            <Lock
                                size={19}
                                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                            />


                            <input
                                type={
                                    showPassword
                                        ? "text"
                                        : "password"
                                }
                                value={password}
                                onChange={(event) =>
                                    setPassword(
                                        event.target.value
                                    )
                                }
                                placeholder="Enter your password"
                                className="w-full rounded-lg border border-slate-300 bg-white py-3 pl-10 pr-12 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                                autoComplete="current-password"
                                disabled={loading}
                            />


                            <button
                                type="button"
                                onClick={() =>
                                    setShowPassword(
                                        !showPassword
                                    )
                                }
                                disabled={loading}
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 disabled:opacity-50"
                            >

                                {showPassword ? (
                                    <EyeOff size={19} />
                                ) : (
                                    <Eye size={19} />
                                )}

                            </button>

                        </div>

                    </div>


                    {/* =================================================
                        LOGIN BUTTON
                    ================================================= */}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                    >

                        {loading ? (

                            <>

                                <Loader2
                                    size={18}
                                    className="animate-spin"
                                />

                                Authenticating...

                            </>

                        ) : (

                            "Sign In"

                        )}

                    </button>

                </form>


                {/* =================================================
                    REGISTER
                ================================================= */}

                <div className="mt-7 text-center text-sm text-slate-500">

                    Don't have an account?{" "}

                    <Link
                        to="/register"
                        className="font-semibold text-blue-600 hover:text-blue-700"
                    >
                        Create account
                    </Link>

                </div>

            </div>


            {/* =================================================
                FOOTER
            ================================================= */}

            <p className="text-center text-xs text-slate-400 mt-6">

                MediLink Healthcare Management System

            </p>

        </AuthLayout>
    );
};


export default Login;