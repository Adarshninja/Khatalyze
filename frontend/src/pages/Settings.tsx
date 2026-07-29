import {
  Bell,
  Moon,
  Shield,
  User,
  Database,
  ChevronRight,
} from "lucide-react";

import { Card } from "@/components/ui/card";

const settings = [
  {
    title: "Profile",
    description: "Manage your personal information",
    icon: User,
  },
  {
    title: "Appearance",
    description: "Dark mode and UI preferences",
    icon: Moon,
  },
  {
    title: "Notifications",
    description: "Email and in-app notifications",
    icon: Bell,
  },
  {
    title: "Security",
    description: "Password and authentication",
    icon: Shield,
  },
  {
    title: "Data & Storage",
    description: "Manage uploaded statements",
    icon: Database,
  },
];

export default function Settings() {
  return (
    <main className="flex-1 bg-[#09090B] p-10">

      <h1 className="text-4xl font-bold text-white">
        Settings
      </h1>

      <p className="mt-2 text-zinc-400">
        Customize your Khatalyse experience.
      </p>

      <div className="mt-8 space-y-5">

        {settings.map((item) => {
          const Icon = item.icon;

          return (
            <Card
              key={item.title}
              className="group rounded-3xl border-white/10 bg-[#111113] p-6 transition hover:border-cyan-500/20 hover:bg-[#151517]"
            >
              <div className="flex items-center justify-between">

                <div className="flex items-center gap-5">

                  <div className="rounded-2xl bg-cyan-500/10 p-4">
                    <Icon className="text-cyan-400" />
                  </div>

                  <div>

                    <h2 className="text-lg font-semibold text-white">
                      {item.title}
                    </h2>

                    <p className="mt-1 text-sm text-zinc-400">
                      {item.description}
                    </p>

                  </div>

                </div>

                <ChevronRight className="text-zinc-500 transition group-hover:translate-x-1 group-hover:text-cyan-400" />

              </div>
            </Card>
          );
        })}

      </div>

    </main>
  );
}

