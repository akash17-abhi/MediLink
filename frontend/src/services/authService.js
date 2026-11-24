import api from "./api";

const authService = {

    // =========================================================
    // REGISTER
    // =========================================================

    register: async (userData) => {

        const response =
            await api.post(
                "/auth/register",
                userData
            );

        return response.data;
    },


    // =========================================================
    // LOGIN - STEP 1
    // =========================================================

    login: async (credentials) => {

        const response =
            await api.post(
                "/auth/login",
                credentials
            );

        return response.data;
    },


    // =========================================================
    // VERIFY LOGIN OTP - STEP 2
    // =========================================================

    verifyLoginOtp: async (data) => {

        const response =
            await api.post(
                "/auth/verify-login-otp",
                data
            );

        return response.data;
    },


    // =========================================================
    // RESEND LOGIN OTP
    // =========================================================

    resendLoginOtp: async (data) => {

        const response =
            await api.post(
                "/auth/resend-login-otp",
                data
            );

        return response.data;
    },


    // =========================================================
    // CURRENT USER
    // =========================================================

    getCurrentUser: async () => {

        const response =
            await api.get(
                "/auth/me"
            );

        return response.data;
    },


    // =========================================================
    // VERIFY EMAIL
    // =========================================================

    verifyEmail: async (data) => {

        const response =
            await api.post(
                "/auth/verify-email",
                data
            );

        return response.data;
    },


    // =========================================================
    // RESEND EMAIL VERIFICATION
    // =========================================================

    resendVerification: async (data) => {

        const response =
            await api.post(
                "/auth/resend-verification",
                data
            );

        return response.data;
    },


    // =========================================================
    // FORGOT PASSWORD
    // =========================================================

    forgotPassword: async (data) => {

        const response =
            await api.post(
                "/auth/forgot-password",
                data
            );

        return response.data;
    },


    // =========================================================
    // VERIFY RESET OTP
    // =========================================================

    verifyResetOtp: async (data) => {

        const response =
            await api.post(
                "/auth/verify-reset-otp",
                data
            );

        return response.data;
    },


    // =========================================================
    // RESET PASSWORD
    // =========================================================

    resetPassword: async (data) => {

        const response =
            await api.post(
                "/auth/reset-password",
                data
            );

        return response.data;
    },
};

export default authService;