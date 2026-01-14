"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Home, BarChart2, CreditCard, Wrench, User, FileText, Rocket, HelpCircle 
} from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();
  const isActive = (path) => pathname === path;

  return (
    <aside className="h-[calc(100vh-32px)] w-64 m-4 bg-white rounded-2xl flex flex-col shadow-xl border border-gray-100/50 fixed left-0 top-0 z-50">
      
      {/* 1. Logo Section */}
      <div className="flex items-center justify-center h-24 border-b border-gray-100 mx-6 mb-2">
        <div className="flex items-center gap-3 text-gray-800 font-bold text-sm tracking-wide">
          <div className="p-1.5 bg-teal-400 text-white rounded-lg shadow-md">
             <Rocket size={14} fill="currentColor" />
          </div>
          PURITY UI DASHBOARD
        </div>
      </div>

      {/* 2. Navigation Links */}
      <div className="px-4 flex-1 overflow-y-auto py-4">
        <ul className="flex flex-col gap-1 space-y-1">
          
          <NavItem 
            href="/dashboard" 
            icon={<Home size={15} />} 
            label="Dashboard" 
            active={isActive("/dashboard")} 
          />
          <NavItem 
            href="/tables" 
            icon={<BarChart2 size={15} />} 
            label="Tables" 
            active={isActive("/tables")} 
          />
          <NavItem 
            href="/billing" 
            icon={<CreditCard size={15} />} 
            label="Billing" 
            active={isActive("/billing")} 
          />
          <NavItem 
            href="/rtl" 
            icon={<Wrench size={15} />} 
            label="RTL" 
            active={isActive("/rtl")} 
          />

          {/* Section Header */}
          <li className="mt-6 mb-4 px-4 text-[10px] font-bold text-gray-400 uppercase tracking-wider">
            Account Pages
          </li>
          <NavItem 
            href="/dashboard/profile" 
            icon={<BarChart2 size={15} />} 
            label="profile" 
            active={isActive("/dashboard/profile")} 
          />
          <NavItem 
            href="/dashboard/signin"
            icon={<CreditCard size={15} />} 
            label="signin" 
            active={isActive("/dashboard/signin")} 
          />
          <NavItem 
            href="/dashboard/signup" 
            icon={<Wrench size={15} />} 
            label="signup" 
            active={isActive("/dashboard/signup")} 
          />
          
          
          
        </ul>
      </div>
    </aside>
  );
}

// Helper Component for Links
function NavItem({ href, icon, label, active }) {
  return (
    <li>
      <Link
        href={href}
        className={`flex items-center gap-4 px-4 py-3 rounded-xl transition-all text-xs font-bold ${
          active 
            ? "bg-white shadow-md text-gray-800" 
            : "text-gray-500 hover:bg-gray-50 hover:text-gray-900"
        }`}
      >
        <div className={`p-1.5 rounded-lg shadow-sm transition-colors ${
          active 
            ? "bg-teal-400 text-white" 
            : "bg-white text-teal-400 border border-gray-100"
        }`}>
            {icon}
        </div>
        {label}
      </Link>
    </li>
  );
}