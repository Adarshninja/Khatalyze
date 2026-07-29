import { useState } from "react";
import {
  BrainCircuit,
  PanelLeftClose,
  PanelLeftOpen,
} from "lucide-react";

import SidebarContent from "./SidebarContent";

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`flex h-screen flex-col border-r border-zinc-800 bg-[#09090B] transition-all duration-300 ${
        collapsed ? "w-20" : "w-72"
      }`}
    >
      {/* Header */}
      <div className="border-b border-zinc-800 px-4 py-6">
        <div
          className={`flex items-center ${
            collapsed ? "flex-col gap-4" : "justify-between"
          }`}
        >
          <div
            className={`flex items-center ${
              collapsed ? "justify-center" : "gap-4"
            }`}
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-400 via-blue-500 to-violet-500">
              <span className="text-lg font-bold text-white">
                K
              </span>
            </div>

            {!collapsed && (
              <div>
                <h1 className="text-xl font-bold text-white">
                  Khatalyse
                </h1>

                <p className="text-xs text-zinc-500">
                  AI Financial Intelligence
                </p>
              </div>
            )}
          </div>

          <button
            onClick={() => setCollapsed(!collapsed)}
            className="rounded-lg p-2 text-zinc-500 transition hover:bg-zinc-800 hover:text-white"
          >
            {collapsed ? (
              <PanelLeftOpen size={18} />
            ) : (
              <PanelLeftClose size={18} />
            )}
          </button>
        </div>
      </div>

      <SidebarContent collapsed={collapsed} />

      <div className="border-t border-zinc-800 p-4">
        {!collapsed ? (
          <div className="rounded-2xl bg-gradient-to-r from-cyan-500/10 via-blue-500/10 to-violet-500/10 p-4">
            <p className="font-semibold text-white">
              AI Ready
            </p>

            <p className="mt-2 text-sm text-zinc-400">
              Upload a statement and let Khatalyse uncover financial insights.
            </p>
          </div>
        ) : (
          <div className="flex justify-center">
            <div className="rounded-xl bg-cyan-500/10 p-3">
              <BrainCircuit className="text-cyan-400" />
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}