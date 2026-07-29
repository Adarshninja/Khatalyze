import Hero from "@/components/dashboard/Hero";
// import Navbar from "@/components/layout/Navbar";
import StatCard from "@/components/dashboard/StatCard";

export default function Dashboard() {
  return (
    <main className="flex-1 bg-[#09090B] p-1">
        <Hero />

        <div className="mt-8 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          <StatCard
            title="Financial Score"
            value="92"
            subtitle="+8 this month"
            color="cyan"
          />

          <StatCard
            title="Monthly Spending"
            value="₹25,000"
            subtitle="-12%"
            color="violet"
          />

          <StatCard
            title="Savings"
            value="₹620"
            subtitle="+18%"
            color="emerald"
          />

          <StatCard
            title="Risk Index"
            value="Low"
            subtitle="Healthy"
            color="rose"
          />
      </div>
    </main>
  );
}