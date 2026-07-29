import {
  LineChart,
  Line,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";

const data = [
  { day: "Mon", amount: 120 },
  { day: "Tue", amount: 210 },
  { day: "Wed", amount: 160 },
  { day: "Thu", amount: 340 },
  { day: "Fri", amount: 280 },
  { day: "Sat", amount: 500 },
  { day: "Sun", amount: 380 },
];

export default function SpendingChart() {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">
      <h2 className="mb-6 text-lg font-semibold text-white">
        Spending Trend
      </h2>

      <ResponsiveContainer
        width="100%"
        height={320}
      >
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

