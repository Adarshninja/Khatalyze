import Sidebar from "./Sidebar";
import Dashboard from "@/pages/Dashboard";

export default function AppShell() {
  return (
    <div className="flex h-screen bg-[#09090B]">
      <Sidebar />

      <Dashboard />
    </div>
  );
}
