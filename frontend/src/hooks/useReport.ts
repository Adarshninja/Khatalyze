import { useQuery } from "@tanstack/react-query";

import { getReport } from "@/api/report";
import { queryKeys } from "@/lib/queryKeys";

export function useReport(statementId: string) {
  return useQuery({
    queryKey: queryKeys.report(statementId),

    queryFn: async () => {
      const response = await getReport(statementId);
      return response.report;
    },

    enabled: !!statementId,

    staleTime: Infinity,
    gcTime: Infinity,

    refetchOnMount: false,
    refetchOnReconnect: false,
    refetchOnWindowFocus: false,
  });
}
