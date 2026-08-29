export interface Account {
  account_holder: string;
  account_number: string;
  bank: string;
  branch: string;
  ifsc: string;
  micr: string;
  customer_id: string;

  statement_start: string | null;
  statement_end: string | null;
  statement_generated_on: string | null;

  opening_balance: number;
  closing_balance: number;

  currency: string;
  account_type: string;
  mode_of_operation: string;

  metadata: Record<string, unknown>;
}

export interface Transaction {
  transaction_id: string;

  date: string;

  description: string;
  party: string;

  amount: number;
  balance: number;

  transaction_type: "DEBIT" | "CREDIT";

  category: string;

  payment_mode: string;

  bank: string;

  currency: string;

  reference_number: string;
  cheque_number: string;
  branch: string;

  remarks: string;

  confidence: number;

  tags: string[];

  metadata: Record<string, unknown>;
}

export interface Recommendation {
  priority: string;
  title: string;
  reason: string;
  recommended_action: string;
}

export interface FinancialReport {

  report_id: string;

  created_at: string;

  version: string;

  account: Account;

  transactions: Transaction[];

  kpis: Record<string, any>;

  category_analysis: Record<string, any>;

  merchant_statistics: Record<string, any>;

  cashflow_analysis: Record<string, any>;

  monthly_summary: Record<string, any>;

  behavioural_insights: Record<string, any>;

  recurring_transactions: any[];

  anomaly_detection: Record<string, any>;

  insights: {
  spending_insights: string[];
  category_insights: string[];
  merchant_insights: string[];
  cashflow_insights: string[];
  behaviour_insights: string[];
  monthly_insights: string[];
  risk_insights: string[];
};

  risks: any[];

  recommendations: Recommendation[];

  financial_health_score: number;

  financial_health_status: string;

  embeddings_generated: boolean;

  vector_ids: string[];

  metadata: Record<string, any>;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  data: {
    statement_id: string;
    status: string;
    pdf: string;
    metadata: string;
  };
}

export interface AnalyzeResponse {
  status: string;
  statement_id: string;
  message: string;
  report: FinancialReport;
}

export interface ChatRequest {
  question: string;
  top_k?: number;
}

export interface ChatResponse {
  status: string;
  statement_id: string;
  question: string;
  answer: string;
  route: string;
  context: string | null;
}