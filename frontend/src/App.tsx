import { Navigate, Route, Routes } from "react-router-dom";
import { RunHistoryPage } from "./pages/RunHistoryPage";
import { RunPage } from "./pages/RunPage";
import { TargetsPage } from "./pages/TargetsPage";

export function App() {
  return (
    <Routes>
      <Route path="/targets" element={<TargetsPage />} />
      <Route path="/runs" element={<RunPage />} />
      <Route path="/history" element={<RunHistoryPage />} />
      <Route path="*" element={<Navigate to="/runs" replace />} />
    </Routes>
  );
}
