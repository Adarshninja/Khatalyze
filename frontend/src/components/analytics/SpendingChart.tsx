import {
  LineChart,
  Line,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";

interface SpendingPoint {
  day: string;
  amount: number;
}

interface SpendingChartProps {
  data: SpendingPoint[];
}

export default function SpendingChart({
  data,
}: SpendingChartProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">
      <h2 className="mb-6 text-lg font-semibold text-white">
        Spending Trend
      </h2>

      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data}>
          <CartesianGrid stroke="#27272a" />
          <XAxis dataKey="day" stroke="#71717a" />
          <YAxis stroke="#71717a" />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="amount"
            stroke="#22d3ee"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}