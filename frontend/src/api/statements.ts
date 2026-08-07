import axios from "./axios";

export interface StatementItem {
  statement_id: string;
  bank: string;
  original_filename: string;
  uploaded_at: string;
  analysis_completed: string;
  transaction_count: number;
}

interface StatementsResponse {
  status: string;
  statements: StatementItem[];
}

export async function getStatements() {
  const { data } = await axios.get<StatementsResponse>("/statements");
  return data.statements;
}

