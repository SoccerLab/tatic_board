import React from "react";
import Auth from "./Authorization"

export default function Success() {
    console.log("success page")
  return (
    <>
    <div className="flex items-center justify-center min-h-screen bg-green-100">
      <h1 className="text-3xl font-bold text-green-800">성공했습니다 success🎉</h1>
    </div>
    </>
  );
}
