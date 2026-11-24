import { Navigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {

    const {
        isAuthenticated,
        loading,
    } = useAuth();

    if (loading) {

        return (
            <div className="min-h-screen flex items-center justify-center bg-slate-50">

                <div className="text-center">

                    <div className="w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>

                    <p className="text-slate-600">
                        Checking authentication...
                    </p>

                </div>

            </div>
        );
    }

    if (!isAuthenticated) {

        return (
            <Navigate
                to="/login"
                replace
            />
        );
    }

    return children;
};

export default ProtectedRoute;