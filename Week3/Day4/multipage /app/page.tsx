import Link from "next/link";
import { ArrowRight, CheckCircle, Zap, Shield, Layout, Star } from "lucide-react";
import Button from "./components/ui/Button"; // Using your custom Button
import Card from "./components/ui/Card";     // Using your custom Card

// 1. SEO METADATA (Day 4 Requirement)
export const metadata = {
  title: "Purity UI - The Future of Dashboards",
  description: "A modern, fast, and responsive dashboard template built with Next.js and Tailwind CSS.",
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white text-gray-800 font-sans">
      
      {/* --- NAVBAR --- */}
      <nav className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto sticky top-0 bg-white/80 backdrop-blur-md z-50">
        <div className="flex items-center gap-2 font-bold text-xl tracking-tight text-gray-900">
          <div className="w-8 h-8 bg-teal-400 rounded-lg flex items-center justify-center text-white shadow-teal-200 shadow-lg">
            <Zap size={18} fill="currentColor" />
          </div>
          Purity UI
        </div>
        <div className="flex items-center gap-4">
          <Link href="/dashboard/signin" className="text-sm font-bold text-gray-500 hover:text-gray-900 hidden sm:block transition-colors">
            Sign In
          </Link>
          <Link href="/dashboard">
            {/* Using your custom Button component */}
            <Button className="shadow-xl hover:scale-105 transition-transform">
              Go to Dashboard
            </Button>
          </Link>
        </div>
      </nav>

      {/* --- HERO SECTION --- */}
      <section className="px-6 pt-16 pb-24 md:pt-28 md:pb-32 max-w-7xl mx-auto text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 text-teal-600 text-xs font-bold uppercase tracking-wide mb-6 border border-teal-100">
          <span className="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
          v1.0 is now live
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-gray-900 mb-6 max-w-4xl mx-auto leading-[1.1]">
          Build faster with <br className="hidden md:block" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-teal-600">
            intelligent dashboards.
          </span>
        </h1>
        
        <p className="text-lg md:text-xl text-gray-500 mb-10 max-w-2xl mx-auto leading-relaxed">
          Don't waste time building layouts from scratch. Purity UI gives you a production-ready, 
          accessible, and responsive foundation for your next big idea.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
           <Link href="/dashboard">
             <Button className="h-14 px-8 text-lg shadow-teal-300/50 shadow-xl hover:-translate-y-1">
               Get Started Now <ArrowRight size={20} className="ml-2" />
             </Button>
           </Link>
           <button className="px-8 py-4 bg-white text-gray-700 font-bold rounded-xl border border-gray-100 hover:bg-gray-50 transition-all shadow-sm">
             View Documentation
           </button>
        </div>
      </section>


     {/* --- TESTIMONIALS (Fixed Gradient UI) --- */}
      <section className="py-24 px-6 max-w-7xl mx-auto">
        <Card className="bg-[#0f172a] text-white border-none p-10 md:p-20 text-center relative overflow-hidden shadow-2xl ring-1 ring-white/10">
          
          {/* 1. The Main Gradient (Stronger & Visible) */}
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-teal-600/40 via-[#0f172a] to-transparent pointer-events-none z-0" />
          
          {/* 2. The Glow Blob (Adds the 'Premium' feel) */}
          <div className="absolute -top-20 -left-20 w-72 h-72 bg-teal-500/30 rounded-full blur-[100px] pointer-events-none z-0" />
          
          {/* Content */}
          <div className="relative z-10 max-w-4xl mx-auto">
             
             {/* Stars */}
             <div className="flex justify-center mb-8 gap-1.5">
               {[1,2,3,4,5].map(i => (
                 <Star key={i} size={20} fill="#fbbf24" className="text-amber-400 drop-shadow-md" />
               ))}
             </div>

             {/* Quote */}
             <h3 className="text-2xl md:text-4xl font-bold mb-10 leading-snug tracking-tight text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-400">
               "This template saved me weeks of work. The code structure is clean, 
               and the design is simply stunning."
             </h3>

             {/* User Info */}
             <div className="flex flex-col items-center">
               <div className="w-14 h-14 bg-gradient-to-tr from-gray-700 to-gray-600 rounded-full mb-4 p-1 border border-teal-500/50 shadow-lg">
                  {/* Placeholder Avatar */}
                  <div className="w-full h-full bg-gray-800 rounded-full flex items-center justify-center text-xs text-gray-400 font-bold">
                    AJ
                  </div>
               </div>
               <p className="font-bold text-lg text-white">Alex Johnson</p>
               <p className="text-teal-400 text-sm font-medium tracking-wide uppercase">Full Stack Developer</p>
             </div>
          </div>
        </Card>
      </section>

      {/* --- FOOTER --- */}
      <footer className="bg-white border-t border-gray-100 py-12 px-6">
         <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-2 font-bold text-gray-900">
               <div className="w-6 h-6 bg-teal-400 rounded-md flex items-center justify-center text-white">
                  <Zap size={14} fill="currentColor" />
               </div>
               Purity UI
            </div>
            <p className="text-gray-400 text-sm">
              © 2024 Purity UI Dashboard. All rights reserved.
            </p>
            <div className="flex gap-6 text-gray-500 text-sm font-medium">
              <a href="#" className="hover:text-teal-400 transition">Privacy</a>
              <a href="#" className="hover:text-teal-400 transition">Terms</a>
              <a href="#" className="hover:text-teal-400 transition">Twitter</a>
            </div>
         </div>
      </footer>
    </div>
  );
}

// Helper Component for Features (Reusing your custom Card)
function FeatureCard({ icon, title, desc }: { icon: React.ReactNode, title: string, desc: string }) {
  return (
    <Card className="p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group cursor-pointer border border-gray-100">
      <div className="w-12 h-12 bg-teal-50 text-teal-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-gray-900 mb-3">{title}</h3>
      <p className="text-gray-500 leading-relaxed text-sm">
        {desc}
      </p>
    </Card>
  );
} 