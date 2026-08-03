# Database Design

# MediLink

## Smart Healthcare Management & Emergency Response Platform

---

# Database Goal

The database is designed to support a scalable, secure, multi-hospital healthcare ecosystem.

The design follows:

- Third Normal Form (3NF)
- Referential Integrity
- Soft Deletes
- Audit Logging
- Role-Based Access
- Scalability

---

# Database Categories

Instead of creating random tables, we divide them into domains.

## 1. Identity Domain

Responsible for authentication and user management.

Contains:

- Users
- Roles
- Permissions
- Sessions
- Audit Logs

---

## 2. Hospital Domain

Responsible for hospitals.

Contains:

- Hospital Organization
- Hospital Branch
- Departments
- Wards
- Rooms
- Beds

---

## 3. Staff Domain

Contains:

- Doctors
- Nurses
- Receptionists
- Finance Staff
- Emergency Operators

---

## 4. Patient Domain

Contains:

- Patient Profile
- Emergency Contacts
- Family Members
- Medical History

---

## 5. Appointment Domain

Contains:

- Appointments
- Doctor Schedule
- Queue

---

## 6. Emergency Domain

Contains:

- SOS Requests
- Ambulances
- Drivers
- Dispatch
- GPS Tracking

---

## 7. Laboratory Domain

Contains:

- Lab Tests
- Reports
- Sample Collection

---

## 8. Pharmacy Domain

Contains:

- Medicines
- Prescriptions
- Inventory

---

## 9. Blood Bank Domain

Contains:

- Blood Inventory
- Donors
- Blood Requests

---

## 10. Billing Domain

Contains:

- Bills
- Payments
- Insurance

---

## 11. Notification Domain

Contains:

- Notifications
- Emails
- SMS Logs

---

## 12. Analytics Domain

Contains:

- Reports
- Dashboard Statistics
- Audit Metrics

---

# Naming Convention

Tables:

snake_case

Example:

users

hospital_branches

doctor_schedules

Columns:

snake_case

Primary Key:

id

Foreign Key:

domain_id

Example:

doctor_id

patient_id

hospital_id

created_at

updated_at

deleted_at

---

# Soft Delete Strategy

Every major table will contain:

deleted_at

instead of permanent deletion.

---

# Audit Strategy

Every important action will be recorded.

Examples:

Login

Logout

Appointment Created

Prescription Updated

Bill Generated

Emergency SOS

---

# Scalability

The database must support:

Unlimited hospitals

Unlimited branches

Unlimited doctors

Unlimited patients

Future mobile apps

Future AI modules

Future government integration

---

# Conclusion

The database architecture is modular.

Every domain is independent while maintaining relationships through foreign keys.