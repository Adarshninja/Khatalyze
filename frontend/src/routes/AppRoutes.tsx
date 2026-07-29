import { Routes, Route, Navigate } from "react-router-dom";

import AppLayout from "@/layouts/AppLayout";

import Dashboard from "@/pages/Dashboard";
import Upload from "@/pages/Upload";
import Analysis from "@/pages/Analysis";
import Statements from "@/pages/Statements";
import Chat from "@/pages/Chat";
import Settings from "@/pages/Settings";

export default function AppRoutes() {
  return (
    <Routes>

      <Route element={<AppLayout />}>

        <Route
          path="/"
          element={<Dashboard />}
        />

        <Route
          path="/upload"
          element={<Upload />}
        />

        <Route
          path="/analysis"
          element={<Analysis />}
        />

        <Route
          path="/statements"
          element={<Statements />}
        />

        <Route
          path="/chat"
          element={<Chat />}
        />

        <Route
          path="/settings"
          element={<Settings />}
        />

      </Route>

      <Route
        path="*"
        element={<Navigate to="/" replace />}
      />

    </Routes>
  );
}

