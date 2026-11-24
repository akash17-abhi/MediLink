import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import {
  Mail,
  ShieldCheck,
  ArrowLeft,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";

import api from "../../services/api";

export default function VerifyEmail() {
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState(
    location.state?.email ||
      localStorage.getItem("verification_email") ||
      ""
  );

  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [resendCountdown, setResendCountdown] = useState(0);

  // Save email so refresh doesn't lose it
  useEffect(() => {
    if (email) {
      localStorage.setItem("verification_email", email);
    }
  }, [email]);

  // Resend countdown
  useEffect(() => {
    if (resendCountdown <= 0) {
      return;
    }

    const timer = setInterval(() => {
      setResendCountdown((previous) => previous - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [resendCountdown]);

  // =========================================================
  // VERIFY EMAIL
  // =========================================================

  const handleVerify = async (event) => {
    event.preventDefault();

    setError("");
    setMessage("");

    if (!email.trim()) {
      setError("Please enter your email address.");
      return;
    }

    if (!code.trim()) {
      setError("Please enter the verification code.");
      return;
    }

    if (!/^\d{6}$/.test(code)) {
      setError("Verification code must be 6 digits.");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post("/auth/verify-email", {
        email: email.trim(),
        code: code.trim(),
      });

      setMessage(
        response.data?.message ||
          "Email verified successfully."
      );

      localStorage.removeItem("verification_email");

      setTimeout(() => {
        navigate("/login", {
          replace: true,
          state: {
            message:
              "Email verified successfully. You can now sign in.",
          },
        });
      }, 1200);
    } catch (err) {
      const backendMessage =
        err.response?.data?.message ||
        "Unable to verify email. Please check your code.";

      setError(backendMessage);
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // RESEND VERIFICATION CODE
  // =========================================================

  const handleResend = async () => {
    setError("");
    setMessage("");

    if (!email.trim()) {
      setError("Please enter your email address.");
      return;
    }

    if (resendCountdown > 0) {
      return;
    }

    try {
      setResending(true);

      const response = await api.post(
        "/auth/resend-verification",
        {
          email: email.trim(),
        }
      );

      setMessage(
        response.data?.message ||
          "A new verification code has been sent."
      );

      setCode("");
      setResendCountdown(30);
    } catch (err) {
      const backendMessage =
        err.response?.data?.message ||
        "Unable to resend verification code.";

      setError(backendMessage);
    } finally {
      setResending(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex">

      {/* =====================================================
          LEFT SIDE
      ===================================================== */}

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
            Verify your
            <br />
            email address.
          </h2>

          <p className="text-lg text-blue-100 leading-8 max-w-lg">
            We sent a verification code to your email
            address. Enter the code to activate your
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
                Enter your 6-digit verification code
              </span>
            </div>

          </div>

        </div>
      </div>

      {/* =====================================================
          RIGHT SIDE
      ===================================================== */}

      <div className="w-full lg:w-1/2 flex items-center justify-center p-6">

        <div className="w-full max-w-md">

          {/* Mobile logo */}

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

          {/* Card */}

          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8">

            {/* Header */}

            <div className="text-center mb-8">

              <div className="mx-auto w-16 h-16 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mb-5">
                <Mail size={30} />
              </div>

              <h2 className="text-3xl font-bold text-slate-900">
                Verify your email
              </h2>

              <p className="text-slate-500 mt-3 leading-6">
                Enter the 6-digit code we sent to your
                email address.
              </p>

            </div>

            {/* Success */}

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

            {/* Error */}

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

            <form onSubmit={handleVerify}>

              {/* Email */}

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
                      setEmail(event.target.value)
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
                  Verification code
                </label>

                <input
                  type="text"
                  inputMode="numeric"
                  maxLength={6}
                  value={code}
                  onChange={(event) => {
                    const value =
                      event.target.value
                        .replace(/\D/g, "")
                        .slice(0, 6);

                    setCode(value);
                  }}
                  placeholder="000000"
                  className="w-full px-4 py-4 rounded-xl border border-slate-300 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition text-center text-2xl font-bold tracking-[0.5em]"
                  autoComplete="one-time-code"
                />

                <p className="text-xs text-slate-500 mt-2">
                  The verification code expires after 10
                  minutes.
                </p>

              </div>

              {/* Verify */}

              <button
                type="submit"
                disabled={loading || !email || code.length !== 6}
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
                    <ShieldCheck size={19} />
                    Verify Email
                  </>
                )}

              </button>

            </form>

            {/* Resend */}

            <div className="text-center mt-6">

              <p className="text-sm text-slate-500 mb-2">
                Didn't receive the code?
              </p>

              <button
                type="button"
                onClick={handleResend}
                disabled={
                  resending ||
                  resendCountdown > 0 ||
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
                  : resendCountdown > 0
                  ? `Resend code in ${resendCountdown}s`
                  : "Resend verification code"}

              </button>

            </div>

            {/* Login */}

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