export const getToken = () => {
    return localStorage.getItem("access_token");
};

export const getStoredUser = () => {
    const user = localStorage.getItem("user");

    if (!user) {
        return null;
    }

    try {
        return JSON.parse(user);
    } catch {
        return null;
    }
};

export const saveAuth = (token, user) => {
    localStorage.setItem(
        "access_token",
        token
    );

    if (user) {
        localStorage.setItem(
            "user",
            JSON.stringify(user)
        );
    }
};

export const clearAuth = () => {
    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "user"
    );
};