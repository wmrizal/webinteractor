import { Navigate, Route, Routes } from "react-router-dom";
import { NavBar } from "./components/layout/NavBar";
import { LandingPage } from "./pages/LandingPage";
import { RunHistoryPage } from "./pages/RunHistoryPage";
import { RunPage } from "./pages/RunPage";
import { TargetsPage } from "./pages/TargetsPage";

export function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/targets" element={<TargetsPage />} />
        <Route path="/runs" element={<RunPage />} />
        <Route path="/history" element={<RunHistoryPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
