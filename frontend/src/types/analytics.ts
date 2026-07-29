export interface Metric {
  title: string;
  value: string | number;
  change: string;
  trend: "up" | "down" | "neutral";
}

export interface SpendingPoint {
  day: string;
  amount: number;
}

export interface CategoryItem {
  name: string;
  value: number;
}

export interface Insight {
  id: number;
  type: "success" | "warning" | "info";
  message: string;
}

export interface Recommendation {
  id: number;
  title: string;
  description: string;
}

export interface Transaction {
  id: number;
  merchant: string;
  category: string;
  date: string;
  amount: number;
  type: "credit" | "debit";
}

export interface AnalyticsResponse {
  financialScore: number;

  metrics: Metric[];

  spendingTrend: SpendingPoint[];

  categoryBreakdown: CategoryItem[];

  insights: Insight[];

  recommendations: Recommendation[];

  transactions: Transaction[];
}

