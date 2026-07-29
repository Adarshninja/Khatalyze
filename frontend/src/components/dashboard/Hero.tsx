import { ArrowUpRight, Sparkles, TrendingUp } from "lucide-react";
import { motion } from "motion/react";

export default function Hero() {
  return (
    <motion.section
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="relative overflow-hidden rounded-3xl border border-white/10 bg-[#111113] p-8"
    >
      {/* Background Glow */}
      <div className="absolute -right-32 -top-20 h-96 w-96 rounded-full bg-cyan-500/10 blur-[120px]" />
      <div className="absolute -left-20 bottom-0 h-72 w-72 rounded-full bg-violet-500/10 blur-[120px]" />

      <div className="relative flex flex-col justify-between gap-8 lg:flex-row">
        {/* Left */}
        <div className="max-w-2xl">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/10 px-3 py-1 text-sm text-cyan-400">
            <Sparkles size={16} />
            AI Financial Intelligence
          </div>

          <h1 className="text-5xl font-bold leading-tight text-white">
            Welcome to
            <br />
            <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-violet-400 bg-clip-text text-transparent">
              Khatalyse
            </span>
          </h1>

          <p className="mt-5 max-w-xl text-lg leading-8 text-zinc-400">
            Turn bank statements into meaningful insights using AI-powered
            analytics, spending intelligence, and conversational finance.
          </p>

          <div className="mt-8 flex gap-4">
            <button className="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 px-6 py-3 font-medium text-white transition hover:scale-105">
              Upload Statement
            </button>

            <button className="rounded-xl border border-white/10 bg-white/5 px-6 py-3 font-medium text-white transition hover:bg-white/10">
              AI Workspace
            </button>
          </div>
        </div>

        {/* Right */}
        <div className="flex w-full max-w-sm flex-col gap-4">
          <div className="rounded-2xl border border-white/10 bg-black/30 p-5 backdrop-blur-xl">
            <p className="text-sm text-zinc-400">Financial Health</p>

            <div className="mt-2 flex items-end justify-between">
              <h2 className="text-5xl font-bold text-white">92</h2>

              <div className="flex items-center gap-1 rounded-full bg-emerald-500/15 px-3 py-1 text-sm text-emerald-400">
                <TrendingUp size={16} />
                +12%
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-black/30 p-5 backdrop-blur-xl">
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">AI Summary</span>

              <ArrowUpRight className="text-cyan-400" size={18} />
            </div>

            <p className="mt-4 leading-7 text-zinc-300">
              Spending decreased by{" "}
              <span className="font-semibold text-cyan-400">12%</span> this
              month while savings increased by{" "}
              <span className="font-semibold text-emerald-400">18%</span>.
            </p>
          </div>
        </div>
      </div>
    </motion.section>
  );
}
