import { create } from "zustand";

export const useAuth = create((set, get) => ({
    user: null,
    token: null,
    
    setUser: (user) => {
        if (typeof window !== 'undefined') {
            if (user) {
                localStorage.setItem("user", JSON.stringify(user));
            } else {
                localStorage.removeItem("user");
            }
        }
        set({ user });
    },
    
    setToken: (token) => {
        if (typeof window !== 'undefined') {
            if (token) {
                localStorage.setItem("token", token);
            } else {
                localStorage.removeItem("token");
            }
        }
        set({ token });
    },
    
    logout: () => {
        if (typeof window !== 'undefined') {
            localStorage.removeItem("token");
            localStorage.removeItem("user");
        }
        set({ user: null, token: null });
    },
    
    restoreUser: () => {
        if (typeof window !== 'undefined') {
            const token = localStorage.getItem("token");
            const userStr = localStorage.getItem("user");
            if (token && userStr) {
                try {
                    const parsedUser = JSON.parse(userStr);
                    set({ 
                        token,
                        user: parsedUser
                    });
                } catch (error) {
                    localStorage.removeItem("token");
                    localStorage.removeItem("user");
                    set({ user: null, token: null });
                }
            }
        }
    },
    
    initialize: () => {
        get().restoreUser();
    }
})); 