import { Bell, Menu, Search } from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet";

import Sidebar from "./Sidebar";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-zinc-800 bg-[#09090B]/80 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between px-4 md:px-6 lg:px-8">

        {/* Left Section */}
        <div className="flex items-center gap-4">

          {/* Mobile Menu */}
          <div className="lg:hidden">
            <Sheet>
              <SheetTrigger asChild>
                <button className="rounded-lg p-2 transition hover:bg-zinc-800">
                  <Menu className="h-5 w-5 text-white" />
                </button>
              </SheetTrigger>

              <SheetContent
                side="left"
                className="w-72 border-zinc-800 bg-[#09090B] p-0"
              >
                <Sidebar />
              </SheetContent>
            </Sheet>
          </div>

          {/* Search */}
          <div className="relative w-48 sm:w-72 md:w-80">
            <Search
              size={18}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500"
            />

            <Input
              placeholder="Search statements..."
              className="pl-10"
            />
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-4">

          <button className="rounded-lg p-2 transition hover:bg-zinc-800">
            <Bell
              size={20}
              className="text-zinc-400"
            />
          </button>

          <Avatar className="cursor-pointer">
            <AvatarFallback>
              AB
            </AvatarFallback>
          </Avatar>

        </div>
      </div>
    </header>
  );
}
