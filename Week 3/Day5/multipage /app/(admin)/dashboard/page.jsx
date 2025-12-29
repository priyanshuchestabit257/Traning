import {
  Wallet,
  Users,
  UserPlus,
  ShoppingCart,
} from "lucide-react";

export default function DashboardPage() {
  const stats = [
    {
      title: "Today's Money",
      value: "$53,000",
      change: "+55%",
      icon: Wallet,
    },
    {
      title: "Today's Users",
      value: "2,300",
      change: "+5%",
      icon: Users,
    },
    {
      title: "New Clients",
      value: "+3,052",
      change: "-14%",
      icon: UserPlus,
    },
    {
      title: "Total Sales",
      value: "$173,000",
      change: "+8%",
      icon: ShoppingCart,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-semibold text-gray-800">Dashboard</h1>
        <p className="text-sm text-gray-500">
          Overview of your business
        </p>
      </div>

      {/* Stat Cards */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item, index) => {
          const Icon = item.icon;
          return (
            <div
              key={index}
              className="flex items-center justify-between rounded-xl bg-white p-4 shadow-sm"
            >
              <div>
                <p className="text-sm text-gray-500">{item.title}</p>
                <p className="text-lg font-bold text-gray-800">
                  {item.value}
                </p>
                <p
                  className={`text-xs font-semibold ${
                    item.change.startsWith("+")
                      ? "text-green-500"
                      : "text-red-500"
                  }`}
                >
                  {item.change}
                </p>
              </div>

              <div className="rounded-lg bg-teal-100 p-3 text-teal-600">
                <Icon size={20} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Middle Section */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Info Card */}
        <div className="lg:col-span-2 rounded-xl bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800">
            Built by developers
          </h2>
          <p className="mt-2 text-sm text-gray-500">
            Purity UI Dashboard is built with modern UI principles
            using Next.js and Tailwind CSS.
          </p>

          <button className="mt-4 text-sm font-semibold text-teal-600 hover:underline">
            Read more →
          </button>
        </div>

        {/* Promo Card */}
        <div className="rounded-xl bg-gradient-to-r from-teal-400 to-teal-500 p-6 text-white shadow-sm">
          <h3 className="text-lg font-semibold">chakra</h3>
          <p className="mt-2 text-sm opacity-90">
            Build modern UI faster with Chakra design system.
          </p>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Active Users */}
        <div className="lg:col-span-2 rounded-xl bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800">
            Active Users
          </h2>
          <p className="text-sm text-green-500">(+23) than last week</p>

          <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
            <StatBox label="Users" value="32,984" />
            <StatBox label="Clicks" value="2.4m" />
            <StatBox label="Sales" value="2,400$" />
            <StatBox label="Items" value="320" />
          </div>
        </div>

               {/* Orders */}  
        <div className="rounded-xl bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800">
            Orders overview
          </h2>
          <p className="text-sm text-green-500">+30% this month</p>

          <ul className="mt-4 space-y-3 text-sm text-gray-600">
            <li>🟢 $2400, Design changes</li>
            <li>🔵 New order #4219423</li>
            <li>🟣 Server payments</li>
            <li>🟠 New card added</li>
            <li>🔴 New order #9851258</li>
          </ul>
        </div>
      </div>
    </div>
  );
}


function StatBox({ label, value }) {
  return (
    <div>
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-lg font-bold text-gray-800">{value}</p>
    </div>
  );
}
