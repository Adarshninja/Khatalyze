import { useMutation } from "@tanstack/react-query";
import { askQuestion } from "@/api/chat";

export function useChat(statementId: string) {
  return useMutation({
    mutationFn: (question: string) =>
      askQuestion(statementId, question),
  });
}
