import {
    HeartPulse,
    ShieldCheck,
    Activity,
} from "lucide-react";

const AuthLayout = ({ children }) => {

    return (
        <div className="min-h-screen bg-slate-50 flex">

            {/* LEFT SIDE */}

            <div className="hidden lg:flex lg:w-1/2 bg-blue-700 text-white relative overflow-hidden">

                <div className="absolute inset-0 bg-gradient-to-br from-blue-700 via-blue-800 to-indigo-900"></div>

                <div className="relative z-10 flex flex-col justify-center px-16 xl:px-24">

                    {/* LOGO */}

                    <div className="flex items-center gap-3 mb-10">

                        <div className="w-12 h-12 rounded-xl bg-white/15 flex items-center justify-center">

                            <HeartPulse
                                size={28}
                                strokeWidth={2}
                            />

                        </div>

                        <div>

                            <h1 className="text-2xl font-bold">
                                MediLink
                            </h1>

                            <p className="text-blue-200 text-sm">
                                Smart Healthcare Management
                            </p>

                        </div>

                    </div>

                    <h2 className="text-4xl xl:text-5xl font-bold leading-tight mb-6">

                        Healthcare,
                        <br />

                        connected
                        <br />

                        smarter.

                    </h2>

                    <p className="text-blue-100 text-lg leading-relaxed max-w-lg mb-10">

                        Manage appointments, medical records,
                        prescriptions, laboratories, hospitals,
                        ambulances and more — all from one
                        connected healthcare platform.

                    </p>

                    <div className="space-y-4">

                        <div className="flex items-center gap-3">

                            <div className="w-9 h-9 rounded-lg bg-white/10 flex items-center justify-center">

                                <ShieldCheck size={20} />

                            </div>

                            <span className="text-blue-100">
                                Secure healthcare management
                            </span>

                        </div>

                        <div className="flex items-center gap-3">

                            <div className="w-9 h-9 rounded-lg bg-white/10 flex items-center justify-center">

                                <Activity size={20} />

                            </div>

                            <span className="text-blue-100">
                                Real-time healthcare services
                            </span>

                        </div>

                    </div>

                </div>

            </div>

            {/* RIGHT SIDE */}

            <div className="flex-1 flex items-center justify-center px-6 py-10">

                <div className="w-full max-w-md">

                    {children}

                </div>

            </div>

        </div>
    );
};

export default AuthLayout;