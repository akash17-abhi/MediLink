def validate_laboratory(data):

    required_fields = [
        "patient_id",
        "doctor_id",
        "hospital_id",
        "test_name"
    ]

    for field in required_fields:
        if field not in data or data[field] in (None, ""):
            return False, f"{field} is required"

    return True, ""


def laboratory_to_dict(test):

    return {
        "id": test.id,
        "patient_id": test.patient_id,
        "doctor_id": test.doctor_id,
        "hospital_id": test.hospital_id,
        "test_name": test.test_name,
        "category": test.category,
        "status": test.status,
        "result": test.result,
        "report_file": test.report_file,
        "created_at": test.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if test.created_at else None,
        "updated_at": test.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        if test.updated_at else None
    }