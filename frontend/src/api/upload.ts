import api from "./axios";
import type { UploadResponse } from "@/types/report";

export async function uploadStatement(
  file: File,
  password?: string
): Promise<UploadResponse> {
  const formData = new FormData();

  formData.append("file", file);

  if (password) {
    formData.append("password", password);
  }

  const { data } = await api.post<UploadResponse>(
    "/upload/",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return data;
}
