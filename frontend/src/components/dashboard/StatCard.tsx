import { motion } from "motion/react";

type Props = {
  title: string;
  value: string;
  subtitle: string;
  color: string;
};

// const glow: Record<string, string> = {
//   cyan: "from-cyan-500/20",
//   violet: "from-violet-500/20",
//   emerald: "from-emerald-500/20",
//   rose: "from-rose-500/20",
// };


export default function StatCard({
  title,
  value,
  subtitle,
}: Props) {
  return (
    <motion.div
      whileHover={{
        y: -6,
        scale: 1.02,
      }}
      transition={{
        duration: .2,
      }}
        className={`group relative overflow-hidden rounded-3xl border border-white/10 bg-[#111113] p-6 transition-all duration-300 hover:-translate-y-1 hover:border-cyan-500/20`}
    >

      <div className="absolute right-0 top-0 h-24 w-24 rounded-full bg-cyan-500/10 blur-3xl opacity-0 transition-opacity duration-300 group-hover:opacity-100" />

      <div className="absolute -right-8 -top-8 h-24 w-24 rounded-full bg-white/5 blur-2xl"/>

      <p className="text-sm text-zinc-400">
        {title}
      </p>

      <h2 className="mt-5 text-4xl font-bold text-white">
        {value}
      </h2>

      <p className="mt-3 text-sm text-zinc-400">
        {subtitle}
      </p>

    </motion.div>
  );
}


