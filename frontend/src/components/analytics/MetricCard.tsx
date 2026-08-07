import type { ReactNode } from "react";
import { motion } from "motion/react";

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: string;
  icon: ReactNode;
}

export default function MetricCard({
  title,
  value,
  change,
  icon,
}: MetricCardProps) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
      className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6 backdrop-blur-xl"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-zinc-400">
            {title}
          </p>

          <h2 className="mt-2 text-3xl font-bold text-white">
            {value}
          </h2>

          {change && (
            <span className="mt-3 inline-block rounded-full bg-emerald-500/10 px-3 py-1 text-xs text-emerald-400">
              {change}
            </span>
          )}
        </div>

        <div className="rounded-xl bg-cyan-500/10 p-4 text-cyan-400">
          {icon}
        </div>
      </div>
    </motion.div>
  );
}

