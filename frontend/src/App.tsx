import { Navigate, Route, Routes } from "react-router-dom";
import { TargetsPage } from "./pages/TargetsPage";

export function App() {
  return (
    <Routes>
      <Route path="/targets" element={<TargetsPage />} />
      <Route path="*" element={<Navigate to="/targets" replace />} />
    </Routes>
  );
}
