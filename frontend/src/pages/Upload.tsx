import { UploadCloud } from "lucide-react";

export default function Upload() {
  return (
    <div className="flex-1 bg-[#09090B] p-10">

      <h1 className="text-4xl font-bold text-white">
        Upload Statement
      </h1>

      <p className="mt-2 text-zinc-400">
        Upload a bank statement and let Khatalyse analyze it using AI.
      </p>

      <div className="mt-10 rounded-3xl border-2 border-dashed border-cyan-500/30 bg-white/[0.02] p-16 transition hover:border-cyan-400">

        <div className="flex flex-col items-center">

          <div className="rounded-full bg-cyan-500/10 p-6">

            <UploadCloud
              className="text-cyan-400"
              size={48}
            />

          </div>

          <h2 className="mt-6 text-2xl font-semibold text-white">
            Drag & Drop PDF
          </h2>

          <p className="mt-2 text-zinc-400">
            or click anywhere to browse
          </p>

          <button className="mt-8 rounded-xl bg-cyan-500 px-8 py-3 font-medium text-white transition hover:scale-105">
            Choose File
          </button>

        </div>

      </div>

    </div>
  );
}

