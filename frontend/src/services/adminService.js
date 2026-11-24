import api from "./api";

const adminService = {
    getOverview: async () => {
        const response = await api.get("/admin/overview");
        return response.data;
    },

    getUsers: async (params) => {
        const response = await api.get("/admin/users", { params });
        return response.data;
    },

    createUser: async (data) => {
        const response = await api.post("/admin/users", data);
        return response.data;
    },

    updateUser: async (userId, data) => {
        const response = await api.patch(`/admin/users/${userId}`, data);
        return response.data;
    },

    deleteUser: async (userId) => {
        const response = await api.delete(`/admin/users/${userId}`);
        return response.data;
    },

    getSystemHealth: async () => {
        const response = await api.get("/admin/system-health");
        return response.data;
    },

    getHospitals: async (params) => {
        const response = await api.get("/admin/hospitals", { params });
        return response.data;
    },

    getHospital: async (hospId) => {
        const response = await api.get(`/admin/hospitals/${hospId}`);
        return response.data;
    },

    onboardHospital: async (data) => {
        const response = await api.post("/admin/hospitals", data);
        return response.data;
    },

    updateHospital: async (hospId, data) => {
        const response = await api.put(`/admin/hospitals/${hospId}`, data);
        return response.data;
    },

    deleteHospital: async (hospId) => {
        const response = await api.delete(`/admin/hospitals/${hospId}`);
        return response.data;
    },

    getEmergencies: async () => {
        const response = await api.get("/admin/emergencies");
        return response.data;
    },

    getAppointments: async () => {
        const response = await api.get("/admin/appointments");
        return response.data;
    },

    purgeCache: async () => {
        const response = await api.post("/admin/maintenance/cache-purge");
        return response.data;
    },

    syncBeds: async () => {
        const response = await api.post("/admin/maintenance/sync-beds");
        return response.data;
    }
};

export default adminService;
