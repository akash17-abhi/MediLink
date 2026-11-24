import React, { useState, useEffect } from "react";
import {
    Building2, Bed, AlertTriangle, Truck, Calendar, CheckCircle2,
    Clock, RefreshCw, Plus, Minus, User, ShieldCheck, Stethoscope,
    Search, X, Phone, MapPin, Edit3, Trash2, HeartPulse, Shield,
    Settings, Check, Filter, Activity, UserPlus, FileText
} from "lucide-react";
import hospitalAdminService from "../../services/hospitalAdminService";

export default function HospitalDashboard() {
    const [summary, setSummary] = useState(null);
    const [beds, setBeds] = useState([]);
    const [ambulances, setAmbulances] = useState([]);
    const [emergencies, setEmergencies] = useState([]);
    const [appointments, setAppointments] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [loading, setLoading] = useState(true);

    // Active Section Tabs: 'beds', 'ambulances', 'emergencies', 'appointments', 'doctors', 'settings'
    const [activeSection, setActiveSection] = useState("beds");

    // Search and Filter States
    const [bedTypeFilter, setBedTypeFilter] = useState("");
    const [bedSearchQuery, setBedSearchQuery] = useState("");
    const [apptFilter, setApptFilter] = useState("all");
    const [apptSearchQuery, setApptSearchQuery] = useState("");
    const [doctorSearchQuery, setDoctorSearchQuery] = useState("");
    const [actionMsg, setActionMsg] = useState("");

    // Modals
    const [showAddBedModal, setShowAddBedModal] = useState(false);
    const [newBedData, setNewBedData] = useState({
        bed_number: "",
        ward: "ICU Ward B",
        bed_type: "ICU",
        floor: "2nd Floor",
        room_number: "204",
        notes: "Oxygen & Ventilator equipped"
    });

    const [showAddAmbulanceModal, setShowAddAmbulanceModal] = useState(false);
    const [newAmbulanceData, setNewAmbulanceData] = useState({
        registration_number: "",
        ambulance_type: "Advanced Life Support (ALS)",
        driver_name: "Paramedic Unit Driver",
        driver_phone: "+91 9800001080",
        current_location: "Hospital Emergency Bay"
    });

    const [showAddDoctorModal, setShowAddDoctorModal] = useState(false);
    const [newDoctorData, setNewDoctorData] = useState({
        full_name: "",
        email: "",
        phone: "+91 9830001234",
        specialization: "Cardiology",
        qualification: "MBBS, MD (Cardiology)",
        experience: 8,
        consultation_fee: 900
    });

    const [showEditHospitalModal, setShowEditHospitalModal] = useState(false);
    const [hospitalFormData, setHospitalFormData] = useState({
        name: "",
        city: "",
        phone: "",
        emergency_contact: "",
        address: ""
    });

    // Prescription (e-Rx) State
    const [showRxModal, setShowRxModal] = useState(false);
    const [showViewRxModal, setShowViewRxModal] = useState(false);
    const [selectedApptForRx, setSelectedApptForRx] = useState(null);
    const [rxData, setRxData] = useState({
        diagnosis: "",
        medicines: "",
        dosage: "1-0-1 (Morning & Night)",
        duration: "5 Days",
        instructions: "Take after meals with warm water. Stay well hydrated.",
        symptoms: "",
        lab_tests: "",
        notes: "",
        follow_up_date: ""
    });

    useEffect(() => {
        loadAllData();
    }, []);

    const loadAllData = async () => {
        setLoading(true);
        try {
            const [sumRes, bedsRes, ambRes, emgRes, apptRes, docRes] = await Promise.all([
                hospitalAdminService.getSummary(),
                hospitalAdminService.getBeds(),
                hospitalAdminService.getAmbulances(),
                hospitalAdminService.getEmergencies(),
                hospitalAdminService.getAppointments(),
                hospitalAdminService.getDoctors().catch(() => ({ doctors: [] }))
            ]);
            setSummary(sumRes);
            setBeds(bedsRes.beds || []);
            setAmbulances(ambRes.ambulances || []);
            setEmergencies(emgRes.emergencies || []);
            setAppointments(apptRes.appointments || []);
            setDoctors(docRes.doctors || []);

            if (sumRes?.hospital) {
                setHospitalFormData({
                    name: sumRes.hospital.name || "",
                    city: sumRes.hospital.city || "",
                    phone: sumRes.hospital.phone || "",
                    emergency_contact: sumRes.hospital.emergency_contact || "",
                    address: sumRes.hospital.address || ""
                });
            }
        } catch (err) {
            console.error("Failed to load hospital admin data:", err);
        } finally {
            setLoading(false);
        }
    };

    const refreshSummary = async () => {
        try {
            const res = await hospitalAdminService.getSummary();
            setSummary(res);
        } catch (_) {}
    };

    const flashMessage = (msg) => {
        setActionMsg(msg);
        setTimeout(() => setActionMsg(""), 3500);
    };

    // Bed Handlers
    const handleBedStatusUpdate = async (bedId, newStatus) => {
        try {
            await hospitalAdminService.updateBed(bedId, { status: newStatus });
            flashMessage(`Bed updated to ${newStatus}`);
            setBeds(prev => prev.map(b => b.id === bedId ? { ...b, status: newStatus } : b));
            refreshSummary();
        } catch (err) {
            alert("Failed to update bed status");
        }
    };

    const handleQuickToggle = async (bedType, action) => {
        try {
            const res = await hospitalAdminService.quickToggleBed(bedType, action);
            flashMessage(res.message);
            const updatedBeds = await hospitalAdminService.getBeds();
            setBeds(updatedBeds.beds || []);
            refreshSummary();
        } catch (err) {
            alert(err.response?.data?.message || "Quick toggle failed");
        }
    };

    const handleCreateBed = async (e) => {
        e.preventDefault();
        try {
            const res = await hospitalAdminService.addBed(newBedData);
            flashMessage(res.message);
            setShowAddBedModal(false);
            setNewBedData({
                bed_number: "",
                ward: "ICU Ward B",
                bed_type: "ICU",
                floor: "2nd Floor",
                room_number: "204",
                notes: "Oxygen & Ventilator equipped"
            });
            const updatedBeds = await hospitalAdminService.getBeds();
            setBeds(updatedBeds.beds || []);
            refreshSummary();
        } catch (err) {
            alert(err.response?.data?.message || "Failed to register new bed");
        }
    };

    const handleDeleteBed = async (bedId, bedNo) => {
        if (!window.confirm(`Are you sure you want to remove Bed #${bedNo}?`)) return;
        try {
            await hospitalAdminService.deleteBed(bedId);
            flashMessage(`Bed #${bedNo} removed successfully`);
            setBeds(prev => prev.filter(b => b.id !== bedId));
            refreshSummary();
        } catch (err) {
            alert("Failed to delete bed");
        }
    };

    // Ambulance Handlers
    const handleAmbulanceStatus = async (ambId, newStatus) => {
        try {
            await hospitalAdminService.updateAmbulance(ambId, { availability_status: newStatus });
            flashMessage(`Ambulance status set to ${newStatus}`);
            setAmbulances(prev => prev.map(a => a.id === ambId ? { ...a, availability_status: newStatus } : a));
            refreshSummary();
        } catch (err) {
            alert("Failed to update ambulance status");
        }
    };

    const handleCreateAmbulance = async (e) => {
        e.preventDefault();
        try {
            const res = await hospitalAdminService.addAmbulance(newAmbulanceData);
            flashMessage(res.message);
            setShowAddAmbulanceModal(false);
            setNewAmbulanceData({
                registration_number: "",
                ambulance_type: "Advanced Life Support (ALS)",
                driver_name: "Paramedic Unit Driver",
                driver_phone: "+91 9800001080",
                current_location: "Hospital Emergency Bay"
            });
            const updatedAmbs = await hospitalAdminService.getAmbulances();
            setAmbulances(updatedAmbs.ambulances || []);
            refreshSummary();
        } catch (err) {
            alert(err.response?.data?.message || "Failed to register ambulance");
        }
    };

    // Emergency Handlers
    const handleEmergencyStatus = async (emergencyId, newStatus) => {
        try {
            await hospitalAdminService.updateEmergencyStatus(emergencyId, newStatus);
            flashMessage(`Emergency #${emergencyId} updated to ${newStatus}`);
            setEmergencies(prev => prev.map(e => e.id === emergencyId ? { ...e, status: newStatus } : e));
            refreshSummary();
        } catch (err) {
            alert("Failed to update emergency status");
        }
    };

    // Appointment Handlers
    const handleAppointmentStatus = async (appointmentId, newStatus) => {
        try {
            await hospitalAdminService.updateAppointmentStatus(appointmentId, newStatus);
            flashMessage(`Appointment #${appointmentId} set to ${newStatus}`);
            setAppointments(prev => prev.map(a => a.id === appointmentId ? { ...a, status: newStatus } : a));
            refreshSummary();
        } catch (err) {
            alert("Failed to update appointment status");
        }
    };

    // Doctor Handlers
    const handleToggleDoctorActive = async (docId, currentActive) => {
        try {
            await hospitalAdminService.updateDoctor(docId, { is_active: !currentActive });
            flashMessage(`Doctor status updated to ${!currentActive ? 'On Duty' : 'Off Duty'}`);
            setDoctors(prev => prev.map(d => d.id === docId ? { ...d, is_active: !currentActive } : d));
        } catch (err) {
            alert("Failed to update doctor status");
        }
    };

    const handleCreateDoctor = async (e) => {
        e.preventDefault();
        try {
            const res = await hospitalAdminService.addDoctor(newDoctorData);
            flashMessage(res.message);
            setShowAddDoctorModal(false);
            setNewDoctorData({
                full_name: "",
                email: "",
                phone: "+91 9830001234",
                specialization: "Cardiology",
                qualification: "MBBS, MD (Cardiology)",
                experience: 8,
                consultation_fee: 900
            });
            const updatedDocs = await hospitalAdminService.getDoctors();
            setDoctors(updatedDocs.doctors || []);
        } catch (err) {
            alert(err.response?.data?.message || "Failed to add specialist doctor");
        }
    };

    // Hospital Facility Profile
    const handleSaveHospitalInfo = async (e) => {
        e.preventDefault();
        try {
            const res = await hospitalAdminService.updateHospitalInfo(hospitalFormData);
            flashMessage(res.message);
            setShowEditHospitalModal(false);
            refreshSummary();
        } catch (err) {
            alert("Failed to update facility details");
        }
    };

    // Prescription (e-Rx) Handlers
    const handleOpenRxModal = (appt) => {
        setSelectedApptForRx(appt);
        if (appt.prescription) {
            setRxData({
                diagnosis: appt.prescription.diagnosis || (appt.reason ? `Clinical Consultation for ${appt.reason}` : "General Outpatient Consultation"),
                medicines: appt.prescription.medicines || "Tab Azithromycin 500mg, Tab Paracetamol 650mg, Tab Pantoprazole 40mg",
                dosage: appt.prescription.dosage || "1-0-1 (Morning & Night)",
                duration: appt.prescription.duration || "5 Days",
                instructions: appt.prescription.instructions || "Take medicines after meals with warm water. Drink plenty of warm fluids.",
                symptoms: appt.reason || "Outpatient Clinical Consult",
                lab_tests: appt.prescription.lab_tests || "",
                notes: appt.prescription.notes || "Adequate hydration and rest advised.",
                follow_up_date: appt.prescription.follow_up_date || new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
            });
        } else {
            setRxData({
                diagnosis: appt.reason ? `Clinical Consultation for ${appt.reason}` : "Acute Upper Respiratory Tract Infection",
                medicines: "Tab Azithromycin 500mg, Tab Paracetamol 650mg, Tab Pantoprazole 40mg",
                dosage: "1-0-1 (Morning & Night)",
                duration: "5 Days",
                instructions: "Take medicines after meals with warm water. Drink plenty of warm fluids and take adequate rest.",
                symptoms: appt.reason || "Fever, mild throat irritation, and fatigue for 2 days",
                lab_tests: "Complete Blood Count (CBC) if fever persists beyond 48 hours",
                notes: "Strict rest advised for 2 days. Return immediately if breathing difficulty develops.",
                follow_up_date: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
            });
        }
        setShowRxModal(true);
    };

    const handleOpenViewRxModal = async (appt) => {
        setSelectedApptForRx(appt);
        setShowViewRxModal(true);
        if (!appt.prescription) {
            try {
                const res = await hospitalAdminService.getAppointmentPrescription(appt.id);
                if (res.success && res.prescription) {
                    setSelectedApptForRx(prev => ({ ...prev, prescription: res.prescription }));
                }
            } catch (err) {
                console.error("Could not fetch prescription details", err);
            }
        }
    };

    const handleSavePrescription = async (e) => {
        e.preventDefault();
        if (!selectedApptForRx) return;
        try {
            const res = await hospitalAdminService.issuePrescription(selectedApptForRx.id, rxData);
            flashMessage(res.message || "Digital Prescription (e-Rx) issued successfully!");
            setShowRxModal(false);
            const apptRes = await hospitalAdminService.getAppointments();
            setAppointments(apptRes.appointments || []);
        } catch (err) {
            alert(err.response?.data?.message || "Failed to issue prescription");
        }
    };

    // Filtered Lists
    const filteredBeds = beds.filter(b => {
        const matchesType = !bedTypeFilter || b.bed_type.toLowerCase() === bedTypeFilter.toLowerCase();
        const matchesSearch = !bedSearchQuery.trim() ||
            b.bed_number.toLowerCase().includes(bedSearchQuery.toLowerCase()) ||
            b.ward.toLowerCase().includes(bedSearchQuery.toLowerCase()) ||
            (b.floor && b.floor.toLowerCase().includes(bedSearchQuery.toLowerCase()));
        return matchesType && matchesSearch;
    });

    const filteredAppointments = appointments.filter(a => {
        const matchesStatus = apptFilter === "all" || a.status === apptFilter;
        const matchesSearch = !apptSearchQuery.trim() ||
            a.patient_name.toLowerCase().includes(apptSearchQuery.toLowerCase()) ||
            a.doctor_name.toLowerCase().includes(apptSearchQuery.toLowerCase()) ||
            (a.reason && a.reason.toLowerCase().includes(apptSearchQuery.toLowerCase()));
        return matchesStatus && matchesSearch;
    });

    const filteredDoctors = doctors.filter(d => {
        return !doctorSearchQuery.trim() ||
            d.full_name.toLowerCase().includes(doctorSearchQuery.toLowerCase()) ||
            d.specialization.toLowerCase().includes(doctorSearchQuery.toLowerCase());
    });

    if (loading) {
        return (
            <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center text-slate-500 text-sm space-y-3">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
                <p className="font-semibold">Loading Hospital Administration & Real-Time Resource Hub...</p>
            </div>
        );
    }

    const icuAvail = summary?.beds?.icu?.available || 0;
    const icuTotal = summary?.beds?.icu?.total || 1;
    const icuPercent = Math.round((icuAvail / icuTotal) * 100);

    const erAvail = summary?.beds?.emergency?.available || 0;
    const erTotal = summary?.beds?.emergency?.total || 1;
    const erPercent = Math.round((erAvail / erTotal) * 100);

    return (
        <div className="space-y-6">
            {/* ACTION NOTIFICATION TOAST */}
            {actionMsg && (
                <div className="bg-emerald-600 text-white px-4 py-3 rounded-2xl text-xs font-bold shadow-lg flex items-center justify-between transition animate-fadeIn">
                    <span className="flex items-center gap-2">
                        <CheckCircle2 size={16} />
                        {actionMsg}
                    </span>
                    <button onClick={() => setActionMsg("")} className="text-white/80 hover:text-white cursor-pointer">✕</button>
                </div>
            )}

            {/* HOSPITAL IDENTITY & LIVE KPI HEADER */}
            <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-6 sm:p-7 shadow-xl border border-indigo-900/40 space-y-6">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
                    <div className="flex items-start sm:items-center gap-4">
                        <div className="w-14 h-14 rounded-2xl bg-blue-600 flex items-center justify-center text-white shadow-md border-2 border-white/20 shrink-0 font-extrabold text-2xl">
                            <Building2 size={28} />
                        </div>
                        <div>
                            <div className="flex flex-wrap items-center gap-2">
                                <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight">
                                    {summary?.hospital?.name || "Apollo Gleneagles Hospital"}
                                </h1>
                                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-400/30">
                                    {summary?.hospital?.registration_number || "REG-HOSP-001"}
                                </span>
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                                    Operational
                                </span>
                            </div>
                            <div className="flex flex-wrap items-center gap-3 text-xs text-indigo-200/80 mt-1.5">
                                <span>City: <strong className="text-white">{summary?.hospital?.city}</strong></span>
                                <span>•</span>
                                <span>Desk Phone: <strong className="text-white">{summary?.hospital?.phone || "+91 33 2289 4000"}</strong></span>
                                <span>•</span>
                                <span>24x7 Emergency: <strong className="text-rose-300">{summary?.hospital?.emergency_contact || "+91 33 2289 9999"}</strong></span>
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center gap-2 self-start md:self-auto">
                        <button
                            onClick={() => setShowEditHospitalModal(true)}
                            className="px-3.5 py-2 bg-white/10 hover:bg-white/20 text-white font-bold text-xs rounded-xl flex items-center gap-1.5 transition border border-white/15 cursor-pointer"
                        >
                            <Settings size={14} />
                            Facility Settings
                        </button>
                        <button
                            onClick={loadAllData}
                            className="px-3.5 py-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-xl flex items-center gap-1.5 transition cursor-pointer shadow-xs"
                        >
                            <RefreshCw size={14} />
                            Live Sync
                        </button>
                    </div>
                </div>

                {/* KPI METRIC CARDS */}
                <div className="grid grid-cols-2 lg:grid-cols-5 gap-3.5">
                    {/* ICU Beds KPI */}
                    <div onClick={() => setActiveSection("beds")} className="p-4 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 cursor-pointer hover:bg-white/15 transition space-y-1.5">
                        <div className="flex items-center justify-between text-indigo-200">
                            <span className="text-[11px] font-bold uppercase">ICU Capacity</span>
                            <Bed size={15} className="text-blue-300" />
                        </div>
                        <p className="text-2xl font-extrabold text-white">
                            {icuAvail}
                            <span className="text-xs text-indigo-300 font-normal"> / {icuTotal} Ready</span>
                        </p>
                        <div className="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                            <div className="h-full bg-blue-400 rounded-full" style={{ width: `${icuPercent}%` }}></div>
                        </div>
                        <p className="text-[10px] text-indigo-300 font-medium text-right">{icuPercent}% Available</p>
                    </div>

                    {/* ER Beds KPI */}
                    <div onClick={() => setActiveSection("beds")} className="p-4 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 cursor-pointer hover:bg-white/15 transition space-y-1.5">
                        <div className="flex items-center justify-between text-indigo-200">
                            <span className="text-[11px] font-bold uppercase">Trauma / ER Beds</span>
                            <AlertTriangle size={15} className="text-rose-300" />
                        </div>
                        <p className="text-2xl font-extrabold text-rose-300">
                            {erAvail}
                            <span className="text-xs text-indigo-300 font-normal"> / {erTotal} Ready</span>
                        </p>
                        <div className="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
                            <div className="h-full bg-rose-500 rounded-full" style={{ width: `${erPercent}%` }}></div>
                        </div>
                        <p className="text-[10px] text-rose-300 font-medium text-right">{erPercent}% Available</p>
                    </div>

                    {/* Ambulances KPI */}
                    <div onClick={() => setActiveSection("ambulances")} className="p-4 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 cursor-pointer hover:bg-white/15 transition space-y-1.5">
                        <div className="flex items-center justify-between text-indigo-200">
                            <span className="text-[11px] font-bold uppercase">Fleet On Standby</span>
                            <Truck size={15} className="text-emerald-300" />
                        </div>
                        <p className="text-2xl font-extrabold text-emerald-300">
                            {summary?.ambulances?.available || 0}
                            <span className="text-xs text-indigo-300 font-normal"> / {summary?.ambulances?.total || 0} Units</span>
                        </p>
                        <p className="text-[10px] text-emerald-200">GPS Tracked Response Units</p>
                    </div>

                    {/* Incoming Emergencies KPI */}
                    <div onClick={() => setActiveSection("emergencies")} className="p-4 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 cursor-pointer hover:bg-white/15 transition space-y-1.5">
                        <div className="flex items-center justify-between text-indigo-200">
                            <span className="text-[11px] font-bold uppercase">Active Emergencies</span>
                            <HeartPulse size={15} className="text-amber-300" />
                        </div>
                        <p className="text-2xl font-extrabold text-amber-300">
                            {summary?.emergencies?.active || 0}
                            <span className="text-xs text-indigo-300 font-normal"> In-Transit</span>
                        </p>
                        <p className="text-[10px] text-amber-200">Immediate Triage Ready</p>
                    </div>

                    {/* Specialist Doctors on Duty */}
                    <div onClick={() => setActiveSection("doctors")} className="p-4 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 cursor-pointer hover:bg-white/15 transition space-y-1.5">
                        <div className="flex items-center justify-between text-indigo-200">
                            <span className="text-[11px] font-bold uppercase">Doctors On Duty</span>
                            <Stethoscope size={15} className="text-indigo-300" />
                        </div>
                        <p className="text-2xl font-extrabold text-white">
                            {doctors.filter(d => d.is_active).length}
                            <span className="text-xs text-indigo-300 font-normal"> / {doctors.length} Active</span>
                        </p>
                        <p className="text-[10px] text-indigo-200">Consultation OPD Roster</p>
                    </div>
                </div>
            </div>

            {/* TAB SELECTION NAVIGATION */}
            <div className="flex flex-wrap items-center gap-1.5 bg-white border border-slate-200 rounded-2xl p-2.5 shadow-xs">
                <button
                    onClick={() => setActiveSection("beds")}
                    className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                        activeSection === "beds" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                    }`}
                >
                    <Bed size={14} />
                    Bed Inventory ({beds.length})
                </button>

                <button
                    onClick={() => setActiveSection("ambulances")}
                    className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                        activeSection === "ambulances" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                    }`}
                >
                    <Truck size={14} />
                    Ambulance Fleet ({ambulances.length})
                </button>

                <button
                    onClick={() => setActiveSection("emergencies")}
                    className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                        activeSection === "emergencies" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                    }`}
                >
                    <AlertTriangle size={14} />
                    Emergency Queue ({emergencies.length})
                </button>

                <button
                    onClick={() => setActiveSection("appointments")}
                    className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                        activeSection === "appointments" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                    }`}
                >
                    <Calendar size={14} />
                    OPD Appointments ({appointments.length})
                </button>

                <button
                    onClick={() => setActiveSection("doctors")}
                    className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                        activeSection === "doctors" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                    }`}
                >
                    <Stethoscope size={14} />
                    Specialist Doctors ({doctors.length})
                </button>
            </div>

            {/* ============================================================== */}
            {/* TAB 1: BEDS MANAGEMENT & 1-CLICK CAPACITY CONTROLS             */}
            {/* ============================================================== */}
            {activeSection === "beds" && (
                <div className="space-y-6">
                    {/* FAST SIMULATOR BAR */}
                    <div className="bg-slate-900 text-white rounded-2xl p-5 shadow-xs">
                        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                            <div>
                                <h4 className="text-sm font-bold flex items-center gap-2">
                                    <Activity size={16} className="text-blue-400" />
                                    1-Click Real-Time Bed Occupancy Simulator
                                </h4>
                                <p className="text-xs text-slate-300 mt-0.5">
                                    Instantly simulate live admissions or discharges. Immediately updates public patient recommendations and admin metrics.
                                </p>
                            </div>
                            <div className="flex flex-wrap items-center gap-2">
                                <button
                                    onClick={() => handleQuickToggle("ICU", "occupy")}
                                    className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition flex items-center gap-1 cursor-pointer"
                                >
                                    <Plus size={13} /> Occupy 1 ICU
                                </button>
                                <button
                                    onClick={() => handleQuickToggle("ICU", "release")}
                                    className="px-3 py-1.5 rounded-xl bg-indigo-800 hover:bg-indigo-700 text-white text-xs font-bold transition flex items-center gap-1 cursor-pointer border border-indigo-700"
                                >
                                    <Minus size={13} /> Release 1 ICU
                                </button>
                                <button
                                    onClick={() => handleQuickToggle("Emergency", "occupy")}
                                    className="px-3 py-1.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition flex items-center gap-1 cursor-pointer"
                                >
                                    <Plus size={13} /> Occupy 1 ER
                                </button>
                                <button
                                    onClick={() => handleQuickToggle("Emergency", "release")}
                                    className="px-3 py-1.5 rounded-xl bg-rose-800 hover:bg-rose-700 text-white text-xs font-bold transition flex items-center gap-1 cursor-pointer border border-rose-700"
                                >
                                    <Minus size={13} /> Release 1 ER
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* BED TABLE CONTAINER */}
                    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs space-y-4">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                            <div>
                                <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                    <Bed size={18} className="text-blue-600" />
                                    Facility Bed Inventory Roster
                                </h3>
                                <p className="text-xs text-slate-500">
                                    Manage individual bed allocations, wards, floors, and occupancy status.
                                </p>
                            </div>
                            <button
                                onClick={() => setShowAddBedModal(true)}
                                className="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-xs"
                            >
                                <Plus size={14} /> Register New Bed
                            </button>
                        </div>

                        {/* SEARCH & FILTERS BAR */}
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                            <div className="relative flex-1 max-w-sm">
                                <Search size={14} className="absolute left-3 top-2.5 text-slate-400" />
                                <input
                                    type="text"
                                    placeholder="Search bed number, ward, or floor..."
                                    value={bedSearchQuery}
                                    onChange={(e) => setBedSearchQuery(e.target.value)}
                                    className="w-full text-xs pl-8 pr-3 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
                                />
                            </div>

                            <div className="flex items-center gap-2">
                                <span className="text-xs text-slate-500 font-medium">Bed Type:</span>
                                <div className="flex items-center gap-1 text-xs">
                                    {["", "ICU", "Emergency", "General"].map((t) => (
                                        <button
                                            key={t}
                                            onClick={() => setBedTypeFilter(t)}
                                            className={`px-2.5 py-1 rounded-lg font-bold transition cursor-pointer ${
                                                bedTypeFilter === t
                                                    ? "bg-slate-900 text-white shadow-2xs"
                                                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                                            }`}
                                        >
                                            {t === "" ? "All Beds" : t}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* BEDS TABLE */}
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs">
                                <thead>
                                    <tr className="border-b border-slate-200 text-slate-400 uppercase font-bold text-[10px] tracking-wider bg-slate-50/60">
                                        <th className="py-3 px-3.5">Bed Number</th>
                                        <th className="py-3 px-3.5">Category</th>
                                        <th className="py-3 px-3.5">Ward & Location</th>
                                        <th className="py-3 px-3.5">Status</th>
                                        <th className="py-3 px-3.5">Clinical Equipment Notes</th>
                                        <th className="py-3 px-3.5 text-right">Action</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100">
                                    {filteredBeds.length === 0 ? (
                                        <tr>
                                            <td colSpan={6} className="py-8 text-center text-slate-400">
                                                No beds match the filter criteria.
                                            </td>
                                        </tr>
                                    ) : (
                                        filteredBeds.map((b) => (
                                            <tr key={b.id} className="hover:bg-slate-50/70 transition">
                                                <td className="py-3 px-3.5 font-mono font-bold text-slate-900 text-sm">
                                                    {b.bed_number}
                                                </td>
                                                <td className="py-3 px-3.5">
                                                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                                                        b.bed_type === "ICU" ? "bg-indigo-100 text-indigo-800" :
                                                        b.bed_type === "Emergency" ? "bg-rose-100 text-rose-800" : "bg-slate-100 text-slate-800"
                                                    }`}>
                                                        {b.bed_type}
                                                    </span>
                                                </td>
                                                <td className="py-3 px-3.5 text-slate-700">
                                                    <span className="font-semibold">{b.ward}</span>
                                                    <span className="text-slate-400 block text-[11px]">{b.floor || "Floor 1"} • Room {b.room_number || "Main"}</span>
                                                </td>
                                                <td className="py-3 px-3.5">
                                                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-extrabold flex items-center gap-1.5 w-fit ${
                                                        b.status === "Available"
                                                            ? "bg-emerald-100 text-emerald-800 border border-emerald-200"
                                                            : b.status === "Occupied"
                                                            ? "bg-rose-100 text-rose-800 border border-rose-200"
                                                            : "bg-amber-100 text-amber-800 border border-amber-200"
                                                    }`}>
                                                        <span className={`w-1.5 h-1.5 rounded-full ${
                                                            b.status === "Available" ? "bg-emerald-500 animate-pulse" : b.status === "Occupied" ? "bg-rose-500" : "bg-amber-500"
                                                        }`}></span>
                                                        {b.status}
                                                    </span>
                                                </td>
                                                <td className="py-3 px-3.5 text-slate-500 max-w-xs truncate">
                                                    {b.notes || "Standard monitor setup"}
                                                </td>
                                                <td className="py-3 px-3.5 text-right space-x-1.5">
                                                    {b.status === "Available" ? (
                                                        <button
                                                            onClick={() => handleBedStatusUpdate(b.id, "Occupied")}
                                                            className="px-2.5 py-1 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 text-[11px] font-bold border border-rose-200 transition cursor-pointer"
                                                        >
                                                            Mark Occupied
                                                        </button>
                                                    ) : (
                                                        <button
                                                            onClick={() => handleBedStatusUpdate(b.id, "Available")}
                                                            className="px-2.5 py-1 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-700 text-[11px] font-bold border border-emerald-200 transition cursor-pointer"
                                                        >
                                                            Release / Ready
                                                        </button>
                                                    )}
                                                    <button
                                                        onClick={() => handleDeleteBed(b.id, b.bed_number)}
                                                        className="p-1 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition cursor-pointer"
                                                        title="Remove Bed"
                                                    >
                                                        <Trash2 size={13} />
                                                    </button>
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* TAB 2: AMBULANCE FLEET MANAGEMENT                              */}
            {/* ============================================================== */}
            {activeSection === "ambulances" && (
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                        <div>
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Truck size={18} className="text-emerald-600" />
                                Hospital Emergency Ambulance Fleet
                            </h3>
                            <p className="text-xs text-slate-500">
                                Monitor paramedic crews, vehicle equipment tiers, and toggle readiness for live patient emergency calls.
                            </p>
                        </div>
                        <button
                            onClick={() => setShowAddAmbulanceModal(true)}
                            className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-xs"
                        >
                            <Plus size={14} /> Register New Ambulance
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {ambulances.map((amb) => (
                            <div key={amb.id} className="p-4 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:border-emerald-200 hover:shadow-xs transition space-y-3">
                                <div className="flex items-start justify-between">
                                    <div>
                                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-700">
                                            {amb.ambulance_type}
                                        </span>
                                        <h4 className="text-sm font-bold font-mono text-slate-900 mt-1">
                                            {amb.registration_number}
                                        </h4>
                                    </div>
                                    <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                                        amb.availability_status === "Available"
                                            ? "bg-emerald-100 text-emerald-800 border border-emerald-200"
                                            : amb.availability_status === "On Duty"
                                            ? "bg-rose-100 text-rose-800 border border-rose-200"
                                            : "bg-slate-200 text-slate-700"
                                    }`}>
                                        ● {amb.availability_status}
                                    </span>
                                </div>

                                <div className="text-xs space-y-1 bg-white p-3 rounded-xl border border-slate-200/70">
                                    <p className="text-slate-600">
                                        Crew Driver: <strong className="text-slate-900">{amb.driver_name}</strong>
                                    </p>
                                    <p className="text-slate-600">
                                        Helpline: <strong className="text-slate-800">{amb.driver_phone}</strong>
                                    </p>
                                    <p className="text-slate-500 text-[11px] flex items-center gap-1 mt-1">
                                        <MapPin size={11} /> {amb.current_location || "Hospital Bay"}
                                    </p>
                                </div>

                                <div className="pt-2 flex items-center justify-end gap-2">
                                    <button
                                        onClick={() => handleAmbulanceStatus(amb.id, "Available")}
                                        className="px-2.5 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-lg text-xs font-bold border border-emerald-200 transition cursor-pointer"
                                    >
                                        Set Standby (Available)
                                    </button>
                                    <button
                                        onClick={() => handleAmbulanceStatus(amb.id, "On Duty")}
                                        className="px-2.5 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-lg text-xs font-bold border border-rose-200 transition cursor-pointer"
                                    >
                                        Set On Duty (Dispatched)
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* TAB 3: INCOMING EMERGENCY TRIAGE QUEUE                         */}
            {/* ============================================================== */}
            {activeSection === "emergencies" && (
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                        <div>
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <AlertTriangle size={18} className="text-rose-600" />
                                Active Emergency Triage & Ambulance Dispatch Board
                            </h3>
                            <p className="text-xs text-slate-500">
                                Review live patient SOS dispatch calls, assigned response units, and transition triage status.
                            </p>
                        </div>
                    </div>

                    {emergencies.length === 0 ? (
                        <div className="p-12 text-center text-slate-400 space-y-2">
                            <ShieldCheck size={32} className="mx-auto text-emerald-500" />
                            <h4 className="text-sm font-bold text-slate-800">No Active Emergency Alerts</h4>
                            <p className="text-xs text-slate-500">All emergency dispatches are resolved. Ready for new calls.</p>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {emergencies.map((e) => (
                                <div key={e.id} className="p-4 rounded-2xl border-2 border-rose-200 bg-rose-50/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                                    <div className="space-y-1">
                                        <div className="flex items-center gap-2">
                                            <span className="px-2.5 py-0.5 rounded text-[10px] font-extrabold bg-rose-600 text-white uppercase tracking-wider">
                                                {e.priority} PRIORITY
                                            </span>
                                            <h4 className="text-sm font-bold text-slate-900">{e.emergency_type}</h4>
                                        </div>
                                        <p className="text-xs text-slate-600">
                                            Patient / Caller: <strong>{e.patient_name}</strong> • Pickup: <strong>{e.pickup_location}</strong>
                                        </p>
                                        <p className="text-[11px] text-slate-400">
                                            Assigned Unit: <span className="font-mono font-bold text-slate-700">{e.ambulance_reg || "Standby ALS"}</span> • Alert Logged: {e.created_at}
                                        </p>
                                    </div>

                                    <div className="flex items-center gap-2.5 shrink-0">
                                        <span className="px-3 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-800 border border-blue-200">
                                            {e.status}
                                        </span>
                                        <select
                                            value={e.status}
                                            onChange={(ev) => handleEmergencyStatus(e.id, ev.target.value)}
                                            className="text-xs border border-slate-300 rounded-xl p-2 font-bold bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
                                        >
                                            <option value="Requested">1. Requested</option>
                                            <option value="Dispatched">2. Dispatched</option>
                                            <option value="Arrived">3. Arrived</option>
                                            <option value="Admitted">4. Admitted to ER</option>
                                            <option value="Resolved">5. Resolved</option>
                                        </select>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {/* ============================================================== */}
            {/* TAB 4: OPD APPOINTMENTS                                        */}
            {/* ============================================================== */}
            {activeSection === "appointments" && (
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                        <div>
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Calendar size={18} className="text-blue-600" />
                                Hospital OPD Doctor Consultations
                            </h3>
                            <p className="text-xs text-slate-500">
                                Manage scheduled patient visits, doctor consultation status, and completion records.
                            </p>
                        </div>
                    </div>

                    {/* APPOINTMENT SEARCH & FILTER CHIPS */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div className="relative flex-1 max-w-sm">
                            <Search size={14} className="absolute left-3 top-2.5 text-slate-400" />
                            <input
                                type="text"
                                placeholder="Search patient, doctor, or reason..."
                                value={apptSearchQuery}
                                onChange={(e) => setApptSearchQuery(e.target.value)}
                                className="w-full text-xs pl-8 pr-3 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
                            />
                        </div>

                        <div className="flex items-center gap-1.5 text-xs">
                            {["all", "Scheduled", "Completed", "Cancelled"].map((f) => (
                                <button
                                    key={f}
                                    onClick={() => setApptFilter(f)}
                                    className={`px-3 py-1 rounded-xl font-bold transition cursor-pointer ${
                                        apptFilter === f ? "bg-slate-900 text-white shadow-2xs" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                                    }`}
                                >
                                    {f === "all" ? `All (${appointments.length})` : f}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* APPOINTMENTS LIST */}
                    {filteredAppointments.length === 0 ? (
                        <div className="p-12 text-center text-slate-400 space-y-2">
                            <Calendar size={32} className="mx-auto text-slate-300" />
                            <p className="text-xs">No OPD appointments matching the selected filter.</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {filteredAppointments.map((a) => (
                                <div key={a.id} className="p-4 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:border-blue-200 hover:shadow-xs transition space-y-3">
                                    <div className="flex items-start justify-between">
                                        <div>
                                            <h4 className="text-sm font-bold text-slate-900">{a.patient_name}</h4>
                                            <p className="text-xs text-blue-700 font-semibold mt-0.5">
                                                Attending: {a.doctor_name} ({a.doctor_specialization})
                                            </p>
                                        </div>
                                        <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                                            a.status === "Scheduled" ? "bg-blue-100 text-blue-800" :
                                            a.status === "Completed" ? "bg-emerald-100 text-emerald-800" : "bg-slate-200 text-slate-600"
                                        }`}>
                                            {a.status}
                                        </span>
                                    </div>

                                    <div className="grid grid-cols-2 gap-2 text-xs p-3 rounded-xl bg-white border border-slate-200/70">
                                        <div>
                                            <span className="text-[10px] text-slate-400 font-bold uppercase block">Date & Slot</span>
                                            <span className="font-semibold text-slate-800">{a.date} ({a.time})</span>
                                        </div>
                                        <div>
                                            <span className="text-[10px] text-slate-400 font-bold uppercase block">Payment Status</span>
                                            <span className="font-bold text-emerald-600">{a.payment_status || "Paid"}</span>
                                        </div>
                                        <div className="col-span-2 pt-1 border-t border-slate-100">
                                            <span className="text-[10px] text-slate-400 font-bold uppercase block">Visit Reason</span>
                                            <span className="text-slate-700">{a.reason || "General OPD"}</span>
                                        </div>
                                    </div>

                                    <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-100">
                                        <div className="flex items-center gap-1.5">
                                            {a.has_prescription ? (
                                                <>
                                                    <button
                                                        onClick={() => handleOpenViewRxModal(a)}
                                                        className="px-2.5 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 text-xs font-bold rounded-xl transition cursor-pointer flex items-center gap-1.5 shadow-2xs"
                                                    >
                                                        <CheckCircle2 size={13} className="text-emerald-600" />
                                                        <span>View e-Rx</span>
                                                    </button>
                                                    <button
                                                        onClick={() => handleOpenRxModal(a)}
                                                        className="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-xl transition cursor-pointer flex items-center gap-1"
                                                        title="Edit Prescription"
                                                    >
                                                        <Edit3 size={12} />
                                                        <span>Edit</span>
                                                    </button>
                                                </>
                                            ) : (
                                                <button
                                                    onClick={() => handleOpenRxModal(a)}
                                                    className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition cursor-pointer flex items-center gap-1.5 shadow-xs"
                                                >
                                                    <FileText size={13} />
                                                    <span>Issue e-Rx</span>
                                                </button>
                                            )}
                                        </div>

                                        <div className="flex items-center gap-1.5">
                                            {a.status === "Scheduled" && (
                                                <>
                                                    <button
                                                        onClick={() => handleAppointmentStatus(a.id, "Completed")}
                                                        className="px-2.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl transition shadow-2xs cursor-pointer"
                                                    >
                                                        Mark Done
                                                    </button>
                                                    <button
                                                        onClick={() => handleAppointmentStatus(a.id, "Cancelled")}
                                                        className="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
                                                    >
                                                        Cancel
                                                    </button>
                                                </>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {/* ============================================================== */}
            {/* TAB 5: SPECIALIST DOCTORS ON DUTY                              */}
            {/* ============================================================== */}
            {activeSection === "doctors" && (
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                        <div>
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Stethoscope size={18} className="text-indigo-600" />
                                Facility Specialist Doctors & Duty Roster
                            </h3>
                            <p className="text-xs text-slate-500">
                                Manage specialist doctor profiles, OPD consulting fees, and toggle active duty availability.
                            </p>
                        </div>
                        <button
                            onClick={() => setShowAddDoctorModal(true)}
                            className="px-3.5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-xs"
                        >
                            <Plus size={14} /> Add Specialist Doctor
                        </button>
                    </div>

                    {/* SEARCH DOCTOR INPUT */}
                    <div className="relative max-w-sm">
                        <Search size={14} className="absolute left-3 top-2.5 text-slate-400" />
                        <input
                            type="text"
                            placeholder="Search doctor by name or specialization..."
                            value={doctorSearchQuery}
                            onChange={(e) => setDoctorSearchQuery(e.target.value)}
                            className="w-full text-xs pl-8 pr-3 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-hidden"
                        />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {filteredDoctors.map((doc) => (
                            <div key={doc.id} className="p-4 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:border-indigo-200 hover:shadow-xs transition space-y-3">
                                <div className="flex items-start justify-between">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-bold text-sm shadow-xs">
                                            {doc.full_name.split(" ").map(w => w[0]).join("").slice(0, 2)}
                                        </div>
                                        <div>
                                            <h4 className="text-sm font-bold text-slate-900">{doc.full_name}</h4>
                                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-800">
                                                {doc.specialization}
                                            </span>
                                        </div>
                                    </div>

                                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                                        doc.is_active ? "bg-emerald-100 text-emerald-800" : "bg-slate-200 text-slate-600"
                                    }`}>
                                        {doc.is_active ? "On Duty" : "Off Duty"}
                                    </span>
                                </div>

                                <div className="p-3 bg-white rounded-xl border border-slate-200/70 text-xs space-y-1">
                                    <p className="text-slate-600">Qualification: <strong>{doc.qualification}</strong></p>
                                    <p className="text-slate-600">Experience: <strong>{doc.experience} Years</strong></p>
                                    <p className="text-slate-600">Phone: <strong>{doc.phone}</strong></p>
                                    <p className="text-slate-900 font-bold pt-1 border-t border-slate-100">
                                        Consultation Fee: <span className="text-blue-600 font-extrabold">₹{doc.consultation_fee}</span>
                                    </p>
                                </div>

                                <div className="pt-1 flex items-center justify-end">
                                    <button
                                        onClick={() => handleToggleDoctorActive(doc.id, doc.is_active)}
                                        className={`px-3 py-1.5 rounded-xl text-xs font-bold transition cursor-pointer ${
                                            doc.is_active
                                                ? "bg-slate-100 hover:bg-slate-200 text-slate-700"
                                                : "bg-emerald-600 hover:bg-emerald-700 text-white shadow-2xs"
                                        }`}
                                    >
                                        {doc.is_active ? "Mark Off Duty" : "Set Active On Duty"}
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 1: REGISTER NEW BED                                      */}
            {/* ============================================================== */}
            {showAddBedModal && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Bed size={18} className="text-blue-600" />
                                Register New Facility Bed
                            </h3>
                            <button onClick={() => setShowAddBedModal(false)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        <form onSubmit={handleCreateBed} className="space-y-3.5">
                            <div>
                                <label className="block text-xs font-semibold text-slate-700 mb-1">
                                    Bed Number / Identifier <span className="text-rose-500">*</span>
                                </label>
                                <input
                                    type="text"
                                    required
                                    placeholder="e.g. ICU-B-09, ER-14, GEN-32"
                                    value={newBedData.bed_number}
                                    onChange={(e) => setNewBedData({ ...newBedData, bed_number: e.target.value })}
                                    className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-hidden font-mono font-bold"
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Bed Category</label>
                                    <select
                                        value={newBedData.bed_type}
                                        onChange={(e) => setNewBedData({ ...newBedData, bed_type: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white font-semibold"
                                    >
                                        <option value="ICU">ICU Bed</option>
                                        <option value="Emergency">Emergency Bed</option>
                                        <option value="General">General Bed</option>
                                        <option value="Pediatric">Pediatric Bed</option>
                                    </select>
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Floor</label>
                                    <input
                                        type="text"
                                        value={newBedData.floor}
                                        onChange={(e) => setNewBedData({ ...newBedData, floor: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-xs font-semibold text-slate-700 mb-1">Ward Name</label>
                                <input
                                    type="text"
                                    value={newBedData.ward}
                                    onChange={(e) => setNewBedData({ ...newBedData, ward: e.target.value })}
                                    className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-semibold text-slate-700 mb-1">Equipment / Clinical Notes</label>
                                <input
                                    type="text"
                                    value={newBedData.notes}
                                    onChange={(e) => setNewBedData({ ...newBedData, notes: e.target.value })}
                                    placeholder="e.g. Ventilator & Multi-para monitor equipped"
                                    className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                />
                            </div>

                            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                                <button
                                    type="button"
                                    onClick={() => setShowAddBedModal(false)}
                                    className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition cursor-pointer shadow-xs"
                                >
                                    Add Bed to Inventory
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 2: REGISTER NEW AMBULANCE                                */}
            {/* ============================================================== */}
            {showAddAmbulanceModal && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Truck size={18} className="text-emerald-600" />
                                Register Emergency Ambulance
                            </h3>
                            <button onClick={() => setShowAddAmbulanceModal(false)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        <form onSubmit={handleCreateAmbulance} className="space-y-3.5">
                            <div>
                                <label className="block text-xs font-semibold text-slate-700 mb-1">
                                    Vehicle Registration Number <span className="text-rose-500">*</span>
                                </label>
                                <input
                                    type="text"
                                    required
                                    placeholder="e.g. WB-02-AMB-2026"
                                    value={newAmbulanceData.registration_number}
                                    onChange={(e) => setNewAmbulanceData({ ...newAmbulanceData, registration_number: e.target.value })}
                                    className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500 font-mono font-bold"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-semibold text-slate-700 mb-1">Ambulance Tier</label>
                                <select
                                    value={newAmbulanceData.ambulance_type}
                                    onChange={(e) => setNewAmbulanceData({ ...newAmbulanceData, ambulance_type: e.target.value })}
                                    className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white font-semibold"
                                >
                                    <option value="Advanced Life Support (ALS)">Advanced Life Support (ALS) with Ventilator</option>
                                    <option value="Basic Life Support (BLS)">Basic Life Support (BLS) with Oxygen</option>
                                    <option value="Neonatal Ambulance">Neonatal Critical Ambulance</option>
                                </select>
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Driver Name</label>
                                    <input
                                        type="text"
                                        value={newAmbulanceData.driver_name}
                                        onChange={(e) => setNewAmbulanceData({ ...newAmbulanceData, driver_name: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Driver Phone</label>
                                    <input
                                        type="tel"
                                        value={newAmbulanceData.driver_phone}
                                        onChange={(e) => setNewAmbulanceData({ ...newAmbulanceData, driver_phone: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>
                            </div>

                            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                                <button
                                    type="button"
                                    onClick={() => setShowAddAmbulanceModal(false)}
                                    className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl transition cursor-pointer shadow-xs"
                                >
                                    Register Ambulance Unit
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 3: ADD SPECIALIST DOCTOR                                 */}
            {/* ============================================================== */}
            {showAddDoctorModal && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Stethoscope size={18} className="text-indigo-600" />
                                Add Specialist Doctor
                            </h3>
                            <button onClick={() => setShowAddDoctorModal(false)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        <form onSubmit={handleCreateDoctor} className="space-y-3.5">
                            <div>
                                <label className="block text-xs font-semibold text-slate-700 mb-1">
                                    Doctor Full Name <span className="text-rose-500">*</span>
                                </label>
                                <input
                                    type="text"
                                    required
                                    placeholder="e.g. Dr. Priya Mukherjee"
                                    value={newDoctorData.full_name}
                                    onChange={(e) => setNewDoctorData({ ...newDoctorData, full_name: e.target.value })}
                                    className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 font-bold"
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Email <span className="text-rose-500">*</span></label>
                                    <input
                                        type="email"
                                        required
                                        placeholder="doctor@hospital.com"
                                        value={newDoctorData.email}
                                        onChange={(e) => setNewDoctorData({ ...newDoctorData, email: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Phone</label>
                                    <input
                                        type="tel"
                                        value={newDoctorData.phone}
                                        onChange={(e) => setNewDoctorData({ ...newDoctorData, phone: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Clinical Department</label>
                                    <select
                                        value={newDoctorData.specialization}
                                        onChange={(e) => setNewDoctorData({ ...newDoctorData, specialization: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white font-semibold"
                                    >
                                        <option value="Cardiology">Cardiology</option>
                                        <option value="Orthopedics">Orthopedics</option>
                                        <option value="Neurology">Neurology</option>
                                        <option value="Pulmonology">Pulmonology</option>
                                        <option value="Gastroenterology">Gastroenterology</option>
                                        <option value="Pediatrics">Pediatrics</option>
                                        <option value="General Medicine">General Medicine</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Consultation Fee (₹)</label>
                                    <input
                                        type="number"
                                        value={newDoctorData.consultation_fee}
                                        onChange={(e) => setNewDoctorData({ ...newDoctorData, consultation_fee: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-bold text-blue-600"
                                    />
                                </div>
                            </div>

                            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                                <button
                                    type="button"
                                    onClick={() => setShowAddDoctorModal(false)}
                                    className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl transition cursor-pointer shadow-xs"
                                >
                                    Add Doctor to Roster
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 4: FACILITY SETTINGS & CONTACT DETAILS                   */}
            {/* ============================================================== */}
            {showEditHospitalModal && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                <Settings size={18} className="text-slate-700" />
                                Facility Information & Emergency Contacts
                            </h3>
                            <button onClick={() => setShowEditHospitalModal(false)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        <form onSubmit={handleSaveHospitalInfo} className="space-y-3.5">
                            <div>
                                <label className="block text-xs font-semibold text-slate-700 mb-1">Hospital / Clinic Name</label>
                                <input
                                    type="text"
                                    required
                                    value={hospitalFormData.name}
                                    onChange={(e) => setHospitalFormData({ ...hospitalFormData, name: e.target.value })}
                                    className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-bold"
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Reception Phone</label>
                                    <input
                                        type="tel"
                                        value={hospitalFormData.phone}
                                        onChange={(e) => setHospitalFormData({ ...hospitalFormData, phone: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">24x7 Emergency SOS</label>
                                    <input
                                        type="tel"
                                        value={hospitalFormData.emergency_contact}
                                        onChange={(e) => setHospitalFormData({ ...hospitalFormData, emergency_contact: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl font-bold text-rose-600"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-xs font-semibold text-slate-700 mb-1">City</label>
                                <input
                                    type="text"
                                    value={hospitalFormData.city}
                                    onChange={(e) => setHospitalFormData({ ...hospitalFormData, city: e.target.value })}
                                    className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                />
                            </div>

                            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                                <button
                                    type="button"
                                    onClick={() => setShowEditHospitalModal(false)}
                                    className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition cursor-pointer shadow-xs"
                                >
                                    Save Facility Details
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 5: ISSUE DIGITAL PRESCRIPTION (e-Rx)                     */}
            {/* ============================================================== */}
            {showRxModal && selectedApptForRx && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 overflow-y-auto">
                    <div className="bg-white rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-4 my-8">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2.5">
                                <div className="w-9 h-9 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center">
                                    <FileText size={20} />
                                </div>
                                <div>
                                    <h3 className="text-base font-bold text-slate-900">Issue Electronic Prescription (e-Rx)</h3>
                                    <p className="text-xs text-slate-500">
                                        Patient: <strong className="text-slate-800">{selectedApptForRx.patient_name}</strong> • Doctor: <strong>{selectedApptForRx.doctor_name}</strong>
                                    </p>
                                </div>
                            </div>
                            <button onClick={() => setShowRxModal(false)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={20} />
                            </button>
                        </div>

                        <form onSubmit={handleSavePrescription} className="space-y-4">
                            <div className="bg-blue-50/70 border border-blue-100 rounded-xl p-3 text-xs text-blue-900 flex items-center justify-between">
                                <div>
                                    <span className="font-bold">Consultation Slot:</span> {selectedApptForRx.date} ({selectedApptForRx.time})
                                </div>
                                <div>
                                    <span className="font-bold">Chief Complaint:</span> {selectedApptForRx.reason || "Outpatient Clinical Consult"}
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                                <div className="md:col-span-2">
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Clinical Diagnosis <span className="text-rose-500">*</span>
                                    </label>
                                    <input
                                        type="text"
                                        required
                                        placeholder="e.g. Acute Bronchitis / Hypertension Stage 1"
                                        value={rxData.diagnosis}
                                        onChange={(e) => setRxData({ ...rxData, diagnosis: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 font-semibold"
                                    />
                                </div>

                                <div className="md:col-span-2">
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Prescribed Medicines & Formulations <span className="text-rose-500">*</span>
                                    </label>
                                    <textarea
                                        rows={2}
                                        required
                                        placeholder="e.g. Tab Azithromycin 500mg, Tab Paracetamol 650mg, Tab Pantoprazole 40mg"
                                        value={rxData.medicines}
                                        onChange={(e) => setRxData({ ...rxData, medicines: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Dosage Regimen
                                    </label>
                                    <input
                                        type="text"
                                        placeholder="e.g. 1-0-1 (Morning & Night)"
                                        value={rxData.dosage}
                                        onChange={(e) => setRxData({ ...rxData, dosage: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Treatment Duration
                                    </label>
                                    <input
                                        type="text"
                                        placeholder="e.g. 5 Days / 14 Days"
                                        value={rxData.duration}
                                        onChange={(e) => setRxData({ ...rxData, duration: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>

                                <div className="md:col-span-2">
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Patient Instructions & Administration Advice
                                    </label>
                                    <input
                                        type="text"
                                        placeholder="e.g. Take after meals with warm water. Avoid cold beverages and oily food."
                                        value={rxData.instructions}
                                        onChange={(e) => setRxData({ ...rxData, instructions: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Advised Diagnostic / Lab Tests (Optional)
                                    </label>
                                    <input
                                        type="text"
                                        placeholder="e.g. CBC, Serum Creatinine, Chest X-Ray"
                                        value={rxData.lab_tests}
                                        onChange={(e) => setRxData({ ...rxData, lab_tests: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Follow-Up Date (Optional)
                                    </label>
                                    <input
                                        type="date"
                                        value={rxData.follow_up_date}
                                        onChange={(e) => setRxData({ ...rxData, follow_up_date: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>

                                <div className="md:col-span-2">
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Clinical Notes & Lifestyle Precautions
                                    </label>
                                    <input
                                        type="text"
                                        placeholder="e.g. Strict bed rest for 48 hours, monitor SpO2 and temperature"
                                        value={rxData.notes}
                                        onChange={(e) => setRxData({ ...rxData, notes: e.target.value })}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl"
                                    />
                                </div>
                            </div>

                            <div className="flex items-center justify-between pt-3 border-t border-slate-100">
                                <span className="text-[11px] text-slate-500">
                                    ✓ Instantly uploaded to patient's MediLink electronic health record
                                </span>
                                <div className="flex items-center gap-2">
                                    <button
                                        type="button"
                                        onClick={() => setShowRxModal(false)}
                                        className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        type="submit"
                                        className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition cursor-pointer shadow-xs flex items-center gap-1.5"
                                    >
                                        <CheckCircle2 size={14} />
                                        Sign & Issue e-Rx
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* MODAL 6: VIEW DIGITAL PRESCRIPTION                             */}
            {/* ============================================================== */}
            {showViewRxModal && selectedApptForRx && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 overflow-y-auto">
                    <div className="bg-white rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-4 my-8 border border-slate-200">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-8 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">
                                    ℞
                                </div>
                                <div>
                                    <h3 className="text-base font-bold text-slate-900">Official Electronic Prescription</h3>
                                    <p className="text-[11px] text-slate-500">MediLink Digital Health Record System</p>
                                </div>
                            </div>
                            <button onClick={() => setShowViewRxModal(false)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={20} />
                            </button>
                        </div>

                        <div className="space-y-4 text-xs">
                            <div className="grid grid-cols-2 gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
                                <div>
                                    <span className="text-[10px] text-slate-400 font-bold uppercase block">Patient</span>
                                    <span className="font-bold text-slate-900">{selectedApptForRx.patient_name}</span>
                                </div>
                                <div>
                                    <span className="text-[10px] text-slate-400 font-bold uppercase block">Attending Doctor</span>
                                    <span className="font-bold text-slate-900">{selectedApptForRx.doctor_name} ({selectedApptForRx.doctor_specialization})</span>
                                </div>
                                <div>
                                    <span className="text-[10px] text-slate-400 font-bold uppercase block">Date & Slot</span>
                                    <span className="text-slate-700 font-semibold">{selectedApptForRx.date} ({selectedApptForRx.time})</span>
                                </div>
                                <div>
                                    <span className="text-[10px] text-slate-400 font-bold uppercase block">Status</span>
                                    <span className="text-emerald-700 font-bold">✓ Signed & Verified</span>
                                </div>
                            </div>

                            {selectedApptForRx.prescription ? (
                                <div className="space-y-3">
                                    <div className="p-3 bg-blue-50/60 rounded-xl border border-blue-100">
                                        <span className="text-[10px] text-blue-700 font-bold uppercase block">Diagnosis</span>
                                        <p className="text-slate-900 font-bold mt-0.5">{selectedApptForRx.prescription.diagnosis || "Clinical Consult"}</p>
                                    </div>

                                    <div className="p-3 bg-white rounded-xl border border-slate-200 space-y-2">
                                        <span className="text-[10px] text-slate-400 font-bold uppercase block">Prescribed Medication</span>
                                        <p className="text-slate-800 font-semibold">{selectedApptForRx.prescription.medicines}</p>
                                        <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100 text-[11px]">
                                            <div>
                                                <span className="text-slate-400">Dosage:</span> <strong className="text-slate-700">{selectedApptForRx.prescription.dosage || "1-0-1"}</strong>
                                            </div>
                                            <div>
                                                <span className="text-slate-400">Duration:</span> <strong className="text-slate-700">{selectedApptForRx.prescription.duration || "5 Days"}</strong>
                                            </div>
                                        </div>
                                    </div>

                                    {selectedApptForRx.prescription.instructions && (
                                        <div className="p-3 bg-amber-50/60 rounded-xl border border-amber-100">
                                            <span className="text-[10px] text-amber-800 font-bold uppercase block">Instructions</span>
                                            <p className="text-amber-900 text-xs mt-0.5">{selectedApptForRx.prescription.instructions}</p>
                                        </div>
                                    )}

                                    {selectedApptForRx.prescription.follow_up_date && (
                                        <div className="flex items-center justify-between p-2.5 bg-slate-50 rounded-xl text-xs">
                                            <span className="text-slate-500 font-semibold">Recommended Follow-up:</span>
                                            <span className="font-bold text-blue-700">{selectedApptForRx.prescription.follow_up_date}</span>
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <p className="text-slate-400 text-center py-4">No prescription record found.</p>
                            )}

                            <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                                <span className="text-[11px] text-emerald-600 font-semibold flex items-center gap-1">
                                    <ShieldCheck size={14} /> Tamper-evident Digital Health Record
                                </span>
                                <button
                                    onClick={() => setShowViewRxModal(false)}
                                    className="px-4 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl transition cursor-pointer"
                                >
                                    Close
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
