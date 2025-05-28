import React, { useEffect } from "react";

export default function LoginPage() {
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
        throw new Error("Login failed");
      }

      const data = await res.json();
      console.log("Login Success:", data);
      // 로그인 성공 후 상태 저장 또는 라우팅 처리
    } catch (error) {
      console.error("Login Error:", error);
    }
  };

  useEffect(() => {
    /* global google */
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

  // const handleGoogleLogin = () => {
  //   window.google.accounts.id.prompt(); // 팝업 방식
  //   console.log("button clicked");
  // };

  return (
    <div className="flex min-h-screen">
      {/* 왼쪽 - 전략 그래픽 */}
      <div className="bg-black text-white w-2/3 flex flex-col items-center justify-center relative">
        <h1 className="text-5xl font-bold tracking-widest">FOOTBALL</h1>
        <h2 className="text-3xl mt-2 text-gray-400 tracking-widest">
          STRATEGY
        </h2>
        <div className="w-5/6 h-5/6 border-4 border-white mt-8 relative">
          <div className="absolute inset-0 border border-white" />
          <div className="absolute left-1/2 top-0 bottom-0 w-px bg-white" />
          <div className="absolute left-0 right-0 top-1/2 h-px bg-white" />
          <div className="absolute w-10 h-px bg-red-500 rotate-[35deg] left-[20%] top-[30%]" />
          <div className="absolute w-12 h-px bg-red-500 rotate-[0deg] left-[45%] top-[40%]" />
          <div className="absolute w-16 h-px bg-red-500 rotate-[25deg] left-[35%] top-[60%]" />
          <div className="absolute w-10 h-px bg-red-500 rotate-[45deg] left-[70%] top-[65%]" />
        </div>
      </div>

      {/* 오른쪽 - 로그인 */}
      <div className="w-1/3 bg-white text-black flex flex-col items-center justify-center p-10">
        <h1 className="text-4xl font-bold mb-2 tracking-widest">
          Soccer
          <br />
          Lab
        </h1>
        <h2 className="text-2xl mb-6">Login</h2>

        <p id="google-login-btn">sign in with Google</p>

        <button className="bg-gray-100 border border-gray-300 px-4 py-2 rounded shadow-sm mb-6 hover:bg-gray-200">
          try without signin
        </button>

        <p className="text-sm text-center text-gray-600">
          You can save
          <br />
          your boards
          <br />
          with Google Login
        </p>
      </div>
    </div>
  );
}
