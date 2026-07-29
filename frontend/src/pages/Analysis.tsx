import { Activity, ArrowDown, ArrowUp, ShieldCheck } from "lucide-react";

import PageHeader from "@/components/common/PageHeader";
import MetricCard from "@/components/analytics/MetricCard";
import SpendingChart from "@/components/analytics/SpendingChart";
import CategoryChart from "@/components/analytics/CategoryChart";
import AIInsights from "@/components/analytics/AIInsights";
import Recommendations from "@/components/analytics/Recommendations";
import TransactionsTable from "@/components/analytics/TransactionsTable";

import { Button } from "@/components/ui/button";

import { mockAnalytics } from "@/data/mockAnalytics";

const icons = [
  <Activity size={24} />,
  <ArrowUp size={24} />,
  <ArrowDown size={24} />,
  <ShieldCheck size={24} />,
];

export default function Analysis() {
  return (
    <div className="space-y-8">
      <PageHeader
        title="Financial Analytics"
        subtitle="AI-powered insights into your financial behavior."
      >
        <Button>Export Report</Button>
      </PageHeader>

      <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-4">
        {mockAnalytics.metrics.map((metric, index) => (
          <MetricCard
            key={metric.title}
            title={metric.title}
            value={metric.value}
            change={metric.change}
            icon={icons[index]}
          />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <SpendingChart data={mockAnalytics.spendingTrend} />
        </div>

        <CategoryChart data={mockAnalytics.categoryBreakdown} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <AIInsights insights={mockAnalytics.insights} />

        <Recommendations
          recommendations={mockAnalytics.recommendations}
        />
      </div>

      <TransactionsTable
        transactions={mockAnalytics.transactions}
      />
    </div>
  );
}


