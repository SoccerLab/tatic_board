import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom"; // ✅ 추가


export default function Auth() {
    console.log("try");
    const navigate = useNavigate();
    useEffect(()=>{
        const checkLogin = async () => {
            try{
                const res = await fetch("http://localhost:8000/api/users/me", {
                    credentials: "include"
                })
                if (!res.ok){
                    throw new Error("login needed");
                }
                if (location.pathname === '/login')
                    navigate("/");
            } catch (error){
                if (location.pathname !== '/login')
                    navigate("/login");
            }
        }
        checkLogin();
    },[])
    
    return (
        <>
        </>
    )
}