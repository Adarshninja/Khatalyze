import Hero from "@/components/dashboard/Hero";
import StatCard from "@/components/dashboard/StatCard";
import { createReportViewModel } from "@/services/reportAdapter";

import { useCurrentStatement } from "@/context/CurrentStatementContext";
import { useReport } from "@/hooks/useReport";

export default function Dashboard() {
  const { statementId } = useCurrentStatement();

  const {
    data: report,
    isLoading,
    isError,
  } = useReport(statementId ?? "");

  if (!statementId) {
    return (
      <main className="flex-1 bg-[#09090B] flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-white">
            No statement selected
          </h2>

          <p className="mt-2 text-zinc-400">
            Upload and analyze a bank statement to continue.
          </p>
        </div>
      </main>
    );
  }

  if (isLoading) {
    return (
      <main className="flex-1 bg-[#09090B] flex items-center justify-center text-white">
        Loading dashboard...
      </main>
    );
  }

  if (isError || !report) {
    return (
      <main className="flex-1 bg-[#09090B] flex items-center justify-center text-red-400">
        Failed to load dashboard.
      </main>
    );
  }

  const kpis = report.kpis;
  const vm = createReportViewModel(report);

  return (
    <main className="flex-1 bg-[#09090B] p-1">
      <Hero report={vm} />

      <div className="mt-8 grid gap-6 md:grid-cols-2 xl:grid-cols-4">

        <StatCard
          title="Income"
          value={`₹${kpis.income.toLocaleString("en-IN", {
            maximumFractionDigits: 2,
          })}`}
          subtitle="Total Income"
          color="emerald"
        />

        <StatCard
          title="Expenses"
          value={`₹${kpis.expense.toLocaleString("en-IN", {
            maximumFractionDigits: 2,
          })}`}
          subtitle="Total Expenses"
          color="rose"
        />

        <StatCard
          title="Net Cash Flow"
          value={`₹${kpis.net_cash_flow.toLocaleString("en-IN", {
            maximumFractionDigits: 2,
          })}`}
          subtitle={
            kpis.net_cash_flow >= 0
              ? "Cash Surplus"
              : "Cash Deficit"
          }
          color="cyan"
        />

        <StatCard
          title="Average Debit"
          value={`₹${kpis.average_debit.toLocaleString("en-IN", {
            maximumFractionDigits: 2,
          })}`}
          subtitle="Per debit transaction"
          color="violet"
        />

      </div>
    </main>
  );
}