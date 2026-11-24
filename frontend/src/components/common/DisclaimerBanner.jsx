import React, { useState } from "react";
import { AlertTriangle, X } from "lucide-react";

export default function DisclaimerBanner() {
    const [dismissed, setDismissed] = useState(false);

    if (dismissed) return null;

    return (
        <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-2.5 text-amber-900 text-xs">
            <div className="max-w-7xl mx-auto flex items-center justify-between gap-3">
                <div className="flex items-center gap-2 font-medium">
                    <span className="p-1 rounded bg-amber-500 text-white shrink-0">
                        <AlertTriangle size={14} />
                    </span>
                    <span>
                        <strong className="font-semibold">Academic Demo Notice:</strong> MediLink is a final-year college demonstration project. All bed availability counts, ambulance units, and emergency dispatches are <em>simulated project data</em>. For actual medical emergencies in India, dial <strong>108</strong>.
                    </span>
                </div>
                <button
                    onClick={() => setDismissed(true)}
                    className="p-1 text-amber-800/60 hover:text-amber-900 rounded transition shrink-0"
                    title="Dismiss notification"
                >
                    <X size={14} />
                </button>
            </div>
        </div>
    );
}
