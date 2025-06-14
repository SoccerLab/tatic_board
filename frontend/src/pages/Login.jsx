import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom"; // ✅ 추가
import Auth from "./Authorization"

export default function Login() {
     const navigate = useNavigate(); // ✅ 리디렉션에 사용

     const handleCredentialResponse = async (response) => {
        console.log("callback");
        const idToken = response.credential;
        console.log("ID Token:", idToken);
    
        try {
          const res = await fetch("http://localhost:8000/api/auth/google-login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include", // 쿠키를 사용하는 경우 필요
            body: JSON.stringify({ id_token: idToken }),
          });
    
          if (!res.ok) {
            console.log("res is not ok");
            throw new Error("Login failed");
          }
    
          const data = await res.json();
          console.log("Login Success:", data);
          // 로그인 성공 후 상태 저장 또는 라우팅 처리
        
          navigate("/"); // ✅ 로그인 성공 시 페이지 이동
          console.log("navigate to /called");
        } catch (error) {
          console.error("Login Error:", error);
        }
      };
    
      useEffect(() => {
        /* global google */
        console.log("initializing....");
        window.google.accounts.id.initialize({
          client_id:
            "873432676720-76eoed9btvn2tpoaqcmcbi8d7ojcqhvm.apps.googleusercontent.com", // 구글 클라이언트 ID 입력
          callback: handleCredentialResponse,
        });
        console.log("initialized");
        window.google.accounts.id.renderButton(
          document.getElementById("google-login-btn"),
          { theme: "outline", size: "large" }
        );
      }, []);
    
  return (
    <div className="flex min-h-screen">
        {/* <Auth></Auth> */}
      {/* Left - Strategy Graphic */}
      <div className="bg-black text-white w-3/4 flex flex-col items-center justify-center relative">
        <h1 className="text-5xl font-bold tracking-widest">FOOTBALL</h1>
        <h2 className="text-3xl mt-2 text-gray-400 tracking-widest">STRATEGY</h2>

        <div className="relative w-[90%] aspect-[105/68] border-4 border-white mt-8">
          {/* 경기장 라인 */}
          <div className="absolute inset-0 border border-white" />
          <div className="absolute left-1/2 top-0 bottom-0 w-[0.4%] bg-white" />
          <div className="absolute w-[17.5%] aspect-square border border-white rounded-full top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />

          {/* 페널티 에어리어 */}
          <div className="absolute left-0 top-[28.5%] w-[15.7%] h-[43%] border border-white" />
          <div className="absolute right-0 top-[28.5%] w-[15.7%] h-[43%] border border-white" />

          {/* 골 에어리어 */}
          <div className="absolute left-0 top-[41%] w-[5.2%] h-[18%] border border-white" />
          <div className="absolute right-0 top-[41%] w-[5.2%] h-[18%] border border-white" />
       
          {/* ─── 🥅 골대 추가 ───────────────────────────────── */}
         {/* 왼쪽 골대 */}
        <div className="absolute left-[-2%] top-[46.5%] w-[2%] h-[6%]">
        {/* w = 2%  → 화면 가로선(=실제 골대 높이)  
            h = 6%  → 화면 세로선(=실제 골대 너비)  */}
        <div className="absolute inset-0 border-2 border-white border-r-0" />
        </div>

        {/* 오른쪽 골대 */}
        <div className="absolute right-[-2%] top-[46.5%] w-[2%] h-[6%]">
        <div className="absolute inset-0 border-2 border-white border-l-0" />
        </div>

          {/* 플레이어 말 + 화살표 */}
          {/* 왼쪽 말 */}
          <div className="absolute w-[2%] aspect-square bg-white rounded-full top-[40%] left-[20%]" />
          <div className="absolute w-[12%] h-[0.3%] bg-red-500 top-[40.9%] left-[21%] rotate-[15deg] origin-left">
            <div className="absolute top-[-6px] right-[-9px] w-0 h-0 border-t-[6px] border-b-[6px] border-l-[10px] border-t-transparent border-b-transparent border-l-red-500" />
          </div>

          {/* 중앙 왼쪽 말 */}
          <div className="absolute w-[2%] aspect-square bg-white rounded-full top-[60%] left-[30%]" />
          <div className="absolute w-[12%] h-[0.3%] bg-red-500 top-[60.9%] left-[31%] rotate-[5deg] origin-left">
            <div className="absolute top-[-6px] right-[-9px] w-0 h-0 border-t-[6px] border-b-[6px] border-l-[10px] border-t-transparent border-b-transparent border-l-red-500" />
          </div>

          {/* 중앙 말 */}
          <div className="absolute w-[2%] aspect-square bg-white rounded-full top-[50%] left-[50%]" />
          <div className="absolute w-[12%] h-[0.3%] bg-red-500 top-[50.9%] left-[51%] rotate-[-10deg] origin-left">
            <div className="absolute top-[-6px] right-[-9px] w-0 h-0 border-t-[6px] border-b-[6px] border-l-[10px] border-t-transparent border-b-transparent border-l-red-500" />
          </div>

          {/* 오른쪽 말 */}
          <div className="absolute w-[2%] aspect-square bg-white rounded-full top-[35%] left-[70%]" />
          <div className="absolute w-[12%] h-[0.3%] bg-red-500 top-[35.9%] left-[71%] rotate-[-30deg] origin-left">
            <div className="absolute top-[-6px] right-[-9px] w-0 h-0 border-t-[6px] border-b-[6px] border-l-[10px] border-t-transparent border-b-transparent border-l-red-500" />
          </div>
        </div>
      </div>

      {/* Right - Login Section */}
      <div className="w-1/3 bg-white text-black flex flex-col items-center justify-center p-10">
        <h1 className="text-4xl font-bold mb-2 tracking-widest text-center leading-tight">
          Soccer<br />Lab
        </h1>
        <h2 className="text-2xl mb-6">Login</h2>

        <button id="google-login-btn" className="bg-gray-100 border border-gray-300 px-4 py-2 rounded shadow-sm mb-2 hover:bg-gray-200">
          sign in with Google
        </button>
        <button className="bg-gray-100 border border-gray-300 px-4 py-2 rounded shadow-sm mb-6 hover:bg-gray-200">
          try without signin
        </button>

        <p className="text-sm text-center text-gray-600">
          You can save<br />your boards<br />with Google Login
        </p>
      </div>
    </div>
  );
}
