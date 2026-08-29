import type {
  FinancialReport,
  Recommendation,
} from "@/types/report";

const formatCurrency = (value: number) =>
  `₹${value.toLocaleString("en-IN", {
    maximumFractionDigits: 2,
  })}`;

export type ReportViewModel = {
  metrics: {
    title: string;
    value: string;
    change: string;
    positive: boolean;
  }[];

  spendingTrend: {
    day: string;
    amount: number;
  }[];

  categoryBreakdown: {
    name: string;
    value: number;
  }[];

  insights: string[];

  recommendations: {
    priority: string;
    title: string;
    description: string;
    action: string;
  }[];

  transactions: {
    id: string;
    date: string;
    description: string;
    category: string;
    amount: number;
    type: "DEBIT" | "CREDIT";
    merchant: string;
    paymentMode: string;
    bank: string;
  }[];

  risks: FinancialReport["risks"];

  healthScore: number;

  healthStatus: string;

  account: FinancialReport["account"];

  kpis: FinancialReport["kpis"];
};

export function createReportViewModel(
  report: FinancialReport
): ReportViewModel {
  return {
    kpis: report.kpis,

    metrics: [
      {
        title: "Income",
        value: formatCurrency(report.kpis.income ?? 0),
        change: "",
        positive: true,
      },
      {
        title: "Expenses",
        value: formatCurrency(report.kpis.expense ?? 0),
        change: "",
        positive: false,
      },
      {
        title: "Net Cash Flow",
        value: formatCurrency(report.kpis.net_cash_flow ?? 0),
        change: "",
        positive: (report.kpis.net_cash_flow ?? 0) >= 0,
      },
      {
        title: "Health Score",
        value: `${report.financial_health_score}/100`,
        change: report.financial_health_status,
        positive: report.financial_health_score >= 60,
      },
    ],

    spendingTrend: Object.entries(
  report.cashflow_analysis.daily_spending ?? {}
).map(([date, amount]) => ({
  day: date,
  amount: Number(amount),
})),

    categoryBreakdown: Object.entries(
      report.category_analysis.spending ?? {}
    ).map(([name, value]) => ({
      name,
      value: Number(value),
    })),

    insights: [
      ...(report.insights?.spending_insights ?? []),
      ...(report.insights?.category_insights ?? []),
      ...(report.insights?.merchant_insights ?? []),
      ...(report.insights?.cashflow_insights ?? []),
      ...(report.insights?.behaviour_insights ?? []),
      ...(report.insights?.monthly_insights ?? []),
      ...(report.insights?.risk_insights ?? []),
    ],

    recommendations: (report.recommendations ?? []).map(
      (r: Recommendation) => ({
        priority: r.priority,
        title: r.title,
        description: r.reason,
        action: r.recommended_action,
      })
    ),

    transactions: (report.transactions ?? []).map((t) => ({
      id: t.transaction_id,
      date: new Date(t.date).toLocaleDateString("en-IN"),
      description: t.description,
      category: t.category,
      amount: t.amount,
      type: t.transaction_type === "CREDIT" ? "CREDIT" : "DEBIT",
      merchant: t.party,
      paymentMode: t.payment_mode,
      bank: t.bank,
    })),

    risks: report.risks ?? [],

    healthScore: report.financial_health_score,

    healthStatus: report.financial_health_status,

    account: report.account,
  };
}