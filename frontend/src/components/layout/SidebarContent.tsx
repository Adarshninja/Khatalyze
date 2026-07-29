import { NavLink } from "react-router-dom";
import {
  BrainCircuit,
  ChartColumn,
  FileText,
  LayoutDashboard,
  Settings,
  Upload,
} from "lucide-react";

type Props = {
  collapsed?: boolean;
};

const menuItems = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
    href: "/",
  },
  {
    title: "Analytics",
    icon: ChartColumn,
    href: "/analysis",
  },
  {
    title: "Statements",
    icon: FileText,
    href: "/statements",
  },
  {
    title: "AI Workspace",
    icon: BrainCircuit,
    href: "/chat",
  },
  {
    title: "Upload",
    icon: Upload,
    href: "/upload",
  },
  {
    title: "Settings",
    icon: Settings,
    href: "/settings",
  },
];

export default function SidebarContent({
  collapsed = false,
}: Props) {
  return (
    <nav className="flex-1 px-3 py-4">
      {menuItems.map((item) => {
        const Icon = item.icon;

        return (
          <NavLink
            key={item.title}
            to={item.href}
            className={({ isActive }) =>
              `group mb-2 flex items-center rounded-xl px-4 py-3 transition-all duration-200 ${
                collapsed ? "justify-center" : "gap-3"
              } ${
                isActive
                  ? "bg-cyan-500/10 text-cyan-400"
                  : "text-zinc-400 hover:bg-zinc-900 hover:text-white"
              }`
            }
          >
            <Icon
              size={20}
              className="shrink-0 transition-transform duration-300 group-hover:scale-110"
            />

            {!collapsed && (
              <span className="font-medium">
                {item.title}
              </span>
            )}
          </NavLink>
        );
      })}
    </nav>
  );
}

