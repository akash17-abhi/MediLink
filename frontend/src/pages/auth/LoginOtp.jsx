import {
    useEffect,
    useState,
} from "react";

import {
    Mail,
    ShieldCheck,
    ArrowLeft,
    RefreshCw,
    CheckCircle2,
    AlertCircle,
} from "lucide-react";

import {
    Link,
    useLocation,
    useNavigate,
} from "react-router-dom";

import { useAuth } from "../../context/AuthContext";


export default function LoginOtp() {

    const navigate = useNavigate();

    const location = useLocation();


    const {
        verifyLoginOtp,
        resendLoginOtp,
    } = useAuth();


    // --------------------------------------------------
    // EMAIL
    // --------------------------------------------------

    const [email, setEmail] =
        useState(
            location.state?.email ||
            localStorage.getItem(
                "login_otp_email"
            ) ||
            ""
        );


    // --------------------------------------------------
    // OTP
    // --------------------------------------------------

    const [otp, setOtp] =
        useState("");


    // --------------------------------------------------
    // STATES
    // --------------------------------------------------

    const [loading, setLoading] =
        useState(false);

    const [resending, setResending] =
        useState(false);

    const [error, setError] =
        useState("");

    const [message, setMessage] =
        useState("");

    // Set initial 2-minute (120 seconds) countdown timer
    const [countdown, setCountdown] =
        useState(120);


    // --------------------------------------------------
    // TIME FORMATTER (MM:SS)
    // --------------------------------------------------

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    };


    // --------------------------------------------------
    // SAVE EMAIL
    // --------------------------------------------------

    useEffect(() => {

        if (email) {

            localStorage.setItem(
                "login_otp_email",
                email
            );
        }

    }, [email]);


    // --------------------------------------------------
    // COUNTDOWN
    // --------------------------------------------------

    useEffect(() => {

        if (countdown <= 0) {
            return;
        }


        const timer =
            setInterval(() => {

                setCountdown(
                    (previous) =>
                        previous - 1
                );

            }, 1000);


        return () =>
            clearInterval(timer);

    }, [countdown]);


    // --------------------------------------------------
    // VERIFY OTP
    // --------------------------------------------------

    const handleVerify = async (
        event
    ) => {

        event.preventDefault();

        setError("");
        setMessage("");


        if (!email.trim()) {

            setError(
                "Email address is required."
            );

            return;
        }


        if (!otp.trim()) {

            setError(
                "Please enter the OTP."
            );

            return;
        }


        if (!/^\d{6}$/.test(otp)) {

            setError(
                "OTP must be exactly 6 digits."
            );

            return;
        }


        try {

            setLoading(true);


            await verifyLoginOtp(
                email.trim(),
                otp.trim()
            );


            localStorage.removeItem(
                "login_otp_email"
            );


            setMessage(
                "OTP verified successfully. Redirecting..."
            );


            setTimeout(() => {

                navigate(
                    "/dashboard",
                    {
                        replace: true,
                    }
                );

            }, 700);


        } catch (error) {

            console.error(
                "OTP verification error:",
                error
            );


            const backendMessage =
                error.response?.data?.message ||
                error.message ||
                "Invalid or expired OTP.";


            setError(
                backendMessage
            );

        } finally {

            setLoading(false);
        }
    };


    // --------------------------------------------------
    // RESEND OTP
    // --------------------------------------------------

    const handleResend = async () => {

        setError("");
        setMessage("");


        if (!email.trim()) {

            setError(
                "Email address is required."
            );

            return;
        }


        if (countdown > 0) {
            return;
        }


        try {

            setResending(true);


            const response =
                await resendLoginOtp(
                    email.trim()
                );


            setMessage(
                response?.message ||
                "A new login OTP has been sent to your email."
            );


            setOtp("");

            // Reset timer back to 2 minutes (120s)
            setCountdown(120);


        } catch (error) {

            console.error(
                "Resend OTP error:",
                error
            );


            const backendMessage =
                error.response?.data?.message ||
                error.message ||
                "Unable to resend OTP.";


            setError(
                backendMessage
            );

        } finally {

            setResending(false);
        }
    };


    return (

        <div className="min-h-screen bg-slate-50 flex">


            {/* =================================================
                LEFT SIDE
            ================================================= */}

            <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-700 to-indigo-800 text-white p-16 flex-col justify-center">

                <div className="max-w-xl">

                    <div className="flex items-center gap-4 mb-10">

                        <div className="w-14 h-14 rounded-2xl bg-white/15 flex items-center justify-center">

                            <ShieldCheck size={32} />

                        </div>


                        <div>

                            <h1 className="text-3xl font-bold">
                                MediLink
                            </h1>

                            <p className="text-blue-100">
                                Smart Healthcare Management
                            </p>

                        </div>

                    </div>


                    <h2 className="text-5xl font-bold leading-tight mb-6">

                        Secure
                        <br />
                        sign in.

                    </h2>


                    <p className="text-lg text-blue-100 leading-8 max-w-lg">

                        We sent a one-time verification
                        code to your email. Enter the
                        code to securely access your
                        MediLink account.

                    </p>


                    <div className="mt-10 space-y-5">

                        <div className="flex items-center gap-4">

                            <div className="w-11 h-11 rounded-xl bg-white/10 flex items-center justify-center">

                                <Mail size={22} />

                            </div>

                            <span className="text-blue-50">
                                Check your email inbox
                            </span>

                        </div>


                        <div className="flex items-center gap-4">

                            <div className="w-11 h-11 rounded-xl bg-white/10 flex items-center justify-center">

                                <ShieldCheck size={22} />

                            </div>

                            <span className="text-blue-50">
                                Enter your 6-digit login code
                            </span>

                        </div>

                    </div>

                </div>

            </div>


            {/* =================================================
                RIGHT SIDE
            ================================================= */}

            <div className="w-full lg:w-1/2 flex items-center justify-center p-6">

                <div className="w-full max-w-md">


                    {/* MOBILE LOGO */}

                    <div className="lg:hidden text-center mb-8">

                        <div className="inline-flex w-14 h-14 rounded-2xl bg-blue-600 text-white items-center justify-center mb-3">

                            <ShieldCheck size={30} />

                        </div>


                        <h1 className="text-2xl font-bold text-slate-900">
                            MediLink
                        </h1>


                        <p className="text-slate-500">
                            Smart Healthcare Management
                        </p>

                    </div>


                    {/* CARD */}

                    <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8">


                        {/* HEADER */}

                        <div className="text-center mb-8">

                            <div className="mx-auto w-16 h-16 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mb-5">

                                <Mail size={30} />

                            </div>


                            <h2 className="text-3xl font-bold text-slate-900">
                                Check your email
                            </h2>


                            <p className="text-slate-500 mt-3 leading-6">

                                Enter the 6-digit login
                                verification code we sent
                                to your email.

                            </p>

                        </div>


                        {/* SUCCESS */}

                        {message && (

                            <div className="mb-5 rounded-xl border border-green-200 bg-green-50 px-4 py-3 flex items-start gap-3 text-green-700">

                                <CheckCircle2
                                    size={20}
                                    className="mt-0.5 flex-shrink-0"
                                />

                                <p className="text-sm">
                                    {message}
                                </p>

                            </div>

                        )}


                        {/* ERROR */}

                        {error && (

                            <div className="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 flex items-start gap-3 text-red-700">

                                <AlertCircle
                                    size={20}
                                    className="mt-0.5 flex-shrink-0"
                                />

                                <p className="text-sm">
                                    {error}
                                </p>

                            </div>

                        )}


                        <form
                            onSubmit={handleVerify}
                        >


                            {/* EMAIL */}

                            <div className="mb-5">

                                <label className="block text-sm font-semibold text-slate-700 mb-2">
                                    Email address
                                </label>


                                <div className="relative">

                                    <Mail
                                        size={19}
                                        className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
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
                                        className="w-full pl-11 pr-4 py-3.5 rounded-xl border border-slate-300 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                                        autoComplete="email"
                                    />

                                </div>

                            </div>


                            {/* OTP */}

                            <div className="mb-6">

                                <label className="block text-sm font-semibold text-slate-700 mb-2">
                                    Login verification code
                                </label>


                                <input
                                    type="text"
                                    inputMode="numeric"
                                    maxLength={6}
                                    value={otp}
                                    onChange={(event) => {

                                        const value =
                                            event.target.value
                                                .replace(
                                                    /\D/g,
                                                    ""
                                                )
                                                .slice(
                                                    0,
                                                    6
                                                );

                                        setOtp(value);

                                    }}
                                    placeholder="000000"
                                    className="w-full px-4 py-4 rounded-xl border border-slate-300 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition text-center text-2xl font-bold tracking-[0.5em]"
                                    autoComplete="one-time-code"
                                    autoFocus
                                />


                                <p className="text-xs text-slate-500 mt-2">
                                    Enter the 6-digit code sent to your email.
                                </p>

                            </div>


                            {/* VERIFY BUTTON */}

                            <button
                                type="submit"
                                disabled={
                                    loading ||
                                    !email ||
                                    otp.length !== 6
                                }
                                className="w-full py-3.5 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-semibold transition flex items-center justify-center gap-2"
                            >

                                {loading ? (

                                    <>
                                        <RefreshCw
                                            size={19}
                                            className="animate-spin"
                                        />

                                        Verifying...
                                    </>

                                ) : (

                                    <>
                                        <ShieldCheck
                                            size={19}
                                        />

                                        Verify & Sign In
                                    </>

                                )}

                            </button>

                        </form>


                        {/* RESEND */}

                        <div className="text-center mt-6">

                            <p className="text-sm text-slate-500 mb-2">
                                Didn't receive the code?
                            </p>


                            <button
                                type="button"
                                onClick={handleResend}
                                disabled={
                                    resending ||
                                    countdown > 0 ||
                                    !email
                                }
                                className="text-blue-600 hover:text-blue-700 disabled:text-slate-400 font-semibold text-sm inline-flex items-center gap-2"
                            >

                                <RefreshCw
                                    size={16}
                                    className={
                                        resending
                                            ? "animate-spin"
                                            : ""
                                    }
                                />


                                {resending
                                    ? "Sending..."
                                    : countdown > 0
                                    ? `Resend code in ${formatTime(countdown)}`
                                    : "Resend login code"}

                            </button>

                        </div>


                        {/* BACK TO LOGIN */}

                        <div className="border-t border-slate-200 mt-7 pt-6 text-center">

                            <Link
                                to="/login"
                                className="inline-flex items-center gap-2 text-sm text-slate-600 hover:text-blue-600 font-medium"
                            >

                                <ArrowLeft size={16} />

                                Back to login

                            </Link>

                        </div>

                    </div>


                    <p className="text-center text-sm text-slate-400 mt-6">

                        MediLink Healthcare Management System

                    </p>

                </div>

            </div>

        </div>
    );
}