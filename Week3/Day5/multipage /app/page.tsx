import Link from "next/link";
import { ArrowRight, Zap, Star, BarChart3, Users, Settings } from "lucide-react";
import Button from "./components/ui/Button";
import Card from "./components/ui/Card";

export const metadata = {
  title: "Purity UI Dashboard",
  description: "Clean and professional dashboard built with Next.js",
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">

      {/* NAVBAR */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-gray-900">
            <div className="w-8 h-8 bg-teal-500 rounded-md flex items-center justify-center text-white">
              <Zap size={16} />
            </div>
            Purity UI
          </div>

          <div className="flex items-center gap-6 text-sm font-medium">
            <Link href="/login">Sign In</Link>
            <Link href="/signup">Sign Up</Link>
            <Link href="/about">About</Link>
            <Link href="/dashboard">
              <Button>Dashboard</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* HERO SECTION */}
      <section
        className="h-[380px] bg-cover bg-center flex items-center"
        style={{ backgroundImage: "url('/signup-bg.jpeg')" }}
      >
        <div className="max-w-7xl mx-auto px-6 text-black">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Build Better Dashboards
          </h1>
          <p className="max-w-xl text-white/90 mb-6">
            A clean and scalable dashboard template using Next.js and Tailwind CSS.
          </p>

          <Link href="/dashboard">
            <Button className=" text-gray-900 hover:bg-gray-100">
              Get Started <ArrowRight size={18} className="ml-2" />
            </Button>
          </Link>
        </div>
      </section>

      {/* STATS / FEATURES */}
      <section className="max-w-7xl mx-auto px-6 ">
        <div className="grid gap-6 md:grid-cols-3">
          <StatCard
            icon={<BarChart3 size={20} />}
            title="Analytics"
            value="Real-time data insights"
          />
          <StatCard
            icon={<Users size={20} />}
            title="Users"
            value="Manage users easily"
          />
          <StatCard
            icon={<Settings size={20} />}
            title="Settings"
            value="Customizable configuration"
          />
        </div>
      </section>

      {/* CONTENT */}
      <section className="max-w-7xl mx-auto px-6 py-24 grid gap-6 md:grid-cols-3">
        <Card className="p-6">
          <h3 className="font-semibold text-lg mb-2">Fast Development</h3>
          <p className="text-sm text-gray-600">
            Prebuilt components help you ship faster.
          </p>
        </Card>

        <Card className="p-6">
          <h3 className="font-semibold text-lg mb-2">Responsive Layout</h3>
          <p className="text-sm text-gray-600">
            Optimized for all screen sizes.
          </p>
        </Card>

        <Card className="p-6">
          <h3 className="font-semibold text-lg mb-2">Maintainable Code</h3>
          <p className="text-sm text-gray-600">
            Clean structure that’s easy to scale.
          </p>
        </Card>
      </section>

      {/* TESTIMONIAL */}
      <section className="max-w-4xl mx-auto px-6 pb-24">
        <Card className="p-8 text-center">
          <div className="flex justify-center gap-1 mb-4">
            {[1,2,3,4,5].map(i => (
              <Star key={i} size={18} className="text-yellow-400" fill="currentColor" />
            ))}
          </div>

          <p className="italic text-gray-700 mb-3">
            “This dashboard is simple, clean, and easy to extend.”
          </p>
          <p className="font-medium text-gray-900">
            — Alex Johnson
          </p>
        </Card>
      </section>

      {/* FOOTER */}
      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500 gap-4">
          <p>© 2024 Purity UI</p>
          <div className="flex gap-6">
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
            <a href="#">Support</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

/* STAT CARD COMPONENT */
type StatCardProps = {
  icon: React.ReactNode;
  title: string;
  value: string;
};

function StatCard({ icon, title, value }: StatCardProps) { {
  return (
    <Card className="p-6 flex items-center gap-4">
      <div className="w-10 h-10 bg-teal-50 text-teal-600 rounded-md flex items-center justify-center">
        {icon}
      </div>
      <div>
        <h4 className="font-semibold text-gray-900">{title}</h4>
        <p className="text-sm text-gray-600">{value}</p>
      </div>
    </Card>
  );
}}
