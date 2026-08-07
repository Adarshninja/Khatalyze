import api from "./axios";
import type { AnalyzeResponse } from "@/types/report";

export async function analyzeStatement(
  statementId: string
): Promise<AnalyzeResponse> {
  const { data } = await api.post<AnalyzeResponse>(
    `/analyze/${statementId}`
  );

  return data;
}
