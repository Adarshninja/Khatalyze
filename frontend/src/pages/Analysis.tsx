import { Activity, ArrowDown, ArrowUp, ShieldCheck } from "lucide-react";
import { useParams } from "react-router-dom";

import PageHeader from "@/components/common/PageHeader";
import MetricCard from "@/components/analytics/MetricCard";
import SpendingChart from "@/components/analytics/SpendingChart";
import CategoryChart from "@/components/analytics/CategoryChart";
import AIInsights from "@/components/analytics/AIInsights";
import Recommendations from "@/components/analytics/Recommendations";
import TransactionsTable from "@/components/analytics/TransactionsTable";

import { Button } from "@/components/ui/button";

import { useReport } from "@/hooks/useReport";
import { createReportViewModel } from "@/services/reportAdapter";

const icons = [
  <Activity size={24} />,
  <ArrowUp size={24} />,
  <ArrowDown size={24} />,
  <ShieldCheck size={24} />,
];

export default function Analysis() {
  const { statementId } = useParams<{ statementId: string }>();

  const { data: report } = useReport(statementId!);

  if (!report) {
    return (
      <div className="flex h-[60vh] items-center justify-center">
        <p className="text-zinc-400 text-lg">
          Loading Financial Report...
        </p>
      </div>
    );
  }
  
console.log(report.insights);

  const vm = createReportViewModel(report);

  return (
    <div className="space-y-8">
      <PageHeader
        title="Financial Analytics"
        subtitle="AI-powered insights into your financial behavior."
      >
        <Button>Export Report</Button>
      </PageHeader>

      {/* KPI Cards */}
      <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-4">
        {vm.metrics.map((metric, index) => (
          <MetricCard
            key={metric.title}
            {...metric}
            icon={icons[index]}
          />
        ))}
      </div>

      {/* Charts */}
      <div className="grid gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <SpendingChart data={vm.spendingTrend} />
        </div>

        <CategoryChart data={vm.categoryBreakdown} />
      </div>

      {/* AI */}
      <div className="grid gap-6 lg:grid-cols-2">
        <AIInsights insights={vm.insights} />

        <Recommendations
          recommendations={vm.recommendations}
        />
      </div>

      {/* Transactions */}
      <TransactionsTable
        transactions={vm.transactions}
      />
    </div>
  );
}