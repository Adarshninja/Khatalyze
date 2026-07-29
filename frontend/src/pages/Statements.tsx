import {
  Calendar,
  ChevronRight,
  FileText,
  Landmark,
  Search,
} from "lucide-react";

import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";

const statements = [
  {
    bank: "HDFC Bank",
    period: "January 2026",
    transactions: 154,
  },
  {
    bank: "ICICI Bank",
    period: "December 2025",
    transactions: 138,
  },
  {
    bank: "SBI",
    period: "November 2025",
    transactions: 176,
  },
  {
    bank: "Axis Bank",
    period: "October 2025",
    transactions: 120,
  },
];

export default function Statements() {
  return (
    <main className="flex-1 bg-[#09090B] p-10">

      <div className="flex items-center justify-between">

        <div>
          <h1 className="text-4xl font-bold text-white">
            Statements
          </h1>

          <p className="mt-2 text-zinc-400">
            Browse and manage analyzed bank statements.
          </p>
        </div>

        <div className="relative w-80">

          <Search
            size={18}
            className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500"
          />

          <Input
            className="pl-11"
            placeholder="Search..."
          />

        </div>

      </div>

      <div className="mt-8 space-y-5">

        {statements.map((statement) => (
          <Card
            key={statement.period}
            className="group rounded-3xl border-white/10 bg-[#111113] p-6 transition hover:border-cyan-500/20 hover:bg-[#151517]"
          >
            <div className="flex items-center justify-between">

              <div className="flex items-center gap-5">

                <div className="rounded-2xl bg-cyan-500/10 p-4">
                  <Landmark className="text-cyan-400" />
                </div>

                <div>

                  <h2 className="text-xl font-semibold text-white">
                    {statement.bank}
                  </h2>

                  <div className="mt-2 flex gap-6 text-sm text-zinc-400">

                    <div className="flex items-center gap-2">
                      <Calendar size={16} />
                      {statement.period}
                    </div>

                    <div className="flex items-center gap-2">
                      <FileText size={16} />
                      {statement.transactions} Transactions
                    </div>

                  </div>

                </div>

              </div>

              <ChevronRight className="text-zinc-500 transition group-hover:translate-x-1 group-hover:text-cyan-400" />

            </div>
          </Card>
        ))}

      </div>

    </main>
  );
}
