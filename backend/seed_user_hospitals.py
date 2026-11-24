"""
MediLink Custom Hospitals Seeder
Parses user-provided hospital raw data and safely seeds/updates hospitals,
beds, ambulances, doctors, schedules, and clinical specializations.
"""

import re
import csv
import io
from app import create_app
from app.extensions import db
from app.models.hospital import Hospital
from app.models.bed import Bed
from app.models.ambulance import Ambulance
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.models.specialization import Specialization

RAW_CSV = '''registration_code,hospital_name,hospital_type,address,city,district,state,pincode,latitude,longitude,phone,emergency_phone,emergency_24x7,ambulance_available,accreditation,total_beds,icu_beds,er_beds,general_beds,specialties,doctors
WB-KOL-APOL-001,"Apollo Multispeciality Hospitals",Private,"58 Canal Circular Road, Kadapara, Phoolbagan, Kankurgachi",Kolkata,Kolkata,West Bengal,700054,22.5744,88.4011,"033 2320 3040","1066",Yes,Yes,"NABH, JCI",750,110,45,595,"Cardiology; Oncology; Neurology; Organ Transplants","Dr. Debashis Ghosh (Cardiology); Dr. Ananya Sen (Neurology)"
WB-KOL-CMRI-002,"CMRI Hospital",Private,"7/2 Diamond Harbour Road, New Alipore",Kolkata,Kolkata,West Bengal,700027,22.5236,88.3292,"080 6213 6596","033 4090 3090",Yes,Yes,"NABH",440,65,30,345,"Pulmonology; Cardiac Sciences; Nephrology; Neurology","Dr. Raja Dhar (Pulmonology); Dr. Arindam Pande (Cardiology)"
WB-KOL-MANI-003,"Manipal Hospitals Broadway",Private,"JC-16 & 17, No. 3A Broadway Road, Sector 3, Bidhannagar",Kolkata,North 24 Parganas,West Bengal,700106,22.5735,88.4143,"033 6907 0000","033 6907 0000",Yes,Yes,"NABH",280,45,20,215,"Orthopedics; Gastroenterology; Pediatrics; General Surgery","Dr. Siddhartha Mukherjee (Orthopedics); Dr. Priya Banerjee (Pediatrics)"
WB-KOL-RUBY-004,"Ruby General Hospital",Private,"576 Anandapur Main Road, Golpark, Sector I, Kasba",Kolkata,Kolkata,West Bengal,700107,22.5133,88.4021,"033 6601 1800","033 6687 1800",Yes,Yes,"NABH",320,55,25,240,"Trauma Care; Cardiac Surgery; Urology; Oncology","Dr. Subrata Maitra (Internal Medicine); Dr. S. K. Basu (Urology)"
WB-KOL-PEER-005,"Peerless Hospital",Private,"360 Panchasayar, Kanti Roy Sarani",Kolkata,Kolkata,West Bengal,700094,22.4811,88.3935,"033 4011 1222","033 2462 2462",Yes,Yes,"NABH",500,80,35,385,"Critical Care; Neurology; Cardiology; Endocrinology","Dr. Alok Roy (Critical Care); Dr. Sunandan Sikdar (Cardiology)"
WB-KOL-SSKM-006,"IPGMER and SSKM Hospital",Government,"244 AJC Bose Road, Bhowanipore",Kolkata,Kolkata,West Bengal,700071,22.5393,88.3422,"033 2204 1100","108",Yes,Yes,"NMC Recognized",1775,180,95,1500,"Neurosurgery; Cardiology; Hepatology; General Medicine","Dr. Manimoy Bandyopadhyay (Admin); Dr. Abhijit Chowdhury (Hepatology)"
WB-KOL-FORT-007,"Fortis Hospital Anandapur",Private,"730 Eastern Metropolitan Bypass, Anandapur",Kolkata,Kolkata,West Bengal,700107,22.5186,88.4017,"033 6628 4444","033 6628 4444",Yes,Yes,"NABH",400,70,30,300,"Cardiac Sciences; Pulmonology; Urology; Kidney Transplants","Dr. R. K. Chatterjee (Pulmonology); Dr. Subhashis Roy (Urology)"
WB-KOL-MEDC-008,"Medica Superspecialty Hospital",Private,"127 Mukundapur, E.M. Bypass",Kolkata,Kolkata,West Bengal,700099,22.4952,88.4023,"033 6652 0000","033 6652 0000",Yes,Yes,"NABH",500,90,35,375,"Cardiac Sciences; Neurosciences; Nephrology; Critical Care","Dr. Kunal Sarkar (Cardiac Surgery); Dr. L. N. Tripathy (Neurosurgery)"
WB-KOL-NRS-009,"Nil Ratan Sircar Medical College and Hospital",Government,"138 AJC Bose Road, Sealdah, Raja Bazar",Kolkata,Kolkata,West Bengal,700014,22.5645,88.3694,"033 2286 0033","108",Yes,Yes,"NMC Recognized",1890,150,110,1630,"Hematology; General Surgery; Orthopedics; Pediatrics","Dr. Pitbaran Chakraborty (Admin); Dr. Tuphan Kanti Dolai (Hematology)"
WB-HOW-NARA-010,"Narayana Hospital Howrah",Private,"120/1 Andul Road, near Nabanna, Shibpur",Howrah,Howrah,West Bengal,711103,22.5668,88.3121,"080 6215 4783","1800 309 0309",Yes,Yes,"NABH",350,60,25,265,"Oncology; Cardiac Sciences; Renal Sciences; Orthopedics","Dr. Soumen Devidutta (Cardiology); Dr. Tapas Kumar Sahoo (Critical Care)"
WB-N24-BASI-011,"Basirhat District Hospital",Government,"Badartala Hospital More, Itinda Road, Basirhat",Basirhat,North 24 Parganas,West Bengal,743411,22.6574,88.8672,"076994 39231","108",Yes,Yes,"State Govt",300,24,20,256,"General Medicine; Obstetrics & Gynecology; Pediatrics; Emergency Trauma","Dr. S. Mondal (General Medicine); Dr. P. Das (Pediatrics)"
WB-N24-BARA-012,"Barasat Government Medical College and Hospital",Government,"Banamalipur, Jessore Road, Barasat",Barasat,North 24 Parganas,West Bengal,700124,22.7214,88.4832,"033 2552 3129","108",Yes,Yes,"NMC Recognized",650,50,40,560,"General Medicine; Pediatrics; Gynecology; Orthopedics","Dr. Suhrita Paul (Admin); Dr. A. K. Jana (General Medicine)"
WB-DUR-MISS-013,"The Mission Hospital Durgapur",Private,"Immon Kalyan Sarani, Sector IIC, Bidhannagar",Durgapur,Paschim Bardhaman,West Bengal,713212,23.5323,87.3458,"086875 00500","0343 253 5555",Yes,Yes,"NABH",350,90,30,230,"Cardiac Surgery; Neonatology; Neurosurgery; Gastroenterology","Dr. Satyajit Bose (Cardiac Surgery); Dr. Koushik Das (Neurosurgery)"
WB-SIL-NEOT-014,"Neotia Getwel Multispecialty Hospital",Private,"Uttorayon Township, Matigara",Siliguri,Darjeeling,West Bengal,734010,26.7271,88.3953,"0353 660 3000","0353 660 3000",Yes,Yes,"NABH",250,50,20,180,"Cardiology; Nephrology; Orthopedics; Minimal Access Surgery","Dr. Dipankar Ghosh (Cardiology); Dr. Amitava Ray (Orthopedics)"
WB-BUR-BMCH-015,"Burdwan Medical College and Hospital",Government,"Baburbag, Rajbati, Bardhaman",Bardhaman,Purba Bardhaman,West Bengal,713104,23.2494,87.8548,"0342 266 2322","108",Yes,Yes,"NMC Recognized",1200,95,75,1030,"General Medicine; Cardiology; Ophthalmology; Trauma Care","Dr. Mousumi Bandyopadhyay (Admin); Dr. S. K. Roy (Cardiology)"
'''

def parse_doctor_str(doc_str):
    """
    Parses 'Dr. Debashis Ghosh (Cardiology)' -> ('Dr. Debashis Ghosh', 'Cardiology')
    """
    m = re.match(r"(.*?)\s*\((.*?)\)", doc_str.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return doc_str.strip(), "General Medicine"

def run_seeder():
    app = create_app()
    with app.app_context():
        reader = csv.DictReader(io.StringIO(RAW_CSV.strip()))
        added_hosp = 0
        updated_hosp = 0
        added_docs = 0
        added_beds = 0
        added_ambs = 0

        for row in reader:
            reg_code = row["registration_code"].strip()
            name = row["hospital_name"].strip()
            h_type = row["hospital_type"].strip()
            address = row["address"].strip()
            city = row["city"].strip()
            state = row["state"].strip()
            pincode = row["pincode"].strip()
            lat = float(row["latitude"])
            lng = float(row["longitude"])
            phone = row["phone"].strip()
            emg_phone = row["emergency_phone"].strip()
            is_24x7 = row["emergency_24x7"].strip().lower() == "yes"
            accreditation = row["accreditation"].strip()
            tot_beds = int(row["total_beds"])
            icu_beds = int(row["icu_beds"])
            er_beds = int(row["er_beds"])
            specs_raw = row["specialties"].strip()
            doctors_raw = row["doctors"].strip()

            email_slug = re.sub(r'[^a-z0-9]', '', name.lower())[:15]
            email = f"{email_slug}@medilink.com"
            desc = f"{name} is an accredited ({accreditation}) facility in {city}, {state}. Offering comprehensive departments: {specs_raw}."

            hosp = Hospital.query.filter((Hospital.registration_number == reg_code) | (Hospital.name == name)).first()
            if not hosp:
                hosp = Hospital(
                    name=name,
                    registration_number=reg_code,
                    hospital_type=h_type,
                    description=desc,
                    email=email,
                    phone=phone,
                    emergency_contact=emg_phone,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    latitude=lat,
                    longitude=lng,
                    is_24x7=is_24x7,
                    total_beds=tot_beds,
                    icu_beds=icu_beds,
                    emergency_beds=er_beds,
                    is_verified=True,
                    is_active=True
                )
                db.session.add(hosp)
                db.session.flush()
                added_hosp += 1
            else:
                hosp.registration_number = reg_code
                hosp.address = address
                hosp.city = city
                hosp.state = state
                hosp.pincode = pincode
                hosp.latitude = lat
                hosp.longitude = lng
                hosp.phone = phone
                hosp.emergency_contact = emg_phone
                hosp.is_24x7 = is_24x7
                hosp.total_beds = tot_beds
                hosp.icu_beds = icu_beds
                hosp.emergency_beds = er_beds
                hosp.description = desc
                updated_hosp += 1

            # Ensure specializations exist
            for s_name in specs_raw.split(";"):
                s_clean = s_name.strip()
                if s_clean:
                    sp = Specialization.query.filter_by(name=s_clean).first()
                    if not sp:
                        s_code = re.sub(r'[^A-Z0-9]', '', s_clean.upper())[:12]
                        # Ensure uniqueness of code
                        existing_code = Specialization.query.filter_by(code=s_code).first()
                        if existing_code:
                            s_code = f"{s_code[:9]}_{len(s_clean)}"
                        db.session.add(Specialization(
                            name=s_clean,
                            code=s_code,
                            description=f"{s_clean} clinical department",
                            icon="Activity",
                            is_active=True
                        ))
                        db.session.flush()

            # Seed beds if not present
            existing_beds = Bed.query.filter_by(hospital_id=hosp.id).count()
            if existing_beds == 0:
                # Add discrete beds for live tracker
                for i in range(1, 9):
                    db.session.add(Bed(
                        hospital_id=hosp.id,
                        bed_number=f"ICU-{i:02d}",
                        ward="Intensive Care Unit (ICU)",
                        bed_type="ICU",
                        status="Available" if i <= 4 else "Occupied"
                    ))
                    added_beds += 1
                for i in range(1, 9):
                    db.session.add(Bed(
                        hospital_id=hosp.id,
                        bed_number=f"ER-{i:02d}",
                        ward="Emergency Trauma Center",
                        bed_type="Emergency",
                        status="Available" if i <= 5 else "Occupied"
                    ))
                    added_beds += 1
                for i in range(1, 13):
                    db.session.add(Bed(
                        hospital_id=hosp.id,
                        bed_number=f"GEN-{i:02d}",
                        ward="General Medical Ward",
                        bed_type="General",
                        status="Available" if i <= 7 else "Occupied"
                    ))
                    added_beds += 1

            # Seed Ambulances if available
            if row["ambulance_available"].strip().lower() == "yes":
                existing_amb = Ambulance.query.filter_by(hospital_id=hosp.id).count()
                if existing_amb == 0:
                    clean_reg = re.sub(r'[^A-Z0-9]', '', reg_code)[:8]
                    db.session.add(Ambulance(
                        hospital_id=hosp.id,
                        registration_number=f"{clean_reg}-AMB-01",
                        ambulance_type="Advanced Life Support (ALS) with Ventilator",
                        driver_name="Ramesh Soren",
                        driver_phone="+91 98301 23456",
                        current_location=f"{city} Base Unit",
                        availability_status="Available"
                    ))
                    db.session.add(Ambulance(
                        hospital_id=hosp.id,
                        registration_number=f"{clean_reg}-AMB-02",
                        ambulance_type="Basic Life Support (BLS)",
                        driver_name="Debabrata Roy",
                        driver_phone="+91 98302 34567",
                        current_location=f"{city} Standby",
                        availability_status="Available"
                    ))
                    added_ambs += 2

            # Seed Doctors
            doc_items = [d.strip() for d in doctors_raw.split(";") if d.strip()]
            for d_idx, doc_item in enumerate(doc_items):
                d_name, d_spec = parse_doctor_str(doc_item)
                d_email_slug = re.sub(r'[^a-z0-9]', '', d_name.lower())[:15]
                d_email = f"{d_email_slug}.{hosp.id}@medilink.com"

                existing_doc = Doctor.query.filter_by(full_name=d_name, hospital_id=hosp.id).first()
                if not existing_doc:
                    doc = Doctor(
                        full_name=d_name,
                        email=d_email,
                        phone=phone,
                        specialization=d_spec,
                        qualification="MBBS, MD / MS / DM",
                        experience=10 + (d_idx * 3),
                        consultation_fee=800.0 + (d_idx * 200.0),
                        is_active=True,
                        hospital_id=hosp.id
                    )
                    db.session.add(doc)
                    db.session.flush()
                    added_docs += 1

                    # Add OPD schedule for doctor
                    from datetime import time
                    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                    for day in days:
                        db.session.add(DoctorSchedule(
                            doctor_id=doc.id,
                            day_of_week=day,
                            start_time=time(9, 0),
                            end_time=time(17, 0),
                            slot_duration=30,
                            is_available=True
                        ))

        db.session.commit()
        print(f"SUCCESS: Seeded {added_hosp} new hospitals, updated {updated_hosp} hospitals.")
        print(f"Added {added_docs} doctors, {added_beds} beds, and {added_ambs} ambulance units.")

if __name__ == "__main__":
    run_seeder()
