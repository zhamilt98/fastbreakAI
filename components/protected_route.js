"use client"

import { useContext, useEffect } from "react";
import { useRouter } from "next/navigation";
import AuthContext from "../app/auth/auth_context";

const ProtectedRoute = ({ children }) => {
    const { user } = useContext(AuthContext);
    const router = useRouter();

    useEffect(() => {
        if (!user) {
            router.push('/auth');
        }
    }, [user, router]);

    return user ? children : null;
};

export default ProtectedRoute;