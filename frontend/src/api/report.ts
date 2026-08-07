import api from "./axios";
import type { AnalyzeResponse } from "@/types/report";

export async function getReport(
  statementId: string
): Promise<AnalyzeResponse> {
  const { data } = await api.get<AnalyzeResponse>(
    `/report/${statementId}`
  );

  return data;
}