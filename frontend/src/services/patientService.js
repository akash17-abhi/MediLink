import api from "./api";

const patientService = {
    bookAppointment: async (appointmentData) => {
        const response = await api.post("/patient/appointments", appointmentData);
        return response.data;
    },

    getMyAppointments: async () => {
        const response = await api.get("/patient/appointments");
        return response.data;
    },

    requestEmergency: async (emergencyData) => {
        const response = await api.post("/patient/emergencies", emergencyData);
        return response.data;
    },

    getMyEmergencies: async () => {
        const response = await api.get("/patient/emergencies");
        return response.data;
    },

    getMyPrescriptions: async () => {
        const response = await api.get("/patient/prescriptions");
        return response.data;
    },

    getMyMedicalRecords: async () => {
        const response = await api.get("/patient/medical-records");
        return response.data;
    },

    getMyBills: async () => {
        const response = await api.get("/patient/bills");
        return response.data;
    },

    getMyProfile: async () => {
        const response = await api.get("/patient/profile");
        return response.data;
    },

    updateMyProfile: async (profileData) => {
        const response = await api.put("/patient/profile", profileData);
        return response.data;
    },

    cancelAppointment: async (appointmentId) => {
        const response = await api.post(`/patient/appointments/${appointmentId}/cancel`);
        return response.data;
    }
};

export default patientService;
