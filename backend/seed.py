"""
MediLink Pan-India Database Seeder
Idempotent seeding script for hospitals, beds, ambulances, doctors,
specializations, demo users (Admin, Hospital, Patient), and simulated emergency/appointment activity.

Supports:
    python seed.py          # Idempotent incremental seeding (skips existing records)
    python seed.py --reset  # Full reset and clean re-seeding
"""

import sys
import random
from datetime import datetime, timedelta, time
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models.role import Role
from app.models.user import User
from app.models.hospital import Hospital
from app.models.specialization import Specialization
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.models.bed import Bed
from app.models.ambulance import Ambulance
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.emergency import Emergency

app = create_app()

PAN_INDIA_HOSPITALS = [
    # Kolkata (Eastern Hub)
    {
        "name": "Apollo Gleneagles Hospital",
        "registration_number": "WB-KOL-APO-001",
        "hospital_type": "Multi-Specialty",
        "description": "Premier multi-specialty tertiary care hospital with world-class cardiac and emergency trauma centers.",
        "email": "apollo.kolkata@medilink.com",
        "phone": "+91 33 2320 3040",
        "emergency_contact": "1066",
        "website": "https://kolkata.apollohospitals.com",
        "address": "58 Canal Circular Road, Kadapara, Phool Bagan",
        "city": "Kolkata",
        "state": "West Bengal",
        "pincode": "700054",
        "latitude": 22.5684,
        "longitude": 88.3982,
        "is_24x7": True,
        "total_beds": 510,
        "icu_beds": 65,
        "emergency_beds": 35
    },
    {
        "name": "City Care Hospital",
        "registration_number": "WB-KOL-CCH-002",
        "hospital_type": "Super Specialty",
        "description": "Comprehensive healthcare center known for orthopedics, cardiology, and 24x7 trauma care.",
        "email": "citycare@medilink.com",
        "phone": "+91 33 2289 4000",
        "emergency_contact": "+91 33 2289 9999",
        "website": "https://citycarehospital.com",
        "address": "123 Main Road, Park Circus",
        "city": "Kolkata",
        "state": "West Bengal",
        "pincode": "700017",
        "latitude": 22.5411,
        "longitude": 88.3653,
        "is_24x7": True,
        "total_beds": 350,
        "icu_beds": 45,
        "emergency_beds": 25
    },
    {
        "name": "Fortis Hospital Anandapur",
        "registration_number": "WB-KOL-FOR-003",
        "hospital_type": "Multi-Specialty",
        "description": "State-of-the-art super-specialty hospital specializing in cardiology, neurosurgery, and nephrology.",
        "email": "fortis.kolkata@medilink.com",
        "phone": "+91 33 6628 4444",
        "emergency_contact": "105010",
        "website": "https://www.fortishealthcare.com",
        "address": "730 Anandapur, E.M. Bypass Road",
        "city": "Kolkata",
        "state": "West Bengal",
        "pincode": "700107",
        "latitude": 22.5165,
        "longitude": 88.4042,
        "is_24x7": True,
        "total_beds": 400,
        "icu_beds": 55,
        "emergency_beds": 30
    },

    # New Delhi (Northern Hub)
    {
        "name": "All India Institute of Medical Sciences (AIIMS)",
        "registration_number": "DL-ND-AIIMS-001",
        "hospital_type": "Government Apex",
        "description": "India's premier public medical research institute and apex tertiary healthcare facility.",
        "email": "aiims.delhi@medilink.com",
        "phone": "+91 11 2658 8500",
        "emergency_contact": "+91 11 2659 4405",
        "website": "https://www.aiims.edu",
        "address": "Sri Aurobindo Marg, Ansari Nagar",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110029",
        "latitude": 28.5672,
        "longitude": 77.2100,
        "is_24x7": True,
        "total_beds": 2400,
        "icu_beds": 250,
        "emergency_beds": 120
    },
    {
        "name": "Max Super Speciality Hospital Saket",
        "registration_number": "DL-ND-MAX-002",
        "hospital_type": "Multi-Specialty",
        "description": "Accredited super-specialty medical center offering leading-edge robotic surgery, oncology, and cardiology.",
        "email": "max.saket@medilink.com",
        "phone": "+91 11 2651 5050",
        "emergency_contact": "011 4055 4055",
        "website": "https://www.maxhealthcare.in",
        "address": "1, 2 Press Enclave Road, Saket",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110017",
        "latitude": 28.5283,
        "longitude": 77.2114,
        "is_24x7": True,
        "total_beds": 530,
        "icu_beds": 70,
        "emergency_beds": 40
    },
    {
        "name": "Fortis Escorts Heart Institute",
        "registration_number": "DL-ND-ESC-003",
        "hospital_type": "Super Specialty",
        "description": "Internationally renowned cardiac care center pioneer in pediatric and adult cardiovascular surgery.",
        "email": "escorts.delhi@medilink.com",
        "phone": "+91 11 4713 5000",
        "emergency_contact": "105010",
        "website": "https://www.fortishealthcare.com",
        "address": "Okhla Road, Sukhdev Vihar Metro Station",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110025",
        "latitude": 28.5606,
        "longitude": 77.2774,
        "is_24x7": True,
        "total_beds": 310,
        "icu_beds": 60,
        "emergency_beds": 25
    },

    # Mumbai (Western Hub)
    {
        "name": "Lilavati Hospital & Research Centre",
        "registration_number": "MH-MUM-LIL-001",
        "hospital_type": "Multi-Specialty",
        "description": "Premier multi-specialty healthcare institution in Bandra with comprehensive emergency response.",
        "email": "lilavati.mumbai@medilink.com",
        "phone": "+91 22 2675 1000",
        "emergency_contact": "+91 22 2656 8064",
        "website": "https://www.lilavatihospital.com",
        "address": "A-791 Bandra Reclamation, Bandra West",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400050",
        "latitude": 19.0519,
        "longitude": 72.8291,
        "is_24x7": True,
        "total_beds": 320,
        "icu_beds": 50,
        "emergency_beds": 30
    },
    {
        "name": "Kokilaben Dhirubhai Ambani Hospital",
        "registration_number": "MH-MUM-KDA-002",
        "hospital_type": "Multi-Specialty",
        "description": "Full-time specialist system hospital with cutting-edge robotic technology and comprehensive trauma units.",
        "email": "kokilaben.mumbai@medilink.com",
        "phone": "+91 22 4269 6969",
        "emergency_contact": "+91 22 4269 9999",
        "website": "https://www.kokilabenhospital.com",
        "address": "Rao Saheb Achutrao Patwardhan Marg, Four Bungalows, Andheri West",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400053",
        "latitude": 19.1311,
        "longitude": 72.8252,
        "is_24x7": True,
        "total_beds": 750,
        "icu_beds": 100,
        "emergency_beds": 50
    },

    # Bengaluru (Southern Tech & Health Hub)
    {
        "name": "Manipal Hospital Old Airport Road",
        "registration_number": "KA-BLR-MAN-001",
        "hospital_type": "Multi-Specialty",
        "description": "Flagship hospital of Manipal Group renowned for cardiology, oncology, and organ transplants.",
        "email": "manipal.blr@medilink.com",
        "phone": "+91 80 2502 4444",
        "emergency_contact": "080 2502 3333",
        "website": "https://www.manipalhospitals.com",
        "address": "98 HAL Old Airport Road, Kodihalli",
        "city": "Bengaluru",
        "state": "Karnataka",
        "pincode": "560017",
        "latitude": 12.9592,
        "longitude": 77.6476,
        "is_24x7": True,
        "total_beds": 600,
        "icu_beds": 80,
        "emergency_beds": 45
    },
    {
        "name": "Narayana Health City",
        "registration_number": "KA-BLR-NH-002",
        "hospital_type": "Super Specialty",
        "description": "World-renowned cardiac, cancer, and pediatric healthcare city founded by Dr. Devi Shetty.",
        "email": "narayana.blr@medilink.com",
        "phone": "+91 80 7122 2222",
        "emergency_contact": "+91 80 7122 2200",
        "website": "https://www.narayanahealth.org",
        "address": "258/A Bommasandra Industrial Area, Anekal Taluk",
        "city": "Bengaluru",
        "state": "Karnataka",
        "pincode": "560099",
        "latitude": 12.8173,
        "longitude": 77.6908,
        "is_24x7": True,
        "total_beds": 1400,
        "icu_beds": 180,
        "emergency_beds": 70
    },

    # Chennai
    {
        "name": "Apollo Hospitals Greams Road",
        "registration_number": "TN-CHE-APO-001",
        "hospital_type": "Multi-Specialty",
        "description": "The flagship Apollo Hospital known worldwide for clinical excellence, cardiac care, and neurosciences.",
        "email": "apollo.chennai@medilink.com",
        "phone": "+91 44 2829 0200",
        "emergency_contact": "1066",
        "website": "https://chennai.apollohospitals.com",
        "address": "21 Greams Lane, Off Greams Road, Thousand Lights",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600006",
        "latitude": 13.0569,
        "longitude": 80.2514,
        "is_24x7": True,
        "total_beds": 560,
        "icu_beds": 75,
        "emergency_beds": 40
    },

    # Hyderabad
    {
        "name": "Apollo Hospitals Jubilee Hills",
        "registration_number": "TS-HYD-APO-001",
        "hospital_type": "Multi-Specialty",
        "description": "Comprehensive healthcare campus with high-end institutes of cardiology, oncology, and neurosurgery.",
        "email": "apollo.hyd@medilink.com",
        "phone": "+91 40 2360 7777",
        "emergency_contact": "1066",
        "website": "https://hyderabad.apollohospitals.com",
        "address": "Road No 72, Opposite Bharatiya Vidya Bhavan, Film Nagar, Jubilee Hills",
        "city": "Hyderabad",
        "state": "Telangana",
        "pincode": "500033",
        "latitude": 17.4162,
        "longitude": 78.4116,
        "is_24x7": True,
        "total_beds": 550,
        "icu_beds": 70,
        "emergency_beds": 35
    },

    # Pune
    {
        "name": "Ruby Hall Clinic Pune",
        "registration_number": "MH-PUN-RUB-001",
        "hospital_type": "Multi-Specialty",
        "description": "NABH and NABL accredited hospital offering leading emergency response and trauma management in Western India.",
        "email": "rubyhall.pune@medilink.com",
        "phone": "+91 20 6645 5100",
        "emergency_contact": "020 2616 3391",
        "website": "https://rubyhall.com",
        "address": "40 Sassoon Road, Near Pune Railway Station",
        "city": "Pune",
        "state": "Maharashtra",
        "pincode": "411001",
        "latitude": 18.5308,
        "longitude": 73.8743,
        "is_24x7": True,
        "total_beds": 600,
        "icu_beds": 80,
        "emergency_beds": 40
    },

    # Jaipur
    {
        "name": "Sawai Man Singh (SMS) Hospital",
        "registration_number": "RJ-JAI-SMS-001",
        "hospital_type": "Government Apex",
        "description": "Major public medical center in Rajasthan providing advanced trauma, surgical, and inpatient care.",
        "email": "sms.jaipur@medilink.com",
        "phone": "+91 141 251 8224",
        "emergency_contact": "+91 141 251 8380",
        "website": "https://education.rajasthan.gov.in/smsmcjaipur",
        "address": "Jawahar Lal Nehru Marg, Ashok Nagar",
        "city": "Jaipur",
        "state": "Rajasthan",
        "pincode": "302004",
        "latitude": 26.8928,
        "longitude": 75.8157,
        "is_24x7": True,
        "total_beds": 1800,
        "icu_beds": 140,
        "emergency_beds": 80
    },

    # Lucknow
    {
        "name": "Sanjay Gandhi Postgraduate Institute (SGPGI)",
        "registration_number": "UP-LKO-SGPGI-001",
        "hospital_type": "Government Apex",
        "description": "Autonomous tertiary care super-specialty teaching hospital serving Northern and Central India.",
        "email": "sgpgi.lucknow@medilink.com",
        "phone": "+91 522 266 8004",
        "emergency_contact": "+91 522 249 4000",
        "website": "https://www.sgpgi.ac.in",
        "address": "Raebareli Road",
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "pincode": "226014",
        "latitude": 26.7460,
        "longitude": 80.9388,
        "is_24x7": True,
        "total_beds": 1200,
        "icu_beds": 110,
        "emergency_beds": 50
    },

    # Chandigarh
    {
        "name": "Post Graduate Institute of Medical Education and Research (PGIMER)",
        "registration_number": "CH-CHD-PGI-001",
        "hospital_type": "Government Apex",
        "description": "Premier medical and research institute providing super-specialty tertiary care for the northern states.",
        "email": "pgimer.chd@medilink.com",
        "phone": "+91 172 274 7585",
        "emergency_contact": "0172 275 6565",
        "website": "https://pgimer.edu.in",
        "address": "Sector 12",
        "city": "Chandigarh",
        "state": "Chandigarh",
        "pincode": "160012",
        "latitude": 30.7634,
        "longitude": 76.7844,
        "is_24x7": True,
        "total_beds": 1900,
        "icu_beds": 160,
        "emergency_beds": 90
    }
]

SPECIALIZATIONS_DATA = [
    {"name": "Cardiology", "code": "CARDIO", "icon": "HeartPulse", "is_emergency": True, "description": "Heart disease, chest pain, arrhythmias, hypertension, and cardiovascular interventions."},
    {"name": "Orthopedics", "code": "ORTHO", "icon": "Bone", "is_emergency": False, "description": "Joint replacement, fracture care, spine treatment, and musculoskeletal injuries."},
    {"name": "General Medicine", "code": "GENMED", "icon": "Stethoscope", "is_emergency": False, "description": "Adult primary care, fever, diabetes, infections, and preventative health."},
    {"name": "Gastroenterology", "code": "GASTRO", "icon": "Activity", "is_emergency": False, "description": "Stomach, liver, digestive disorders, endoscopy, and inflammatory bowel diseases."},
    {"name": "Neurology", "code": "NEURO", "icon": "Brain", "is_emergency": True, "description": "Brain disorders, stroke intervention, seizures, migraines, and nerve care."},
    {"name": "Dermatology", "code": "DERMA", "icon": "Sparkles", "is_emergency": False, "description": "Skin conditions, eczema, psoriasis, acne, allergy tests, and hair disorders."},
    {"name": "Pediatrics", "code": "PEDIAT", "icon": "Baby", "is_emergency": False, "description": "Child health, infant care, pediatric immunization, and developmental disorders."},
    {"name": "Emergency Medicine", "code": "EMERMED", "icon": "AlertTriangle", "is_emergency": True, "description": "Acute trauma, resuscitations, immediate triage, cardiac arrests, and critical injuries."},
    {"name": "Pulmonology", "code": "PULMO", "icon": "Wind", "is_emergency": False, "description": "Respiratory illnesses, asthma attacks, pneumonia, COPD, and lung diagnostics."},
    {"name": "Oncology", "code": "ONCO", "icon": "ShieldCheck", "is_emergency": False, "description": "Comprehensive cancer diagnostics, chemotherapy, and surgical oncology."}
]

DOCTOR_NAMES = [
    ("Dr. Rajesh Sharma", "Cardiology", "MD, DM (Cardiology), FACC", 16, 1200.0),
    ("Dr. Ananya Sengupta", "Cardiology", "MD, DNB (Cardiology)", 11, 900.0),
    ("Dr. Vikram Rathore", "Orthopedics", "MS (Ortho), MCh (Joint Replacement)", 18, 1000.0),
    ("Dr. Sunita Deshmukh", "Neurology", "MD, DM (Neurology)", 14, 1100.0),
    ("Dr. Amit Banerjee", "General Medicine", "MBBS, MD (Internal Medicine)", 12, 600.0),
    ("Dr. Preeti Nair", "Pediatrics", "MBBS, MD (Pediatrics), DCH", 9, 700.0),
    ("Dr. Rohan Mehta", "Gastroenterology", "MD, DM (Gastroenterology)", 13, 950.0),
    ("Dr. Kavita Verma", "Dermatology", "MD (Dermatology, Venereology)", 8, 800.0),
    ("Dr. Arvind Swaminathan", "Emergency Medicine", "MBBS, MEM (Emergency Medicine)", 10, 850.0)
]


def seed_database(reset=False):
    print("=" * 65)
    print("🏥 MediLink Pan-India Database Seeding Engine")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    with app.app_context():
        if reset:
            print("⚠️ RESET FLAG ACTIVE: Dropping and re-creating all database tables...")
            db.drop_all()
            db.create_all()
            print("✅ All tables cleanly recreated.")
        else:
            db.create_all()

        # ---------------------------------------------------------
        # 1. SEED ROLES
        # ---------------------------------------------------------
        print("\n[1/7] Seeding User Roles...")
        roles_data = [
            {"name": "Admin", "description": "System Administrator"},
            {"name": "Doctor", "description": "Medical Practitioner"},
            {"name": "Patient", "description": "Patient / Normal User"},
            {"name": "Hospital", "description": "Hospital / Clinic Administrator"},
            {"name": "Laboratory", "description": "Diagnostic Laboratory"},
            {"name": "Ambulance Owner", "description": "Ambulance Service Provider"}
        ]
        roles_dict = {}
        for r_item in roles_data:
            role = Role.query.filter_by(name=r_item["name"]).first()
            if not role:
                role = Role(name=r_item["name"], description=r_item["description"])
                db.session.add(role)
                db.session.flush()
                print(f"  + Role created: {r_item['name']}")
            roles_dict[r_item["name"]] = role
        db.session.commit()

        # ---------------------------------------------------------
        # 2. SEED SPECIALIZATIONS
        # ---------------------------------------------------------
        print("\n[2/7] Seeding Medical Specializations...")
        for s_item in SPECIALIZATIONS_DATA:
            spec = Specialization.query.filter_by(code=s_item["code"]).first()
            if not spec:
                spec = Specialization(**s_item)
                db.session.add(spec)
                print(f"  + Specialization added: {s_item['name']} ({s_item['code']})")
        db.session.commit()

        # ---------------------------------------------------------
        # 3. SEED PAN-INDIA HOSPITALS
        # ---------------------------------------------------------
        print(f"\n[3/7] Seeding Pan-India Hospitals ({len(PAN_INDIA_HOSPITALS)} facilities)...")
        hospitals_map = {}
        for h_data in PAN_INDIA_HOSPITALS:
            existing_h = Hospital.query.filter(
                (Hospital.registration_number == h_data["registration_number"]) |
                (Hospital.name == h_data["name"]) |
                (Hospital.email == h_data["email"])
            ).first()
            if not existing_h:
                hosp = Hospital(**h_data)
                db.session.add(hosp)
                db.session.flush()
                hospitals_map[hosp.id] = hosp
                print(f"  + Added: {hosp.name} in {hosp.city}, {hosp.state}")
            else:
                hospitals_map[existing_h.id] = existing_h

        db.session.commit()

        # ---------------------------------------------------------
        # 4. SEED SIMULATED BEDS & AMBULANCES FOR EACH HOSPITAL
        # ---------------------------------------------------------
        print("\n[4/7] Generating Simulated Beds (ICU, Emergency, General) & Ambulances...")
        for hosp_id, hosp in hospitals_map.items():
            existing_beds = Bed.query.filter_by(hospital_id=hosp_id).count()
            if existing_beds == 0:
                # Seed ICU Beds
                icu_count = min(35, max(15, int(hosp.icu_beds * 0.4)))
                for b in range(1, icu_count + 1):
                    status = "Available" if (b % 3 != 0) else "Occupied"
                    db.session.add(Bed(
                        hospital_id=hosp_id,
                        bed_number=f"ICU-{b:02d}",
                        ward="Intensive Care Unit (Critical Care)",
                        bed_type="ICU",
                        floor="Level 2",
                        room_number=f"ICU-{200+b}",
                        status=status,
                        notes="Simulated bed status with ventilator support"
                    ))

                # Seed Emergency Trauma Beds
                emg_count = min(25, max(10, int(hosp.emergency_beds * 0.45)))
                for b in range(1, emg_count + 1):
                    status = "Available" if (b % 4 != 0) else "Occupied"
                    db.session.add(Bed(
                        hospital_id=hosp_id,
                        bed_number=f"ER-{b:02d}",
                        ward="Emergency & Trauma Unit",
                        bed_type="Emergency",
                        floor="Ground Floor",
                        room_number=f"ER-{100+b}",
                        status=status,
                        notes="Emergency triage priority bed"
                    ))

                # Seed General Inpatient Beds
                gen_count = min(60, max(25, int(hosp.total_beds * 0.15)))
                for b in range(1, gen_count + 1):
                    status = "Available" if (b % 2 == 0) else "Occupied"
                    db.session.add(Bed(
                        hospital_id=hosp_id,
                        bed_number=f"GEN-{b:03d}",
                        ward="General Medical Ward",
                        bed_type="General",
                        floor=f"Level {(b % 4) + 3}",
                        room_number=f"GEN-{300+b}",
                        status=status,
                        notes="Standard inpatient monitored bed"
                    ))

            # Seed Ambulances
            existing_amb = Ambulance.query.filter_by(hospital_id=hosp_id).count()
            if existing_amb == 0:
                city_code = hosp.city[:3].upper()
                # 1 ALS Ambulance
                db.session.add(Ambulance(
                    hospital_id=hosp_id,
                    registration_number=f"{hosp.state[:2].upper()}-{city_code}-AMB-{random.randint(100, 999)}",
                    ambulance_type="Advanced Life Support (ALS)",
                    driver_name=f"Driver {hosp.city} ALS",
                    driver_phone=f"+91 98300 {random.randint(10000, 99999)}",
                    current_location=f"{hosp.address}, {hosp.city}",
                    availability_status="Available",
                    emergency_status="Normal"
                ))
                # 1 BLS Ambulance
                db.session.add(Ambulance(
                    hospital_id=hosp_id,
                    registration_number=f"{hosp.state[:2].upper()}-{city_code}-AMB-{random.randint(100, 999)}",
                    ambulance_type="Basic Life Support (BLS)",
                    driver_name=f"Driver {hosp.city} BLS",
                    driver_phone=f"+91 98311 {random.randint(10000, 99999)}",
                    current_location=f"{hosp.city} Sector Rapid Response",
                    availability_status="Available" if (hosp_id % 2 == 0) else "On Duty",
                    emergency_status="Normal"
                ))

        db.session.commit()
        print(f"  + Beds and ambulances verified across {len(hospitals_map)} hospitals.")

        # ---------------------------------------------------------
        # 5. SEED DOCTORS
        # ---------------------------------------------------------
        print("\n[5/7] Seeding Specialist Doctors across Facilities...")
        doc_count = 0
        for hosp_id, hosp in hospitals_map.items():
            existing_docs = Doctor.query.filter_by(hospital_id=hosp_id).count()
            if existing_docs == 0:
                # Assign 3-4 doctors to each facility
                assigned_sample = random.sample(DOCTOR_NAMES, k=min(4, len(DOCTOR_NAMES)))
                for doc_tpl in assigned_sample:
                    clean_name = doc_tpl[0]
                    spec = doc_tpl[1]
                    qual = doc_tpl[2]
                    exp = doc_tpl[3]
                    fee = doc_tpl[4]
                    unique_email = f"{clean_name.lower().replace(' ', '.').replace('dr.', '')}.h{hosp_id}@medilink.com"

                    doctor = Doctor(
                        full_name=clean_name,
                        email=unique_email,
                        phone=f"+91 98{random.randint(10000000, 99999999)}",
                        specialization=spec,
                        qualification=qual,
                        experience=exp,
                        consultation_fee=fee,
                        is_active=True,
                        hospital_id=hosp_id
                    )
                    db.session.add(doctor)
                    db.session.flush()

                    # Seed consultation schedule for doctor
                    sched_patterns = [
                        ("Mon - Sat", time(9, 0), time(13, 0)),
                        ("Mon - Fri", time(14, 0), time(18, 0)),
                        ("Mon - Sat", time(10, 0), time(14, 0)),
                        ("Tue - Sun", time(11, 0), time(16, 0))
                    ]
                    sp = sched_patterns[doc_count % len(sched_patterns)]
                    schedule = DoctorSchedule(
                        doctor_id=doctor.id,
                        day_of_week=sp[0],
                        start_time=sp[1],
                        end_time=sp[2],
                        slot_duration=30,
                        is_available=True
                    )
                    db.session.add(schedule)
                    doc_count += 1
        db.session.commit()
        print(f"  + Seeded {doc_count} specialist doctors & schedules across hospital departments.")

        # ---------------------------------------------------------
        # 6. SEED DEMO USERS (SUPER ADMIN, HOSPITAL ADMIN, PATIENT)
        # ---------------------------------------------------------
        print("\n[6/7] Seeding Standard Demo Accounts...")

        first_hosp = Hospital.query.first()
        hosp_id_ref = first_hosp.id if first_hosp else 1

        demo_users = [
            # Super Admin
            {
                "full_name": "MediLink Super Administrator",
                "email": "admin@medilink.com",
                "password": "Admin@123",
                "role": "Admin",
                "is_active": True,
                "is_email_verified": True
            },
            # Hospital Admin
            {
                "full_name": f"Hospital Administrator ({first_hosp.name if first_hosp else 'Central'})",
                "email": "hospital@medilink.com",
                "password": "Hospital@123",
                "role": "Hospital",
                "is_active": True,
                "is_email_verified": True
            },
            # Patient User
            {
                "full_name": "Rahul Verma",
                "email": "patient@medilink.com",
                "password": "Patient@123",
                "role": "Patient",
                "is_active": True,
                "is_email_verified": True
            },
            # Legacy Accounts for Seamless Backward Compatibility
            {
                "full_name": "MediLink Official Admin",
                "email": "medilink.officialadmin.ap@gmail.com",
                "password": "Admin@123",
                "role": "Admin",
                "is_active": True,
                "is_email_verified": True
            },
            {
                "full_name": "Debu Roy",
                "email": "gourhari755@gmail.com",
                "password": "Patient@123",
                "role": "Patient",
                "is_active": True,
                "is_email_verified": True
            }
        ]

        created_patients = []
        for u_data in demo_users:
            user = User.query.filter_by(email=u_data["email"]).first()
            if not user:
                user = User(
                    full_name=u_data["full_name"],
                    email=u_data["email"],
                    password_hash=generate_password_hash(u_data["password"]),
                    is_active=u_data["is_active"],
                    is_email_verified=u_data["is_email_verified"]
                )
                db.session.add(user)
                db.session.flush()
                print(f"  + Demo Account created: {u_data['email']} ({u_data['role']})")
            else:
                user.password_hash = generate_password_hash(u_data["password"])
                user.is_email_verified = True
                user.is_active = True

            # Assign Role
            role_obj = roles_dict.get(u_data["role"])
            if role_obj and role_obj not in user.roles:
                user.roles.append(role_obj)

            # If Patient, ensure patient profile exists
            if u_data["role"] == "Patient":
                pat = Patient.query.filter_by(email=u_data["email"]).first()
                if not pat:
                    pat = Patient(
                        full_name=u_data["full_name"],
                        email=u_data["email"],
                        phone=f"+91 97{random.randint(10000000, 99999999)}",
                        gender="Male",
                        date_of_birth=datetime(1996, 5, 14).date(),
                        age=29
                    )
                    db.session.add(pat)
                    db.session.flush()
                created_patients.append(pat)

        db.session.commit()

        # Link hospital admin user to the first hospital
        hosp_admin_user = User.query.filter_by(email="hospital@medilink.com").first()
        if hosp_admin_user and first_hosp:
            first_hosp.user_id = hosp_admin_user.id
            db.session.commit()

        # ---------------------------------------------------------
        # 7. SEED SIMULATED ACTIVITY (Appointments & Emergency Alerts)
        # ---------------------------------------------------------
        print("\n[7/7] Seeding Live Simulated Activity for Dashboards...")
        if created_patients and first_hosp:
            sample_patient = created_patients[0]
            first_doc = Doctor.query.filter_by(hospital_id=first_hosp.id).first()

            # Seed Simulated Appointment if none
            if Appointment.query.filter_by(patient_id=sample_patient.id).count() == 0 and first_doc:
                db.session.add(Appointment(
                    patient_id=sample_patient.id,
                    doctor_id=first_doc.id,
                    hospital_id=first_hosp.id,
                    appointment_date=datetime.now().date() + timedelta(days=1),
                    appointment_time=datetime.strptime("10:30", "%H:%M").time(),
                    status="Scheduled",
                    consultation_mode="Offline",
                    payment_status="Paid",
                    reason="Cardiac evaluation and follow-up consultation"
                ))
                print(f"  + Created sample appointment for {sample_patient.full_name}")

            # Seed Simulated Emergency Alert if none
            if Emergency.query.filter_by(hospital_id=first_hosp.id).count() == 0:
                first_amb = Ambulance.query.filter_by(hospital_id=first_hosp.id).first()
                db.session.add(Emergency(
                    patient_id=sample_patient.id,
                    hospital_id=first_hosp.id,
                    ambulance_id=first_amb.id if first_amb else None,
                    emergency_type="Severe Chest Pain / Trauma Triage",
                    description="Patient experiencing acute discomfort. Priority triage assigned.",
                    priority="Critical",
                    pickup_location="Park Street Crossing, Kolkata",
                    destination=first_hosp.name,
                    status="Dispatched"
                ))
                print(f"  + Created active emergency dispatch alert for {first_hosp.name}")

        try:
            from seed_user_hospitals import run_seeder
            run_seeder()
        except Exception as e:
            print(f"User hospitals seed note: {e}")

        db.session.commit()

        print("\n" + "=" * 65)
        print("🎉 PAN-INDIA SEEDING SUCCESSFULLY COMPLETED!")
        print("=" * 65)
        print(f"Total Hospitals in Database:      {Hospital.query.count()}")
        print(f"Total Hospital Beds Tracked:      {Bed.query.count()} (ICU, Emergency, General)")
        print(f"Total Ambulances in Fleet:        {Ambulance.query.count()}")
        print(f"Total Doctors Configured:         {Doctor.query.count()}")
        print(f"Medical Specializations Available:{Specialization.query.count()}")
        print("\nDemo Credentials to Log In:")
        print("  👑 Super Admin:    admin@medilink.com    | Password: Admin@123")
        print("  🏥 Hospital Admin: hospital@medilink.com | Password: Hospital@123")
        print("  🧑 Patient User:   patient@medilink.com  | Password: Patient@123")
        print("=" * 65)


if __name__ == "__main__":
    reset_mode = "--reset" in sys.argv
    seed_database(reset=reset_mode)
