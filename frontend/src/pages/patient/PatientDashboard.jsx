import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
    MapPin, Search, Navigation, AlertTriangle, ShieldCheck,
    Stethoscope, Clock, Phone, Calendar, HeartPulse, Building2,
    Bed, CheckCircle2, ChevronRight, X, PhoneCall, LogIn, UserPlus,
    ExternalLink, Sparkles, Filter, ArrowUpDown, Truck, Activity,
    FileText, Receipt, QrCode, Download, Printer, UserCircle, Pill,
    AlertCircle, Check, Map, Eye, PlusCircle, ArrowRight, User,
    Edit3, Save, Award, CheckCheck, HelpCircle, ChevronDown, ChevronUp,
    Zap, Shield, Heart, Smile, Flame, ShieldAlert, PhoneForwarded, Lock, Loader2
} from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import recommendationService from "../../services/recommendationService";
import patientService from "../../services/patientService";

const PRESET_CITIES = [
    { name: "Kolkata", lat: 22.5726, lng: 88.3639 },
    { name: "New Delhi", lat: 28.6139, lng: 77.2090 },
    { name: "Mumbai", lat: 19.0760, lng: 72.8777 },
    { name: "Bengaluru", lat: 12.9716, lng: 77.5946 },
    { name: "Chennai", lat: 13.0827, lng: 80.2707 },
    { name: "Hyderabad", lat: 17.3850, lng: 78.4867 },
    { name: "Pune", lat: 18.5204, lng: 73.8567 },
    { name: "Jaipur", lat: 26.9124, lng: 75.7873 },
    { name: "Lucknow", lat: 26.8467, lng: 80.9462 },
    { name: "Chandigarh", lat: 30.7333, lng: 76.7794 }
];

const SAMPLE_SYMPTOMS = [
    { label: "🫀 Chest pain & sweating", text: "Severe chest pain radiating to left arm with excessive sweating and tightness" },
    { label: "🧠 Dizziness & slurred speech", text: "Sudden onset dizziness, blurred vision and facial weakness" },
    { label: "🦴 Knee swelling & fracture pain", text: "Severe knee joint pain, acute swelling and inability to bear weight" },
    { label: "🫁 Wheezing & breathlessness", text: "Continuous cough with wheezing, difficulty breathing and chest congestion" },
    { label: "🤢 Acid reflux & stomach ache", text: "Persistent upper abdominal pain with acute nausea and burning sensation" }
];

const CLINICAL_SPECIALTIES = [
    { name: "Cardiology", label: "Heart & Vascular", icon: "🫀", badge: "Critical Ready" },
    { name: "Neurology", label: "Brain & Nerves", icon: "🧠", badge: "Stroke Ready" },
    { name: "Orthopedics", label: "Bones & Joints", icon: "🦴", badge: "Trauma Units" },
    { name: "Pediatrics", label: "Child Health", icon: "👶", badge: "NICU/PICU" },
    { name: "Emergency Medicine", label: "Acute Trauma", icon: "🚨", badge: "24x7 Ready" },
    { name: "General Medicine", label: "Primary Care", icon: "🩺", badge: "OPD Available" },
    { name: "Oncology", label: "Cancer Care", icon: "🔬", badge: "Specialist Care" },
    { name: "Pulmonology", label: "Lungs & Chest", icon: "🫁", badge: "Ventilator Ready" },
];

const FAQ_ITEMS = [
    {
        q: "How does MediLink verify live ICU and emergency bed availability?",
        a: "MediLink connects directly with partner hospital ward admission systems. Bed statuses (ICU, Emergency Trauma, General) are synchronized via real-time WebSocket buffers every 15 seconds, eliminating the need to call hospitals during critical moments."
    },
    {
        q: "Can I request an ambulance without registering or logging in?",
        a: "Yes. In an emergency, every second counts. MediLink provides zero-login 1-click ambulance dispatch with GPS landmark auto-detection. Paramedic units from the nearest facility are mobilized immediately."
    },
    {
        q: "How does the AI Symptom Triage work?",
        a: "Our machine learning engine utilizes TF-IDF vectorization and multiclass classification trained on over 5,000 verified clinical cases. It maps your plain-language symptoms to the appropriate clinical department with confidence scoring and flags critical emergencies."
    },
    {
        q: "Is MediLink integrated with Ayushman Bharat Digital Mission (ABDM)?",
        a: "Yes. All digital prescriptions and consultation tokens can be linked with your national Ayushman Bharat Health Account (ABHA), enabling secure electronic health record (EHR) portability across India."
    },
    {
        q: "What should I do if my city is not listed in the popular presets?",
        a: "Use the 'GPS Auto-Detect' button or expand the proximity radius slider up to 150 km. MediLink monitors healthcare facilities across both major metros and tier-2 regional centers."
    }
];

export default function PatientDashboard() {
    const { user } = useAuth();
    const navigate = useNavigate();

    // Homepage FAQ State
    const [openFaq, setOpenFaq] = useState(null);
    const toggleFaq = (idx) => setOpenFaq(openFaq === idx ? null : idx);

    // Location & Filters
    const [selectedCity, setSelectedCity] = useState("Kolkata");
    const [coordinates, setCoordinates] = useState({ lat: 22.5726, lng: 88.3639 });
    const [radiusKm, setRadiusKm] = useState(25);
    const [selectedDepartment, setSelectedDepartment] = useState("");
    const [emergencyMode, setEmergencyMode] = useState(false);
    const [hospitalSearchQuery, setHospitalSearchQuery] = useState("");

    // Dynamic Filter & Sort Controls
    const [bedFilter, setBedFilter] = useState("all"); // 'all', 'icu', 'emergency', 'ambulance'
    const [sortBy, setSortBy] = useState("match"); // 'match', 'distance', 'icu_beds'

    // AI Symptom Checker
    const [symptomText, setSymptomText] = useState("");
    const [aiResult, setAiResult] = useState(null);
    const [analyzingSymptoms, setAnalyzingSymptoms] = useState(false);

    // Results & State
    const [hospitals, setHospitals] = useState([]);
    const [loadingHospitals, setLoadingHospitals] = useState(false);
    const [specializations, setSpecializations] = useState([]);

    // Modals & Booking
    const [bookingHospital, setBookingHospital] = useState(null);
    const [bookingDoctorId, setBookingDoctorId] = useState("");
    const [bookingDate, setBookingDate] = useState("");
    const [bookingTime, setBookingTime] = useState("10:30 AM");
    const [bookingReason, setBookingReason] = useState("");
    const [bookingSuccess, setBookingSuccess] = useState("");

    // Patient Records State
    const [myAppointments, setMyAppointments] = useState([]);
    const [myEmergencies, setMyEmergencies] = useState([]);
    const [myPrescriptions, setMyPrescriptions] = useState([]);
    const [myMedicalRecords, setMyMedicalRecords] = useState([]);
    const [myBills, setMyBills] = useState([]);
    const [myProfile, setMyProfile] = useState(null);

    // Navigation Tabs for Logged-In User:
    // When logged in as Patient, we strictly show Patient Portal views ('appointments', 'emergencies', 'prescriptions', 'bills', 'profile')
    // Hospital & Bed Finder is for public visitors / landing.
    const [activeTab, setActiveTab] = useState(user ? "appointments" : "search");

    useEffect(() => {
        if (user && activeTab === "search") {
            setActiveTab("appointments");
        } else if (!user && activeTab !== "search") {
            setActiveTab("search");
        }
    }, [user]);

    // Modal Viewers & UI State
    const [selectedOpdPass, setSelectedOpdPass] = useState(null);
    const [selectedBillReceipt, setSelectedBillReceipt] = useState(null);
    const [selectedPrescription, setSelectedPrescription] = useState(null);
    const [copiedToken, setCopiedToken] = useState(false);
    const [apptFilter, setApptFilter] = useState("all"); // 'all', 'Scheduled', 'Cancelled'

    // Profile Management & Editor State
    const [isEditingProfile, setIsEditingProfile] = useState(false);
    const [profileSaveLoading, setProfileSaveLoading] = useState(false);
    const [profileSaveMessage, setProfileSaveMessage] = useState("");
    const [profileFormData, setProfileFormData] = useState({
        full_name: "",
        phone: "",
        gender: "Male",
        age: 30,
        blood_group: "B+",
        address: "",
        city: "Kolkata",
        emergency_contact_name: "",
        emergency_contact_phone: "",
        emergency_contact_relation: "Family",
        allergies: "",
        chronic_conditions: "",
        current_medications: ""
    });

    useEffect(() => {
        if (myProfile) {
            setProfileFormData({
                full_name: myProfile.full_name || user?.full_name || user?.name || "",
                phone: myProfile.phone || user?.phone || "",
                gender: myProfile.gender || "Male",
                age: myProfile.age || 30,
                blood_group: myProfile.blood_group || "B+",
                address: myProfile.address || "",
                city: myProfile.city || "Kolkata",
                emergency_contact_name: myProfile.emergency_contact_name || "",
                emergency_contact_phone: myProfile.emergency_contact_phone || myProfile.emergency_contact || "",
                emergency_contact_relation: myProfile.emergency_contact_relation || "Family",
                allergies: myProfile.allergies || "",
                chronic_conditions: myProfile.chronic_conditions || "",
                current_medications: myProfile.current_medications || ""
            });
        }
    }, [myProfile, user]);

    useEffect(() => {
        const handleOpenProfile = () => {
            setActiveTab("profile");
        };
        window.addEventListener("open-patient-profile", handleOpenProfile);
        return () => window.removeEventListener("open-patient-profile", handleOpenProfile);
    }, []);

    const handleSaveProfile = async (e) => {
        e.preventDefault();
        setProfileSaveLoading(true);
        setProfileSaveMessage("");
        try {
            const res = await patientService.updateMyProfile(profileFormData);
            if (res.success) {
                setMyProfile(res.profile);
                setProfileSaveMessage("Profile information updated successfully!");
                setIsEditingProfile(false);
                loadUserRecords();
                setTimeout(() => setProfileSaveMessage(""), 3500);
            }
        } catch (err) {
            alert("Failed to update profile. Please check your network connection.");
        } finally {
            setProfileSaveLoading(false);
        }
    };

    // Unauthenticated Trigger Modals
    const [authRequiredHospital, setAuthRequiredHospital] = useState(null);
    const [emergencyModalHospital, setEmergencyModalHospital] = useState(null);
    const [emergencyCallerName, setEmergencyCallerName] = useState("");
    const [emergencyPhone, setEmergencyPhone] = useState("");
    const [emergencyPickupLocation, setEmergencyPickupLocation] = useState("");
    const [emergencyCondition, setEmergencyCondition] = useState("Cardiac Arrest / Severe Chest Pain (Critical)");
    const [emergencySending, setEmergencySending] = useState(false);
    const [dispatchedAlert, setDispatchedAlert] = useState(null);

    // Check for pending booking after login
    useEffect(() => {
        if (user) {
            const pendingRaw = sessionStorage.getItem("pending_booking");
            if (pendingRaw) {
                try {
                    const pending = JSON.parse(pendingRaw);
                    sessionStorage.removeItem("pending_booking");
                    if (pending && pending.hospital) {
                        openBookingModal(pending.hospital);
                    }
                } catch (e) {}
            }
        }
    }, [user]);

    // Load initial specializations & user records
    useEffect(() => {
        recommendationService.getSpecializations()
            .then(res => setSpecializations(res.data || []))
            .catch(() => {});
        loadUserRecords();
    }, [user]);

    const loadUserRecords = () => {
        if (!user) return;
        patientService.getMyAppointments()
            .then(res => setMyAppointments(res.appointments || []))
            .catch(() => {});
        patientService.getMyEmergencies()
            .then(res => setMyEmergencies(res.emergencies || []))
            .catch(() => {});
        patientService.getMyPrescriptions()
            .then(res => setMyPrescriptions(res.prescriptions || []))
            .catch(() => {});
        patientService.getMyMedicalRecords()
            .then(res => setMyMedicalRecords(res.records || []))
            .catch(() => {});
        patientService.getMyBills()
            .then(res => setMyBills(res.bills || []))
            .catch(() => {});
        patientService.getMyProfile()
            .then(res => setMyProfile(res.profile || null))
            .catch(() => {});
    };

    // Fetch ranked hospitals whenever coordinates, radius, or department change
    useEffect(() => {
        fetchHospitals();
    }, [coordinates, radiusKm, selectedDepartment, emergencyMode]);

    const fetchHospitals = async () => {
        setLoadingHospitals(true);
        try {
            const res = await recommendationService.getRankedHospitals({
                lat: coordinates.lat,
                lng: coordinates.lng,
                radius_km: radiusKm,
                department: selectedDepartment || undefined,
                emergency_mode: emergencyMode,
                limit: 15
            });
            setHospitals(res.data || []);
        } catch (err) {
            console.error("Failed to load hospitals:", err);
        } finally {
            setLoadingHospitals(false);
        }
    };

    const handleCityChange = (cityName) => {
        const found = PRESET_CITIES.find(c => c.name === cityName);
        if (found) {
            setSelectedCity(found.name);
            setCoordinates({ lat: found.lat, lng: found.lng });
        }
    };

    const handleUseMyLocation = () => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    setCoordinates({
                        lat: pos.coords.latitude,
                        lng: pos.coords.longitude
                    });
                    setSelectedCity("My Exact GPS Location");
                },
                () => {
                    alert("Location access denied or unavailable. Using Kolkata as default.");
                }
            );
        } else {
            alert("Geolocation is not supported in this browser.");
        }
    };

    const handleAutoFillEmergencyGps = () => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    setEmergencyPickupLocation(`GPS Lat: ${pos.coords.latitude.toFixed(4)}, Lng: ${pos.coords.longitude.toFixed(4)} (${selectedCity})`);
                },
                () => {
                    setEmergencyPickupLocation(`${selectedCity} Central, Nearby Landmark`);
                }
            );
        } else {
            setEmergencyPickupLocation(`${selectedCity} Central, Nearby Landmark`);
        }
    };

    const runSymptomClassification = async (textToAnalyze) => {
        if (!textToAnalyze.trim()) return;
        setAnalyzingSymptoms(true);
        try {
            const res = await recommendationService.getDepartmentRecommendation(textToAnalyze);
            const data = res.data;
            setAiResult(data);
            if (data.suggested_department) {
                setSelectedDepartment(data.suggested_department);
                if (data.is_emergency) {
                    setEmergencyMode(true);
                }
            }
        } catch (err) {
            console.error(err);
        } finally {
            setAnalyzingSymptoms(false);
        }
    };

    const handleAnalyzeSymptoms = (e) => {
        e.preventDefault();
        runSymptomClassification(symptomText);
    };

    const handleInitiateBookDoctor = (item) => {
        if (!user) {
            setAuthRequiredHospital(item);
            return;
        }
        openBookingModal(item);
    };

    const handleHospitalChangeInModal = (hospitalId) => {
        const found = hospitals.find(h => (h.hospital?.id || h.id) === hospitalId);
        if (found) {
            openBookingModal(found);
        }
    };

    const handleCopyToken = (tokenText) => {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(tokenText);
        }
        setCopiedToken(true);
        setTimeout(() => setCopiedToken(false), 2000);
    };

    const openBookingModal = (item) => {
        const hosp = item.hospital || item;
        const docs = item.doctors || item.matching_doctors || [];
        const matching = item.matching_doctors || [];
        const chosenHosp = {
            ...hosp,
            doctors: docs,
            matching_doctors: matching
        };
        setBookingHospital(chosenHosp);
        const defaultDoc = matching.length > 0 ? matching[0] : (docs.length > 0 ? docs[0] : null);
        setBookingDoctorId(defaultDoc ? defaultDoc.id : "");
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        setBookingDate(tomorrow.toISOString().split("T")[0]);
        setBookingTime("10:30 AM");
        setBookingReason(selectedDepartment ? `${selectedDepartment} consultation` : "General Checkup");
        setBookingSuccess("");
    };

    const handleBookAppointment = async (e) => {
        e.preventDefault();
        if (!bookingHospital) return;

        try {
            const allDocs = bookingHospital.doctors || bookingHospital.matching_doctors || [];
            const docId = bookingDoctorId ? Number(bookingDoctorId) : (allDocs[0] ? allDocs[0].id : null);
            const res = await patientService.bookAppointment({
                hospital_id: bookingHospital.id,
                doctor_id: docId,
                appointment_date: bookingDate || new Date().toISOString().split("T")[0],
                appointment_time: bookingTime || "10:30 AM",
                reason: bookingReason || (selectedDepartment ? `${selectedDepartment} consultation` : "General Checkup")
            });
            setBookingSuccess("Appointment confirmed & scheduled with doctor!");
            loadUserRecords();
            setTimeout(() => {
                const newAppt = res.appointment;
                setBookingHospital(null);
                setBookingSuccess("");
                if (newAppt) {
                    setSelectedOpdPass({
                        id: newAppt.id,
                        hospital_name: newAppt.hospital || bookingHospital.name,
                        doctor_name: newAppt.doctor,
                        specialization: selectedDepartment || "General Medicine",
                        date: newAppt.date,
                        time: newAppt.time,
                        consultation_fee: 900
                    });
                }
            }, 1200);
        } catch (err) {
            alert("Booking failed. Please try again.");
        }
    };

    const handleCancelAppointment = async (apptId) => {
        if (!window.confirm("Are you sure you want to cancel this appointment?")) return;
        try {
            await patientService.cancelAppointment(apptId);
            loadUserRecords();
        } catch (err) {
            alert("Could not cancel appointment");
        }
    };

    const openEmergencyModal = (item) => {
        const hosp = item.hospital || item;
        setEmergencyModalHospital(hosp);
        setEmergencyCallerName(user ? (user.full_name || user.name || "") : "");
        setEmergencyPhone(user?.phone || "");
        setEmergencyPickupLocation(`${selectedCity || "Current City"}, Landmark Address`);
        setEmergencyCondition(
            aiResult?.suggested_department === "Cardiology"
                ? "Cardiac Arrest / Severe Chest Pain (Critical)"
                : "Acute Trauma / Road Accident (Critical)"
        );
        setDispatchedAlert(null);
    };

    const handleConfirmEmergencyDispatch = async (e) => {
        e.preventDefault();
        if (!emergencyModalHospital) return;

        setEmergencySending(true);
        try {
            const res = await patientService.requestEmergency({
                hospital_id: emergencyModalHospital.id,
                caller_name: emergencyCallerName || "Emergency Caller",
                phone: emergencyPhone || "+91 9999999999",
                pickup_location: emergencyPickupLocation || selectedCity,
                emergency_type: emergencyCondition,
                priority: emergencyCondition.includes("Critical") ? "Critical" : "High"
            });
            setDispatchedAlert(res.emergency || {
                hospital: emergencyModalHospital.name,
                ambulance: "Response Unit #01",
                driver_name: "On-Duty Paramedic",
                driver_phone: "+91 9800001080",
                eta_minutes: "8 - 12 mins",
                hospital_phone: emergencyModalHospital.emergency_contact || emergencyModalHospital.phone
            });
            loadUserRecords();
        } catch (err) {
            alert("Emergency dispatch failed. Please dial 108 immediately.");
        } finally {
            setEmergencySending(false);
        }
    };

    // Filter & Sort Hospitals in memory
    const displayedHospitals = hospitals.filter(item => {
        const matchesQuery = hospitalSearchQuery.trim() === "" ||
            item.hospital.name.toLowerCase().includes(hospitalSearchQuery.toLowerCase()) ||
            item.hospital.city.toLowerCase().includes(hospitalSearchQuery.toLowerCase()) ||
            (item.matching_doctors || []).some(d => d.name.toLowerCase().includes(hospitalSearchQuery.toLowerCase()));

        if (!matchesQuery) return false;
        if (bedFilter === "icu") return item.beds.icu.available > 0;
        if (bedFilter === "emergency") return item.beds.emergency.available > 0;
        if (bedFilter === "ambulance") return item.ambulances.available > 0;
        return true;
    }).sort((a, b) => {
        if (sortBy === "distance") return a.distance_km - b.distance_km;
        if (sortBy === "icu_beds") return b.beds.icu.available - a.beds.icu.available;
        return b.match_score - a.match_score;
    });

    const nextUpcomingAppt = myAppointments.find(a => a.status === "Scheduled") || myAppointments[0];
    const latestEmergency = myEmergencies[0];

    // Aggregated Featured Doctors for Homepage Showcase
    const featuredDoctors = [];
    hospitals.forEach(item => {
        const docs = item.doctors || item.matching_doctors || [];
        docs.forEach(doc => {
            if (!featuredDoctors.some(d => d.id === doc.id || (d.name === doc.name && d.hospital_name === item.hospital.name))) {
                featuredDoctors.push({
                    ...doc,
                    hospital_name: item.hospital.name,
                    hospital_city: item.hospital.city,
                    hospital_phone: item.hospital.phone,
                    hospital_item: item
                });
            }
        });
    });

    const handleSelectSpecialty = (specName) => {
        setSelectedDepartment(specName);
        const el = document.getElementById("hospitals-results-section");
        if (el) {
            el.scrollIntoView({ behavior: "smooth" });
        }
    };

    return (
        <div className="space-y-6">

            {/* ============================================================== */}
            {/* 1. PERSONALIZED PATIENT HEALTH CARD (SHOWN TO LOGGED-IN USERS) */}
            {/* ============================================================== */}
            {user ? (
                <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 rounded-3xl p-6 sm:p-7 text-white shadow-xl shadow-indigo-950/20 border border-indigo-800/40">
                    <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                        {/* Left: Patient Identity (Clickable to view & edit Profile) */}
                        <div
                            onClick={() => setActiveTab("profile")}
                            className="flex items-center gap-4 cursor-pointer group"
                            title="Click to view and edit Profile"
                        >
                            <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-500 text-white flex items-center justify-center font-extrabold text-xl shadow-md border-2 border-white/20 group-hover:scale-105 transition">
                                {(user.full_name || user.name || "PT").split(" ").map(w => w[0]).join("").slice(0, 2).toUpperCase()}
                            </div>
                            <div>
                                <div className="flex flex-wrap items-center gap-2">
                                    <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight group-hover:text-blue-200 transition flex items-center gap-2">
                                        Welcome, {user.full_name || user.name || "Patient"}
                                        <Edit3 size={15} className="opacity-0 group-hover:opacity-100 transition text-blue-300" />
                                    </h1>
                                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 flex items-center gap-1">
                                        <CheckCircle2 size={11} /> Verified Patient
                                    </span>
                                </div>
                                <div className="flex flex-wrap items-center gap-3 text-xs text-indigo-200/80 mt-1">
                                    <span>Patient ID: <strong className="text-white font-mono">{myProfile?.patient_code || `#MED-PT-${user.id || '001'}`}</strong></span>
                                    <span>•</span>
                                    <span>Registered Email: <strong className="text-white">{user.email}</strong></span>
                                    <span>•</span>
                                    <span>Blood Group: <strong className="text-rose-300">{myProfile?.blood_group || "B+ (RH+)"}</strong></span>
                                </div>
                            </div>
                        </div>

                        {/* Right: Quick Action Buttons */}
                        <div className="flex flex-wrap items-center gap-2">
                            <button
                                onClick={() => {
                                    if (hospitals.length > 0) {
                                        openBookingModal(hospitals[0]);
                                    } else {
                                        setActiveTab("appointments");
                                    }
                                }}
                                className="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-xs cursor-pointer"
                            >
                                <Calendar size={14} /> Schedule New OPD
                            </button>
                            <button
                                onClick={() => {
                                    if (hospitals.length > 0) {
                                        openEmergencyModal(hospitals[0]);
                                    } else {
                                        setActiveTab("emergencies");
                                    }
                                }}
                                className="px-3.5 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-xs cursor-pointer animate-pulse"
                            >
                                <PhoneCall size={14} /> Emergency SOS 108
                            </button>
                            {nextUpcomingAppt && (
                                <button
                                    onClick={() => setSelectedOpdPass(nextUpcomingAppt)}
                                    className="px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-bold transition flex items-center gap-1.5 border border-white/20 cursor-pointer"
                                >
                                    <QrCode size={14} /> View Digital OPD Pass
                                </button>
                            )}
                        </div>
                    </div>

                    {/* Vitals & Summary Counters */}
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-6 mt-6 border-t border-white/10">
                        <div onClick={() => setActiveTab("appointments")} className="bg-white/10 hover:bg-white/15 backdrop-blur-md rounded-2xl p-3 border border-white/10 cursor-pointer transition">
                            <div className="flex items-center justify-between text-indigo-200 mb-1">
                                <span className="text-[11px] font-medium">Scheduled OPDs</span>
                                <Calendar size={14} className="text-blue-300" />
                            </div>
                            <p className="text-xl font-extrabold text-white">{myAppointments.length}</p>
                            <p className="text-[10px] text-indigo-300 truncate mt-0.5">
                                {nextUpcomingAppt ? `${nextUpcomingAppt.date} (${nextUpcomingAppt.time})` : "No visits scheduled"}
                            </p>
                        </div>

                        <div onClick={() => setActiveTab("emergencies")} className="bg-white/10 hover:bg-white/15 backdrop-blur-md rounded-2xl p-3 border border-white/10 cursor-pointer transition">
                            <div className="flex items-center justify-between text-indigo-200 mb-1">
                                <span className="text-[11px] font-medium">SOS Ambulances</span>
                                <Truck size={14} className="text-rose-300" />
                            </div>
                            <p className="text-xl font-extrabold text-rose-300">{myEmergencies.length}</p>
                            <p className="text-[10px] text-indigo-300 truncate mt-0.5">
                                {latestEmergency ? `${latestEmergency.status} (${latestEmergency.hospital_name})` : "Fleet on standby"}
                            </p>
                        </div>

                        <div onClick={() => setActiveTab("prescriptions")} className="bg-white/10 hover:bg-white/15 backdrop-blur-md rounded-2xl p-3 border border-white/10 cursor-pointer transition">
                            <div className="flex items-center justify-between text-indigo-200 mb-1">
                                <span className="text-[11px] font-medium">Digital Prescriptions</span>
                                <Pill size={14} className="text-emerald-300" />
                            </div>
                            <p className="text-xl font-extrabold text-emerald-300">{myPrescriptions.length}</p>
                            <p className="text-[10px] text-indigo-300 truncate mt-0.5">
                                {myPrescriptions.length > 0 ? "Active clinical meds" : "No prescriptions yet"}
                            </p>
                        </div>

                        <div onClick={() => setActiveTab("bills")} className="bg-white/10 hover:bg-white/15 backdrop-blur-md rounded-2xl p-3 border border-white/10 cursor-pointer transition">
                            <div className="flex items-center justify-between text-indigo-200 mb-1">
                                <span className="text-[11px] font-medium">Billing & Invoices</span>
                                <Receipt size={14} className="text-amber-300" />
                            </div>
                            <p className="text-xl font-extrabold text-amber-300">{myBills.length}</p>
                            <p className="text-[10px] text-indigo-300 truncate mt-0.5">
                                {myBills.length > 0 ? "All consultation fees settled" : "No pending dues"}
                            </p>
                        </div>
                    </div>
                </div>
            ) : (
                /* REFINED HOMEPAGE HERO SECTION & COMMAND SUITE */
                <div className="space-y-6">
                    {/* 1. IMMERSIVE HERO BANNER */}
                    <div className="relative overflow-hidden bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-950 rounded-3xl p-6 sm:p-9 text-white shadow-xl shadow-indigo-950/30 border border-indigo-900/40">
                        {/* Background Ambient Glow */}
                        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-80 h-80 rounded-full bg-blue-600/20 blur-3xl pointer-events-none"></div>
                        <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-80 h-80 rounded-full bg-indigo-600/20 blur-3xl pointer-events-none"></div>

                        <div className="relative z-10 space-y-5">
                            {/* Top Emergency Hotline Callout */}
                            <div className="flex flex-wrap items-center justify-between gap-3">
                                <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-blue-500/15 border border-blue-400/30 text-blue-200 text-xs font-bold">
                                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                                    <span>Pan-India Live Healthcare Grid • NABH Verified Network</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <a
                                        href="tel:108"
                                        className="text-xs text-rose-300 font-extrabold bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/40 px-3.5 py-1 rounded-full flex items-center gap-1.5 transition cursor-pointer shadow-xs"
                                        title="Click to dial 108 Emergency Helpline"
                                    >
                                        <PhoneCall size={13} className="animate-bounce text-rose-400" />
                                        <span>24x7 Emergency SOS: 108</span>
                                    </a>
                                </div>
                            </div>

                            {/* Headline & Mission */}
                            <div className="max-w-3xl space-y-2">
                                <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight leading-tight text-white">
                                    Instant Emergency Care, Real-Time Bed Tracking & Specialist Consultations
                                </h1>
                                <p className="text-xs sm:text-sm text-indigo-200/90 leading-relaxed font-normal">
                                    Zero-latency ICU & trauma bed tracking updated every 15 seconds, 1-click GPS ambulance dispatch in under 8 minutes, and intelligent AI symptom triage across accredited Indian hospitals.
                                </p>
                            </div>

                            {/* 4 FAST CTA ACTION CARDS */}
                            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 pt-2">
                                <button
                                    onClick={() => {
                                        if (hospitals.length > 0) openEmergencyModal(hospitals[0]);
                                    }}
                                    className="p-3.5 rounded-2xl bg-gradient-to-br from-rose-600/90 to-rose-700/90 hover:from-rose-500 hover:to-rose-600 text-white text-left border border-rose-400/30 shadow-md shadow-rose-950/30 transition-all cursor-pointer group"
                                >
                                    <div className="w-8 h-8 rounded-xl bg-white/20 flex items-center justify-center mb-2 group-hover:scale-110 transition">
                                        <HeartPulse size={18} className="text-white animate-pulse" />
                                    </div>
                                    <h4 className="text-xs font-extrabold">Emergency SOS 108</h4>
                                    <p className="text-[10px] text-rose-100 mt-0.5">Zero-login 1-click dispatch</p>
                                </button>

                                <button
                                    onClick={() => {
                                        const el = document.getElementById("hospitals-results-section");
                                        if (el) el.scrollIntoView({ behavior: "smooth" });
                                    }}
                                    className="p-3.5 rounded-2xl bg-white/10 hover:bg-white/15 text-white text-left border border-white/15 shadow-sm transition-all cursor-pointer group"
                                >
                                    <div className="w-8 h-8 rounded-xl bg-indigo-500/30 flex items-center justify-center mb-2 group-hover:scale-110 transition">
                                        <Bed size={18} className="text-indigo-300" />
                                    </div>
                                    <h4 className="text-xs font-extrabold">Live Bed Registry</h4>
                                    <p className="text-[10px] text-indigo-200 mt-0.5">1,692 ICU & ER beds tracked</p>
                                </button>

                                <button
                                    onClick={() => {
                                        const el = document.getElementById("featured-doctors-section");
                                        if (el) el.scrollIntoView({ behavior: "smooth" });
                                    }}
                                    className="p-3.5 rounded-2xl bg-white/10 hover:bg-white/15 text-white text-left border border-white/15 shadow-sm transition-all cursor-pointer group"
                                >
                                    <div className="w-8 h-8 rounded-xl bg-blue-500/30 flex items-center justify-center mb-2 group-hover:scale-110 transition">
                                        <Stethoscope size={18} className="text-blue-300" />
                                    </div>
                                    <h4 className="text-xs font-extrabold">Book OPD Doctor</h4>
                                    <p className="text-[10px] text-blue-200 mt-0.5">Confirmed slot & digital pass</p>
                                </button>

                                <button
                                    onClick={() => {
                                        const el = document.getElementById("ai-triage-card");
                                        if (el) el.scrollIntoView({ behavior: "smooth" });
                                    }}
                                    className="p-3.5 rounded-2xl bg-white/10 hover:bg-white/15 text-white text-left border border-white/15 shadow-sm transition-all cursor-pointer group"
                                >
                                    <div className="w-8 h-8 rounded-xl bg-purple-500/30 flex items-center justify-center mb-2 group-hover:scale-110 transition">
                                        <Sparkles size={18} className="text-purple-300" />
                                    </div>
                                    <h4 className="text-xs font-extrabold">AI Symptom Triage</h4>
                                    <p className="text-[10px] text-purple-200 mt-0.5">Instant department & bed triage</p>
                                </button>
                            </div>

                            {/* POPULAR CITIES SWITCHER */}
                            <div className="pt-2 flex flex-wrap items-center gap-1.5 border-t border-white/10">
                                <span className="text-[11px] font-bold text-white/70 mr-1 flex items-center gap-1">
                                    <MapPin size={12} className="text-blue-400" /> Select Metro Hub:
                                </span>
                                {PRESET_CITIES.map(c => (
                                    <button
                                        key={c.name}
                                        onClick={() => handleCityChange(c.name)}
                                        className={`text-xs px-2.5 py-1 rounded-xl transition font-semibold cursor-pointer ${
                                            selectedCity === c.name
                                                ? "bg-white text-slate-900 font-bold shadow-xs scale-105"
                                                : "bg-white/10 hover:bg-white/20 text-white border border-white/15"
                                        }`}
                                    >
                                        {c.name}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* 2. CLINICAL SPECIALTIES QUICK EXPLORER */}
                    <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-3">
                        <div className="flex items-center justify-between">
                            <div>
                                <h3 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                                    <Award size={14} className="text-blue-600" />
                                    Explore by Clinical Specialization
                                </h3>
                                <p className="text-[11px] text-slate-500">Filter hospitals and on-duty specialists by medical department</p>
                            </div>
                            {selectedDepartment && (
                                <button
                                    onClick={() => setSelectedDepartment("")}
                                    className="text-[11px] font-bold text-blue-600 hover:text-blue-700 bg-blue-50 px-2 py-0.5 rounded-lg cursor-pointer"
                                >
                                    Clear Specialization Filter
                                </button>
                            )}
                        </div>

                        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
                            {CLINICAL_SPECIALTIES.map(s => {
                                const isSelected = selectedDepartment === s.name;
                                return (
                                    <button
                                        key={s.name}
                                        onClick={() => handleSelectSpecialty(s.name)}
                                        className={`p-2.5 rounded-xl border text-center transition-all cursor-pointer flex flex-col items-center justify-center gap-1 ${
                                            isSelected
                                                ? "bg-blue-600 text-white border-blue-600 shadow-xs scale-105"
                                                : "bg-slate-50 hover:bg-blue-50/60 border-slate-200/80 text-slate-800 hover:border-blue-300"
                                        }`}
                                    >
                                        <span className="text-xl">{s.icon}</span>
                                        <span className="text-xs font-extrabold block truncate w-full">{s.name}</span>
                                        <span className={`text-[9px] font-bold px-1.5 py-0.2 rounded-full ${
                                            isSelected ? "bg-white/20 text-white" : "bg-slate-200 text-slate-600"
                                        }`}>
                                            {s.badge}
                                        </span>
                                    </button>
                                );
                            })}
                        </div>
                    </div>

                    {/* 3. EMERGENCY SOS CALLOUT RIBBON */}
                    <div className="bg-gradient-to-r from-rose-600 via-rose-700 to-red-800 rounded-2xl p-4 text-white shadow-md flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center shrink-0">
                                <PhoneCall size={20} className="text-white animate-bounce" />
                            </div>
                            <div>
                                <h4 className="text-sm font-extrabold">Life-Threatening Emergency? Immediate Action Available</h4>
                                <p className="text-xs text-rose-100">Zero-login ambulance dispatch with live GPS tracking • National SOS Hotline 108</p>
                            </div>
                        </div>

                        <div className="flex items-center gap-2">
                            <a
                                href="tel:108"
                                className="px-4 py-2 bg-white text-rose-700 hover:bg-rose-50 text-xs font-extrabold rounded-xl transition shadow-xs flex items-center gap-1.5 cursor-pointer"
                            >
                                <Phone size={13} /> Dial 108
                            </a>
                            <button
                                onClick={() => {
                                    if (hospitals.length > 0) openEmergencyModal(hospitals[0]);
                                }}
                                className="px-4 py-2 bg-slate-950 hover:bg-slate-900 text-white text-xs font-extrabold rounded-xl transition shadow-xs flex items-center gap-1.5 cursor-pointer"
                            >
                                <HeartPulse size={14} className="text-rose-400" /> Dispatch Ambulance
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 2. TAB SELECTOR FOR PATIENT PORTAL                             */}
            {/* ============================================================== */}
            {user ? (
                /* LOGGED-IN PATIENT MEDICAL PORTAL NAVIGATION */
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-white border border-slate-200 rounded-2xl p-3.5 shadow-xs">
                    <div className="flex flex-wrap items-center gap-1.5">
                        <button
                            onClick={() => setActiveTab("search")}
                            className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                                activeTab === "search" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                            }`}
                        >
                            <Search size={14} />
                            Explore Care & Beds
                        </button>

                        <button
                            onClick={() => setActiveTab("appointments")}
                            className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                                activeTab === "appointments" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                            }`}
                        >
                            <Calendar size={14} />
                            My Consultations ({myAppointments.length})
                        </button>

                        <button
                            onClick={() => setActiveTab("emergencies")}
                            className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                                activeTab === "emergencies" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                            }`}
                        >
                            <Truck size={14} />
                            Ambulance Tracker ({myEmergencies.length})
                        </button>

                        <button
                            onClick={() => setActiveTab("prescriptions")}
                            className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                                activeTab === "prescriptions" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                            }`}
                        >
                            <Pill size={14} />
                            Prescriptions ({myPrescriptions.length})
                        </button>

                        <button
                            onClick={() => setActiveTab("bills")}
                            className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                                activeTab === "bills" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                            }`}
                        >
                            <Receipt size={14} />
                            Invoices ({myBills.length})
                        </button>

                        <button
                            onClick={() => setActiveTab("profile")}
                            className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                                activeTab === "profile" ? "bg-blue-600 text-white shadow-xs" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                            }`}
                        >
                            <UserCircle size={14} />
                            Profile
                        </button>
                    </div>

                    <button
                        onClick={() => {
                            if (hospitals.length > 0) {
                                openEmergencyModal(hospitals[0]);
                            } else {
                                setActiveTab("emergencies");
                            }
                        }}
                        className="px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 cursor-pointer bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200"
                    >
                        <PhoneCall size={14} />
                        Emergency SOS 108
                    </button>
                </div>
            ) : null}

            {/* ============================================================== */}
            {/* 3. PUBLIC VISITOR LANDING: HOSPITAL & BED FINDER + AIML TRIAGE */}
            {/* ============================================================== */}
            {activeTab === "search" && (
                <div className="space-y-8">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* LEFT PANEL: LOCATION CONTROLS & AIML SYMPTOM CLASSIFIER */}
                    <div className="space-y-6">
                        {/* 1. LOCATION & RADIUS PICKER */}
                        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs space-y-4">
                            <div className="flex items-center justify-between">
                                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                                    <MapPin size={16} className="text-blue-600" />
                                    Your Location & Search Radius
                                </h3>
                                <button
                                    onClick={handleUseMyLocation}
                                    className="text-[11px] font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1 bg-blue-50 hover:bg-blue-100 px-2 py-1 rounded-lg transition cursor-pointer"
                                >
                                    <Navigation size={12} />
                                    GPS Auto-Detect
                                </button>
                            </div>

                            <div className="space-y-3.5">
                                <div>
                                    <label className="block text-[11px] font-bold text-slate-600 uppercase mb-1">Target Indian City</label>
                                    <select
                                        value={selectedCity}
                                        onChange={(e) => handleCityChange(e.target.value)}
                                        className="w-full text-xs font-semibold p-2.5 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-blue-500/20"
                                    >
                                        {PRESET_CITIES.map(c => (
                                            <option key={c.name} value={c.name}>{c.name}</option>
                                        ))}
                                    </select>
                                </div>

                                <div>
                                    <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                                        <span>Proximity Radius Filter</span>
                                        <span className="font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">{radiusKm} km</span>
                                    </div>
                                    <input
                                        type="range"
                                        min="5"
                                        max="150"
                                        step="5"
                                        value={radiusKm}
                                        onChange={(e) => setRadiusKm(Number(e.target.value))}
                                        className="w-full accent-blue-600 cursor-pointer"
                                    />
                                    <div className="flex justify-between text-[10px] text-slate-400 mt-0.5 font-medium">
                                        <span>5 km (Local)</span>
                                        <span>50 km (Metro)</span>
                                        <span>150 km (Regional)</span>
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-[11px] font-bold text-slate-600 uppercase mb-1">Filter by Department</label>
                                    <select
                                        value={selectedDepartment}
                                        onChange={(e) => setSelectedDepartment(e.target.value)}
                                        className="w-full text-xs font-semibold p-2.5 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-blue-500/20"
                                    >
                                        <option value="">All Clinical Departments ({specializations.length})</option>
                                        {specializations.map(s => (
                                            <option key={s.id} value={s.name}>{s.name}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                        </div>

                        {/* 2. AIML SYMPTOM CLASSIFIER */}
                        <div id="ai-triage-card" className="bg-white border border-slate-200 rounded-3xl p-5 sm:p-6 shadow-xs space-y-4">
                            {/* Header */}
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold shrink-0">
                                        <Stethoscope size={20} />
                                    </div>
                                    <div>
                                        <h3 className="text-base font-bold text-slate-900">
                                            AI Symptom Triage
                                        </h3>
                                        <p className="text-xs text-slate-500">
                                            Instant department matching & bed availability
                                        </p>
                                    </div>
                                </div>
                                <span className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-medium border border-emerald-200">
                                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                                    Active
                                </span>
                            </div>

                            {/* Form */}
                            <form onSubmit={handleAnalyzeSymptoms} className="space-y-4">
                                <div className="space-y-1.5">
                                    <div className="flex items-center justify-between text-xs">
                                        <label className="font-semibold text-slate-700">
                                            Describe your symptoms:
                                        </label>
                                        {symptomText && (
                                            <button
                                                type="button"
                                                onClick={() => { setSymptomText(""); setAiResult(null); }}
                                                className="text-slate-400 hover:text-slate-600 transition flex items-center gap-1 cursor-pointer"
                                            >
                                                <X size={12} /> Clear
                                            </button>
                                        )}
                                    </div>
                                    <textarea
                                        rows={3}
                                        value={symptomText}
                                        onChange={(e) => setSymptomText(e.target.value)}
                                        placeholder="Type symptoms in plain words (e.g. sharp chest tightness radiating to left arm with shortness of breath)..."
                                        className="w-full text-xs sm:text-sm p-3.5 rounded-2xl bg-slate-50 border border-slate-200 focus:bg-white focus:border-blue-500 text-slate-900 placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-blue-100 transition resize-none leading-relaxed"
                                    />
                                </div>

                                {/* Common Symptom Examples */}
                                <div className="space-y-2">
                                    <p className="text-xs font-semibold text-slate-600">
                                        Try common symptom examples:
                                    </p>
                                    <div className="flex flex-wrap gap-1.5">
                                        {SAMPLE_SYMPTOMS.map((sample, sIdx) => {
                                            const isSelected = symptomText === sample.text;
                                            return (
                                                <button
                                                    key={sIdx}
                                                    type="button"
                                                    onClick={() => {
                                                        setSymptomText(sample.text);
                                                        runSymptomClassification(sample.text);
                                                    }}
                                                    className={`text-xs px-2.5 py-1.5 rounded-xl border transition cursor-pointer font-medium ${
                                                        isSelected
                                                            ? "bg-blue-50 border-blue-400 text-blue-700 shadow-xs"
                                                            : "bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-700 hover:text-slate-900"
                                                    }`}
                                                >
                                                    {sample.label}
                                                </button>
                                            );
                                        })}
                                    </div>
                                </div>

                                {/* Action Button */}
                                <button
                                    type="submit"
                                    disabled={analyzingSymptoms || !symptomText.trim()}
                                    className={`w-full py-2.5 px-4 rounded-xl text-xs sm:text-sm font-bold transition flex items-center justify-center gap-2 cursor-pointer shadow-xs ${
                                        analyzingSymptoms || !symptomText.trim()
                                            ? "bg-slate-100 text-slate-400 border border-slate-200 cursor-not-allowed"
                                            : "bg-blue-600 hover:bg-blue-700 text-white"
                                    }`}
                                >
                                    {analyzingSymptoms ? (
                                        <>
                                            <Loader2 size={16} className="animate-spin text-white" />
                                            <span>Analyzing Symptoms...</span>
                                        </>
                                    ) : (
                                        <>
                                            <Sparkles size={15} />
                                            <span>Predict Department & Rank Facilities</span>
                                        </>
                                    )}
                                </button>
                            </form>

                            {/* AIML Prediction Output */}
                            {aiResult && (
                                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3 text-xs text-slate-700">
                                    <div className="flex items-center justify-between">
                                        <span className="font-semibold text-slate-600">Suggested Department:</span>
                                        <span className="px-3 py-1 rounded-full font-bold bg-blue-600 text-white text-xs shadow-xs">
                                            {aiResult.suggested_department}
                                        </span>
                                    </div>

                                    {/* Confidence Progress Meter */}
                                    <div className="space-y-1">
                                        <div className="flex items-center justify-between text-[11px] text-slate-500">
                                            <span>Model Confidence</span>
                                            <span className="font-bold text-slate-800">
                                                {(aiResult.confidence * 100).toFixed(0)}%
                                            </span>
                                        </div>
                                        <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                                            <div
                                                className="h-full bg-blue-600 rounded-full transition-all duration-500"
                                                style={{ width: `${Math.min(100, Math.round(aiResult.confidence * 100))}%` }}
                                            />
                                        </div>
                                    </div>

                                    {/* Alternative Candidates */}
                                    {aiResult.top_candidates && aiResult.top_candidates.length > 1 && (
                                        <div className="pt-2 border-t border-slate-200 text-[11px] flex flex-wrap items-center gap-1.5">
                                            <span className="text-slate-400">Also considered:</span>
                                            {aiResult.top_candidates.slice(1, 3).map((cand, cIdx) => (
                                                <span key={cIdx} className="px-2 py-0.5 rounded-md bg-white border border-slate-200 text-slate-600">
                                                    {cand.department} ({(cand.score !== undefined ? cand.score * 100 : (cand.confidence || 0) * 100).toFixed(0)}%)
                                                </span>
                                            ))}
                                        </div>
                                    )}

                                    {aiResult.is_emergency && (
                                        <div className="p-2.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 flex items-center gap-2 font-medium">
                                            <AlertTriangle size={15} className="text-rose-600 shrink-0" />
                                            <span>Emergency flags detected! ICU & ER beds prioritized below.</span>
                                        </div>
                                    )}

                                    {/* Scroll to Ranked Hospitals CTA */}
                                    <button
                                        type="button"
                                        onClick={() => {
                                            const el = document.getElementById("hospitals-results-section");
                                            if (el) el.scrollIntoView({ behavior: "smooth" });
                                        }}
                                        className="w-full py-2 rounded-xl bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 font-semibold text-xs transition flex items-center justify-center gap-1.5 cursor-pointer"
                                    >
                                        <span>View Ranked Hospitals Below</span>
                                        <ChevronDown size={14} />
                                    </button>

                                    <p className="text-[10px] text-slate-400 italic">
                                        {aiResult.disclaimer || aiResult.medical_disclaimer || "Clinical AI routing guidance. In emergencies, please call 108 immediately."}
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* RIGHT PANEL: RANKED HOSPITALS & BEDS */}
                    <div id="hospitals-results-section" className="lg:col-span-2 space-y-4">
                        {/* SEARCH BAR & QUICK FILTERS */}
                        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-3">
                            <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
                                <div className="relative flex-1">
                                    <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                                    <input
                                        type="text"
                                        placeholder="Search by hospital name, locality, or specialist..."
                                        value={hospitalSearchQuery}
                                        onChange={(e) => setHospitalSearchQuery(e.target.value)}
                                        className="w-full pl-9 pr-3 py-2 text-xs border border-slate-200 rounded-xl focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 bg-slate-50/50 focus:bg-white"
                                    />
                                </div>

                                <div className="flex items-center gap-2">
                                    <div className="flex items-center gap-1 text-xs text-slate-500">
                                        <ArrowUpDown size={13} />
                                        <span>Sort:</span>
                                    </div>
                                    <select
                                        value={sortBy}
                                        onChange={(e) => setSortBy(e.target.value)}
                                        className="text-xs font-semibold p-1.5 border border-slate-200 rounded-lg bg-slate-50"
                                    >
                                        <option value="match">Best Match</option>
                                        <option value="distance">Nearest First</option>
                                        <option value="icu_beds">Most ICU Beds</option>
                                    </select>
                                </div>
                            </div>

                            {/* BED AVAILABILITY TOGGLES */}
                            <div className="flex flex-wrap items-center gap-1.5 pt-1 border-t border-slate-100">
                                <span className="text-[11px] font-bold text-slate-400 mr-1 flex items-center gap-1">
                                    <Filter size={11} /> Filters:
                                </span>
                                <button
                                    onClick={() => setBedFilter("all")}
                                    className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                                        bedFilter === "all" ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                                    }`}
                                >
                                    All Facilities ({hospitals.length})
                                </button>
                                <button
                                    onClick={() => setBedFilter("icu")}
                                    className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                                        bedFilter === "icu" ? "bg-indigo-600 text-white" : "bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200"
                                    }`}
                                >
                                    ICU Ready
                                </button>
                                <button
                                    onClick={() => setBedFilter("emergency")}
                                    className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                                        bedFilter === "emergency" ? "bg-rose-600 text-white" : "bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200"
                                    }`}
                                >
                                    ER Beds Available
                                </button>
                                <button
                                    onClick={() => setBedFilter("ambulance")}
                                    className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                                        bedFilter === "ambulance" ? "bg-emerald-600 text-white" : "bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200"
                                    }`}
                                >
                                    Ambulance Standby
                                </button>
                            </div>
                        </div>

                        {/* RESULTS LIST */}
                        {loadingHospitals ? (
                            <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 shadow-xs">
                                <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent mb-2"></div>
                                <p className="text-xs text-slate-500 font-medium">Scanning live bed registries & GPS coordinates across {selectedCity}...</p>
                            </div>
                        ) : displayedHospitals.length === 0 ? (
                            <div className="p-8 text-center bg-white rounded-2xl border border-slate-200 shadow-xs space-y-2">
                                <AlertTriangle size={24} className="mx-auto text-amber-500" />
                                <h4 className="text-sm font-bold text-slate-900">No Hospitals Found in Radius</h4>
                                <p className="text-xs text-slate-500 max-w-sm mx-auto">
                                    No facilities match within {radiusKm} km of {selectedCity}. Try expanding the radius slider to 50 km or 100 km.
                                </p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {displayedHospitals.map((item, idx) => {
                                    const h = item.hospital;
                                    const beds = item.beds;
                                    const isTopMatch = idx === 0 && !emergencyMode;
                                    const isTopEmergency = idx === 0 && emergencyMode;

                                    return (
                                        <div
                                            key={h.id}
                                            className={`bg-white rounded-2xl p-5 shadow-xs transition space-y-4 ${
                                                isTopEmergency
                                                    ? "border-2 border-rose-500 ring-4 ring-rose-500/10"
                                                    : isTopMatch
                                                    ? "border-2 border-blue-500 ring-4 ring-blue-500/10"
                                                    : "border border-slate-200 hover:border-slate-300"
                                            }`}
                                        >
                                            {/* HEADER INFO */}
                                            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
                                                <div>
                                                    <div className="flex flex-wrap items-center gap-2">
                                                        <h4 className="text-base font-bold text-slate-900 tracking-tight">
                                                            {h.name}
                                                        </h4>
                                                        {item.recommendation_badge && (
                                                            <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                                                                item.recommendation_badge.includes("Emergency") || item.recommendation_badge.includes("Fastest")
                                                                    ? "bg-rose-100 text-rose-800 border border-rose-200"
                                                                    : "bg-blue-100 text-blue-800 border border-blue-200"
                                                            }`}>
                                                                {item.recommendation_badge}
                                                            </span>
                                                        )}
                                                        <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                                                            24x7
                                                        </span>
                                                    </div>
                                                    <p className="text-xs text-slate-500 mt-0.5 flex items-center gap-1">
                                                        <MapPin size={12} className="text-slate-400 shrink-0" />
                                                        {h.address || `${h.city}, India`}
                                                    </p>
                                                </div>

                                                <div className="text-left sm:text-right shrink-0">
                                                    <span className="text-[10px] font-medium text-slate-400 block uppercase">Match Score</span>
                                                    <span className="text-xl font-extrabold text-blue-600">
                                                        {item.match_score}<span className="text-xs font-normal text-slate-400">/100</span>
                                                    </span>
                                                </div>
                                            </div>

                                            {/* WHY TAGS CHIPS */}
                                            <div className="flex flex-wrap gap-1.5">
                                                {item.why_tags.map((tag, tIdx) => (
                                                    <span
                                                        key={tIdx}
                                                        className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold border ${
                                                            tag.includes("km")
                                                                ? "bg-blue-50 text-blue-700 border-blue-100"
                                                                : tag.includes("ICU")
                                                                ? "bg-indigo-50 text-indigo-700 border-indigo-100"
                                                                : tag.includes("ER") || tag.includes("Emergency")
                                                                ? "bg-rose-50 text-rose-700 border-rose-100"
                                                                : tag.includes("Ambulance")
                                                                ? "bg-emerald-50 text-emerald-700 border-emerald-100"
                                                                : "bg-slate-50 text-slate-700 border-slate-200"
                                                        }`}
                                                    >
                                                        {tag}
                                                    </span>
                                                ))}
                                            </div>

                                            {/* WHY THIS HOSPITAL SUMMARY */}
                                            {item.why_summary && (
                                                <p className="text-xs text-slate-600 bg-slate-50/70 p-2.5 rounded-xl border border-slate-100 leading-relaxed">
                                                    <strong className="text-slate-800">Why This Hospital:</strong> {item.why_summary}
                                                </p>
                                            )}

                                            {/* BED CAPACITY METERS WITH VISUAL PERCENTAGE GAUGES */}
                                            <div className="grid grid-cols-3 gap-2.5 text-center">
                                                {/* ICU BEDS */}
                                                <div className="p-3 rounded-xl bg-indigo-50/70 border border-indigo-100 space-y-1">
                                                    <div className="flex items-center justify-between text-[11px] font-bold text-indigo-950">
                                                        <span>ICU Beds</span>
                                                        <span>{beds.icu.available} / {beds.icu.total}</span>
                                                    </div>
                                                    <div className="w-full bg-indigo-200/60 h-1.5 rounded-full overflow-hidden">
                                                        <div
                                                            className={`h-full rounded-full ${beds.icu.available > 3 ? 'bg-indigo-600' : beds.icu.available > 0 ? 'bg-amber-500' : 'bg-rose-500'}`}
                                                            style={{ width: `${beds.icu.total > 0 ? Math.round((beds.icu.available / beds.icu.total) * 100) : 0}%` }}
                                                        ></div>
                                                    </div>
                                                    <p className="text-[10px] text-indigo-600 font-semibold text-right">
                                                        {beds.icu.total > 0 ? `${Math.round((beds.icu.available / beds.icu.total) * 100)}% Available` : "N/A"}
                                                    </p>
                                                </div>

                                                {/* ER BEDS */}
                                                <div className="p-3 rounded-xl bg-rose-50/70 border border-rose-100 space-y-1">
                                                    <div className="flex items-center justify-between text-[11px] font-bold text-rose-950">
                                                        <span>Emergency</span>
                                                        <span>{beds.emergency.available} / {beds.emergency.total}</span>
                                                    </div>
                                                    <div className="w-full bg-rose-200/60 h-1.5 rounded-full overflow-hidden">
                                                        <div
                                                            className={`h-full rounded-full ${beds.emergency.available > 2 ? 'bg-rose-600' : 'bg-amber-500'}`}
                                                            style={{ width: `${beds.emergency.total > 0 ? Math.round((beds.emergency.available / beds.emergency.total) * 100) : 0}%` }}
                                                        ></div>
                                                    </div>
                                                    <p className="text-[10px] text-rose-600 font-semibold text-right">
                                                        {beds.emergency.total > 0 ? `${Math.round((beds.emergency.available / beds.emergency.total) * 100)}% Available` : "N/A"}
                                                    </p>
                                                </div>

                                                {/* GENERAL BEDS */}
                                                <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
                                                    <div className="flex items-center justify-between text-[11px] font-bold text-slate-800">
                                                        <span>General</span>
                                                        <span>{beds.general.available} / {beds.general.total}</span>
                                                    </div>
                                                    <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                                                        <div
                                                            className="h-full bg-blue-600 rounded-full"
                                                            style={{ width: `${beds.general.total > 0 ? Math.round((beds.general.available / beds.general.total) * 100) : 0}%` }}
                                                        ></div>
                                                    </div>
                                                    <p className="text-[10px] text-slate-500 font-semibold text-right">
                                                        {beds.general.total > 0 ? `${Math.round((beds.general.available / beds.general.total) * 100)}% Available` : "N/A"}
                                                    </p>
                                                </div>
                                            </div>

                                            {/* DOCTORS ON DUTY */}
                                            {item.doctors && item.doctors.length > 0 && (
                                                <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-100 flex flex-wrap items-center gap-2">
                                                    <span className="text-[11px] font-bold text-slate-700 flex items-center gap-1.5">
                                                        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                                        {item.doctors.length} Doctors On Duty
                                                        {item.matching_doctors && item.matching_doctors.length > 0 && (
                                                            <span className="text-blue-600 font-normal">
                                                                ({item.matching_doctors.length} matched Specialists)
                                                            </span>
                                                        )}:
                                                    </span>
                                                    <div className="flex flex-wrap gap-1.5">
                                                        {item.doctors.slice(0, 3).map((d) => (
                                                            <span key={d.id} className="text-[11px] px-2 py-0.5 rounded-md bg-white border border-slate-200 text-slate-800 font-medium">
                                                                {d.name} • {d.specialization} (₹{d.consultation_fee})
                                                            </span>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}

                                            {/* FOOTER ACTIONS */}
                                            <div className="pt-2 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                                                <div className="flex items-center gap-3 text-xs text-slate-500">
                                                    <a href={`tel:${h.phone}`} className="flex items-center gap-1 hover:text-blue-600 font-medium">
                                                        <Phone size={12} /> {h.phone}
                                                    </a>
                                                    {h.emergency_contact && (
                                                        <a href={`tel:${h.emergency_contact}`} className="flex items-center gap-1 text-rose-600 font-bold hover:underline">
                                                            <PhoneCall size={12} /> Emergency: {h.emergency_contact}
                                                        </a>
                                                    )}
                                                    <a
                                                        href={`https://www.google.com/maps/dir/?api=1&destination=${h.latitude},${h.longitude}`}
                                                        target="_blank"
                                                        rel="noreferrer"
                                                        className="flex items-center gap-1 text-indigo-600 hover:text-indigo-800 font-medium"
                                                        title="Open in Google Maps"
                                                    >
                                                        <Navigation size={12} /> Directions
                                                    </a>
                                                </div>

                                                <div className="flex items-center gap-2">
                                                    <button
                                                        onClick={() => handleInitiateBookDoctor(item)}
                                                        className="px-3.5 py-1.5 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-700 font-bold text-xs border border-blue-200 transition flex items-center gap-1.5 cursor-pointer shadow-2xs"
                                                    >
                                                        <Calendar size={13} />
                                                        Book Doctor OPD
                                                    </button>
                                                    <button
                                                        onClick={() => openEmergencyModal(item)}
                                                        className="px-3.5 py-1.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs shadow-xs transition flex items-center gap-1.5 cursor-pointer"
                                                    >
                                                        <HeartPulse size={14} />
                                                        Dispatch Ambulance
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </div>
                </div>

                {/* ============================================================== */}
                {/* SECTION 4: TOP VERIFIED SPECIALIST DOCTORS ON DUTY             */}
                {/* ============================================================== */}
                <div id="featured-doctors-section" className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs space-y-5">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                        <div>
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-8 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
                                    <Stethoscope size={18} />
                                </div>
                                <h3 className="text-base font-extrabold text-slate-900">
                                    Top Verified Specialist Doctors on Duty
                                </h3>
                                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-100 text-emerald-800 border border-emerald-200">
                                    ● OPD Active Today
                                </span>
                            </div>
                            <p className="text-xs text-slate-500 mt-1">
                                Consult top-rated board-certified specialists across partner hospitals with digital tokens & prescriptions
                            </p>
                        </div>

                        <div className="flex items-center gap-2">
                            <span className="text-xs font-semibold text-slate-500">
                                Showing {featuredDoctors.length} Specialists
                            </span>
                        </div>
                    </div>

                    {featuredDoctors.length === 0 ? (
                        <p className="text-xs text-slate-400 py-6 text-center">Scanning on-duty doctor rosters across {selectedCity}...</p>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
                            {featuredDoctors.slice(0, 8).map((doc, dIdx) => (
                                <div
                                    key={dIdx}
                                    className="p-4 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:border-blue-300 hover:shadow-sm transition space-y-3 flex flex-col justify-between"
                                >
                                    <div className="space-y-2">
                                        <div className="flex items-start justify-between gap-2">
                                            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white flex items-center justify-center font-bold text-sm shadow-xs">
                                                {(doc.name || "Dr").replace("Dr.", "").trim().slice(0, 2).toUpperCase()}
                                            </div>
                                            <span className="text-[11px] font-extrabold text-blue-700 bg-blue-50 px-2 py-0.5 rounded-lg border border-blue-100">
                                                ₹{doc.consultation_fee || 800}
                                            </span>
                                        </div>

                                        <div>
                                            <h4 className="font-extrabold text-slate-900 text-sm leading-tight">{doc.name}</h4>
                                            <p className="text-xs text-blue-600 font-bold mt-0.5">{doc.specialization}</p>
                                            <p className="text-[11px] text-slate-500 flex items-center gap-1 mt-1 truncate" title={doc.hospital_name}>
                                                <Building2 size={11} className="text-slate-400 shrink-0" />
                                                <span className="truncate">{doc.hospital_name}</span>
                                            </p>
                                        </div>
                                    </div>

                                    <div className="pt-2 border-t border-slate-200/60 flex items-center justify-between gap-2">
                                        <span className="text-[10px] text-emerald-700 font-bold flex items-center gap-1">
                                            <Clock size={11} /> {doc.experience_years ? `${doc.experience_years} yrs exp` : "9:00 AM - 1:00 PM"}
                                        </span>
                                        <button
                                            onClick={() => handleInitiateBookDoctor(doc.hospital_item)}
                                            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-xs transition flex items-center gap-1 cursor-pointer"
                                        >
                                            <Calendar size={12} /> Book
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* ============================================================== */}
                {/* SECTION 5: HOW MEDILINK WORKS (3-STEP VISUAL PIPELINE)         */}
                {/* ============================================================== */}
                <div className="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-950 rounded-3xl p-6 sm:p-8 text-white shadow-xl space-y-6">
                    <div className="text-center max-w-2xl mx-auto space-y-1.5">
                        <span className="px-3 py-1 rounded-full text-xs font-bold bg-blue-500/20 text-blue-300 border border-blue-400/30">
                            Streamlined Patient Experience
                        </span>
                        <h3 className="text-xl sm:text-2xl font-extrabold tracking-tight">
                            How MediLink Connects You to Care in Seconds
                        </h3>
                        <p className="text-xs text-indigo-200/80">
                            Powered by real-time hospital bed sockets, AI triage, and live emergency telemetry
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                        <div className="p-5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 space-y-3">
                            <div className="w-10 h-10 rounded-xl bg-blue-500/30 text-blue-300 flex items-center justify-center font-bold text-lg">
                                1
                            </div>
                            <h4 className="text-sm font-extrabold text-white">Smart Triage & Proximity Scan</h4>
                            <p className="text-xs text-indigo-200/80 leading-relaxed">
                                Type symptoms or pick a specialty. Our TF-IDF machine learning engine determines care urgency and scans facilities within your radius.
                            </p>
                        </div>

                        <div className="p-5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 space-y-3">
                            <div className="w-10 h-10 rounded-xl bg-indigo-500/30 text-indigo-300 flex items-center justify-center font-bold text-lg">
                                2
                            </div>
                            <h4 className="text-sm font-extrabold text-white">Real-Time Bed Verification</h4>
                            <p className="text-xs text-indigo-200/80 leading-relaxed">
                                No phone calls needed. Live counters for ICU, ER trauma, and general beds synchronize directly from hospital admission desks every 15s.
                            </p>
                        </div>

                        <div className="p-5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 space-y-3">
                            <div className="w-10 h-10 rounded-xl bg-rose-500/30 text-rose-300 flex items-center justify-center font-bold text-lg">
                                3
                            </div>
                            <h4 className="text-sm font-extrabold text-white">Instant Care or SOS Dispatch</h4>
                            <p className="text-xs text-indigo-200/80 leading-relaxed">
                                Book a verified doctor consultation with an instant digital token pass, or mobilize a paramedic ambulance in under 8 minutes.
                            </p>
                        </div>
                    </div>
                </div>

                {/* ============================================================== */}
                {/* SECTION 6: CLINICAL ACCREDITATIONS & SECURITY STANDARDS        */}
                {/* ============================================================== */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
                    <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-1.5">
                        <div className="flex items-center gap-2 text-blue-600">
                            <ShieldCheck size={18} />
                            <h4 className="text-xs font-extrabold text-slate-900">NABH Verified Network</h4>
                        </div>
                        <p className="text-[11px] text-slate-500">Partnered exclusively with accredited clinical & emergency infrastructure.</p>
                    </div>

                    <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-1.5">
                        <div className="flex items-center gap-2 text-emerald-600">
                            <CheckCircle2 size={18} />
                            <h4 className="text-xs font-extrabold text-slate-900">ABDM Health Records</h4>
                        </div>
                        <p className="text-[11px] text-slate-500">National Ayushman Bharat Digital Mission interoperable electronic health records.</p>
                    </div>

                    <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-1.5">
                        <div className="flex items-center gap-2 text-purple-600">
                            <Activity size={18} />
                            <h4 className="text-xs font-extrabold text-slate-900">15s Live Sockets</h4>
                        </div>
                        <p className="text-[11px] text-slate-500">Active WebSocket broadcast between hospital triage wards and public registries.</p>
                    </div>

                    <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs space-y-1.5">
                        <div className="flex items-center gap-2 text-indigo-600">
                            <Lock size={18} />
                            <h4 className="text-xs font-extrabold text-slate-900">256-Bit Data Privacy</h4>
                        </div>
                        <p className="text-[11px] text-slate-500">End-to-end encrypted consultations, diagnostic history, and patient profiles.</p>
                    </div>
                </div>

                {/* ============================================================== */}
                {/* SECTION 7: FREQUENTLY ASKED QUESTIONS (FAQ) ACCORDION          */}
                {/* ============================================================== */}
                <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs space-y-4">
                    <div className="border-b border-slate-100 pb-3">
                        <h3 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
                            <HelpCircle size={18} className="text-blue-600" />
                            <span>Frequently Asked Questions</span>
                        </h3>
                        <p className="text-xs text-slate-500">Everything you need to know about real-time bed tracking, emergency dispatch, and digital OPD passes</p>
                    </div>

                    <div className="divide-y divide-slate-100">
                        {FAQ_ITEMS.map((item, idx) => {
                            const isOpen = openFaq === idx;
                            return (
                                <div key={idx} className="py-3">
                                    <button
                                        onClick={() => toggleFaq(idx)}
                                        className="w-full text-left flex items-center justify-between gap-3 text-xs font-bold text-slate-900 hover:text-blue-600 transition cursor-pointer"
                                    >
                                        <span className="text-sm font-bold">{item.q}</span>
                                        {isOpen ? <ChevronUp size={16} className="text-blue-600 shrink-0" /> : <ChevronDown size={16} className="text-slate-400 shrink-0" />}
                                    </button>
                                    {isOpen && (
                                        <p className="mt-2 text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100 animate-in fade-in slide-in-from-top-1">
                                            {item.a}
                                        </p>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                </div>

                {/* ============================================================== */}
                {/* SECTION 8: 24x7 EMERGENCY COMMAND BANNER                       */}
                {/* ============================================================== */}
                <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 rounded-3xl p-6 sm:p-7 text-white shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-5 border border-indigo-800/40">
                    <div className="space-y-1">
                        <span className="text-xs font-bold text-rose-400 uppercase tracking-wider block">National Emergency Response Network</span>
                        <h4 className="text-lg sm:text-xl font-extrabold">Require Immediate Medical Assistance?</h4>
                        <p className="text-xs text-indigo-200">Our dispatch center operates 24 hours a day, 7 days a week with zero toll charges.</p>
                    </div>

                    <div className="flex flex-wrap items-center gap-2.5">
                        <a
                            href="tel:108"
                            className="px-5 py-2.5 bg-rose-600 hover:bg-rose-500 text-white font-extrabold text-xs rounded-xl transition flex items-center gap-2 shadow-xs cursor-pointer"
                        >
                            <PhoneCall size={15} />
                            <span>Emergency SOS (108)</span>
                        </a>
                        <a
                            href="tel:102"
                            className="px-4 py-2.5 bg-white/15 hover:bg-white/20 text-white font-bold text-xs rounded-xl transition border border-white/20 cursor-pointer"
                        >
                            <span>Ambulance (102)</span>
                        </a>
                        <a
                            href="tel:112"
                            className="px-4 py-2.5 bg-white/15 hover:bg-white/20 text-white font-bold text-xs rounded-xl transition border border-white/20 cursor-pointer"
                        >
                            <span>All-in-One (112)</span>
                        </a>
                    </div>
                </div>
            </div>
            )}

            {/* ============================================================== */}
            {/* 4. TAB 2: MY CONSULTATIONS & DIGITAL OPD PASSES                */}
            {/* ============================================================== */}
            {activeTab === "appointments" && (
                <div className="space-y-6">
                    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                            <div>
                                <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                    <Calendar size={18} className="text-blue-600" />
                                    My Scheduled OPD Consultations
                                </h3>
                                <p className="text-xs text-slate-500">
                                    View your doctor appointments, download official digital OPD token passes, or manage schedules.
                                </p>
                            </div>
                            <button
                                onClick={() => {
                                    if (hospitals.length > 0) {
                                        openBookingModal(hospitals[0]);
                                    }
                                }}
                                className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-xs"
                            >
                                <PlusCircle size={14} /> Schedule New OPD
                            </button>
                        </div>

                        {/* Status Filter Chips */}
                        <div className="flex flex-wrap items-center gap-2 pt-1">
                            {["all", "Scheduled", "Cancelled"].map(f => {
                                const count = f === "all" ? myAppointments.length : myAppointments.filter(a => a.status === f).length;
                                return (
                                    <button
                                        key={f}
                                        onClick={() => setApptFilter(f)}
                                        className={`px-3 py-1 rounded-xl text-xs font-bold transition cursor-pointer ${
                                            apptFilter === f
                                                ? "bg-slate-900 text-white shadow-xs"
                                                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                                        }`}
                                    >
                                        {f === "all" ? `All Consultations (${count})` :
                                         f === "Scheduled" ? `Upcoming / Confirmed (${count})` :
                                         `Cancelled (${count})`}
                                    </button>
                                );
                            })}
                        </div>

                        {myAppointments.filter(a => apptFilter === "all" || a.status === apptFilter).length === 0 ? (
                            <div className="p-12 text-center space-y-2">
                                <Calendar size={32} className="mx-auto text-slate-300" />
                                <h4 className="text-sm font-bold text-slate-800">
                                    {apptFilter === "all" ? "No OPD Appointments Booked Yet" : `No ${apptFilter} Consultations`}
                                </h4>
                                <p className="text-xs text-slate-500 max-w-sm mx-auto">
                                    You don't have any appointments in this status. Schedule a direct OPD visit with network specialists.
                                </p>
                                <button
                                    onClick={() => {
                                        if (hospitals.length > 0) {
                                            openBookingModal(hospitals[0]);
                                        }
                                    }}
                                    className="mt-2 px-4 py-2 bg-blue-600 text-white text-xs font-bold rounded-xl hover:bg-blue-700 transition cursor-pointer"
                                >
                                    Schedule Doctor OPD
                                </button>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {myAppointments.filter(a => apptFilter === "all" || a.status === apptFilter).map((apt) => (
                                    <div key={apt.id} className="p-4 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:border-blue-200 hover:shadow-xs transition space-y-3">
                                        <div className="flex items-start justify-between gap-2">
                                            <div className="flex items-center gap-3">
                                                <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-sm">
                                                    {(apt.doctor_name || "DR").split(" ").map(w => w[0]).join("").slice(0, 2)}
                                                </div>
                                                <div>
                                                    <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                                                        {apt.doctor_name}
                                                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200">
                                                            {apt.specialization}
                                                        </span>
                                                    </h4>
                                                    <p className="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                                                        <Building2 size={12} className="text-slate-400" />
                                                        {apt.hospital_name}
                                                    </p>
                                                </div>
                                            </div>

                                            <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                                                apt.status === "Scheduled" ? "bg-emerald-100 text-emerald-800" :
                                                apt.status === "Cancelled" ? "bg-slate-200 text-slate-600" : "bg-blue-100 text-blue-800"
                                            }`}>
                                                {apt.status}
                                            </span>
                                        </div>

                                        <div className="grid grid-cols-2 gap-2 text-xs p-3 rounded-xl bg-white border border-slate-200/70">
                                            <div>
                                                <span className="text-[10px] font-bold text-slate-400 uppercase block">Consultation Date</span>
                                                <span className="font-semibold text-slate-800">{apt.date}</span>
                                            </div>
                                            <div>
                                                <span className="text-[10px] font-bold text-slate-400 uppercase block">Appointment Slot</span>
                                                <span className="font-semibold text-slate-800">{apt.time}</span>
                                            </div>
                                            <div className="col-span-2 pt-1 border-t border-slate-100">
                                                <span className="text-[10px] font-bold text-slate-400 uppercase block">Reason for Visit</span>
                                                <span className="text-slate-700">{apt.reason || "Routine Clinical Consultation"}</span>
                                            </div>
                                        </div>

                                        <div className="flex items-center justify-between pt-1">
                                            <span className="text-xs font-bold text-slate-700">
                                                Fee: <span className="text-blue-600 font-extrabold">₹{apt.consultation_fee || 900}</span>
                                                <span className="text-[10px] font-normal text-slate-400 ml-1">({apt.payment_status || 'Paid'})</span>
                                            </span>

                                            <div className="flex items-center gap-2">
                                                {apt.status === "Scheduled" && (
                                                    <button
                                                        onClick={() => handleCancelAppointment(apt.id)}
                                                        className="px-2.5 py-1.5 text-xs text-rose-600 hover:bg-rose-50 rounded-lg transition font-semibold cursor-pointer"
                                                    >
                                                        Cancel
                                                    </button>
                                                )}
                                                {apt.status === "Completed" && (
                                                    <button
                                                        onClick={() => {
                                                            const rx = myPrescriptions.find(p => p.doctor_name === apt.doctor_name) || myPrescriptions[0];
                                                            if (rx) {
                                                                setSelectedPrescription(rx);
                                                            } else {
                                                                setActiveTab("prescriptions");
                                                            }
                                                        }}
                                                        className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 shadow-2xs cursor-pointer"
                                                    >
                                                        <FileText size={13} /> View Prescription (e-Rx)
                                                    </button>
                                                )}
                                                <button
                                                    onClick={() => setSelectedOpdPass(apt)}
                                                    className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 shadow-2xs cursor-pointer"
                                                >
                                                    <QrCode size={13} /> View OPD Pass
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 5. TAB 3: EMERGENCY SOS DISPATCH TRACKING                      */}
            {/* ============================================================== */}
            {activeTab === "emergencies" && (
                <div className="space-y-6">
                    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                            <div>
                                <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                    <Truck size={18} className="text-rose-600" />
                                    Active Emergency Ambulance Tracker
                                </h3>
                                <p className="text-xs text-slate-500">
                                    Real-time tracking of mobilized ambulances, paramedic contacts, and destination hospital trauma units.
                                </p>
                            </div>
                            <button
                                onClick={() => setEmergencyMode(true)}
                                className="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 cursor-pointer animate-pulse"
                            >
                                <PhoneCall size={14} /> Dispatch SOS Ambulance
                            </button>
                        </div>

                        {myEmergencies.length === 0 ? (
                            <div className="p-12 text-center space-y-2">
                                <Truck size={32} className="mx-auto text-slate-300" />
                                <h4 className="text-sm font-bold text-slate-800">No Active Emergency Requests</h4>
                                <p className="text-xs text-slate-500 max-w-sm mx-auto">
                                    You have not mobilized any ambulances. In case of medical emergencies, click "Dispatch Ambulance" on any hospital card or dial 108.
                                </p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {myEmergencies.map((emg) => (
                                    <div key={emg.id} className="p-5 rounded-2xl border-2 border-rose-200 bg-rose-50/30 space-y-4">
                                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <span className="px-2.5 py-0.5 rounded text-[10px] font-extrabold bg-rose-600 text-white uppercase tracking-wider">
                                                        {emg.priority} PRIORITY
                                                    </span>
                                                    <h4 className="text-sm font-bold text-slate-900">{emg.emergency_type}</h4>
                                                </div>
                                                <p className="text-xs text-slate-600 mt-1">
                                                    Target Facility: <strong className="text-slate-900">{emg.hospital_name}</strong>
                                                </p>
                                                <p className="text-[11px] text-slate-400">
                                                    Pickup Landmark: {emg.pickup_location} • Logged: {emg.created_at}
                                                </p>
                                            </div>

                                            <div className="text-left sm:text-right">
                                                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                                                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                                    {emg.status}
                                                </span>
                                                {emg.ambulance_reg && (
                                                    <p className="text-xs font-mono font-bold text-slate-800 mt-1">Unit: {emg.ambulance_reg}</p>
                                                )}
                                            </div>
                                        </div>

                                        {/* DISPATCH STEPPER */}
                                        <div className="p-4 bg-white rounded-xl border border-rose-100 space-y-2">
                                            <p className="text-[10px] font-bold text-slate-400 uppercase">Live Milestone Stepper</p>
                                            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
                                                <div className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 font-semibold flex items-center gap-2">
                                                    <CheckCircle2 size={16} className="text-emerald-600 shrink-0" />
                                                    <span>1. SOS Alert Logged</span>
                                                </div>
                                                <div className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 font-semibold flex items-center gap-2">
                                                    <CheckCircle2 size={16} className="text-emerald-600 shrink-0" />
                                                    <span>2. Unit Mobilized</span>
                                                </div>
                                                <div className="p-2.5 rounded-lg bg-rose-50 border border-rose-300 text-rose-900 font-bold flex items-center gap-2">
                                                    <span className="w-2.5 h-2.5 rounded-full bg-rose-600 animate-ping shrink-0"></span>
                                                    <span>3. En Route (ETA ~8-12m)</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex items-center justify-between text-xs pt-1">
                                            <span className="text-slate-500">
                                                Emergency Helpline: <strong className="text-rose-600">108 / 112</strong>
                                            </span>
                                            <a
                                                href="tel:108"
                                                className="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-lg transition flex items-center gap-1.5"
                                            >
                                                <PhoneCall size={12} /> Call Paramedic
                                            </a>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 6. TAB 4: PRESCRIPTIONS & CLINICAL RECORDS                     */}
            {/* ============================================================== */}
            {activeTab === "prescriptions" && (
                <div className="space-y-6">
                    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                            <div>
                                <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                    <Pill size={18} className="text-emerald-600" />
                                    Digital Prescriptions & Clinical Advice
                                </h3>
                                <p className="text-xs text-slate-500">
                                    Official electronic prescriptions issued by attending doctors across MediLink partner facilities.
                                </p>
                            </div>
                        </div>

                        {myPrescriptions.length === 0 ? (
                            <div className="p-12 text-center space-y-2">
                                <Pill size={32} className="mx-auto text-slate-300" />
                                <h4 className="text-sm font-bold text-slate-800">No Prescriptions On Record</h4>
                                <p className="text-xs text-slate-500 max-w-sm mx-auto">
                                    Your digital prescriptions will appear here once you complete a doctor consultation.
                                </p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {myPrescriptions.map((rx) => (
                                    <div key={rx.id} className="p-5 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:border-emerald-200 hover:shadow-xs transition space-y-3">
                                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200/70 pb-3">
                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <h4 className="text-sm font-bold text-slate-900">{rx.doctor_name}</h4>
                                                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                                                        {rx.specialization}
                                                    </span>
                                                </div>
                                                <p className="text-xs text-slate-500 mt-0.5">{rx.hospital_name}</p>
                                            </div>
                                            <span className="text-xs font-semibold text-slate-500">
                                                Issued: {rx.created_at}
                                            </span>
                                        </div>

                                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs p-3.5 rounded-xl bg-white border border-slate-200/80">
                                            <div>
                                                <span className="text-[10px] font-bold text-slate-400 uppercase block">Prescribed Medicine</span>
                                                <span className="font-bold text-slate-900 text-sm">{rx.medicines}</span>
                                            </div>
                                            <div>
                                                <span className="text-[10px] font-bold text-slate-400 uppercase block">Dosage & Frequency</span>
                                                <div className="flex items-center gap-1.5 mt-0.5">
                                                    <span className="font-bold text-emerald-700 font-mono">{rx.dosage}</span>
                                                    <span className="px-1.5 py-0.2 rounded text-[10px] bg-amber-50 text-amber-800 border border-amber-200">
                                                        ☀️ Morning
                                                    </span>
                                                    <span className="px-1.5 py-0.2 rounded text-[10px] bg-indigo-50 text-indigo-800 border border-indigo-200">
                                                        🌙 Night
                                                    </span>
                                                </div>
                                            </div>
                                            <div>
                                                <span className="text-[10px] font-bold text-slate-400 uppercase block">Duration</span>
                                                <span className="font-semibold text-slate-800">{rx.duration}</span>
                                            </div>
                                            <div className="sm:col-span-3 pt-2 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                                                <div>
                                                    <span className="text-[10px] font-bold text-slate-400 uppercase block">Doctor Instructions</span>
                                                    <p className="text-slate-600 mt-0.5">{rx.instructions}</p>
                                                </div>
                                                <button
                                                    type="button"
                                                    onClick={() => setSelectedPrescription(rx)}
                                                    className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-2xs shrink-0"
                                                >
                                                    <FileText size={13} /> View & Print Digital Rx
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                ))}

                                {/* MEDICAL RECORDS SUMMARY */}
                                {myMedicalRecords.length > 0 && (
                                    <div className="mt-6 pt-6 border-t border-slate-200 space-y-3">
                                        <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                                            <FileText size={16} className="text-blue-600" />
                                            Attending Physician Diagnostic Notes
                                        </h4>
                                        {myMedicalRecords.map((mr) => (
                                            <div key={mr.id} className="p-4 rounded-xl border border-blue-100 bg-blue-50/30 text-xs space-y-2">
                                                <div className="flex items-center justify-between">
                                                    <span className="font-bold text-blue-950 text-sm">Diagnosis: {mr.diagnosis}</span>
                                                    <span className="text-slate-500">Follow-up: {mr.follow_up_date || "2 weeks"}</span>
                                                </div>
                                                <p className="text-slate-700"><strong>Symptoms Recorded:</strong> {mr.symptoms}</p>
                                                <p className="text-slate-700"><strong>Recommended Labs:</strong> {mr.lab_tests}</p>
                                                <p className="text-slate-600 bg-white p-2.5 rounded-lg border border-blue-100">
                                                    <strong>Clinical Advice:</strong> {mr.notes}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 7. TAB 5: BILLS & ITEMISED INVOICES                           */}
            {/* ============================================================== */}
            {activeTab === "bills" && (
                <div className="space-y-6">
                    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-4">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                            <div>
                                <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                    <Receipt size={18} className="text-amber-600" />
                                    Billing & Official Consultation Receipts
                                </h3>
                                <p className="text-xs text-slate-500">
                                    Review paid consultation fees, diagnostic invoice receipts, and pharmacy breakdowns.
                                </p>
                            </div>
                        </div>

                        {myBills.length === 0 ? (
                            <div className="p-12 text-center space-y-2">
                                <Receipt size={32} className="mx-auto text-slate-300" />
                                <h4 className="text-sm font-bold text-slate-800">No Billing Invoices Generated</h4>
                                <p className="text-xs text-slate-500 max-w-sm mx-auto">
                                    Your paid OPD consultation bills and medical receipts will be cataloged here.
                                </p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {myBills.map((b) => (
                                    <div key={b.id} className="p-5 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:border-amber-200 hover:shadow-xs transition space-y-3">
                                        <div className="flex items-center justify-between border-b border-slate-200/70 pb-3">
                                            <div>
                                                <h4 className="text-sm font-bold text-slate-900">{b.hospital_name}</h4>
                                                <span className="text-xs font-mono font-semibold text-slate-500">{b.invoice_number}</span>
                                            </div>
                                            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                                                ✓ {b.payment_status}
                                            </span>
                                        </div>

                                        <div className="space-y-1.5 text-xs text-slate-600">
                                            <div className="flex justify-between">
                                                <span>Doctor Consultation Charge:</span>
                                                <span className="font-semibold text-slate-800">₹{b.consultation_charge}</span>
                                            </div>
                                            {b.laboratory_charge > 0 && (
                                                <div className="flex justify-between">
                                                    <span>Laboratory & ECG Charges:</span>
                                                    <span className="font-semibold text-slate-800">₹{b.laboratory_charge}</span>
                                                </div>
                                            )}
                                            {b.medicine_charge > 0 && (
                                                <div className="flex justify-between">
                                                    <span>Pharmacy / Medication Charge:</span>
                                                    <span className="font-semibold text-slate-800">₹{b.medicine_charge}</span>
                                                </div>
                                            )}
                                            {b.discount > 0 && (
                                                <div className="flex justify-between text-emerald-700">
                                                    <span>Network Scheme Discount:</span>
                                                    <span>- ₹{b.discount}</span>
                                                </div>
                                            )}
                                            <div className="flex justify-between pt-2 border-t border-slate-200 font-extrabold text-sm text-slate-900">
                                                <span>Total Amount Paid:</span>
                                                <span className="text-blue-600">₹{b.total_amount}</span>
                                            </div>
                                        </div>

                                        <div className="pt-2 flex items-center justify-between">
                                            <span className="text-[11px] text-slate-400">Date: {b.created_at}</span>
                                            <button
                                                onClick={() => setSelectedBillReceipt(b)}
                                                className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-2xs"
                                            >
                                                <Download size={13} /> View Official Receipt
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 8. TAB 6: PATIENT PROFILE & HEALTH CARD (VIEW & EDIT)           */}
            {/* ============================================================== */}
            {activeTab === "profile" && (
                <div className="space-y-6">
                    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-6">
                        {/* HEADER WITH TOGGLE EDIT BUTTON */}
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                            <div>
                                <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                                    <UserCircle size={20} className="text-blue-600" />
                                    Patient Profile & ABDM Health Details
                                </h3>
                                <p className="text-xs text-slate-500">
                                    Manage your personal identity, contact details, medical information, and emergency contacts.
                                </p>
                            </div>

                            <button
                                type="button"
                                onClick={() => setIsEditingProfile(!isEditingProfile)}
                                className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 cursor-pointer shadow-xs ${
                                    isEditingProfile
                                        ? "bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200"
                                        : "bg-blue-600 hover:bg-blue-700 text-white"
                                }`}
                            >
                                {isEditingProfile ? (
                                    <>
                                        <X size={14} /> Cancel Editing
                                    </>
                                ) : (
                                    <>
                                        <Edit3 size={14} /> Edit Profile Information
                                    </>
                                )}
                            </button>
                        </div>

                        {/* SUCCESS FEEDBACK TOAST BANNER */}
                        {profileSaveMessage && (
                            <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold flex items-center gap-2">
                                <CheckCircle2 size={16} className="text-emerald-600 shrink-0" />
                                <span>{profileSaveMessage}</span>
                            </div>
                        )}

                        {/* MODE A: VIEW PROFILE & HEALTH CARD */}
                        {!isEditingProfile ? (
                            <div className="space-y-6">
                                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                                    {/* DIGITAL HEALTH CARD DISPLAY */}
                                    <div className="lg:col-span-1">
                                        <div className="bg-gradient-to-tr from-slate-900 via-indigo-950 to-blue-950 text-white rounded-3xl p-6 shadow-xl border border-white/10 space-y-5">
                                            <div className="flex items-center justify-between border-b border-white/15 pb-4">
                                                <div className="flex items-center gap-2.5">
                                                    <div className="w-10 h-10 rounded-2xl bg-blue-600 flex items-center justify-center font-bold text-white shadow-xs">
                                                        <HeartPulse size={20} />
                                                    </div>
                                                    <div>
                                                        <h4 className="font-extrabold text-sm tracking-tight">MediLink Health Card</h4>
                                                        <p className="text-[10px] text-indigo-300">National Healthcare Network</p>
                                                    </div>
                                                </div>
                                                <span className="font-mono text-xs font-bold text-emerald-400 border border-emerald-500/30 px-2.5 py-0.5 rounded-lg bg-emerald-500/10">
                                                    ACTIVE
                                                </span>
                                            </div>

                                            <div className="space-y-3">
                                                <div>
                                                    <span className="text-[10px] text-white/50 uppercase font-bold block">Patient Full Name</span>
                                                    <h3 className="text-lg font-bold tracking-tight">{myProfile?.full_name || user?.full_name || "Rahul Verma"}</h3>
                                                </div>

                                                <div className="grid grid-cols-2 gap-3 text-xs">
                                                    <div>
                                                        <span className="text-[10px] text-white/50 uppercase font-bold block">Patient Code</span>
                                                        <span className="font-mono font-bold text-blue-300">{myProfile?.patient_code || "#MED-PT-0001"}</span>
                                                    </div>
                                                    <div>
                                                        <span className="text-[10px] text-white/50 uppercase font-bold block">Blood Group</span>
                                                        <span className="font-bold text-rose-300">{myProfile?.blood_group || "B+ (RH+)"}</span>
                                                    </div>
                                                    <div>
                                                        <span className="text-[10px] text-white/50 uppercase font-bold block">Emergency Phone</span>
                                                        <span className="font-semibold text-white">{myProfile?.emergency_contact || "+91 9830099999"}</span>
                                                    </div>
                                                    <div>
                                                        <span className="text-[10px] text-white/50 uppercase font-bold block">Gender / Age</span>
                                                        <span className="font-semibold text-white">{myProfile?.gender || "Male"} • {myProfile?.age || 30} Yrs</span>
                                                    </div>
                                                </div>
                                            </div>

                                            {/* BARCODE FOOTER */}
                                            <div className="pt-3 border-t border-white/10 flex items-center justify-between text-[11px] text-indigo-200/80">
                                                <span>ABDM Interoperable Profile</span>
                                                <span className="font-mono text-[10px]">VERIFIED 2026</span>
                                            </div>
                                        </div>
                                    </div>

                                    {/* DETAILED PERSONAL & CLINICAL INFO SUMMARY */}
                                    <div className="lg:col-span-2 space-y-4">
                                        {/* PERSONAL INFORMATION CARD */}
                                        <div className="p-4 rounded-2xl bg-slate-50/70 border border-slate-200 space-y-3">
                                            <div className="flex items-center justify-between">
                                                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                                                    <User size={14} className="text-blue-600" /> Personal & Demographic Information
                                                </h4>
                                                <button
                                                    onClick={() => setIsEditingProfile(true)}
                                                    className="text-[11px] font-bold text-blue-600 hover:text-blue-800 flex items-center gap-1 cursor-pointer"
                                                >
                                                    <Edit3 size={12} /> Edit
                                                </button>
                                            </div>
                                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                                                <div className="p-2.5 rounded-xl bg-white border border-slate-200/70">
                                                    <span className="text-[10px] text-slate-400 font-bold uppercase block">Full Legal Name</span>
                                                    <span className="font-bold text-slate-900">{myProfile?.full_name || user?.full_name || "Rahul Verma"}</span>
                                                </div>
                                                <div className="p-2.5 rounded-xl bg-white border border-slate-200/70">
                                                    <span className="text-[10px] text-slate-400 font-bold uppercase block">Registered Email</span>
                                                    <span className="font-semibold text-slate-800">{user?.email}</span>
                                                </div>
                                                <div className="p-2.5 rounded-xl bg-white border border-slate-200/70">
                                                    <span className="text-[10px] text-slate-400 font-bold uppercase block">Primary Contact Phone</span>
                                                    <span className="font-semibold text-slate-800">{myProfile?.phone || "+91 9800000000"}</span>
                                                </div>
                                                <div className="p-2.5 rounded-xl bg-white border border-slate-200/70">
                                                    <span className="text-[10px] text-slate-400 font-bold uppercase block">Gender & Age</span>
                                                    <span className="font-semibold text-slate-800">{myProfile?.gender || "Male"} • {myProfile?.age || 30} Years</span>
                                                </div>
                                                <div className="sm:col-span-2 p-2.5 rounded-xl bg-white border border-slate-200/70">
                                                    <span className="text-[10px] text-slate-400 font-bold uppercase block">Residential City / Address</span>
                                                    <span className="font-semibold text-slate-800">{myProfile?.address || "Park Circus, Kolkata, West Bengal"}, {myProfile?.city || "Kolkata"}</span>
                                                </div>
                                            </div>
                                        </div>

                                        {/* EMERGENCY CONTACT & MEDICAL DETAILS */}
                                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                            {/* EMERGENCY CONTACT */}
                                            <div className="p-4 rounded-2xl bg-rose-50/40 border border-rose-200 space-y-2.5">
                                                <h4 className="text-xs font-bold text-rose-900 uppercase tracking-wider flex items-center gap-1.5">
                                                    <PhoneCall size={14} className="text-rose-600" /> Emergency Contact
                                                </h4>
                                                <div className="p-3 rounded-xl bg-white border border-rose-100 text-xs space-y-1">
                                                    <div className="flex justify-between">
                                                        <span className="text-slate-500">Contact Person:</span>
                                                        <span className="font-bold text-slate-900">{myProfile?.emergency_contact_name || "Family Contact"}</span>
                                                    </div>
                                                    <div className="flex justify-between">
                                                        <span className="text-slate-500">Relation:</span>
                                                        <span className="font-semibold text-slate-800">{myProfile?.emergency_contact_relation || "Immediate Family"}</span>
                                                    </div>
                                                    <div className="flex justify-between pt-1 border-t border-rose-50">
                                                        <span className="text-slate-500">Emergency Phone:</span>
                                                        <span className="font-bold text-rose-700">{myProfile?.emergency_contact_phone || myProfile?.emergency_contact || "+91 9830099999"}</span>
                                                    </div>
                                                </div>
                                            </div>

                                            {/* MEDICAL INFORMATION */}
                                            <div className="p-4 rounded-2xl bg-indigo-50/40 border border-indigo-200 space-y-2.5">
                                                <h4 className="text-xs font-bold text-indigo-900 uppercase tracking-wider flex items-center gap-1.5">
                                                    <HeartPulse size={14} className="text-indigo-600" /> Medical & Health History
                                                </h4>
                                                <div className="p-3 rounded-xl bg-white border border-indigo-100 text-xs space-y-1.5">
                                                    <div className="flex justify-between">
                                                        <span className="text-slate-500">Blood Group:</span>
                                                        <span className="font-bold text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">{myProfile?.blood_group || "B+"}</span>
                                                    </div>
                                                    <div>
                                                        <span className="text-[10px] text-slate-400 font-bold uppercase block">Known Allergies</span>
                                                        <span className="font-semibold text-slate-800">{myProfile?.allergies || "No drug allergies recorded"}</span>
                                                    </div>
                                                    <div>
                                                        <span className="text-[10px] text-slate-400 font-bold uppercase block">Chronic Conditions</span>
                                                        <span className="font-semibold text-slate-800">{myProfile?.chronic_conditions || "Stage 1 Hypertension"}</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            /* MODE B: INTERACTIVE PROFILE EDITOR FORM */
                            <form onSubmit={handleSaveProfile} className="space-y-6">
                                {/* SECTION 1: PERSONAL INFORMATION */}
                                <div className="p-5 rounded-2xl bg-slate-50/70 border border-slate-200 space-y-4">
                                    <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                                        <User size={14} className="text-blue-600" />
                                        1. Personal & Contact Information
                                    </h4>

                                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3.5">
                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Full Name <span className="text-rose-500">*</span>
                                            </label>
                                            <input
                                                type="text"
                                                required
                                                value={profileFormData.full_name}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, full_name: e.target.value })}
                                                placeholder="e.g. Rahul Verma"
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden font-medium"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Phone Number <span className="text-rose-500">*</span>
                                            </label>
                                            <input
                                                type="tel"
                                                required
                                                value={profileFormData.phone}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, phone: e.target.value })}
                                                placeholder="e.g. +91 9800000000"
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden font-medium"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Age (Years)
                                            </label>
                                            <input
                                                type="number"
                                                min="1"
                                                max="120"
                                                value={profileFormData.age}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, age: e.target.value })}
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden font-medium"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Gender
                                            </label>
                                            <select
                                                value={profileFormData.gender}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, gender: e.target.value })}
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden font-semibold"
                                            >
                                                <option value="Male">Male</option>
                                                <option value="Female">Female</option>
                                                <option value="Other">Other</option>
                                            </select>
                                        </div>

                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Blood Group
                                            </label>
                                            <select
                                                value={profileFormData.blood_group}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, blood_group: e.target.value })}
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden font-semibold"
                                            >
                                                <option value="A+">A+ (A Positive)</option>
                                                <option value="A-">A- (A Negative)</option>
                                                <option value="B+">B+ (B Positive)</option>
                                                <option value="B-">B- (B Negative)</option>
                                                <option value="O+">O+ (O Positive)</option>
                                                <option value="O-">O- (O Negative)</option>
                                                <option value="AB+">AB+ (AB Positive)</option>
                                                <option value="AB-">AB- (AB Negative)</option>
                                            </select>
                                        </div>

                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                City
                                            </label>
                                            <input
                                                type="text"
                                                value={profileFormData.city}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, city: e.target.value })}
                                                placeholder="e.g. Kolkata"
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden font-medium"
                                            />
                                        </div>

                                        <div className="sm:col-span-2 md:col-span-3">
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Residential Address
                                            </label>
                                            <input
                                                type="text"
                                                value={profileFormData.address}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, address: e.target.value })}
                                                placeholder="e.g. 42/B Park Circus 7-Point, Kolkata - 700017"
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden font-medium"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* SECTION 2: EMERGENCY CONTACT INFORMATION */}
                                <div className="p-5 rounded-2xl bg-rose-50/30 border border-rose-200 space-y-4">
                                    <h4 className="text-xs font-bold text-rose-950 uppercase tracking-wider flex items-center gap-1.5">
                                        <PhoneCall size={14} className="text-rose-600" />
                                        2. Emergency SOS Contact Person
                                    </h4>

                                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Emergency Contact Name
                                            </label>
                                            <input
                                                type="text"
                                                value={profileFormData.emergency_contact_name}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, emergency_contact_name: e.target.value })}
                                                placeholder="e.g. Anita Verma"
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-rose-500 focus:outline-hidden font-medium"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Relationship
                                            </label>
                                            <select
                                                value={profileFormData.emergency_contact_relation}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, emergency_contact_relation: e.target.value })}
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-rose-500 focus:outline-hidden font-semibold"
                                            >
                                                <option value="Spouse">Spouse</option>
                                                <option value="Parent">Parent</option>
                                                <option value="Child">Child</option>
                                                <option value="Sibling">Sibling</option>
                                                <option value="Guardian">Guardian</option>
                                                <option value="Friend">Friend / Relative</option>
                                                <option value="Other">Other</option>
                                            </select>
                                        </div>

                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Emergency Contact Phone
                                            </label>
                                            <input
                                                type="tel"
                                                value={profileFormData.emergency_contact_phone}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, emergency_contact_phone: e.target.value })}
                                                placeholder="e.g. +91 9830099999"
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-rose-500 focus:outline-hidden font-medium"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* SECTION 3: MEDICAL & CLINICAL HISTORY */}
                                <div className="p-5 rounded-2xl bg-indigo-50/30 border border-indigo-200 space-y-4">
                                    <h4 className="text-xs font-bold text-indigo-950 uppercase tracking-wider flex items-center gap-1.5">
                                        <HeartPulse size={14} className="text-indigo-600" />
                                        3. Medical & Clinical Background
                                    </h4>

                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Known Allergies (Drugs, Foods, Latex)
                                            </label>
                                            <input
                                                type="text"
                                                value={profileFormData.allergies}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, allergies: e.target.value })}
                                                placeholder="e.g. Penicillin, Peanuts, Sulfa antibiotics"
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-hidden font-medium"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Chronic Health Conditions
                                            </label>
                                            <input
                                                type="text"
                                                value={profileFormData.chronic_conditions}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, chronic_conditions: e.target.value })}
                                                placeholder="e.g. Stage 1 Hypertension, Type-2 Diabetes"
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-hidden font-medium"
                                            />
                                        </div>

                                        <div className="sm:col-span-2">
                                            <label className="block text-xs font-semibold text-slate-700 mb-1">
                                                Ongoing Medications
                                            </label>
                                            <input
                                                type="text"
                                                value={profileFormData.current_medications}
                                                onChange={(e) => setProfileFormData({ ...profileFormData, current_medications: e.target.value })}
                                                placeholder="e.g. Telmisartan 40mg once daily after breakfast"
                                                className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-hidden font-medium"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* FORM ACTION BUTTONS */}
                                <div className="flex items-center justify-end gap-3 pt-2">
                                    <button
                                        type="button"
                                        onClick={() => setIsEditingProfile(false)}
                                        className="px-4 py-2.5 rounded-xl border border-slate-200 text-xs font-bold text-slate-700 hover:bg-slate-50 transition cursor-pointer"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        type="submit"
                                        disabled={profileSaveLoading}
                                        className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-xs cursor-pointer"
                                    >
                                        <Save size={14} />
                                        {profileSaveLoading ? "Saving Changes..." : "Save Profile Information"}
                                    </button>
                                </div>
                            </form>
                        )}
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 9. DIGITAL OPD PASS MODAL (POPUP)                              */}
            {/* ============================================================== */}
            {selectedOpdPass && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl space-y-5 border border-slate-200">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-8 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold">
                                    <QrCode size={18} />
                                </div>
                                <div>
                                    <h3 className="text-sm font-bold text-slate-900">Digital OPD Consultation Pass</h3>
                                    <p className="text-[11px] text-slate-500">Present this token at the hospital reception</p>
                                </div>
                            </div>
                            <button onClick={() => setSelectedOpdPass(null)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        {/* PASS TICKET CONTAINER */}
                        <div className="p-5 rounded-2xl bg-gradient-to-b from-blue-50/60 to-slate-50 border-2 border-dashed border-blue-200 space-y-4">
                            <div className="text-center space-y-1">
                                <span className="text-[10px] uppercase font-bold text-blue-700 tracking-wider">Hospital OPD Queue Token</span>
                                <div className="flex items-center justify-center gap-2">
                                    <h2 className="text-3xl font-extrabold font-mono text-blue-900 tracking-tight">
                                        TK-OPD-10{selectedOpdPass.id}
                                    </h2>
                                    <button
                                        type="button"
                                        onClick={() => handleCopyToken(`TK-OPD-10${selectedOpdPass.id}`)}
                                        className="px-2 py-1 rounded-lg bg-blue-100 hover:bg-blue-200 text-blue-800 text-xs font-bold transition flex items-center gap-1 cursor-pointer"
                                        title="Copy token to clipboard"
                                    >
                                        {copiedToken ? <Check size={12} className="text-emerald-600" /> : <QrCode size={12} />}
                                        <span className="text-[10px]">{copiedToken ? "Copied!" : "Copy"}</span>
                                    </button>
                                </div>
                                <p className="text-xs font-bold text-slate-800">{selectedOpdPass.hospital_name}</p>
                            </div>

                            <div className="grid grid-cols-2 gap-3 text-xs p-3.5 bg-white rounded-xl border border-slate-200/80 shadow-2xs">
                                <div>
                                    <span className="text-[10px] text-slate-400 uppercase font-bold block">Patient Name</span>
                                    <span className="font-bold text-slate-900">{user?.full_name || user?.name || "Rahul Verma"}</span>
                                </div>
                                <div>
                                    <span className="text-[10px] text-slate-400 uppercase font-bold block">Patient ID</span>
                                    <span className="font-mono font-semibold text-slate-800">#MED-PT-0001</span>
                                </div>
                                <div>
                                    <span className="text-[10px] text-slate-400 uppercase font-bold block">Specialist Doctor</span>
                                    <span className="font-bold text-blue-900">{selectedOpdPass.doctor_name || "Attending Specialist"}</span>
                                </div>
                                <div>
                                    <span className="text-[10px] text-slate-400 uppercase font-bold block">Department</span>
                                    <span className="font-semibold text-slate-800">{selectedOpdPass.specialization || "Cardiology"}</span>
                                </div>
                                <div>
                                    <span className="text-[10px] text-slate-400 uppercase font-bold block">Reporting Date</span>
                                    <span className="font-bold text-slate-900">{selectedOpdPass.date}</span>
                                </div>
                                <div>
                                    <span className="text-[10px] text-slate-400 uppercase font-bold block">Window Slot</span>
                                    <span className="font-bold text-emerald-700">{selectedOpdPass.time}</span>
                                </div>
                            </div>

                            {/* OPD DESK REPORTING INSTRUCTIONS */}
                            <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl space-y-1 text-xs text-amber-900">
                                <p className="font-bold flex items-center gap-1.5 text-[11px]">
                                    <AlertCircle size={13} className="text-amber-600 shrink-0" />
                                    Reporting Desk: Room 204, OPD Block B
                                </p>
                                <p className="text-[10px] text-amber-800 leading-normal">
                                    Please arrive 15 minutes prior to your time slot ({selectedOpdPass.time}) with your government photo ID & previous diagnostic reports.
                                </p>
                            </div>

                            <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center justify-between text-xs">
                                <span className="font-semibold text-emerald-900">OPD Consultation Fee:</span>
                                <span className="font-extrabold text-emerald-700">₹{selectedOpdPass.consultation_fee || 900} (Paid)</span>
                            </div>

                            {/* BARCODE PLACEHOLDER */}
                            <div className="pt-2 text-center">
                                <div className="h-9 bg-slate-900 rounded-md flex items-center justify-around px-4 opacity-80">
                                    {[...Array(24)].map((_, i) => (
                                        <div key={i} className={`h-6 bg-white ${i % 3 === 0 ? 'w-1' : i % 2 === 0 ? 'w-0.5' : 'w-1.5'}`}></div>
                                    ))}
                                </div>
                                <span className="font-mono text-[10px] text-slate-400 mt-1 block">OPD-AUTH-SECURE-TOKEN-2026</span>
                            </div>
                        </div>

                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => window.print()}
                                className="flex-1 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-xs transition flex items-center justify-center gap-1.5 cursor-pointer"
                            >
                                <Printer size={14} /> Print / Save PDF
                            </button>
                            <button
                                onClick={() => setSelectedOpdPass(null)}
                                className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs rounded-xl transition cursor-pointer"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 10. DIGITAL BILL RECEIPT MODAL                                 */}
            {/* ============================================================== */}
            {selectedBillReceipt && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl space-y-4 border border-slate-200">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-8 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold">
                                    <Receipt size={18} />
                                </div>
                                <div>
                                    <h3 className="text-sm font-bold text-slate-900">Official Payment Invoice</h3>
                                    <p className="text-[11px] text-slate-500">{selectedBillReceipt.invoice_number}</p>
                                </div>
                            </div>
                            <button onClick={() => setSelectedBillReceipt(null)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-3 text-xs">
                            <div className="border-b border-slate-200 pb-2">
                                <h4 className="font-bold text-slate-900 text-sm">{selectedBillReceipt.hospital_name}</h4>
                                <p className="text-slate-500 text-[11px]">Billed To: {user?.full_name || "Rahul Verma"}</p>
                            </div>

                            <div className="space-y-1.5">
                                <div className="flex justify-between">
                                    <span>Specialist Consultation Fee:</span>
                                    <span className="font-semibold text-slate-800">₹{selectedBillReceipt.consultation_charge}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>ECG / Clinical Lab Fee:</span>
                                    <span className="font-semibold text-slate-800">₹{selectedBillReceipt.laboratory_charge}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span>Prescribed Pharmacy Items:</span>
                                    <span className="font-semibold text-slate-800">₹{selectedBillReceipt.medicine_charge}</span>
                                </div>
                                {selectedBillReceipt.discount > 0 && (
                                    <div className="flex justify-between text-emerald-700">
                                        <span>MediLink Discount:</span>
                                        <span>- ₹{selectedBillReceipt.discount}</span>
                                    </div>
                                )}
                                <div className="flex justify-between pt-2 border-t border-slate-200 font-extrabold text-sm text-slate-900">
                                    <span>Total Settled:</span>
                                    <span className="text-blue-600">₹{selectedBillReceipt.total_amount}</span>
                                </div>
                            </div>
                        </div>

                        <div className="flex items-center justify-between text-xs">
                            <span className="px-2.5 py-1 rounded-full font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                                Payment Status: {selectedBillReceipt.payment_status}
                            </span>
                            <button
                                onClick={() => window.print()}
                                className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition flex items-center gap-1 cursor-pointer"
                            >
                                <Printer size={13} /> Print
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 10B. DIGITAL PRESCRIPTION (e-Rx) MODAL                         */}
            {/* ============================================================== */}
            {selectedPrescription && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl space-y-4 border border-slate-200 max-h-[90vh] overflow-y-auto">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-8 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold">
                                    <Pill size={18} />
                                </div>
                                <div>
                                    <h3 className="text-sm font-bold text-slate-900">Official Electronic Prescription (e-Rx)</h3>
                                    <p className="text-[11px] text-slate-500">MediLink ABDM Integrated Clinical Document</p>
                                </div>
                            </div>
                            <button onClick={() => setSelectedPrescription(null)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        {/* PRESCRIPTION SHEET */}
                        <div className="p-5 rounded-2xl bg-white border-2 border-slate-200 space-y-4 text-xs shadow-xs">
                            {/* HOSPITAL & CLINIC HEADER */}
                            <div className="flex items-start justify-between border-b border-slate-200 pb-3">
                                <div>
                                    <h3 className="font-extrabold text-base text-slate-900">{selectedPrescription.hospital_name}</h3>
                                    <p className="text-slate-500 text-[11px]">Department of {selectedPrescription.specialization || "Clinical Medicine"}</p>
                                </div>
                                <div className="text-right">
                                    <p className="font-bold text-slate-900">{selectedPrescription.doctor_name}</p>
                                    <p className="text-[10px] text-slate-400 font-mono">REG #NMC-2018-WB</p>
                                </div>
                            </div>

                            {/* PATIENT INFO BANNER */}
                            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 p-3 bg-slate-50 rounded-xl border border-slate-200/70 text-[11px]">
                                <div>
                                    <span className="text-slate-400 block font-bold uppercase text-[9px]">Patient Name</span>
                                    <span className="font-bold text-slate-900">{user?.full_name || "Rahul Verma"}</span>
                                </div>
                                <div>
                                    <span className="text-slate-400 block font-bold uppercase text-[9px]">Patient ID</span>
                                    <span className="font-mono font-semibold text-slate-800">#MED-PT-0001</span>
                                </div>
                                <div>
                                    <span className="text-slate-400 block font-bold uppercase text-[9px]">Date</span>
                                    <span className="font-semibold text-slate-800">{selectedPrescription.created_at}</span>
                                </div>
                                <div>
                                    <span className="text-slate-400 block font-bold uppercase text-[9px]">Blood Group</span>
                                    <span className="font-bold text-rose-600">{myProfile?.blood_group || "B+"}</span>
                                </div>
                            </div>

                            {/* MEDICATIONS Rx */}
                            <div className="space-y-2 pt-1">
                                <span className="font-serif text-2xl font-extrabold text-blue-900 block">℞</span>
                                <div className="p-3.5 bg-emerald-50/50 rounded-xl border border-emerald-200 space-y-2">
                                    <div className="flex items-center justify-between">
                                        <h4 className="font-bold text-sm text-emerald-950">{selectedPrescription.medicines}</h4>
                                        <span className="px-2 py-0.5 rounded font-mono font-bold text-xs bg-emerald-100 text-emerald-800">
                                            {selectedPrescription.dosage}
                                        </span>
                                    </div>
                                    <div className="flex items-center gap-3 text-slate-600 text-xs">
                                        <span>Duration: <strong className="text-slate-900">{selectedPrescription.duration}</strong></span>
                                        <span>•</span>
                                        <span>Route: <strong>Oral Tablet</strong></span>
                                    </div>
                                    <p className="text-slate-600 bg-white p-2 rounded-lg border border-emerald-100 text-[11px]">
                                        <strong>Instructions:</strong> {selectedPrescription.instructions}
                                    </p>
                                </div>
                            </div>

                            {/* DOCTOR SIGNATURE & VERIFICATION */}
                            <div className="pt-3 border-t border-slate-200 flex items-center justify-between">
                                <div className="flex items-center gap-1.5 text-[11px] text-emerald-700 font-semibold">
                                    <ShieldCheck size={14} className="text-emerald-600" />
                                    <span>Digitally Signed & Validated</span>
                                </div>
                                <div className="text-right">
                                    <div className="font-serif italic text-sm text-slate-700">{selectedPrescription.doctor_name}</div>
                                    <span className="text-[10px] text-slate-400 block">Attending Consultant</span>
                                </div>
                            </div>
                        </div>

                        {/* ACTIONS */}
                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => window.print()}
                                className="flex-1 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-xs transition flex items-center justify-center gap-1.5 cursor-pointer"
                            >
                                <Printer size={14} /> Print / Save Prescription PDF
                            </button>
                            <button
                                onClick={() => setSelectedPrescription(null)}
                                className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs rounded-xl transition cursor-pointer"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 11. ENHANCED DOCTOR BOOKING MODAL                              */}
            {/* ============================================================== */}
            {bookingHospital && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div>
                                <h3 className="text-base font-bold text-slate-900">Book Doctor Consultation</h3>
                                <p className="text-xs text-slate-500">
                                    {bookingHospital.name} • {bookingHospital.city}
                                </p>
                            </div>
                            <button onClick={() => setBookingHospital(null)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        {bookingSuccess ? (
                            <div className="p-4 rounded-xl bg-emerald-50 text-emerald-800 text-xs font-semibold flex items-center gap-2 border border-emerald-200">
                                <CheckCircle2 size={18} className="text-emerald-600 shrink-0" />
                                {bookingSuccess}
                            </div>
                        ) : (
                            <form onSubmit={handleBookAppointment} className="space-y-4">
                                {hospitals.length > 0 && (
                                    <div>
                                        <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                                            Select Hospital / Healthcare Facility
                                        </label>
                                        <select
                                            value={bookingHospital.id}
                                            onChange={(e) => handleHospitalChangeInModal(Number(e.target.value))}
                                            className="w-full text-xs font-semibold p-2.5 border border-slate-200 rounded-xl bg-slate-50/70 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
                                        >
                                            {hospitals.map((hItem) => {
                                                const h = hItem.hospital || hItem;
                                                return (
                                                    <option key={h.id} value={h.id}>
                                                        {h.name} ({h.city}) — {hItem.distance_km || 3.5} km away
                                                    </option>
                                                );
                                            })}
                                        </select>
                                    </div>
                                )}
                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                                        Select Available Specialist Doctor
                                    </label>
                                    <select
                                        value={bookingDoctorId}
                                        onChange={(e) => setBookingDoctorId(Number(e.target.value))}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-slate-50/50 focus:bg-white focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
                                        required
                                    >
                                        {(bookingHospital.doctors || bookingHospital.matching_doctors || []).map((doc) => (
                                            <option key={doc.id} value={doc.id}>
                                                {doc.name} — {doc.specialization} (₹{doc.consultation_fee}) | {doc.schedule_display}
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                {/* DOCTOR PROFILE PREVIEW */}
                                {(() => {
                                    const allDocs = bookingHospital.doctors || bookingHospital.matching_doctors || [];
                                    const currentDoc = allDocs.find(d => d.id === Number(bookingDoctorId)) || allDocs[0];
                                    if (!currentDoc) return null;
                                    return (
                                        <div className="p-3.5 rounded-xl bg-blue-50/40 border border-blue-100 space-y-2">
                                            <div className="flex items-start justify-between">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-sm">
                                                        {currentDoc.name.split(" ").map(w => w[0]).join("").slice(0, 2)}
                                                    </div>
                                                    <div>
                                                        <h4 className="text-xs font-bold text-slate-900 flex items-center gap-2">
                                                            {currentDoc.name}
                                                            <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-100 text-blue-700">
                                                                {currentDoc.specialization}
                                                            </span>
                                                        </h4>
                                                        <p className="text-[11px] text-slate-500 mt-0.5">
                                                            {currentDoc.qualification} • {currentDoc.experience} Years Exp
                                                        </p>
                                                    </div>
                                                </div>
                                                <div className="text-right">
                                                    <span className="text-[10px] text-slate-400 block font-medium">Fee</span>
                                                    <span className="text-xs font-extrabold text-blue-600">
                                                        ₹{currentDoc.consultation_fee}
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-2 pt-1 border-t border-blue-100 text-[11px] text-slate-600">
                                                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                                <span className="font-semibold text-emerald-800">
                                                    Hours: {currentDoc.schedule_display}
                                                </span>
                                            </div>
                                        </div>
                                    );
                                })()}

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Appointment Date</label>
                                    <input
                                        type="date"
                                        required
                                        min={new Date().toISOString().split("T")[0]}
                                        value={bookingDate}
                                        onChange={(e) => setBookingDate(e.target.value)}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
                                    />
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                                        Select Preferred Time Slot ({bookingTime})
                                    </label>
                                    <div className="grid grid-cols-3 gap-1.5">
                                        {[
                                            "09:30 AM", "10:00 AM", "10:30 AM",
                                            "11:00 AM", "11:30 AM", "12:00 PM",
                                            "02:30 PM", "03:30 PM", "04:30 PM"
                                        ].map((slot) => (
                                            <button
                                                key={slot}
                                                type="button"
                                                onClick={() => setBookingTime(slot)}
                                                className={`py-1.5 px-2 rounded-lg text-xs font-bold transition border cursor-pointer ${
                                                    bookingTime === slot
                                                        ? "bg-blue-600 text-white border-blue-600 shadow-xs"
                                                        : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                                                }`}
                                            >
                                                {slot}
                                            </button>
                                        ))}
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">Reason / Symptoms for Visit</label>
                                    <input
                                        type="text"
                                        placeholder="e.g. Follow-up consultation, chest tightness, routine checkup"
                                        value={bookingReason}
                                        onChange={(e) => setBookingReason(e.target.value)}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
                                    />
                                </div>

                                <button
                                    type="submit"
                                    className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-xs transition cursor-pointer"
                                >
                                    Confirm & Generate OPD Pass
                                </button>
                            </form>
                        )}
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 12. AUTH REQUIRED POPUP                                        */}
            {/* ============================================================== */}
            {authRequiredHospital && (
                <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
                                    <Calendar size={18} />
                                </div>
                                <h3 className="text-base font-bold text-slate-900">Sign In to Book Doctor OPD</h3>
                            </div>
                            <button onClick={() => setAuthRequiredHospital(null)} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        <p className="text-xs text-slate-600 leading-relaxed">
                            You are scheduling an OPD visit at <strong>{authRequiredHospital.hospital.name}</strong> ({authRequiredHospital.hospital.city}).
                        </p>
                        <div className="p-3 bg-blue-50/70 rounded-xl border border-blue-100 text-xs text-blue-900 space-y-1">
                            <p className="font-bold flex items-center gap-1.5">
                                <ShieldCheck size={14} className="text-blue-600" />
                                Why is an account required for Doctor Booking?
                            </p>
                            <p className="text-[11px] text-blue-700 leading-normal">
                                An authenticated patient profile securely links your consultation slot, digital prescriptions, and doctor OPD token under your personal records.
                            </p>
                        </div>

                        <div className="space-y-2 pt-2">
                            <button
                                onClick={() => {
                                    sessionStorage.setItem("pending_booking", JSON.stringify({ hospital: authRequiredHospital }));
                                    navigate("/login");
                                }}
                                className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-xs transition flex items-center justify-center gap-2 cursor-pointer"
                            >
                                <LogIn size={14} />
                                Sign In to Existing Account
                            </button>
                            <button
                                onClick={() => {
                                    sessionStorage.setItem("pending_booking", JSON.stringify({ hospital: authRequiredHospital }));
                                    navigate("/register");
                                }}
                                className="w-full py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs rounded-xl transition flex items-center justify-center gap-2 cursor-pointer"
                            >
                                <UserPlus size={14} />
                                Create New Patient Account
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* ============================================================== */}
            {/* 13. EMERGENCY AMBULANCE DISPATCH POPUP (ZERO LOGIN REQUIRED)   */}
            {/* ============================================================== */}
            {emergencyModalHospital && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
                        <div className="flex items-center justify-between border-b border-rose-100 pb-3">
                            <div className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-rose-500 animate-ping"></span>
                                <h3 className="text-base font-bold text-rose-950">Immediate Ambulance Dispatch</h3>
                            </div>
                            <button onClick={() => { setEmergencyModalHospital(null); setDispatchedAlert(null); }} className="p-1 text-slate-400 hover:text-slate-600 cursor-pointer">
                                <X size={18} />
                            </button>
                        </div>

                        {dispatchedAlert ? (
                            <div className="space-y-4 py-2">
                                <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 space-y-1.5">
                                    <div className="flex items-center gap-2">
                                        <CheckCircle2 size={22} className="text-emerald-600 shrink-0" />
                                        <h4 className="text-sm font-bold">Ambulance Dispatched & En Route!</h4>
                                    </div>
                                    <p className="text-xs text-emerald-800">
                                        Emergency response unit has been mobilized from <strong>{dispatchedAlert.hospital}</strong>.
                                    </p>
                                </div>

                                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 space-y-2">
                                    <p className="text-[10px] text-slate-400 font-bold uppercase">Live Response Milestones</p>
                                    <div className="space-y-1.5 text-xs">
                                        <div className="flex items-center gap-2 text-emerald-700 font-semibold">
                                            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                                            <span>Triage Alert Acknowledged by Hospital</span>
                                        </div>
                                        <div className="flex items-center gap-2 text-emerald-700 font-semibold">
                                            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                                            <span>Ambulance Unit Mobilized with Oxygen & Defibrillator</span>
                                        </div>
                                        <div className="flex items-center gap-2 text-rose-700 font-bold">
                                            <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                                            <span>En Route to Caller Landmark (ETA ~8-12m)</span>
                                        </div>
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-3 text-xs">
                                    <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/80">
                                        <span className="text-[10px] text-slate-400 font-bold block uppercase">Assigned Unit</span>
                                        <p className="font-extrabold text-slate-900 text-sm mt-0.5">{dispatchedAlert.ambulance}</p>
                                        <p className="text-[11px] text-slate-500">{dispatchedAlert.driver_name}</p>
                                    </div>
                                    <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/80">
                                        <span className="text-[10px] text-slate-400 font-bold block uppercase">Estimated Arrival</span>
                                        <p className="font-extrabold text-rose-600 text-sm mt-0.5">{dispatchedAlert.eta_minutes}</p>
                                        <p className="text-[11px] text-slate-500">Live GPS tracking active</p>
                                    </div>
                                </div>

                                <div className="p-3 bg-rose-50 rounded-xl border border-rose-200 flex items-center justify-between">
                                    <div>
                                        <span className="text-[10px] font-bold text-rose-700 uppercase">Paramedic Helpline</span>
                                        <p className="text-xs font-bold text-rose-900">{dispatchedAlert.driver_phone || dispatchedAlert.hospital_phone}</p>
                                    </div>
                                    <a
                                        href={`tel:${dispatchedAlert.driver_phone || dispatchedAlert.hospital_phone}`}
                                        className="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold rounded-lg shadow-xs transition"
                                    >
                                        Call Emergency
                                    </a>
                                </div>

                                <button
                                    onClick={() => { setEmergencyModalHospital(null); setDispatchedAlert(null); }}
                                    className="w-full py-2.5 bg-slate-800 hover:bg-slate-900 text-white font-bold text-xs rounded-xl transition cursor-pointer"
                                >
                                    Close Window
                                </button>
                            </div>
                        ) : (
                            <form onSubmit={handleConfirmEmergencyDispatch} className="space-y-3.5">
                                <div className="p-3 bg-rose-50/80 border border-rose-200 rounded-xl text-xs text-rose-900">
                                    <p className="font-bold">Requesting Unit from: {emergencyModalHospital.name}</p>
                                    <p className="text-[11px] text-rose-700 mt-0.5">
                                        Facility Emergency Helpline: <strong>{emergencyModalHospital.emergency_contact || emergencyModalHospital.phone}</strong>
                                    </p>
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Patient / Caller Name <span className="text-rose-500">*</span>
                                    </label>
                                    <input
                                        type="text"
                                        required
                                        placeholder="e.g. Rahul Sen"
                                        value={emergencyCallerName}
                                        onChange={(e) => setEmergencyCallerName(e.target.value)}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-rose-500 focus:outline-hidden"
                                    />
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Emergency Contact Phone <span className="text-rose-500">*</span>
                                    </label>
                                    <input
                                        type="tel"
                                        required
                                        placeholder="e.g. +91 9876543210"
                                        value={emergencyPhone}
                                        onChange={(e) => setEmergencyPhone(e.target.value)}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-rose-500 focus:outline-hidden"
                                    />
                                </div>

                                <div>
                                    <div className="flex items-center justify-between mb-1">
                                        <label className="text-xs font-semibold text-slate-700">
                                            Current Pickup Address / Landmark <span className="text-rose-500">*</span>
                                        </label>
                                        <button
                                            type="button"
                                            onClick={handleAutoFillEmergencyGps}
                                            className="text-[10px] text-blue-600 font-bold hover:underline flex items-center gap-1 cursor-pointer"
                                        >
                                            <Navigation size={10} /> Auto-Detect GPS
                                        </button>
                                    </div>
                                    <input
                                        type="text"
                                        required
                                        placeholder="e.g. Near Park Circus 7-point crossing, Kolkata"
                                        value={emergencyPickupLocation}
                                        onChange={(e) => setEmergencyPickupLocation(e.target.value)}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl focus:ring-2 focus:ring-rose-500 focus:outline-hidden"
                                    />
                                </div>

                                <div>
                                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                                        Emergency Condition / Severity
                                    </label>
                                    <select
                                        value={emergencyCondition}
                                        onChange={(e) => setEmergencyCondition(e.target.value)}
                                        className="w-full text-xs p-2.5 border border-slate-200 rounded-xl bg-white focus:ring-2 focus:ring-rose-500 focus:outline-hidden font-semibold"
                                    >
                                        <option value="Cardiac Arrest / Severe Chest Pain (Critical)">Cardiac Arrest / Severe Chest Pain (Critical)</option>
                                        <option value="Severe Trauma / Road Accident (Critical)">Severe Trauma / Road Accident (Critical)</option>
                                        <option value="Acute Respiratory Distress / Asthma (High)">Acute Respiratory Distress / Asthma (High)</option>
                                        <option value="Neurological Emergency / Stroke Symptoms (Critical)">Neurological Emergency / Stroke Symptoms (Critical)</option>
                                        <option value="Maternity / Labor Urgency (High)">Maternity / Labor Urgency (High)</option>
                                        <option value="Acute Unconscious / Collapse (Critical)">Acute Unconscious / Collapse (Critical)</option>
                                        <option value="General Acute Medical Emergency (High)">General Acute Medical Emergency (High)</option>
                                    </select>
                                </div>

                                <div className="pt-2">
                                    <button
                                        type="submit"
                                        disabled={emergencySending}
                                        className="w-full py-3 bg-rose-600 hover:bg-rose-700 text-white font-extrabold text-xs rounded-xl shadow-sm shadow-rose-500/30 transition flex items-center justify-center gap-2 cursor-pointer"
                                    >
                                        <HeartPulse size={16} />
                                        {emergencySending ? "Dispatching Response Unit..." : "🚨 Confirm Immediate Ambulance Dispatch"}
                                    </button>
                                </div>
                            </form>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
