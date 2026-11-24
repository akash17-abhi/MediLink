import api from "./api";

const recommendationService = {
    getDepartmentRecommendation: async (symptoms) => {
        const response = await api.post("/recommend/department", { symptoms });
        return response.data;
    },

    getRankedHospitals: async (params) => {
        const response = await api.get("/hospitals/recommend", { params });
        return response.data;
    },

    getNearestEmergencyBeds: async (params) => {
        const response = await api.get("/emergencies/nearest-beds", { params });
        return response.data;
    },

    getSpecializations: async () => {
        const response = await api.get("/specializations");
        return response.data;
    },

    getHospitalDoctors: async (hospitalId) => {
        const response = await api.get(`/hospitals/${hospitalId}/doctors`);
        return response.data;
    }
};

export default recommendationService;
