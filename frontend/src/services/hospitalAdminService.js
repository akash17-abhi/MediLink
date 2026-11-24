import api from "./api";

const hospitalAdminService = {
    getSummary: async () => {
        const response = await api.get("/hospital-admin/summary");
        return response.data;
    },

    getBeds: async (bedType) => {
        const response = await api.get("/hospital-admin/beds", {
            params: bedType ? { bed_type: bedType } : {}
        });
        return response.data;
    },

    updateBed: async (bedId, data) => {
        const response = await api.patch(`/hospital-admin/beds/${bedId}`, data);
        return response.data;
    },

    quickToggleBed: async (bedType, action) => {
        const response = await api.post("/hospital-admin/beds/quick-toggle", {
            bed_type: bedType,
            action
        });
        return response.data;
    },

    getAmbulances: async () => {
        const response = await api.get("/hospital-admin/ambulances");
        return response.data;
    },

    updateAmbulance: async (ambId, data) => {
        const response = await api.patch(`/hospital-admin/ambulances/${ambId}`, data);
        return response.data;
    },

    getEmergencies: async () => {
        const response = await api.get("/hospital-admin/emergencies");
        return response.data;
    },

    updateEmergencyStatus: async (emergencyId, status) => {
        const response = await api.patch("/hospital-admin/emergencies", {
            emergency_id: emergencyId,
            status
        });
        return response.data;
    },

    getAppointments: async () => {
        const response = await api.get("/hospital-admin/appointments");
        return response.data;
    },

    updateAppointmentStatus: async (appointmentId, status) => {
        const response = await api.patch("/hospital-admin/appointments", {
            appointment_id: appointmentId,
            status
        });
        return response.data;
    },

    issuePrescription: async (appointmentId, data) => {
        const response = await api.post(`/hospital-admin/appointments/${appointmentId}/prescription`, data);
        return response.data;
    },

    getAppointmentPrescription: async (appointmentId) => {
        const response = await api.get(`/hospital-admin/appointments/${appointmentId}/prescription`);
        return response.data;
    },

    addBed: async (bedData) => {
        const response = await api.post("/hospital-admin/beds", bedData);
        return response.data;
    },

    deleteBed: async (bedId) => {
        const response = await api.delete(`/hospital-admin/beds/${bedId}`);
        return response.data;
    },

    addAmbulance: async (ambData) => {
        const response = await api.post("/hospital-admin/ambulances", ambData);
        return response.data;
    },

    getDoctors: async () => {
        const response = await api.get("/hospital-admin/doctors");
        return response.data;
    },

    addDoctor: async (doctorData) => {
        const response = await api.post("/hospital-admin/doctors", doctorData);
        return response.data;
    },

    updateDoctor: async (doctorId, data) => {
        const response = await api.patch(`/hospital-admin/doctors/${doctorId}`, data);
        return response.data;
    },

    updateHospitalInfo: async (data) => {
        const response = await api.put("/hospital-admin/info", data);
        return response.data;
    }
};

export default hospitalAdminService;
