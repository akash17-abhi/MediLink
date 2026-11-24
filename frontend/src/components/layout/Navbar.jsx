import React from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { HeartPulse, LogOut, Shield, Building2, User, PhoneCall } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export default function Navbar({ activeRole, setActiveRole }) {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const userRoles = user?.roles || [];
    const isSuperAdmin = userRoles.includes("Admin") || user?.email?.includes("admin");
    const isHospitalAdmin = userRoles.includes("Hospital") || user?.email?.includes("hospital");
    const isPatient = user && !isSuperAdmin && !isHospitalAdmin;

    const handleLogout = () => {
        logout();
        navigate("/");
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    return (
        <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between gap-4">
                {/* Brand & Scoped Portal Title */}
                <div className="flex items-center gap-4 sm:gap-6">
                    <Link to="/" className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold shadow-sm shadow-blue-500/20">
                            <HeartPulse size={22} />
                        </div>
                        <div>
                            <div className="flex items-center gap-2">
                                <span className="text-lg font-bold text-slate-900 tracking-tight">MediLink</span>
                            </div>
                            <p className="text-[11px] text-slate-500 hidden sm:block">Smart Healthcare & Emergency Network</p>
                        </div>
                    </Link>

                    {!user && (
                        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-bold">
                            <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                            <span>Emergency SOS Helpline: 108</span>
                        </div>
                    )}
                </div>

                {/* Right controls */}
                <div className="flex items-center gap-3">
                    {user ? (
                        <>
                            <div className="hidden sm:block text-right">
                                {isPatient ? (
                                    <button
                                        onClick={() => {
                                            window.dispatchEvent(new CustomEvent("open-patient-profile"));
                                            navigate("/dashboard");
                                        }}
                                        className="text-xs font-bold text-slate-800 hover:text-blue-600 transition cursor-pointer flex items-center gap-2 group"
                                        title="Click to view and edit Profile"
                                    >
                                        <div className="w-7 h-7 rounded-full bg-blue-100 text-blue-700 group-hover:bg-blue-600 group-hover:text-white transition flex items-center justify-center text-[10px] font-extrabold border border-blue-200">
                                            {(user.full_name || user.name || "PT").slice(0, 2).toUpperCase()}
                                        </div>
                                        <span className="group-hover:underline">{user.full_name || user.name || "MediLink User"}</span>
                                    </button>
                                ) : isHospitalAdmin ? (
                                    <p className="text-xs font-bold text-slate-800">
                                        {user.full_name || user.name || "Hospital Staff"}
                                    </p>
                                ) : (
                                    <p className="text-xs font-bold text-slate-800">
                                        {user.full_name || user.name || "Administrator"}
                                    </p>
                                )}
                            </div>

                            <button
                                onClick={handleLogout}
                                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition cursor-pointer"
                                title="Sign Out"
                            >
                                <LogOut size={14} />
                                <span className="hidden sm:inline">Logout</span>
                            </button>
                        </>
                    ) : (
                        <div className="flex items-center gap-2">
                            <Link
                                to="/login"
                                className="px-3.5 py-1.5 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition"
                            >
                                Sign In
                            </Link>
                            <Link
                                to="/register"
                                className="px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition shadow-xs"
                            >
                                Register
                            </Link>
                        </div>
                    )}
                </div>
            </div>

            {/* Mobile Scoped Banner */}
            <div className="flex md:hidden border-t border-slate-100 px-4 py-2 bg-slate-50 items-center justify-between text-xs font-semibold">
                {user ? (
                    <>
                        {isPatient ? (
                            <button
                                onClick={() => {
                                    window.dispatchEvent(new CustomEvent("open-patient-profile"));
                                    navigate("/dashboard");
                                }}
                                className="flex items-center gap-1.5 text-slate-800 font-bold hover:text-blue-600 cursor-pointer"
                                title="Click to view and edit Profile"
                            >
                                <User size={13} className="text-blue-600" />
                                <span>{user.full_name || user.name || "Patient"}</span>
                            </button>
                        ) : isHospitalAdmin ? (
                            <span className="flex items-center gap-1.5 text-slate-800 font-bold">
                                <Building2 size={13} className="text-indigo-600" />
                                <span>{user.full_name || user.name || "Hospital Staff"}</span>
                            </span>
                        ) : (
                            <span className="flex items-center gap-1.5 text-slate-800 font-bold">
                                <span>{user.full_name || user.name || "Administrator"}</span>
                            </span>
                        )}
                        <span className="text-[11px] text-slate-400 font-normal truncate max-w-[180px]">
                            {user.email}
                        </span>
                    </>
                ) : (
                    <div className="w-full flex items-center justify-between text-xs">
                        <span className="text-rose-600 font-bold flex items-center gap-1">
                            <PhoneCall size={12} /> Dial 108 for Emergency
                        </span>
                        <div className="flex items-center gap-2">
                            <Link to="/login" className="text-blue-600 font-bold">Login</Link>
                            <span className="text-slate-300">•</span>
                            <Link to="/register" className="text-slate-700 font-bold">Register</Link>
                        </div>
                    </div>
                )}
            </div>
        </header>
    );
}
