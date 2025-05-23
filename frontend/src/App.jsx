import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
// import TeamPage from './pages/TeamPage';
// import BoardPage from './pages/BoardPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        {/* <Route path="/teams" element={<TeamPage />} /> */}
        {/* <Route path="/boards" element={<BoardPage />} /> */}

      </Routes>
    </BrowserRouter>
  );
}
