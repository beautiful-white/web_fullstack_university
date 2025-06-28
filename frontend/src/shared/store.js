import { create } from "zustand";

export const useAuth = create((set) => ({
    user: null,
    token: null,
    setUser: (user) => set({ user }),
    setToken: (token) => {
        if (token) localStorage.setItem("token", token);
        else localStorage.removeItem("token");
        set({ token });
    },
    logout: () => {
        localStorage.removeItem("token");
        set({ user: null, token: null });
    },
})); 