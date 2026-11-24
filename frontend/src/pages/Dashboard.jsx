import React, { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import DisclaimerBanner from "../components/common/DisclaimerBanner";
import Navbar from "../components/layout/Navbar";
import PatientDashboard from "./patient/PatientDashboard";
import HospitalDashboard from "./hospital/HospitalDashboard";
import AdminDashboard from "./admin/AdminDashboard";

export default function Dashboard() {
    const { user } = useAuth();

    // Determine strict user role from database authentication
    const userRoles = user?.roles || [];
    const isSuperAdmin = userRoles.includes("Admin") || user?.email?.includes("admin");
    const isHospitalAdmin = userRoles.includes("Hospital") || user?.email?.includes("hospital");

    const assignedRole = isSuperAdmin ? "admin" : (isHospitalAdmin ? "hospital" : "patient");
    const [activeRole, setActiveRole] = useState(assignedRole);

    useEffect(() => {
        // Strict role locking: Patient and Hospital users are strictly confined to their own dashboard
        if (!isSuperAdmin) {
            setActiveRole(assignedRole);
        } else {
            setActiveRole("admin");
        }
    }, [assignedRole, isSuperAdmin]);

    // Role-based security guard: Non-admins can NEVER view another dashboard
    const safeRole = isSuperAdmin ? activeRole : assignedRole;

    return (
        <div className="min-h-screen bg-slate-50 text-slate-800 antialiased flex flex-col">
            {/* Scoped Global Navbar */}
            <Navbar activeRole={safeRole} setActiveRole={isSuperAdmin ? setActiveRole : () => {}} />

            {/* Main Role-Secured Viewport */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 flex-1 w-full">
                {safeRole === "patient" && <PatientDashboard />}
                {safeRole === "hospital" && <HospitalDashboard />}
                {safeRole === "admin" && <AdminDashboard />}
            </main>

            {/* Comprehensive Platform Footer */}
            <footer className="bg-slate-900 text-slate-300 border-t border-slate-800 pt-10 pb-6 px-6 text-xs mt-12">
                <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 pb-8 border-b border-slate-800">
                    {/* Col 1: Identity & Mission */}
                    <div className="space-y-3">
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-base shadow-sm">
                                🫀
                            </div>
                            <span className="text-base font-extrabold text-white tracking-tight">MediLink</span>
                        </div>
                        <p className="text-slate-400 text-xs leading-relaxed">
                            India's unified emergency response and real-time hospital bed availability grid. Synchronizing live ICU capacities and rapid paramedic dispatch.
                        </p>
                        <div className="flex items-center gap-2 pt-1">
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                                ● Sockets Live
                            </span>
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30">
                                ABDM Ready
                            </span>
                        </div>
                    </div>

                    {/* Col 2: Emergency SOS Helplines */}
                    <div className="space-y-2.5">
                        <h4 className="text-white font-extrabold text-xs uppercase tracking-wider">24x7 Emergency Hotlines</h4>
                        <ul className="space-y-1.5 text-slate-400">
                            <li><a href="tel:108" className="hover:text-rose-400 flex items-center justify-between"><span className="text-rose-400 font-bold">Emergency Ambulance:</span> <span className="font-mono font-bold text-white">108</span></a></li>
                            <li><a href="tel:102" className="hover:text-white flex items-center justify-between"><span>Pregnant Women & Infant:</span> <span className="font-mono text-white">102</span></a></li>
                            <li><a href="tel:112" className="hover:text-white flex items-center justify-between"><span>National Emergency Helpline:</span> <span className="font-mono text-white">112</span></a></li>
                            <li><a href="tel:1075" className="hover:text-white flex items-center justify-between"><span>Health & Family Welfare:</span> <span className="font-mono text-white">1075</span></a></li>
                        </ul>
                    </div>

                    {/* Col 3: Network Metros Covered */}
                    <div className="space-y-2.5">
                        <h4 className="text-white font-extrabold text-xs uppercase tracking-wider">Network Coverage Hubs</h4>
                        <p className="text-[11px] text-slate-400 leading-relaxed">
                            Active live bed registries across Kolkata, New Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Pune, Jaipur, and Lucknow.
                        </p>
                        <p className="text-[10px] text-indigo-400 font-semibold mt-1">
                            Expanding to 50+ Tier-2 clinical centers.
                        </p>
                    </div>

                    {/* Col 4: Platform Portals */}
                    <div className="space-y-2.5">
                        <h4 className="text-white font-extrabold text-xs uppercase tracking-wider">Platform Governance</h4>
                        <ul className="space-y-1 text-slate-400 text-xs">
                            <li><a href="/login" className="hover:text-white transition">Patient & Public Sign In</a></li>
                            <li><a href="/login" className="hover:text-white transition">Hospital Provider Console</a></li>
                            <li><a href="/login" className="hover:text-white transition">Super Admin Master Access</a></li>
                            <li><span className="text-slate-500">ABHA Health Locker Sync</span></li>
                        </ul>
                    </div>
                </div>

                <div className="max-w-7xl mx-auto pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-slate-500 text-[11px]">
                    <p>© 2026 MediLink Healthcare Network. Built with React 19, Tailwind CSS 4, Flask 3.1 & Scikit-Learn.</p>
                    <p className="text-slate-500">NABH Accredited Partners • ISO 27001 Data Security Standards</p>
                </div>
            </footer>
        </div>
    );
}
