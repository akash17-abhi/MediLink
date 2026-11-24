import { useState } from "react";

import {
    User,
    Mail,
    Lock,
    Eye,
    EyeOff,
    Loader2,
    HeartPulse,
} from "lucide-react";

import {
    Link,
    useNavigate,
} from "react-router-dom";

import AuthLayout from "../layouts/AuthLayout";

import { useAuth } from "../context/AuthContext";

const Register = () => {

    const navigate = useNavigate();

    const {
        register,
    } = useAuth();

    const [fullName, setFullName] =
        useState("");

    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [confirmPassword, setConfirmPassword] =
        useState("");

    const [showPassword, setShowPassword] =
        useState(false);

    const [showConfirmPassword, setShowConfirmPassword] =
        useState(false);

    const [error, setError] =
        useState("");

    const [success, setSuccess] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    const handleSubmit = async (event) => {

        event.preventDefault();

        setError("");
        setSuccess("");

        if (!fullName.trim()) {

            setError(
                "Please enter your full name."
            );

            return;
        }

        if (!email.trim()) {

            setError(
                "Please enter your email."
            );

            return;
        }

        if (!password) {

            setError(
                "Please enter a password."
            );

            return;
        }

        if (password.length < 6) {

            setError(
                "Password must contain at least 6 characters."
            );

            return;
        }

        if (password !== confirmPassword) {

            setError(
                "Passwords do not match."
            );

            return;
        }

        try {

            setLoading(true);

            await register(
                fullName.trim(),
                email.trim(),
                password
            );

            setSuccess(
                "Registration successful! Redirecting to login..."
            );

            setTimeout(() => {
                navigate("/login");
            }, 1200);

        } catch (error) {

            console.error(error);

            const message =
                error.response?.data?.message ||
                error.response?.data?.error ||
                "Registration failed. Please try again.";

            setError(message);

        } finally {

            setLoading(false);

        }
    };

    return (
        <AuthLayout>

            {/* MOBILE LOGO */}

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

            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8">

                <div className="mb-7">

                    <h2 className="text-2xl font-bold text-slate-900">
                        Create your account
                    </h2>

                    <p className="text-slate-500 mt-2">
                        Join MediLink and manage healthcare smarter.
                    </p>

                </div>

                {error && (

                    <div className="mb-5 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">

                        {error}

                    </div>

                )}

                {success && (

                    <div className="mb-5 rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">

                        {success}

                    </div>

                )}

                <form
                    onSubmit={handleSubmit}
                    className="space-y-4"
                >

                    {/* FULL NAME */}

                    <div>

                        <label className="block text-sm font-medium text-slate-700 mb-2">
                            Full name
                        </label>

                        <div className="relative">

                            <User
                                size={19}
                                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                            />

                            <input
                                type="text"
                                value={fullName}
                                onChange={(e) =>
                                    setFullName(
                                        e.target.value
                                    )
                                }
                                placeholder="Enter your full name"
                                className="w-full rounded-lg border border-slate-300 py-3 pl-10 pr-4 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                            />

                        </div>

                    </div>

                    {/* EMAIL */}

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
                                onChange={(e) =>
                                    setEmail(
                                        e.target.value
                                    )
                                }
                                placeholder="you@example.com"
                                className="w-full rounded-lg border border-slate-300 py-3 pl-10 pr-4 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                            />

                        </div>

                    </div>

                    {/* PASSWORD */}

                    <div>

                        <label className="block text-sm font-medium text-slate-700 mb-2">
                            Password
                        </label>

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
                                onChange={(e) =>
                                    setPassword(
                                        e.target.value
                                    )
                                }
                                placeholder="Create a password"
                                className="w-full rounded-lg border border-slate-300 py-3 pl-10 pr-12 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                            />

                            <button
                                type="button"
                                onClick={() =>
                                    setShowPassword(
                                        !showPassword
                                    )
                                }
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400"
                            >

                                {showPassword ? (
                                    <EyeOff size={19} />
                                ) : (
                                    <Eye size={19} />
                                )}

                            </button>

                        </div>

                    </div>

                    {/* CONFIRM PASSWORD */}

                    <div>

                        <label className="block text-sm font-medium text-slate-700 mb-2">
                            Confirm password
                        </label>

                        <div className="relative">

                            <Lock
                                size={19}
                                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                            />

                            <input
                                type={
                                    showConfirmPassword
                                        ? "text"
                                        : "password"
                                }
                                value={confirmPassword}
                                onChange={(e) =>
                                    setConfirmPassword(
                                        e.target.value
                                    )
                                }
                                placeholder="Confirm your password"
                                className="w-full rounded-lg border border-slate-300 py-3 pl-10 pr-12 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                            />

                            <button
                                type="button"
                                onClick={() =>
                                    setShowConfirmPassword(
                                        !showConfirmPassword
                                    )
                                }
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400"
                            >

                                {showConfirmPassword ? (
                                    <EyeOff size={19} />
                                ) : (
                                    <Eye size={19} />
                                )}

                            </button>

                        </div>

                    </div>

                    {/* REGISTER */}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-3 mt-2 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-60"
                    >

                        {loading ? (

                            <>
                                <Loader2
                                    size={18}
                                    className="animate-spin"
                                />

                                Creating account...
                            </>

                        ) : (

                            "Create account"

                        )}

                    </button>

                </form>

                <div className="mt-6 text-center text-sm text-slate-500">

                    Already have an account?{" "}

                    <Link
                        to="/login"
                        className="font-semibold text-blue-600 hover:text-blue-700"
                    >
                        Sign in
                    </Link>

                </div>

            </div>

        </AuthLayout>
    );
};

export default Register;