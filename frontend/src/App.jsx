import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Board from './pages/Board';
import Success from "./pages/Success";
import Auth from "./pages/Authorization"
// import Team from './pages/Team';

export function App() {
    console.log("app");
  return (
    <BrowserRouter>
    <Auth />
      <Routes>
        <Route path="/" element={<Board />} />
        <Route path="/login" element={<Login />} />
        {/* <Route path="/teams" element={<Team />} /> */}
        {/* <Route path="/boards" element={<Board />} /> */}
        <Route path="/success" element={<Success />} />
      </Routes>
    </BrowserRouter>
  );
}
