import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";
import { Route, Routes } from "react-router-dom";
import { Home } from "./pages/Home";

let logged = false;

function App() {
  if (!logged) {
    return <></>;
  }
  return (
    <div className="page">
      <div className="links">
        <a href="/">Home</a>
        <a href="/1">Some</a>
      </div>
      <div className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/:id" element={<Home />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
