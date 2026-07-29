import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet";

import { Menu } from "lucide-react";

import SidebarContent from "./SidebarContent";

export default function MobileSidebar() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <button className="rounded-lg p-2 hover:bg-zinc-800 lg:hidden">
          <Menu className="text-white" />
        </button>
      </SheetTrigger>

      <SheetContent
        side="left"
        className="w-72 border-zinc-800 bg-[#09090B] p-0"
      >
        <div className="border-b border-zinc-800 p-6">

          <div className="flex items-center gap-4">

            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-400 via-blue-500 to-violet-500">
              <span className="font-bold text-white">
                K
              </span>
            </div>

            <div>
              <h1 className="text-xl font-bold text-white">
                Khatalyse
              </h1>

              <p className="text-xs text-zinc-500">
                AI Financial Intelligence
              </p>
            </div>

          </div>

        </div>

        <SidebarContent />
      </SheetContent>
    </Sheet>
  );
}
