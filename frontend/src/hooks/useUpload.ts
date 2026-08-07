import { useMutation } from "@tanstack/react-query";
import { uploadStatement } from "@/api/upload";

export function useUpload() {
  return useMutation({
    mutationFn: ({
      file,
      password,
    }: {
      file: File;
      password?: string;
    }) => uploadStatement(file, password),
  });
}

