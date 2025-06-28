"use client";
import { useAuth } from "./store";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function AuthGuard({ children, role }) {
    const { user } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!user) router.push("/login");
        if (role && user && user.role !== role) router.push("/");
    }, [user, role, router]);

    return <>{children}</>;
} 