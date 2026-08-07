import { useMutation, useQueryClient } from "@tanstack/react-query";
import { analyzeStatement } from "@/api/analysis";
import { queryKeys } from "@/lib/queryKeys";

export function useAnalysis() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: analyzeStatement,

    onSuccess: (data) => {
      queryClient.setQueryData(
        queryKeys.report(data.statement_id),
        data.report
      );
    },
  });
}
