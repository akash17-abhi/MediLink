import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";

import authService from "../services/authService";

import {
    getToken,
    getStoredUser,
    saveAuth,
    clearAuth,
} from "../utils/auth";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {

    const [user, setUser] = useState(
        getStoredUser()
    );

    const [loading, setLoading] = useState(true);

    const [isAuthenticated, setIsAuthenticated] = useState(
        !!getToken()
    );


    // =========================================================
    // CHECK CURRENT USER
    // =========================================================

    useEffect(() => {

        const checkAuthentication = async () => {

            const token = getToken();

            if (!token) {

                setIsAuthenticated(false);
                setUser(null);
                setLoading(false);

                return;
            }

            try {

                const response =
                    await authService.getCurrentUser();

                const currentUser =
                    response?.user ||
                    response?.data?.user ||
                    null;

                if (currentUser) {

                    setUser(currentUser);

                    localStorage.setItem(
                        "user",
                        JSON.stringify(currentUser)
                    );

                    setIsAuthenticated(true);

                } else {

                    clearAuth();

                    setUser(null);
                    setIsAuthenticated(false);
                }

            } catch (error) {

                console.error(
                    "Authentication check failed:",
                    error
                );

                clearAuth();

                setUser(null);
                setIsAuthenticated(false);

            } finally {

                setLoading(false);
            }
        };


        checkAuthentication();

    }, []);


    // =========================================================
    // LOGIN - STEP 1
    // EMAIL + PASSWORD
    // =========================================================

    const login = async (
        email,
        password
    ) => {

        try {

            const response =
                await authService.login({
                    email,
                    password,
                });


            /*
             * IMPORTANT:
             *
             * Step 1 does NOT return an access token.
             *
             * Backend response:
             *
             * {
             *   success: true,
             *   message: "...",
             *   requires_otp: true,
             *   email: "..."
             * }
             *
             * Therefore DO NOT look for access_token here.
             */


            if (
                response?.requires_otp === true
            ) {

                return response;
            }


            /*
             * Fallback:
             *
             * If the backend ever performs direct login
             * and returns a JWT, support that as well.
             */

            const token =
                response?.access_token ||
                response?.token ||
                response?.data?.access_token ||
                response?.data?.token;


            if (token) {

                const loggedInUser =
                    response?.user ||
                    response?.data?.user ||
                    null;

                saveAuth(
                    token,
                    loggedInUser
                );

                setUser(loggedInUser);
                setIsAuthenticated(true);

                return response;
            }


            throw new Error(
                response?.message ||
                "Unexpected login response from the server."
            );

        } catch (error) {

            console.error(
                "Login error:",
                error
            );

            throw error;
        }
    };


    // =========================================================
    // VERIFY LOGIN OTP - STEP 2
    // =========================================================

    const verifyLoginOtp = async (
        email,
        otp
    ) => {

        try {

            const response =
                await authService.verifyLoginOtp({
                    email,
                    otp,
                });


            /*
             * Backend STEP 2 response:
             *
             * {
             *   success: true,
             *   message: "Login successful",
             *   access_token: "...",
             *   user: {...}
             * }
             */


            const token =
                response?.access_token ||
                response?.token ||
                response?.data?.access_token ||
                response?.data?.token;


            if (!token) {

                throw new Error(
                    "Login OTP verified but no access token was received from the server."
                );
            }


            const loggedInUser =
                response?.user ||
                response?.data?.user ||
                null;


            // Save JWT + user
            saveAuth(
                token,
                loggedInUser
            );


            setUser(loggedInUser);
            setIsAuthenticated(true);


            return response;

        } catch (error) {

            console.error(
                "Login OTP verification error:",
                error
            );

            throw error;
        }
    };


    // =========================================================
    // RESEND LOGIN OTP
    // =========================================================

    const resendLoginOtp = async (
        email
    ) => {

        return await authService.resendLoginOtp({
            email,
        });
    };


    // =========================================================
    // REGISTER
    // =========================================================

    const register = async (
        full_name,
        email,
        password
    ) => {

        return await authService.register({
            full_name,
            email,
            password,
        });
    };


    // =========================================================
    // LOGOUT
    // =========================================================

    const logout = () => {

        clearAuth();

        setUser(null);
        setIsAuthenticated(false);
    };


    // =========================================================
    // CONTEXT
    // =========================================================

    return (
        <AuthContext.Provider
            value={{
                user,
                loading,
                isAuthenticated,

                login,
                verifyLoginOtp,
                resendLoginOtp,

                register,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};


// =========================================================
// USE AUTH
// =========================================================

export const useAuth = () => {

    const context =
        useContext(AuthContext);

    if (!context) {

        throw new Error(
            "useAuth must be used inside AuthProvider"
        );
    }

    return context;
};