import api from "./axios";

export async function getAnalysis(statementId: string) {
    const { data } = await api.get(`/analysis/${statementId}`);
    return data;
}
