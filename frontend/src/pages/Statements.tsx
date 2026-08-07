import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Calendar,
  ChevronRight,
  FileText,
  Landmark,
  Search,
} from "lucide-react";

import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

import { useStatements } from "@/hooks/useStatements";
import { useCurrentStatement } from "@/context/CurrentStatementContext";

export default function Statements() {
  const navigate = useNavigate();

  const { setStatementId } = useCurrentStatement();

  const { data: statements = [], isLoading, isError } = useStatements();

  const [search, setSearch] = useState("");

  const filteredStatements = useMemo(() => {
    const q = search.toLowerCase();

    return statements.filter((statement) => {
      return (
        statement.bank.toLowerCase().includes(q) ||
        statement.original_filename.toLowerCase().includes(q)
      );
    });
  }, [search, statements]);

  if (isLoading) {
    return (
      <main className="flex-1 flex items-center justify-center bg-[#09090B] text-white">
        Loading statements...
      </main>
    );
  }

  if (isError) {
    return (
      <main className="flex-1 flex items-center justify-center bg-[#09090B] text-red-400">
        Failed to load statements.
      </main>
    );
  }

  return (
    <main className="flex-1 bg-[#09090B] p-10">

      <div className="flex items-center justify-between">

        <div>
          <h1 className="text-4xl font-bold text-white">
            Statements
          </h1>

          <p className="mt-2 text-zinc-400">
            Browse previously analyzed statements.
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
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

        </div>

      </div>

      {filteredStatements.length === 0 ? (
        <div className="mt-16 text-center text-zinc-400">
          No analyzed statements found.
        </div>
      ) : (
        <div className="mt-8 space-y-5">

          {filteredStatements.map((statement) => (
            <Card
              key={statement.statement_id}
              onClick={() => {
                setStatementId(statement.statement_id);
                navigate(`/analysis/${statement.statement_id}`);
              }}
              className="group cursor-pointer rounded-3xl border-white/10 bg-[#111113] p-6 transition hover:border-cyan-500/30 hover:bg-[#151517]"
            >

              <div className="flex items-center justify-between">

                <div className="flex items-center gap-5">

                  <div className="rounded-2xl bg-cyan-500/10 p-4">
                    <Landmark className="text-cyan-400" />
                  </div>

                  <div>

                    <h2 className="text-xl font-semibold text-white">
                      {statement.bank.replace("BankName.", "")}
                    </h2>

                    <p className="mt-1 text-sm text-zinc-500">
                      {statement.original_filename}
                    </p>

                    <div className="mt-3 flex gap-6 text-sm text-zinc-400">

                      <div className="flex items-center gap-2">
                        <Calendar size={16} />
                        {new Date(
                          statement.analysis_completed
                        ).toLocaleDateString()}
                      </div>

                      <div className="flex items-center gap-2">
                        <FileText size={16} />
                        {statement.transaction_count} Transactions
                      </div>

                    </div>

                  </div>

                </div>

                <ChevronRight className="text-zinc-500 transition group-hover:translate-x-1 group-hover:text-cyan-400" />

              </div>

            </Card>
          ))}

        </div>
      )}

    </main>
  );
}

