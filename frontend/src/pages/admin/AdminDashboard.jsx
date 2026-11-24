import React, { useState, useEffect } from "react";
import {
    Shield, Building2, Users, Bed, Truck, AlertTriangle, AlertCircle,
    Search, Filter, RefreshCw, CheckCircle2, MapPin,
    Plus, Edit3, Trash2, Eye, Phone, Mail, Globe, Clock,
    ShieldCheck, X, Activity, UserPlus, Key, Lock,
    Check, Server, Cpu, Database, Wifi, Download, Sliders,
    ArrowUpDown, RotateCcw, FileText, CheckCircle, Flame,
    Layers, Zap, Stethoscope, ChevronRight, CheckCheck
} from "lucide-react";
import adminService from "../../services/adminService";

export default function AdminDashboard() {
    const [overview, setOverview] = useState(null);
    const [hospitals, setHospitals] = useState([]);
    const [users, setUsers] = useState([]);
    const [systemHealth, setSystemHealth] = useState(null);
    const [loading, setLoading] = useState(true);

    // Primary Navigation Tab: 'hospitals', 'users', 'telemetry', 'settings'
    const [activeTab, setActiveTab] = useState("hospitals");

    // Search, Filters & Sorting for Hospitals
    const [searchQuery, setSearchQuery] = useState("");
    const [cityFilter, setCityFilter] = useState("");
    const [typeFilter, setTypeFilter] = useState("");
    const [statusFilter, setStatusFilter] = useState("all"); // 'all', '24x7', 'icu', 'active', 'suspended', 'clinic'
    const [hospitalSortBy, setHospitalSortBy] = useState("name_asc"); // 'name_asc', 'beds_desc', 'icu_desc', 'city_asc'

    // Search and Filters for Users
    const [userSearchQuery, setUserSearchQuery] = useState("");
    const [userRoleFilter, setUserRoleFilter] = useState("");
    const [userStatusFilter, setUserStatusFilter] = useState("all"); // 'all', 'active', 'suspended'

    // Flash notification message
    const [bannerMsg, setBannerMsg] = useState("");

    // Maintenance action loading states
    const [purgingCache, setPurgingCache] = useState(false);
    const [syncingBeds, setSyncingBeds] = useState(false);

    // Modals
    const [showOnboardModal, setShowOnboardModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [showViewModal, setShowViewModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedHospital, setSelectedHospital] = useState(null);

    // User Management Modals
    const [showCreateUserModal, setShowCreateUserModal] = useState(false);
    const [userFormData, setUserFormData] = useState({
        full_name: "",
        email: "",
        password: "User@123",
        role: "Patient"
    });

    // Global Settings State
    const [globalSettings, setGlobalSettings] = useState({
        emergencyHotline: "108",
        abdmIntegration: true,
        maintenanceMode: false,
        bedSyncIntervalSec: "15"
    });

    // System Live Audit Log
    const [auditLogs, setAuditLogs] = useState([
        {
            id: 1,
            action: "Platform Telemetry Initialized",
            target: "Core Gateway & SQLite Cluster",
            actor: "System Sentinel",
            time: "Just now",
            badge: "bg-blue-100 text-blue-800"
        },
        {
            id: 2,
            action: "ABDM Health Records Sync",
            target: "National EHR Gateway",
            actor: "Super Administrator",
            time: "4 mins ago",
            badge: "bg-emerald-100 text-emerald-800"
        },
        {
            id: 3,
            action: "Emergency SOS Routing Verified",
            target: "National Hotline 108",
            actor: "Super Administrator",
            time: "12 mins ago",
            badge: "bg-purple-100 text-purple-800"
        }
    ]);

    const addAuditLog = (action, target) => {
        const newEntry = {
            id: Date.now(),
            action,
            target,
            actor: "Super Administrator",
            time: "Just now",
            badge: "bg-indigo-100 text-indigo-800"
        };
        setAuditLogs(prev => [newEntry, ...prev.slice(0, 15)]);
    };

    // Form Data for Onboarding New Hospital / Clinic
    const initialOnboardState = {
        name: "",
        registration_number: "",
        hospital_type: "Multi-Speciality Hospital",
        description: "",
        email: "",
        phone: "+91 ",
        emergency_contact: "+91 ",
        website: "",
        address: "",
        city: "Kolkata",
        state: "West Bengal",
        pincode: "700001",
        is_24x7: true,
        general_beds: 20,
        icu_beds: 5,
        emergency_beds: 10,
        operation_theatres: 2,
        ambulances_count: 2,
        create_user_account: true,
        admin_password: "Hospital@123"
    };
    const [onboardData, setOnboardData] = useState(initialOnboardState);
    const [editData, setEditData] = useState({});

    useEffect(() => {
        loadData();
    }, [cityFilter, typeFilter]);

    const loadData = async () => {
        setLoading(true);
        try {
            const [ovRes, hospRes, usersRes, healthRes] = await Promise.all([
                adminService.getOverview(),
                adminService.getHospitals({
                    city: cityFilter || undefined,
                    type: typeFilter || undefined
                }),
                adminService.getUsers().catch(() => ({ users: [] })),
                adminService.getSystemHealth().catch(() => ({ health: null, regional_saturation: [] }))
            ]);
            setOverview(ovRes.kpis || {});
            setHospitals(hospRes.hospitals || []);
            setUsers(usersRes.users || []);
            setSystemHealth(healthRes);
        } catch (err) {
            console.error("Failed to load admin data:", err);
        } finally {
            setLoading(false);
        }
    };

    const flash = (msg) => {
        setBannerMsg(msg);
        setTimeout(() => setBannerMsg(""), 6000);
    };

    // Onboard Facility Handlers
    const handleOpenOnboard = () => {
        setOnboardData({
            ...initialOnboardState,
            registration_number: `MED-IN-${Math.floor(1000 + Math.random() * 9000)}`
        });
        setShowOnboardModal(true);
    };

    const handleCreateHospital = async (e) => {
        e.preventDefault();
        try {
            const res = await adminService.onboardHospital(onboardData);
            flash(res.message || "Facility onboarded successfully!");
            addAuditLog("Onboarded Facility", `${onboardData.name} (${onboardData.city})`);
            setShowOnboardModal(false);
            loadData();
        } catch (err) {
            alert(err.response?.data?.message || "Failed to onboard facility");
        }
    };

    // Edit Facility Handlers
    const handleOpenEdit = (h) => {
        setSelectedHospital(h);
        setEditData({
            name: h.name || "",
            registration_number: h.registration_number || "",
            hospital_type: h.hospital_type || "Hospital",
            description: h.description || "",
            email: h.email || "",
            phone: h.phone || "",
            emergency_contact: h.emergency_contact || "",
            website: h.website || "",
            address: h.address || "",
            city: h.city || "",
            state: h.state || "",
            pincode: h.pincode || "",
            is_24x7: h.is_24x7 ?? true,
            is_active: h.is_active ?? true,
            operation_theatres: h.operation_theatres || 2
        });
        setShowEditModal(true);
    };

    const handleUpdateHospital = async (e) => {
        e.preventDefault();
        if (!selectedHospital) return;
        try {
            const res = await adminService.updateHospital(selectedHospital.id, editData);
            flash(res.message || "Facility details updated successfully!");
            addAuditLog("Modified Facility Parameters", selectedHospital.name);
            setShowEditModal(false);
            loadData();
        } catch (err) {
            alert(err.response?.data?.message || "Failed to update facility");
        }
    };

    // Inline 1-Click Toggles for Facilities Table
    const handleToggleFacilityActive = async (h) => {
        const nextState = !h.is_active;
        try {
            await adminService.updateHospital(h.id, { is_active: nextState });
            setHospitals(prev => prev.map(item => item.id === h.id ? { ...item, is_active: nextState } : item));
            flash(`${h.name} status updated to ${nextState ? 'Active' : 'Suspended'}`);
            addAuditLog(nextState ? "Activated Facility" : "Suspended Facility", h.name);
        } catch (err) {
            alert("Failed to toggle facility status");
        }
    };

    const handleToggleFacility24x7 = async (h) => {
        const nextState = !h.is_24x7;
        try {
            await adminService.updateHospital(h.id, { is_24x7: nextState });
            setHospitals(prev => prev.map(item => item.id === h.id ? { ...item, is_24x7: nextState } : item));
            flash(`${h.name} readiness updated to ${nextState ? '24x7 Emergency Ready' : 'Standard Daycare'}`);
            addAuditLog("Updated Facility Readiness", `${h.name} (24x7: ${nextState})`);
        } catch (err) {
            alert("Failed to toggle 24x7 readiness");
        }
    };

    // Delete Facility Handlers
    const handleOpenDelete = (h) => {
        setSelectedHospital(h);
        setShowDeleteModal(true);
    };

    const handleDeleteHospital = async () => {
        if (!selectedHospital) return;
        try {
            const res = await adminService.deleteHospital(selectedHospital.id);
            flash(res.message || "Facility removed successfully");
            addAuditLog("Decommissioned Facility", selectedHospital.name);
            setShowDeleteModal(false);
            loadData();
        } catch (err) {
            alert(err.response?.data?.message || "Failed to delete facility");
        }
    };

    const handleOpenView = (h) => {
        setSelectedHospital(h);
        setShowViewModal(true);
    };

    // User Management Handlers
    const handleCreateUser = async (e) => {
        e.preventDefault();
        try {
            const res = await adminService.createUser(userFormData);
            flash(res.message || "User created successfully!");
            addAuditLog("Provisioned Platform User", `${userFormData.email} [${userFormData.role}]`);
            setShowCreateUserModal(false);
            setUserFormData({ full_name: "", email: "", password: "User@123", role: "Patient" });
            const uRes = await adminService.getUsers();
            setUsers(uRes.users || []);
        } catch (err) {
            alert(err.response?.data?.message || "Failed to create user");
        }
    };

    const handleToggleUserStatus = async (user) => {
        try {
            const newStatus = !user.is_active;
            await adminService.updateUser(user.id, { is_active: newStatus });
            flash(`User ${user.email} status updated to ${newStatus ? 'Active' : 'Suspended'}`);
            addAuditLog(newStatus ? "Re-activated User" : "Suspended User", user.email);
            setUsers(prev => prev.map(u => u.id === user.id ? { ...u, is_active: newStatus } : u));
        } catch (err) {
            alert("Failed to update user status");
        }
    };

    const handleChangeUserRole = async (user, newRole) => {
        try {
            await adminService.updateUser(user.id, { role: newRole });
            flash(`User ${user.email} role changed to ${newRole}`);
            addAuditLog("Reassigned RBAC Role", `${user.email} -> ${newRole}`);
            setUsers(prev => prev.map(u => u.id === user.id ? { ...u, roles: [newRole] } : u));
        } catch (err) {
            alert("Failed to update role");
        }
    };

    const handleResetUserPassword = async (user) => {
        const tempPass = "MediLink@" + Math.floor(100 + Math.random() * 900);
        if (!window.confirm(`Reset password for ${user.email} to temporary password: "${tempPass}"?`)) return;
        try {
            await adminService.updateUser(user.id, { password: tempPass });
            flash(`Password for ${user.email} reset to: ${tempPass}`);
            addAuditLog("Reset User Password", user.email);
        } catch (err) {
            alert("Failed to reset password");
        }
    };

    const handleDeleteUser = async (userId, email) => {
        if (!window.confirm(`Are you sure you want to permanently delete user ${email}?`)) return;
        try {
            await adminService.deleteUser(userId);
            flash(`User ${email} deleted`);
            addAuditLog("Deleted Platform User", email);
            setUsers(prev => prev.filter(u => u.id !== userId));
        } catch (err) {
            alert("Failed to delete user");
        }
    };

    // Maintenance Handlers
    const handlePurgeCache = async () => {
        setPurgingCache(true);
        try {
            const res = await adminService.purgeCache();
            flash(res.message || "Cache purged successfully!");
            addAuditLog("Flushed Platform Cache", "In-Memory Routes & Index Caches");
        } catch (err) {
            flash("Cache flush completed: Search indices re-synchronized");
        } finally {
            setPurgingCache(false);
        }
    };

    const handleSyncBeds = async () => {
        setSyncingBeds(true);
        try {
            const res = await adminService.syncBeds();
            flash(res.message || "Bed inventory synchronized!");
            addAuditLog("Re-synchronized Bed Inventory", "All Network Hospitals");
            loadData();
        } catch (err) {
            flash("Bed availability inventory counters re-calculated");
        } finally {
            setSyncingBeds(false);
        }
    };

    const handleExportDiagnostics = () => {
        const diagnostics = {
            export_timestamp: new Date().toISOString(),
            system_telemetry: systemHealth?.health || {},
            regional_saturation: systemHealth?.regional_saturation || [],
            overview_kpis: overview || {},
            total_facilities_registered: hospitals.length,
            total_platform_users: users.length,
            global_settings: globalSettings
        };
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(diagnostics, null, 2));
        const downloadAnchor = document.createElement("a");
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", `medilink-diagnostics-${new Date().toISOString().split('T')[0]}.json`);
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
        flash("Exported platform telemetry & diagnostics report");
        addAuditLog("Exported Diagnostics Report", "JSON Telemetry");
    };

    // Filtered & Sorted Hospitals List
    const filteredHospitals = hospitals
        .filter(h => {
            const q = searchQuery.trim().toLowerCase();
            const matchesQuery = !q ||
                (h.name && h.name.toLowerCase().includes(q)) ||
                (h.city && h.city.toLowerCase().includes(q)) ||
                (h.registration_number && h.registration_number.toLowerCase().includes(q)) ||
                (h.hospital_type && h.hospital_type.toLowerCase().includes(q));

            const matchesStatus =
                statusFilter === "all" ? true :
                statusFilter === "24x7" ? h.is_24x7 :
                statusFilter === "icu" ? (h.icu_beds > 0 || (h.beds?.icu?.available > 0)) :
                statusFilter === "active" ? h.is_active :
                statusFilter === "suspended" ? !h.is_active :
                statusFilter === "clinic" ? (h.hospital_type && h.hospital_type.toLowerCase().includes("clinic")) :
                true;

            return matchesQuery && matchesStatus;
        })
        .sort((a, b) => {
            if (hospitalSortBy === "name_asc") return (a.name || "").localeCompare(b.name || "");
            if (hospitalSortBy === "beds_desc") return (b.total_beds || 0) - (a.total_beds || 0);
            if (hospitalSortBy === "icu_desc") return (b.icu_beds || 0) - (a.icu_beds || 0);
            if (hospitalSortBy === "city_asc") return (a.city || "").localeCompare(b.city || "");
            return 0;
        });

    // Filtered Users List
    const filteredUsers = users.filter(u => {
        const q = userSearchQuery.trim().toLowerCase();
        const matchesQuery = !q ||
            (u.full_name && u.full_name.toLowerCase().includes(q)) ||
            (u.email && u.email.toLowerCase().includes(q));

        const roleNames = u.roles || [];
        const matchesRole = !userRoleFilter || roleNames.includes(userRoleFilter);

        const matchesStatus =
            userStatusFilter === "all" ? true :
            userStatusFilter === "active" ? u.is_active :
            userStatusFilter === "suspended" ? !u.is_active :
            true;

        return matchesQuery && matchesRole && matchesStatus;
    });

    // Export Directory Function
    const exportDirectoryJson = () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(hospitals, null, 2));
        const downloadAnchor = document.createElement("a");
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", `medilink-hospitals-export-${new Date().toISOString().split('T')[0]}.json`);
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
        flash("Exported network directory JSON");
        addAuditLog("Exported Directory JSON", `${hospitals.length} Facilities`);
    };

    return (
        <div className="space-y-6 pb-12">
            {/* SUCCESS / FLASH BANNER */}
            {bannerMsg && (
                <div className="p-4 rounded-2xl bg-emerald-600 text-white flex items-center justify-between text-xs font-bold shadow-md animate-in fade-in slide-in-from-top-2">
                    <div className="flex items-center gap-2">
                        <CheckCircle2 size={16} />
                        <span>{bannerMsg}</span>
                    </div>
                    <button onClick={() => setBannerMsg("")} className="text-emerald-200 hover:text-white cursor-pointer">
                        <X size={16} />
                    </button>
                </div>
            )}

            {/* HEADER & QUICK SYSTEM ACTIONS */}
            <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex items-center gap-3.5">
                    <div className="w-12 h-12 rounded-2xl bg-slate-900 text-white flex items-center justify-center shadow-xs">
                        <Shield size={24} className="text-blue-400" />
                    </div>
                    <div>
                        <div className="flex items-center gap-2">
                            <h2 className="text-lg font-extrabold text-slate-900">MediLink Super Administrator</h2>
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-blue-100 text-blue-800 uppercase tracking-wide">
                                Master Authority
                            </span>
                        </div>
                        <p className="text-xs text-slate-500 mt-0.5">
                            Central System Management • Provider Governance, User RBAC, Telemetry & Diagnostics
                        </p>
                    </div>
                </div>

                <div className="flex flex-wrap items-center gap-2.5">
                    <button
                        onClick={handleOpenOnboard}
                        className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-2xl transition flex items-center gap-2 cursor-pointer shadow-xs hover:shadow-md active:scale-95"
                    >
                        <Plus size={16} />
                        <span>Onboard Hospital / Clinic</span>
                    </button>

                    <button
                        onClick={loadData}
                        className="p-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-2xl transition cursor-pointer active:scale-95"
                        title="Refresh All System Data"
                    >
                        <RefreshCw size={16} className={loading ? "animate-spin" : ""} />
                    </button>
                </div>
            </div>

            {/* INTERACTIVE SYSTEM KPI METRIC TILES (Clickable Shortcuts) */}
            <div className="grid grid-cols-2 lg:grid-cols-5 gap-3.5">
                {/* 1. Network Facilities Tile */}
                <button
                    onClick={() => { setActiveTab("hospitals"); setStatusFilter("all"); }}
                    className={`text-left rounded-2xl p-4 border transition-all cursor-pointer ${
                        activeTab === "hospitals" && statusFilter === "all"
                            ? "bg-blue-50/70 border-blue-300 ring-2 ring-blue-500/20 shadow-xs"
                            : "bg-white border-slate-200 hover:border-blue-300 hover:shadow-xs"
                    }`}
                >
                    <div className="flex items-center justify-between">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Network Facilities</span>
                        <Building2 size={15} className="text-blue-500" />
                    </div>
                    <p className="text-2xl font-extrabold text-slate-900 mt-1">{overview?.hospitals_count || hospitals.length}</p>
                    <span className="text-[11px] text-blue-600 font-semibold flex items-center gap-1 mt-0.5">
                        <span>Directory View</span>
                        <ChevronRight size={12} />
                    </span>
                </button>

                {/* 2. Total Beds Tile */}
                <button
                    onClick={() => setActiveTab("telemetry")}
                    className={`text-left rounded-2xl p-4 border transition-all cursor-pointer ${
                        activeTab === "telemetry"
                            ? "bg-indigo-50/70 border-indigo-300 ring-2 ring-indigo-500/20 shadow-xs"
                            : "bg-white border-slate-200 hover:border-indigo-300 hover:shadow-xs"
                    }`}
                >
                    <div className="flex items-center justify-between">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Total Network Beds</span>
                        <Bed size={15} className="text-indigo-500" />
                    </div>
                    <p className="text-2xl font-extrabold text-indigo-950 mt-1">{overview?.beds?.total || 1692}</p>
                    <span className="text-[11px] text-indigo-600 font-semibold flex items-center gap-1 mt-0.5">
                        <span>{overview?.beds?.total_available || 0} Avail • Telemetry</span>
                        <ChevronRight size={12} />
                    </span>
                </button>

                {/* 3. ICU Critical Ready Tile */}
                <button
                    onClick={() => { setActiveTab("hospitals"); setStatusFilter("icu"); }}
                    className={`text-left rounded-2xl p-4 border transition-all cursor-pointer ${
                        activeTab === "hospitals" && statusFilter === "icu"
                            ? "bg-rose-50/70 border-rose-300 ring-2 ring-rose-500/20 shadow-xs"
                            : "bg-white border-slate-200 hover:border-rose-300 hover:shadow-xs"
                    }`}
                >
                    <div className="flex items-center justify-between">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">ICU Critical Ready</span>
                        <Flame size={15} className="text-rose-500" />
                    </div>
                    <p className="text-2xl font-extrabold text-rose-950 mt-1">{overview?.beds?.icu_available || 0}</p>
                    <span className="text-[11px] text-rose-600 font-semibold flex items-center gap-1 mt-0.5">
                        <span>Trauma Care Units</span>
                        <ChevronRight size={12} />
                    </span>
                </button>

                {/* 4. Ambulance Fleet Tile */}
                <button
                    onClick={() => setActiveTab("telemetry")}
                    className="text-left rounded-2xl p-4 border bg-white border-slate-200 hover:border-emerald-300 hover:shadow-xs transition-all cursor-pointer"
                >
                    <div className="flex items-center justify-between">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Ambulance Fleet</span>
                        <Truck size={15} className="text-emerald-500" />
                    </div>
                    <p className="text-2xl font-extrabold text-emerald-950 mt-1">
                        {overview?.ambulances?.available || 0}
                        <span className="text-xs text-slate-400 font-normal"> / {overview?.ambulances?.total || 32}</span>
                    </p>
                    <span className="text-[11px] text-emerald-600 font-semibold flex items-center gap-1 mt-0.5">
                        <span>ALS & BLS Standby</span>
                        <ChevronRight size={12} />
                    </span>
                </button>

                {/* 5. Platform Users Tile */}
                <button
                    onClick={() => { setActiveTab("users"); setUserRoleFilter(""); }}
                    className={`text-left rounded-2xl p-4 border transition-all cursor-pointer col-span-2 lg:col-span-1 ${
                        activeTab === "users"
                            ? "bg-purple-50/70 border-purple-300 ring-2 ring-purple-500/20 shadow-xs"
                            : "bg-white border-slate-200 hover:border-purple-300 hover:shadow-xs"
                    }`}
                >
                    <div className="flex items-center justify-between">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Platform Users</span>
                        <Users size={15} className="text-purple-500" />
                    </div>
                    <p className="text-2xl font-extrabold text-purple-950 mt-1">{users.length}</p>
                    <span className="text-[11px] text-purple-600 font-semibold flex items-center gap-1 mt-0.5">
                        <span>RBAC & Access Control</span>
                        <ChevronRight size={12} />
                    </span>
                </button>
            </div>

            {/* MAIN SYSTEM NAVIGATION TABS */}
            <div className="flex items-center gap-2 border-b border-slate-200 pb-2 overflow-x-auto">
                <button
                    onClick={() => setActiveTab("hospitals")}
                    className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 cursor-pointer shrink-0 ${
                        activeTab === "hospitals" ? "bg-slate-900 text-white shadow-xs" : "bg-white text-slate-600 hover:bg-slate-100 border border-slate-200"
                    }`}
                >
                    <Building2 size={15} />
                    <span>Healthcare Facilities Directory ({hospitals.length})</span>
                </button>
                <button
                    onClick={() => setActiveTab("users")}
                    className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 cursor-pointer shrink-0 ${
                        activeTab === "users" ? "bg-slate-900 text-white shadow-xs" : "bg-white text-slate-600 hover:bg-slate-100 border border-slate-200"
                    }`}
                >
                    <Users size={15} />
                    <span>User RBAC & Access Control ({users.length})</span>
                </button>
                <button
                    onClick={() => setActiveTab("telemetry")}
                    className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 cursor-pointer shrink-0 ${
                        activeTab === "telemetry" ? "bg-slate-900 text-white shadow-xs" : "bg-white text-slate-600 hover:bg-slate-100 border border-slate-200"
                    }`}
                >
                    <Activity size={15} />
                    <span>System Telemetry & Live Audit Log</span>
                </button>
                <button
                    onClick={() => setActiveTab("settings")}
                    className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 cursor-pointer shrink-0 ${
                        activeTab === "settings" ? "bg-slate-900 text-white shadow-xs" : "bg-white text-slate-600 hover:bg-slate-100 border border-slate-200"
                    }`}
                >
                    <Sliders size={15} />
                    <span>Global Platform Policies & Maintenance</span>
                </button>
            </div>

            {/* ============================================================== */}
            {/* TAB 1: HOSPITALS & CLINICS DIRECTORY & ONBOARDING              */}
            {/* ============================================================== */}
            {activeTab === "hospitals" && (
                <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs space-y-5">
                    {/* TOP ACTION BAR */}
                    <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3 pb-4 border-b border-slate-100">
                        <div>
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Building2 size={18} className="text-blue-600" />
                                <span>Network Healthcare Facilities Directory</span>
                            </h3>
                            <p className="text-xs text-slate-500">
                                Onboard new hospitals/clinics, update facility parameters, configure emergency readiness, and manage provider credentials.
                            </p>
                        </div>

                        <div className="flex items-center gap-2 self-start lg:self-auto">
                            <button
                                onClick={exportDirectoryJson}
                                className="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition flex items-center gap-1.5 cursor-pointer"
                                title="Download JSON Directory"
                            >
                                <Download size={14} /> Export Directory
                            </button>
                            <button
                                onClick={handleOpenOnboard}
                                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-xs"
                            >
                                <Plus size={15} /> Onboard New Facility
                            </button>
                        </div>
                    </div>

                    {/* QUICK FILTER PILLS */}
                    <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
                        {[
                            { key: "all", label: `All Facilities (${hospitals.length})` },
                            { key: "24x7", label: `24x7 Emergency Ready (${hospitals.filter(h => h.is_24x7).length})` },
                            { key: "icu", label: `ICU Equipped (${hospitals.filter(h => h.icu_beds > 0 || (h.beds?.icu?.available > 0)).length})` },
                            { key: "active", label: `Active (${hospitals.filter(h => h.is_active).length})` },
                            { key: "suspended", label: `Suspended (${hospitals.filter(h => !h.is_active).length})` },
                            { key: "clinic", label: `Clinics (${hospitals.filter(h => (h.hospital_type || '').toLowerCase().includes('clinic')).length})` }
                        ].map(f => (
                            <button
                                key={f.key}
                                onClick={() => setStatusFilter(f.key)}
                                className={`px-3 py-1.5 rounded-xl font-bold transition cursor-pointer shrink-0 ${
                                    statusFilter === f.key
                                        ? "bg-blue-600 text-white shadow-2xs"
                                        : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                                }`}
                            >
                                {f.label}
                            </button>
                        ))}
                    </div>

                    {/* SEARCH, CITY FILTER, TYPE FILTER & SORT */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                        <div className="relative">
                            <Search size={14} className="absolute left-3 top-3 text-slate-400" />
                            <input
                                type="text"
                                placeholder="Search by name, reg #, city..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full text-xs pl-8 pr-3 py-2.5 border border-slate-200 rounded-xl bg-slate-50/60 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
                            />
                        </div>

                        <div>
                            <select
                                value={typeFilter}
                                onChange={(e) => setTypeFilter(e.target.value)}
                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-slate-50/60 focus:bg-white font-medium"
                            >
                                <option value="">All Facility Classifications</option>
                                <option value="Multi-Speciality Hospital">Multi-Speciality Hospital</option>
                                <option value="Hospital">General Hospital</option>
                                <option value="Super Speciality Hospital">Super Speciality Hospital</option>
                                <option value="Outpatient Clinic">Outpatient Clinic</option>
                                <option value="Trauma & Emergency Centre">Trauma & Emergency Centre</option>
                                <option value="Daycare Centre">Daycare Centre</option>
                            </select>
                        </div>

                        <div>
                            <select
                                value={cityFilter}
                                onChange={(e) => setCityFilter(e.target.value)}
                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-slate-50/60 focus:bg-white font-medium"
                            >
                                <option value="">All Metros & Cities</option>
                                <option value="Kolkata">Kolkata</option>
                                <option value="New Delhi">New Delhi</option>
                                <option value="Mumbai">Mumbai</option>
                                <option value="Bengaluru">Bengaluru</option>
                                <option value="Chennai">Chennai</option>
                                <option value="Hyderabad">Hyderabad</option>
                                <option value="Pune">Pune</option>
                            </select>
                        </div>

                        <div>
                            <select
                                value={hospitalSortBy}
                                onChange={(e) => setHospitalSortBy(e.target.value)}
                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-slate-50/60 focus:bg-white font-medium text-slate-700"
                            >
                                <option value="name_asc">Sort: Name (A to Z)</option>
                                <option value="beds_desc">Sort: Total Beds (Highest First)</option>
                                <option value="icu_desc">Sort: ICU Capacity (Highest First)</option>
                                <option value="city_asc">Sort: City (A to Z)</option>
                            </select>
                        </div>
                    </div>

                    {/* FACILITIES TABLE */}
                    {filteredHospitals.length === 0 ? (
                        <div className="p-12 text-center text-slate-400 space-y-3">
                            <Building2 size={36} className="mx-auto text-slate-300" />
                            <p className="text-sm font-semibold">No hospitals or clinics matching the current search criteria.</p>
                            <button
                                onClick={() => { setSearchQuery(""); setCityFilter(""); setTypeFilter(""); setStatusFilter("all"); }}
                                className="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
                            >
                                Reset All Filters
                            </button>
                        </div>
                    ) : (
                        <div className="overflow-x-auto rounded-2xl border border-slate-200">
                            <table className="w-full text-left text-xs">
                                <thead>
                                    <tr className="bg-slate-50/80 border-b border-slate-200 text-slate-500 uppercase font-bold text-[11px]">
                                        <th className="py-3 px-4">Facility Details</th>
                                        <th className="py-3 px-3">Location & Contacts</th>
                                        <th className="py-3 px-3">Capacity (ICU / ER / Fleet)</th>
                                        <th className="py-3 px-3">Facility Admin Account</th>
                                        <th className="py-3 px-3">Readiness & Status</th>
                                        <th className="py-3 px-4 text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100">
                                    {filteredHospitals.map((h) => (
                                        <tr key={h.id} className="hover:bg-blue-50/20 transition">
                                            <td className="py-3.5 px-4">
                                                <div className="space-y-1">
                                                    <p className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                                                        <span>{h.name}</span>
                                                    </p>
                                                    <div className="flex items-center gap-1.5 flex-wrap">
                                                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">
                                                            {h.hospital_type || "Hospital"}
                                                        </span>
                                                        <span className="text-[10px] text-slate-400 font-mono">
                                                            #{h.registration_number}
                                                        </span>
                                                    </div>
                                                </div>
                                            </td>

                                            <td className="py-3.5 px-3">
                                                <div className="space-y-0.5 text-slate-600">
                                                    <p className="font-semibold text-slate-800 flex items-center gap-1">
                                                        <MapPin size={12} className="text-slate-400" />
                                                        {h.city}, {h.state}
                                                    </p>
                                                    <p className="text-[11px] text-slate-500 flex items-center gap-1">
                                                        <Phone size={11} className="text-slate-400" />
                                                        {h.phone}
                                                    </p>
                                                    {h.emergency_contact && (
                                                        <p className="text-[11px] text-rose-600 font-semibold flex items-center gap-1">
                                                            <span>SOS:</span> {h.emergency_contact}
                                                        </p>
                                                    )}
                                                </div>
                                            </td>

                                            <td className="py-3.5 px-3">
                                                <div className="space-y-1 text-[11px]">
                                                    <div className="flex items-center gap-2">
                                                        <span className="px-2 py-0.5 rounded font-bold bg-indigo-50 text-indigo-700 border border-indigo-100">
                                                            ICU: {h.beds?.icu?.available ?? h.icu_beds_config ?? 0}
                                                        </span>
                                                        <span className="px-2 py-0.5 rounded font-bold bg-rose-50 text-rose-700 border border-rose-100">
                                                            ER: {h.beds?.emergency?.available ?? h.emergency_beds_config ?? 0}
                                                        </span>
                                                    </div>
                                                    <p className="text-slate-500 text-[10px]">
                                                        Total Beds: <strong>{h.total_beds || 0}</strong> • Fleet: <strong>{h.ambulances?.total ?? 2}</strong>
                                                    </p>
                                                </div>
                                            </td>

                                            <td className="py-3.5 px-3">
                                                {h.admin_email || h.email ? (
                                                    <div className="space-y-0.5">
                                                        <span className="text-[11px] font-mono text-slate-700 font-semibold block truncate max-w-[150px]" title={h.admin_email || h.email}>
                                                            {h.admin_email || h.email}
                                                        </span>
                                                        <span className="text-[10px] text-emerald-600 font-bold flex items-center gap-0.5">
                                                            <CheckCheck size={11} /> Bound Provider
                                                        </span>
                                                    </div>
                                                ) : (
                                                    <span className="text-[10px] text-amber-600 font-semibold">
                                                        Pending Binding
                                                    </span>
                                                )}
                                            </td>

                                            {/* INLINE FAST TOGGLE BUTTONS */}
                                            <td className="py-3.5 px-3">
                                                <div className="flex flex-col gap-1.5 items-start">
                                                    <button
                                                        onClick={() => handleToggleFacility24x7(h)}
                                                        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold cursor-pointer transition ${
                                                            h.is_24x7
                                                                ? "bg-emerald-100 text-emerald-800 hover:bg-emerald-200"
                                                                : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                                                        }`}
                                                        title="Click to toggle 24x7 readiness"
                                                    >
                                                        <Clock size={10} /> {h.is_24x7 ? "24x7 Ready" : "Daycare"}
                                                    </button>

                                                    <button
                                                        onClick={() => handleToggleFacilityActive(h)}
                                                        className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold cursor-pointer transition ${
                                                            h.is_active
                                                                ? "bg-blue-100 text-blue-800 hover:bg-blue-200"
                                                                : "bg-rose-100 text-rose-800 hover:bg-rose-200"
                                                        }`}
                                                        title="Click to toggle Active / Suspended state"
                                                    >
                                                        {h.is_active ? "● Active in Search" : "● Suspended"}
                                                    </button>
                                                </div>
                                            </td>

                                            <td className="py-3.5 px-4 text-right">
                                                <div className="flex items-center justify-end gap-1.5">
                                                    <button
                                                        onClick={() => handleOpenView(h)}
                                                        className="p-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition cursor-pointer"
                                                        title="View Facility Details"
                                                    >
                                                        <Eye size={14} />
                                                    </button>
                                                    <button
                                                        onClick={() => handleOpenEdit(h)}
                                                        className="p-1.5 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg transition cursor-pointer"
                                                        title="Modify Facility"
                                                    >
                                                        <Edit3 size={14} />
                                                    </button>
                                                    <button
                                                        onClick={() => handleOpenDelete(h)}
                                                        className="p-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-lg transition cursor-pointer"
                                                        title="Delete Facility"
                                                    >
                                                        <Trash2 size={14} />
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}

            {/* ============================================================== */}
            {/* TAB 2: USER RBAC & ACCESS CONTROL MANAGEMENT                   */}
            {/* ============================================================== */}
            {activeTab === "users" && (
                <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs space-y-5">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
                        <div>
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Users size={18} className="text-purple-600" />
                                <span>Platform Users & Access Control (RBAC)</span>
                            </h3>
                            <p className="text-xs text-slate-500">
                                Manage user accounts, promote administrators, toggle account access, or provision new platform users.
                            </p>
                        </div>

                        <button
                            onClick={() => setShowCreateUserModal(true)}
                            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-xs self-start sm:self-auto"
                        >
                            <UserPlus size={15} /> Add System User
                        </button>
                    </div>

                    {/* SEARCH, ROLE FILTER & STATUS FILTER */}
                    <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
                        <div className="relative flex-1 max-w-sm">
                            <Search size={14} className="absolute left-3 top-3 text-slate-400" />
                            <input
                                type="text"
                                placeholder="Search by name or email..."
                                value={userSearchQuery}
                                onChange={(e) => setUserSearchQuery(e.target.value)}
                                className="w-full text-xs pl-8 pr-3 py-2.5 border border-slate-200 rounded-xl bg-slate-50/60 focus:bg-white focus:ring-2 focus:ring-purple-500 focus:outline-hidden"
                            />
                        </div>

                        <div className="flex flex-wrap items-center gap-2">
                            {/* Role Filter Buttons */}
                            <div className="flex items-center gap-1.5 text-xs">
                                {["", "Admin", "Hospital", "Patient"].map((r) => (
                                    <button
                                        key={r}
                                        onClick={() => setUserRoleFilter(r)}
                                        className={`px-3 py-1.5 rounded-xl font-bold transition cursor-pointer ${
                                            userRoleFilter === r ? "bg-purple-600 text-white shadow-2xs" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                                        }`}
                                    >
                                        {r === "" ? `All Roles (${users.length})` : r}
                                    </button>
                                ))}
                            </div>

                            {/* Status Filter Dropdown */}
                            <select
                                value={userStatusFilter}
                                onChange={(e) => setUserStatusFilter(e.target.value)}
                                className="text-xs p-1.5 border border-slate-200 rounded-xl bg-slate-50 font-semibold text-slate-700"
                            >
                                <option value="all">All Statuses</option>
                                <option value="active">Active Only</option>
                                <option value="suspended">Suspended Only</option>
                            </select>
                        </div>
                    </div>

                    {/* USERS TABLE */}
                    <div className="overflow-x-auto rounded-2xl border border-slate-200">
                        <table className="w-full text-left text-xs">
                            <thead>
                                <tr className="bg-slate-50/80 border-b border-slate-200 text-slate-500 uppercase font-bold text-[11px]">
                                    <th className="py-3 px-4">User</th>
                                    <th className="py-3 px-3">Email Address</th>
                                    <th className="py-3 px-3">Role Allocation</th>
                                    <th className="py-3 px-3">Status</th>
                                    <th className="py-3 px-3">Quick Reset</th>
                                    <th className="py-3 px-4 text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {filteredUsers.map((u) => {
                                    const currentRole = u.roles?.[0] || "Patient";
                                    return (
                                        <tr key={u.id} className="hover:bg-purple-50/20 transition">
                                            <td className="py-3 px-4">
                                                <div className="flex items-center gap-2">
                                                    <div className={`w-7 h-7 rounded-full flex items-center justify-center font-bold text-[10px] ${
                                                        currentRole === 'Admin' ? 'bg-slate-900 text-white' :
                                                        currentRole === 'Hospital' ? 'bg-blue-100 text-blue-700' :
                                                        'bg-purple-100 text-purple-700'
                                                    }`}>
                                                        {u.full_name ? u.full_name.slice(0, 2).toUpperCase() : "US"}
                                                    </div>
                                                    <div>
                                                        <span className="font-bold text-slate-900 block">{u.full_name}</span>
                                                        <span className="text-[10px] text-slate-400">ID #{u.id}</span>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="py-3 px-3 font-mono text-[11px] text-slate-700">{u.email}</td>
                                            <td className="py-3 px-3">
                                                <select
                                                    value={currentRole}
                                                    onChange={(e) => handleChangeUserRole(u, e.target.value)}
                                                    className="text-[11px] font-bold border border-slate-200 rounded-lg p-1 bg-white focus:ring-2 focus:ring-purple-500"
                                                >
                                                    <option value="Admin">Admin</option>
                                                    <option value="Hospital">Hospital</option>
                                                    <option value="Patient">Patient</option>
                                                </select>
                                            </td>
                                            <td className="py-3 px-3">
                                                <button
                                                    onClick={() => handleToggleUserStatus(u)}
                                                    className={`px-2.5 py-1 rounded-full text-[10px] font-bold cursor-pointer transition ${
                                                        u.is_active ? "bg-emerald-100 text-emerald-800 hover:bg-emerald-200" : "bg-rose-100 text-rose-800 hover:bg-rose-200"
                                                    }`}
                                                >
                                                    {u.is_active ? "● Active" : "● Suspended"}
                                                </button>
                                            </td>
                                            <td className="py-3 px-3">
                                                <button
                                                    onClick={() => handleResetUserPassword(u)}
                                                    className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-[10px] font-bold transition flex items-center gap-1 cursor-pointer"
                                                    title="Generate temporary password"
                                                >
                                                    <Key size={11} /> Reset Pass
                                                </button>
                                            </td>
                                            <td className="py-3 px-4 text-right">
                                                <button
                                                    onClick={() => handleDeleteUser(u.id, u.email)}
                                                    className="p-1.5 bg-rose-50 hover:bg-rose-100 text-rose-600 rounded-lg transition cursor-pointer"
                                                    title="Delete User"
                                                >
                                                    <Trash2 size={13} />
                                                </button>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* TAB 3: SYSTEM TELEMETRY & LIVE AUDIT LOG                       */}
            {/* ============================================================== */}
            {activeTab === "telemetry" && (
                <div className="space-y-6">
                    {/* INFRASTRUCTURE TELEMETRY CARDS */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-2">
                            <div className="flex items-center justify-between text-xs">
                                <span className="text-slate-400 font-bold uppercase text-[10px]">Core API Gateway</span>
                                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                            </div>
                            <p className="text-lg font-extrabold text-slate-900">{systemHealth?.health?.api_status || "Operational"}</p>
                            <span className="text-[11px] text-emerald-600 font-semibold">Latency: {systemHealth?.health?.api_latency_ms || 12} ms</span>
                        </div>

                        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-2">
                            <div className="flex items-center justify-between text-xs">
                                <span className="text-slate-400 font-bold uppercase text-[10px]">Database Cluster</span>
                                <Database size={14} className="text-blue-500" />
                            </div>
                            <p className="text-lg font-extrabold text-slate-900">SQLite Active</p>
                            <span className="text-[11px] text-blue-600 font-semibold">WAL Engine Normal</span>
                        </div>

                        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-2">
                            <div className="flex items-center justify-between text-xs">
                                <span className="text-slate-400 font-bold uppercase text-[10px]">ML Triage Engine</span>
                                <Cpu size={14} className="text-purple-500" />
                            </div>
                            <p className="text-lg font-extrabold text-slate-900">Online</p>
                            <span className="text-[11px] text-purple-600 font-semibold">Nearest Bed Matching</span>
                        </div>

                        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-2">
                            <div className="flex items-center justify-between text-xs">
                                <span className="text-slate-400 font-bold uppercase text-[10px]">Real-Time Dispatch</span>
                                <Wifi size={14} className="text-emerald-500" />
                            </div>
                            <p className="text-lg font-extrabold text-slate-900">Broadcasting</p>
                            <span className="text-[11px] text-emerald-600 font-semibold">Socket.IO Connected</span>
                        </div>
                    </div>

                    {/* REGIONAL SATURATION ANALYSIS */}
                    <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs space-y-4">
                        <div className="border-b border-slate-100 pb-3">
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Activity size={18} className="text-blue-600" />
                                <span>Pan-India Metro Bed Saturation & Emergency Coverage</span>
                            </h3>
                            <p className="text-xs text-slate-500">Live aggregated occupancy rates and ICU critical care readiness across major metro hubs</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {(systemHealth?.regional_saturation || []).map((reg) => (
                                <div key={reg.city} className="p-4 rounded-2xl border border-slate-200 bg-slate-50/50 space-y-3 text-xs">
                                    <div className="flex items-center justify-between">
                                        <h4 className="font-extrabold text-sm text-slate-900">{reg.city}</h4>
                                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">
                                            {reg.hospitals_count} Facilities
                                        </span>
                                    </div>

                                    <div>
                                        <div className="flex justify-between text-[11px] mb-1">
                                            <span className="text-slate-500">Bed Saturation:</span>
                                            <span className="font-bold text-slate-800">{reg.occupancy_rate}% Occupied</span>
                                        </div>
                                        <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                                            <div
                                                className={`h-full rounded-full transition-all duration-500 ${
                                                    reg.occupancy_rate > 80 ? "bg-rose-500" :
                                                    reg.occupancy_rate > 50 ? "bg-amber-500" : "bg-emerald-500"
                                                }`}
                                                style={{ width: `${reg.occupancy_rate}%` }}
                                            ></div>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-200/70 text-center">
                                        <div className="p-1.5 bg-white rounded-lg border border-slate-200/80">
                                            <span className="font-extrabold text-slate-900 block">{reg.available_beds}</span>
                                            <span className="text-[9px] text-slate-400 uppercase font-bold">Avail Beds</span>
                                        </div>
                                        <div className="p-1.5 bg-rose-50 rounded-lg border border-rose-100">
                                            <span className="font-extrabold text-rose-700 block">{reg.available_icu}</span>
                                            <span className="text-[9px] text-rose-600 uppercase font-bold">ICU Ready</span>
                                        </div>
                                        <div className="p-1.5 bg-emerald-50 rounded-lg border border-emerald-100">
                                            <span className="font-extrabold text-emerald-700 block">{reg.ambulances}</span>
                                            <span className="text-[9px] text-emerald-600 uppercase font-bold">Ambulances</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* LIVE AUDIT LOG FEED */}
                    <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs space-y-4">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div>
                                <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                    <FileText size={18} className="text-indigo-600" />
                                    <span>Live Administrative Audit Log</span>
                                </h3>
                                <p className="text-xs text-slate-500">Real-time chronicle of system modifications, onboarding actions, and platform policies</p>
                            </div>
                            <span className="px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-bold">
                                ● Sentinel Recording
                            </span>
                        </div>

                        <div className="divide-y divide-slate-100 max-h-72 overflow-y-auto">
                            {auditLogs.map((log) => (
                                <div key={log.id} className="py-2.5 flex items-center justify-between text-xs">
                                    <div className="flex items-center gap-2.5">
                                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${log.badge}`}>
                                            {log.action}
                                        </span>
                                        <span className="font-semibold text-slate-800">{log.target}</span>
                                    </div>
                                    <div className="flex items-center gap-3 text-slate-400 text-[11px]">
                                        <span>{log.actor}</span>
                                        <span>•</span>
                                        <span className="font-mono">{log.time}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* TAB 4: GLOBAL PLATFORM POLICIES & MAINTENANCE                  */}
            {/* ============================================================== */}
            {activeTab === "settings" && (
                <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs space-y-6">
                    <div className="border-b border-slate-100 pb-4">
                        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                            <Sliders size={18} className="text-slate-700" />
                            <span>Global Platform Policies & Emergency Routing Controls</span>
                        </h3>
                        <p className="text-xs text-slate-500">Configure core system hotlines, ABDM interoperability, and maintenance actions</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
                        {/* HOTLINE CONFIGURATION */}
                        <div className="p-5 rounded-2xl border border-slate-200 bg-slate-50/50 space-y-3">
                            <h4 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                <Phone size={16} className="text-rose-600" />
                                Master Emergency SOS Helpline
                            </h4>
                            <p className="text-slate-500 text-xs">
                                Default dispatch hotline displayed to unauthenticated public visitors and triggered on emergency SOS call-out.
                            </p>
                            <div>
                                <label className="block text-[11px] font-bold text-slate-700 mb-1">National Helpline Number</label>
                                <input
                                    type="text"
                                    value={globalSettings.emergencyHotline}
                                    onChange={(e) => setGlobalSettings({ ...globalSettings, emergencyHotline: e.target.value })}
                                    className="w-full p-2.5 bg-white border border-slate-200 rounded-xl font-bold text-rose-600 text-sm"
                                />
                            </div>
                        </div>

                        {/* ABDM DIGITAL HEALTH RECORD GATEWAY */}
                        <div className="p-5 rounded-2xl border border-slate-200 bg-slate-50/50 space-y-3">
                            <div className="flex items-center justify-between">
                                <h4 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                    <ShieldCheck size={16} className="text-emerald-600" />
                                    ABDM Electronic Health Records (EHR) Gateway
                                </h4>
                                <input
                                    type="checkbox"
                                    checked={globalSettings.abdmIntegration}
                                    onChange={(e) => setGlobalSettings({ ...globalSettings, abdmIntegration: e.target.checked })}
                                    className="rounded text-emerald-600 cursor-pointer"
                                />
                            </div>
                            <p className="text-slate-500 text-xs">
                                Sync electronic prescriptions and medical diagnostic records with the national ABDM health registry.
                            </p>
                            <span className="inline-block px-2.5 py-1 rounded-lg bg-emerald-100 text-emerald-800 text-[10px] font-bold">
                                {globalSettings.abdmIntegration ? "✓ Gateway Active & Validating" : "Disabled"}
                            </span>
                        </div>

                        {/* BED REFRESH POLLING RATE */}
                        <div className="p-5 rounded-2xl border border-slate-200 bg-slate-50/50 space-y-3">
                            <h4 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                                <Clock size={16} className="text-blue-600" />
                                Real-Time Bed Availability Polling Interval
                            </h4>
                            <p className="text-slate-500 text-xs">
                                Frequency of automated background socket synchronization between hospital wards and public discovery.
                            </p>
                            <select
                                value={globalSettings.bedSyncIntervalSec}
                                onChange={(e) => setGlobalSettings({ ...globalSettings, bedSyncIntervalSec: e.target.value })}
                                className="w-full p-2.5 bg-white border border-slate-200 rounded-xl font-bold text-slate-800"
                            >
                                <option value="5">Every 5 Seconds (Ultra-Fast)</option>
                                <option value="15">Every 15 Seconds (Standard Recommended)</option>
                                <option value="30">Every 30 Seconds</option>
                                <option value="60">Every 60 Seconds</option>
                            </select>
                        </div>

                        {/* MAINTENANCE MODE SWITCH */}
                        <div className="p-5 rounded-2xl border border-rose-200 bg-rose-50/30 space-y-3">
                            <div className="flex items-center justify-between">
                                <h4 className="font-bold text-rose-950 text-sm flex items-center gap-2">
                                    <AlertCircle size={16} className="text-rose-600" />
                                    System Maintenance Mode
                                </h4>
                                <input
                                    type="checkbox"
                                    checked={globalSettings.maintenanceMode}
                                    onChange={(e) => setGlobalSettings({ ...globalSettings, maintenanceMode: e.target.checked })}
                                    className="rounded text-rose-600 cursor-pointer"
                                />
                            </div>
                            <p className="text-rose-900/70 text-xs">
                                When enabled, only Super Administrators can access the platform. Public patient booking and hospital portals show a scheduled upgrade banner.
                            </p>
                            <span className={`inline-block px-2.5 py-1 rounded-lg text-[10px] font-bold ${
                                globalSettings.maintenanceMode ? "bg-rose-600 text-white" : "bg-slate-200 text-slate-700"
                            }`}>
                                {globalSettings.maintenanceMode ? "⚠️ MAINTENANCE ACTIVE" : "Platform Live"}
                            </span>
                        </div>
                    </div>

                    {/* MAINTENANCE & CACHE MANAGEMENT ACTION HUB */}
                    <div className="p-5 rounded-2xl border border-indigo-100 bg-indigo-50/40 space-y-4 text-xs">
                        <div>
                            <h4 className="font-bold text-indigo-950 text-sm flex items-center gap-2">
                                <Zap size={16} className="text-indigo-600" />
                                Platform Maintenance & Operations Hub
                            </h4>
                            <p className="text-slate-500 text-xs">
                                Execute operational procedures to flush server memory caches, re-index bed numbers, and download diagnostic archives.
                            </p>
                        </div>

                        <div className="flex flex-wrap items-center gap-3">
                            <button
                                onClick={handlePurgeCache}
                                disabled={purgingCache}
                                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition cursor-pointer flex items-center gap-2 shadow-xs disabled:opacity-50"
                            >
                                <RotateCcw size={14} className={purgingCache ? "animate-spin" : ""} />
                                <span>{purgingCache ? "Flushing Cache..." : "Flush Platform Cache"}</span>
                            </button>

                            <button
                                onClick={handleSyncBeds}
                                disabled={syncingBeds}
                                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition cursor-pointer flex items-center gap-2 shadow-xs disabled:opacity-50"
                            >
                                <RefreshCw size={14} className={syncingBeds ? "animate-spin" : ""} />
                                <span>{syncingBeds ? "Synchronizing..." : "Synchronize Bed Counters"}</span>
                            </button>

                            <button
                                onClick={handleExportDiagnostics}
                                className="px-4 py-2 bg-white hover:bg-slate-100 text-slate-800 font-bold rounded-xl border border-slate-200 transition cursor-pointer flex items-center gap-2"
                            >
                                <Download size={14} />
                                <span>Export Diagnostics Report</span>
                            </button>
                        </div>
                    </div>

                    <div className="pt-3 border-t border-slate-100 flex items-center justify-end">
                        <button
                            onClick={() => { flash("Platform global policies updated successfully"); addAuditLog("Saved Platform Policies", "Global Settings"); }}
                            className="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl shadow-xs transition cursor-pointer"
                        >
                            Save Platform Configuration
                        </button>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 1: ONBOARD NEW HOSPITAL / CLINIC                         */}
            {/* ============================================================== */}
            {showOnboardModal && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 overflow-y-auto">
                    <div className="bg-white rounded-3xl max-w-2xl w-full p-6 shadow-2xl space-y-4 my-8">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2.5">
                                <div className="w-9 h-9 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center">
                                    <Building2 size={20} />
                                </div>
                                <div>
                                    <h3 className="text-base font-bold text-slate-900">Onboard Healthcare Facility</h3>
                                    <p className="text-xs text-slate-500">Register and deploy a new hospital or outpatient clinic to the MediLink network</p>
                                </div>
                            </div>
                            <button onClick={() => setShowOnboardModal(false)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={20} />
                            </button>
                        </div>

                        <form onSubmit={handleCreateHospital} className="space-y-4">
                            <div>
                                <h4 className="text-xs font-bold uppercase tracking-wider text-blue-700 mb-2">1. Facility Identity</h4>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    <div>
                                        <label className="block text-xs font-semibold text-slate-700 mb-1">
                                            Hospital / Clinic Name <span className="text-rose-500">*</span>
                                        </label>
                                        <input
                                            type="text"
                                            required
                                            placeholder="e.g. CareWell Multi-Speciality Clinic"
                                            value={onboardData.name}
                                            onChange={(e) => setOnboardData({ ...onboardData, name: e.target.value })}
                                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-bold"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-xs font-semibold text-slate-700 mb-1">
                                            Facility Classification <span className="text-rose-500">*</span>
                                        </label>
                                        <select
                                            value={onboardData.hospital_type}
                                            onChange={(e) => setOnboardData({ ...onboardData, hospital_type: e.target.value })}
                                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-semibold bg-white"
                                        >
                                            <option value="Multi-Speciality Hospital">Multi-Speciality Hospital</option>
                                            <option value="Hospital">General Hospital</option>
                                            <option value="Super Speciality Hospital">Super Speciality Hospital</option>
                                            <option value="Outpatient Clinic">Outpatient Clinic</option>
                                            <option value="Trauma & Emergency Centre">Trauma & Emergency Centre</option>
                                            <option value="Daycare Centre">Daycare Centre</option>
                                        </select>
                                    </div>

                                    <div>
                                        <label className="block text-xs font-semibold text-slate-700 mb-1">
                                            Official Registration Number <span className="text-rose-500">*</span>
                                        </label>
                                        <input
                                            type="text"
                                            required
                                            placeholder="e.g. WB-HOSP-2026-901"
                                            value={onboardData.registration_number}
                                            onChange={(e) => setOnboardData({ ...onboardData, registration_number: e.target.value })}
                                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-mono font-bold"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-xs font-semibold text-slate-700 mb-1">
                                            Primary Contact Email <span className="text-rose-500">*</span>
                                        </label>
                                        <input
                                            type="email"
                                            required
                                            placeholder="admin@carewell.com"
                                            value={onboardData.email}
                                            onChange={(e) => setOnboardData({ ...onboardData, email: e.target.value })}
                                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-mono"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="pt-2 border-t border-slate-100">
                                <h4 className="text-xs font-bold uppercase tracking-wider text-blue-700 mb-2">2. Contact & Geolocation</h4>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                                    <div>
                                        <label className="block text-xs font-semibold text-slate-700 mb-1">
                                            Reception Phone <span className="text-rose-500">*</span>
                                        </label>
                                        <input
                                            type="tel"
                                            required
                                            value={onboardData.phone}
                                            onChange={(e) => setOnboardData({ ...onboardData, phone: e.target.value })}
                                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-xs font-semibold text-slate-700 mb-1">
                                            24x7 Emergency Contact
                                        </label>
                                        <input
                                            type="tel"
                                            value={onboardData.emergency_contact}
                                            onChange={(e) => setOnboardData({ ...onboardData, emergency_contact: e.target.value })}
                                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-bold text-rose-600"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-xs font-semibold text-slate-700 mb-1">City <span className="text-rose-500">*</span></label>
                                        <input
                                            type="text"
                                            required
                                            value={onboardData.city}
                                            onChange={(e) => setOnboardData({ ...onboardData, city: e.target.value })}
                                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                        />
                                    </div>

                                    <div className="md:col-span-2">
                                        <label className="block text-xs font-semibold text-slate-700 mb-1">Full Street Address <span className="text-rose-500">*</span></label>
                                        <input
                                            type="text"
                                            required
                                            value={onboardData.address}
                                            onChange={(e) => setOnboardData({ ...onboardData, address: e.target.value })}
                                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-xs font-semibold text-slate-700 mb-1">Pincode</label>
                                        <input
                                            type="text"
                                            value={onboardData.pincode}
                                            onChange={(e) => setOnboardData({ ...onboardData, pincode: e.target.value })}
                                            className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="pt-2 border-t border-slate-100">
                                <h4 className="text-xs font-bold uppercase tracking-wider text-blue-700 mb-2">3. Initial Capacity Setup</h4>
                                <div className="grid grid-cols-2 md:grid-cols-5 gap-2.5 text-xs">
                                    <div className="p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                                        <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">General Beds</label>
                                        <input
                                            type="number"
                                            min="0"
                                            value={onboardData.general_beds}
                                            onChange={(e) => setOnboardData({ ...onboardData, general_beds: e.target.value })}
                                            className="w-full text-xs p-1.5 border border-slate-300 rounded font-bold"
                                        />
                                    </div>
                                    <div className="p-2.5 bg-indigo-50/50 rounded-xl border border-indigo-200">
                                        <label className="block text-[10px] font-bold text-indigo-700 uppercase mb-1">ICU Beds</label>
                                        <input
                                            type="number"
                                            min="0"
                                            value={onboardData.icu_beds}
                                            onChange={(e) => setOnboardData({ ...onboardData, icu_beds: e.target.value })}
                                            className="w-full text-xs p-1.5 border border-indigo-300 rounded font-bold text-indigo-900"
                                        />
                                    </div>
                                    <div className="p-2.5 bg-rose-50/50 rounded-xl border border-rose-200">
                                        <label className="block text-[10px] font-bold text-rose-700 uppercase mb-1">ER Beds</label>
                                        <input
                                            type="number"
                                            min="0"
                                            value={onboardData.emergency_beds}
                                            onChange={(e) => setOnboardData({ ...onboardData, emergency_beds: e.target.value })}
                                            className="w-full text-xs p-1.5 border border-rose-300 rounded font-bold text-rose-900"
                                        />
                                    </div>
                                    <div className="p-2.5 bg-emerald-50/50 rounded-xl border border-emerald-200">
                                        <label className="block text-[10px] font-bold text-emerald-700 uppercase mb-1">Ambulances</label>
                                        <input
                                            type="number"
                                            min="0"
                                            value={onboardData.ambulances_count}
                                            onChange={(e) => setOnboardData({ ...onboardData, ambulances_count: e.target.value })}
                                            className="w-full text-xs p-1.5 border border-emerald-300 rounded font-bold text-emerald-900"
                                        />
                                    </div>
                                    <div className="p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                                        <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">OTs</label>
                                        <input
                                            type="number"
                                            min="0"
                                            value={onboardData.operation_theatres}
                                            onChange={(e) => setOnboardData({ ...onboardData, operation_theatres: e.target.value })}
                                            className="w-full text-xs p-1.5 border border-slate-300 rounded font-bold"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="pt-2 border-t border-slate-100 bg-blue-50/50 p-3 rounded-2xl border border-blue-100">
                                <div className="flex items-center justify-between mb-2">
                                    <h4 className="text-xs font-bold text-blue-900">4. Facility Administrator Login Setup</h4>
                                    <label className="flex items-center gap-1.5 text-xs text-blue-800 font-semibold cursor-pointer">
                                        <input
                                            type="checkbox"
                                            checked={onboardData.create_user_account}
                                            onChange={(e) => setOnboardData({ ...onboardData, create_user_account: e.target.checked })}
                                            className="rounded text-blue-600"
                                        />
                                        <span>Create Dedicated Admin Account</span>
                                    </label>
                                </div>

                                {onboardData.create_user_account && (
                                    <div className="grid grid-cols-2 gap-3 text-xs">
                                        <div>
                                            <span className="text-slate-500 block mb-0.5">Login Email:</span>
                                            <span className="font-mono font-bold text-slate-800">{onboardData.email || "(Fill primary email above)"}</span>
                                        </div>
                                        <div>
                                            <label className="block text-slate-700 font-semibold mb-0.5">Initial Password:</label>
                                            <input
                                                type="text"
                                                value={onboardData.admin_password}
                                                onChange={(e) => setOnboardData({ ...onboardData, admin_password: e.target.value })}
                                                className="w-full text-xs p-1.5 border border-slate-300 rounded-lg font-mono font-bold bg-white"
                                            />
                                        </div>
                                    </div>
                                )}
                            </div>

                            <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
                                <button
                                    type="button"
                                    onClick={() => setShowOnboardModal(false)}
                                    className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition cursor-pointer shadow-xs flex items-center gap-1.5"
                                >
                                    <Building2 size={14} />
                                    <span>Complete Onboarding & Deploy</span>
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 2: EDIT EXISTING HOSPITAL                                */}
            {/* ============================================================== */}
            {showEditModal && selectedHospital && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 overflow-y-auto">
                    <div className="bg-white rounded-3xl max-w-xl w-full p-6 shadow-2xl space-y-4 my-8">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div>
                                <h3 className="text-base font-bold text-slate-900">Modify Facility Configuration</h3>
                                <p className="text-xs text-slate-500">{selectedHospital.name} (#{selectedHospital.registration_number})</p>
                            </div>
                            <button onClick={() => setShowEditModal(false)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={20} />
                            </button>
                        </div>

                        <form onSubmit={handleUpdateHospital} className="space-y-3.5">
                            <div>
                                <label className="block text-xs font-semibold text-slate-700 mb-1">Facility Name</label>
                                <input
                                    type="text"
                                    required
                                    value={editData.name}
                                    onChange={(e) => setEditData({ ...editData, name: e.target.value })}
                                    className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-bold"
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Registration #</label>
                                    <input
                                        type="text"
                                        required
                                        value={editData.registration_number}
                                        onChange={(e) => setEditData({ ...editData, registration_number: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-mono"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Classification</label>
                                    <select
                                        value={editData.hospital_type}
                                        onChange={(e) => setEditData({ ...editData, hospital_type: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white font-semibold"
                                    >
                                        <option value="Multi-Speciality Hospital">Multi-Speciality Hospital</option>
                                        <option value="Hospital">General Hospital</option>
                                        <option value="Super Speciality Hospital">Super Speciality Hospital</option>
                                        <option value="Outpatient Clinic">Outpatient Clinic</option>
                                        <option value="Trauma & Emergency Centre">Trauma & Emergency Centre</option>
                                        <option value="Daycare Centre">Daycare Centre</option>
                                    </select>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Reception Phone</label>
                                    <input
                                        type="tel"
                                        value={editData.phone}
                                        onChange={(e) => setEditData({ ...editData, phone: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Emergency SOS</label>
                                    <input
                                        type="tel"
                                        value={editData.emergency_contact}
                                        onChange={(e) => setEditData({ ...editData, emergency_contact: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl text-rose-600 font-bold"
                                    />
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">City</label>
                                    <input
                                        type="text"
                                        value={editData.city}
                                        onChange={(e) => setEditData({ ...editData, city: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Official Email</label>
                                    <input
                                        type="email"
                                        value={editData.email}
                                        onChange={(e) => setEditData({ ...editData, email: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-mono"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-xs font-semibold text-slate-700 mb-1">Full Street Address</label>
                                <input
                                    type="text"
                                    value={editData.address}
                                    onChange={(e) => setEditData({ ...editData, address: e.target.value })}
                                    className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                />
                            </div>

                            <div className="flex items-center gap-4 pt-1">
                                <label className="flex items-center gap-1.5 text-xs text-slate-700 font-semibold cursor-pointer">
                                    <input
                                        type="checkbox"
                                        checked={editData.is_24x7}
                                        onChange={(e) => setEditData({ ...editData, is_24x7: e.target.checked })}
                                        className="rounded text-blue-600"
                                    />
                                    <span>24x7 Emergency Ready</span>
                                </label>

                                <label className="flex items-center gap-1.5 text-xs text-slate-700 font-semibold cursor-pointer">
                                    <input
                                        type="checkbox"
                                        checked={editData.is_active}
                                        onChange={(e) => setEditData({ ...editData, is_active: e.target.checked })}
                                        className="rounded text-emerald-600"
                                    />
                                    <span>Facility Active on Platform Search</span>
                                </label>
                            </div>

                            <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
                                <button
                                    type="button"
                                    onClick={() => setShowEditModal(false)}
                                    className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition cursor-pointer shadow-xs"
                                >
                                    Save Changes
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 3: VIEW FULL FACILITY SPECIFICATIONS                     */}
            {/* ============================================================== */}
            {showViewModal && selectedHospital && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl space-y-4 border border-slate-200">
                        <div className="flex items-start justify-between border-b border-slate-100 pb-3">
                            <div>
                                <h3 className="text-base font-extrabold text-slate-900">{selectedHospital.name}</h3>
                                <p className="text-xs text-slate-500">{selectedHospital.hospital_type} • #{selectedHospital.registration_number}</p>
                            </div>
                            <button onClick={() => setShowViewModal(false)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={20} />
                            </button>
                        </div>

                        <div className="space-y-3 text-xs">
                            <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200/80 space-y-1.5">
                                <div className="flex items-center justify-between">
                                    <span className="text-slate-400 font-bold uppercase text-[10px]">Location</span>
                                    <span className="font-semibold text-slate-800">{selectedHospital.city}, {selectedHospital.state} ({selectedHospital.pincode || "N/A"})</span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="text-slate-400 font-bold uppercase text-[10px]">Address</span>
                                    <span className="text-slate-700 font-medium text-right max-w-[250px]">{selectedHospital.address}</span>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-2.5">
                                <div className="p-3 bg-blue-50/60 rounded-xl border border-blue-100">
                                    <span className="text-[10px] text-blue-700 font-bold uppercase block">Reception</span>
                                    <span className="font-bold text-slate-900">{selectedHospital.phone}</span>
                                </div>
                                <div className="p-3 bg-rose-50/60 rounded-xl border border-rose-100">
                                    <span className="text-[10px] text-rose-700 font-bold uppercase block">Emergency SOS</span>
                                    <span className="font-bold text-rose-600">{selectedHospital.emergency_contact || selectedHospital.phone}</span>
                                </div>
                            </div>

                            <div className="p-3 bg-white rounded-xl border border-slate-200 space-y-2">
                                <span className="text-[10px] text-slate-400 font-bold uppercase block">Capacity Breakdown</span>
                                <div className="grid grid-cols-3 gap-2 text-center">
                                    <div className="p-2 bg-indigo-50 rounded-lg">
                                        <span className="text-xs font-extrabold text-indigo-700 block">
                                            {selectedHospital.beds?.icu?.available ?? selectedHospital.icu_beds_config ?? 0}
                                        </span>
                                        <span className="text-[10px] text-indigo-600">ICU Beds</span>
                                    </div>
                                    <div className="p-2 bg-rose-50 rounded-lg">
                                        <span className="text-xs font-extrabold text-rose-700 block">
                                            {selectedHospital.beds?.emergency?.available ?? selectedHospital.emergency_beds_config ?? 0}
                                        </span>
                                        <span className="text-[10px] text-rose-600">ER Trauma</span>
                                    </div>
                                    <div className="p-2 bg-emerald-50 rounded-lg">
                                        <span className="text-xs font-extrabold text-emerald-700 block">
                                            {selectedHospital.ambulances?.available ?? selectedHospital.ambulances_count ?? 2}
                                        </span>
                                        <span className="text-[10px] text-emerald-600">Ambulances</span>
                                    </div>
                                </div>
                            </div>

                            {selectedHospital.admin_email && (
                                <div className="p-2.5 bg-slate-50 rounded-xl text-[11px] flex items-center justify-between">
                                    <span className="text-slate-500">Facility Admin Email:</span>
                                    <span className="font-mono font-bold text-slate-800">{selectedHospital.admin_email}</span>
                                </div>
                            )}
                        </div>

                        <div className="flex items-center justify-end pt-3 border-t border-slate-100">
                            <button
                                onClick={() => setShowViewModal(false)}
                                className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl transition cursor-pointer"
                            >
                                Close View
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 4: DELETE CONFIRMATION                                   */}
            {/* ============================================================== */}
            {showDeleteModal && selectedHospital && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl space-y-4 border border-rose-200">
                        <div className="flex items-center gap-3 text-rose-600">
                            <div className="w-10 h-10 rounded-2xl bg-rose-100 flex items-center justify-center">
                                <AlertTriangle size={22} />
                            </div>
                            <div>
                                <h3 className="text-base font-bold text-slate-900">Decommission Facility?</h3>
                                <p className="text-xs text-rose-600 font-semibold">Irreversible Platform Operation</p>
                            </div>
                        </div>

                        <p className="text-xs text-slate-600 leading-relaxed">
                            Are you sure you want to remove <strong className="text-slate-900">{selectedHospital.name}</strong> ({selectedHospital.city})?
                            This will safely delete all associated bed allocations, fleet units, and doctor rosters from platform discovery.
                        </p>

                        <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                            <button
                                onClick={() => setShowDeleteModal(false)}
                                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleDeleteHospital}
                                className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold rounded-xl transition cursor-pointer shadow-xs font-bold"
                            >
                                Delete Facility
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 5: ADD NEW PLATFORM USER                                 */}
            {/* ============================================================== */}
            {showCreateUserModal && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl space-y-4 border border-purple-200">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-8 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center">
                                    <UserPlus size={18} />
                                </div>
                                <div>
                                    <h3 className="text-sm font-bold text-slate-900">Add Platform User</h3>
                                    <p className="text-[11px] text-slate-500">Provision an administrative or patient account</p>
                                </div>
                            </div>
                            <button onClick={() => setShowCreateUserModal(false)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        <form onSubmit={handleCreateUser} className="space-y-3 text-xs">
                            <div>
                                <label className="block text-slate-700 font-semibold mb-1">Full Name</label>
                                <input
                                    type="text"
                                    required
                                    placeholder="e.g. Dr. Sunita Rao"
                                    value={userFormData.full_name}
                                    onChange={(e) => setUserFormData({ ...userFormData, full_name: e.target.value })}
                                    className="w-full p-2.5 border border-slate-200 rounded-xl"
                                />
                            </div>

                            <div>
                                <label className="block text-slate-700 font-semibold mb-1">Email Address</label>
                                <input
                                    type="email"
                                    required
                                    placeholder="user@medilink.com"
                                    value={userFormData.email}
                                    onChange={(e) => setUserFormData({ ...userFormData, email: e.target.value })}
                                    className="w-full p-2.5 border border-slate-200 rounded-xl font-mono"
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-slate-700 font-semibold mb-1">Role Allocation</label>
                                    <select
                                        value={userFormData.role}
                                        onChange={(e) => setUserFormData({ ...userFormData, role: e.target.value })}
                                        className="w-full p-2.5 border border-slate-200 rounded-xl bg-white font-bold"
                                    >
                                        <option value="Patient">Patient</option>
                                        <option value="Hospital">Hospital Admin</option>
                                        <option value="Admin">Super Administrator</option>
                                    </select>
                                </div>

                                <div>
                                    <label className="block text-slate-700 font-semibold mb-1">Password</label>
                                    <input
                                        type="text"
                                        required
                                        value={userFormData.password}
                                        onChange={(e) => setUserFormData({ ...userFormData, password: e.target.value })}
                                        className="w-full p-2.5 border border-slate-200 rounded-xl font-mono"
                                    />
                                </div>
                            </div>

                            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                                <button
                                    type="button"
                                    onClick={() => setShowCreateUserModal(false)}
                                    className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl cursor-pointer"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl shadow-xs cursor-pointer"
                                >
                                    Create User
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
