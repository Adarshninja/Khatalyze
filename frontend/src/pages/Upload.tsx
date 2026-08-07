import { useRef, useState } from "react";
import { UploadCloud, FileText, Trash2, Loader2 } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { uploadStatement } from "@/api/upload";
import { analyzeStatement } from "@/api/analysis";
import { useCurrentStatement } from "@/context/CurrentStatementContext";

export default function Upload() {
  const navigate = useNavigate();
  const { setStatementId } = useCurrentStatement();

  const inputRef = useRef<HTMLInputElement>(null);

  const [file, setFile] = useState<File | null>(null);
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const openPicker = () => inputRef.current?.click();

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];

    if (!selected) return;

    setFile(selected);
    setError("");
  };

  const removeFile = () => {
    setFile(null);
    setPassword("");
    setError("");

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please choose a PDF first.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      // Upload PDF
      const upload = await uploadStatement(file, password || undefined);
      const statementId = upload.data.statement_id;

      // Save globally so every page can use it
      setStatementId(statementId);

      // Run analysis once
      await analyzeStatement(statementId);

      // Navigate to dashboard
      navigate(`/analysis/${statementId}`);
    } catch (err: any) {
      console.error(err);

      setError(
        err?.response?.data?.detail ||
          err?.response?.data?.message ||
          "Upload or analysis failed."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 bg-[#09090B] p-10">
      <h1 className="text-4xl font-bold text-white">
        Upload Statement
      </h1>

      <p className="mt-2 text-zinc-400">
        Upload a bank statement and let Khatalyse analyze it using AI.
      </p>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        className="hidden"
        onChange={handleFile}
      />

      {!file ? (
        <div className="mt-10 rounded-3xl border-2 border-dashed border-cyan-500/30 bg-white/2 p-16 text-center">
          <UploadCloud
            className="mx-auto text-cyan-400"
            size={48}
          />

          <h2 className="mt-6 text-2xl font-semibold text-white">
            Choose PDF
          </h2>

          <p className="mt-2 text-zinc-400">
            Select your bank statement PDF.
          </p>

          <button
            onClick={openPicker}
            className="mt-8 rounded-xl bg-cyan-500 px-8 py-3 font-medium text-white transition hover:bg-cyan-600"
          >
            Choose PDF
          </button>
        </div>
      ) : (
        <div className="mt-10 rounded-3xl border border-zinc-800 bg-zinc-900 p-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <FileText
                className="text-cyan-400"
                size={42}
              />

              <div>
                <p className="font-semibold text-white">
                  {file.name}
                </p>

                <p className="text-sm text-zinc-400">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>

            <button
              onClick={removeFile}
              className="rounded-lg p-2 transition hover:bg-zinc-800"
            >
              <Trash2 className="text-red-400" />
            </button>
          </div>

          <div className="mt-8">
            <label className="mb-2 block text-sm text-zinc-300">
              PDF Password (leave empty if not protected)
            </label>

            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-white outline-none focus:border-cyan-500"
            />
          </div>

          {error && (
            <p className="mt-4 text-sm text-red-400">
              {error}
            </p>
          )}

          <div className="mt-8 flex gap-4">
            <button
              onClick={handleUpload}
              disabled={loading}
              className="flex items-center gap-2 rounded-xl bg-cyan-500 px-6 py-3 font-medium text-white transition disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading && (
                <Loader2 className="h-4 w-4 animate-spin" />
              )}

              {loading ? "Processing..." : "Upload & Analyze"}
            </button>

            <button
              onClick={() => navigate("/")}
              disabled={loading}
              className="rounded-xl border border-zinc-700 px-6 py-3 text-white transition hover:bg-zinc-800"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
