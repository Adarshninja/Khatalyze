import api from "./axios";

export async function askQuestion(
  statementId: string,
  question: string
) {
  const { data } = await api.post(
    `/chat/${statementId}`,
    {
      question,
      top_k: 5,
    }
  );

  return data;
}
