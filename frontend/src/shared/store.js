import { create } from "zustand";

export const useAuth = create((set, get) => ({
    user: null,
    token: typeof window !== 'undefined' ? localStorage.getItem("token") : null,
    
    setUser: (user) => set({ user }),
    
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
        }
        set({ user: null, token: null });
    },
    
    restoreUser: () => {
        if (typeof window !== 'undefined') {
            const token = localStorage.getItem("token");
            if (token) {
                try {
                    const payload = JSON.parse(atob(token.split('.')[1]));
                    set({ 
                        token,
                        user: { 
                            id: payload.sub, 
                            email: payload.email || '', 
                            name: payload.name || '', 
                            role: payload.role || 'user' 
                        }
                    });
                } catch (error) {
                    console.error("Ошибка при восстановлении пользователя:", error);
                    localStorage.removeItem("token");
                    set({ user: null, token: null });
                }
            }
        }
    },
    
    initialize: () => {
        get().restoreUser();
    }
})); 