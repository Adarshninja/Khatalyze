import { ArrowUpRight, Sparkles } from "lucide-react";
import { motion } from "motion/react";
import { useNavigate } from "react-router-dom";

import type { ReportViewModel } from "@/services/reportAdapter";

type HeroProps = {
  report: ReportViewModel;
};

export default function Hero({ report }: HeroProps) {
  const navigate = useNavigate();

  const firstInsight =
    report.insights.length > 0
      ? report.insights[0]
      : "Statement analyzed successfully.";

  const isPositive = report.kpis.net_cash_flow >= 0;

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
            Statement
            <br />
            <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-violet-400 bg-clip-text text-transparent">
              Analyzed Successfully
            </span>
          </h1>

          <p className="mt-5 max-w-xl text-lg leading-8 text-zinc-400">
            Your financial report has been generated successfully. Explore
            spending insights, cash flow trends, AI recommendations, and ask
            questions about your statement using Khatalyse AI.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <button
              onClick={() => navigate("/analysis")}
              className="rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 px-6 py-3 font-medium text-white transition-all hover:scale-105 hover:shadow-lg hover:shadow-cyan-500/30"
            >
              View Analytics
            </button>

            <button
              onClick={() => navigate("/chat")}
              className="rounded-xl border border-white/10 bg-white/5 px-6 py-3 font-medium text-white transition-all hover:bg-white/10"
            >
              AI Workspace
            </button>
          </div>
        </div>

        {/* Right */}
        <div className="flex w-full max-w-sm flex-col gap-4">
          <div className="rounded-2xl border border-white/10 bg-black/30 p-5 backdrop-blur-xl">
            <p className="text-sm text-zinc-400">Net Cash Flow</p>

            <div className="mt-3">
              <h2 className="text-4xl font-bold text-white">
                ₹
                {report.kpis.net_cash_flow.toLocaleString("en-IN", {
                  maximumFractionDigits: 2,
                })}
              </h2>

              <div
                className={`mt-3 inline-flex rounded-full px-3 py-1 text-sm ${
                  isPositive
                    ? "bg-emerald-500/15 text-emerald-400"
                    : "bg-rose-500/15 text-rose-400"
                }`}
              >
                {isPositive ? "Cash Surplus" : "Cash Deficit"}
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-black/30 p-5 backdrop-blur-xl">
            <div className="flex items-center justify-between">
              <span className="text-zinc-400">AI Summary</span>

              <ArrowUpRight
                className="text-cyan-400"
                size={18}
              />
            </div>

            <p className="mt-4 leading-7 text-zinc-300">
              {firstInsight}
            </p>
          </div>
        </div>
      </div>
    </motion.section>
  );
}