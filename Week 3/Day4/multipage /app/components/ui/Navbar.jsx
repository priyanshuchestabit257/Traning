"use client";

import { usePathname } from "next/navigation";
import { Search, User, Settings, Bell } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();
  
  // Logic to clean up URL text
  const getPageName = () => {
    const parts = pathname.split("/").filter(Boolean);
    const lastPart = parts[parts.length - 1];
    if (!lastPart || lastPart === "dashboard") return "Dashboard";
    return lastPart.charAt(0).toUpperCase() + lastPart.slice(1);
  };

  const pageTitle = getPageName();

  return (
    <nav className="sticky top-4 z-40 flex flex-col md:flex-row md:items-center justify-between gap-4 px-6 py-3 mb-6 bg-white/80 backdrop-blur-xl rounded-2xl shadow-sm border border-white/20 transition-all mx-4 mt-4">
      
      {/* Breadcrumbs */}
      <div className="flex flex-col">
        <div className="flex items-center gap-1 text-sm text-gray-500 font-medium">
          <span className="opacity-70 hover:opacity-100 cursor-pointer transition-opacity">Pages</span>
          <span className="opacity-70">/</span>
          <span>{pageTitle}</span>
        </div>
        <h1 className="text-sm font-bold mt-0.5 text-gray-800">{pageTitle}</h1>
      </div>

      {/* Right Side Controls */}
      <div className="flex items-center gap-4">
        
        {/* Search Bar */}
        <div className="flex items-center border border-gray-200 rounded-2xl px-3 py-2 bg-white focus-within:ring-2 focus-within:ring-teal-400 transition-all shadow-sm">
           <Search size={14} className="text-gray-500 mr-2"/>
           <input 
             type="text" 
             placeholder="Type here..." 
             className="bg-transparent text-xs outline-none w-32 placeholder-gray-400 text-gray-700" 
           />
        </div>

        {/* Icons */}
        <div className="flex items-center gap-4 text-gray-500">
          <button className="flex items-center gap-1 hover:text-teal-500 transition font-bold text-xs">
            <User size={16} /> 
            <span className="hidden md:block">Sign In</span>
          </button>
          <button className="hover:text-teal-500 transition"><Settings size={16} /></button>
          <button className="hover:text-teal-500 transition"><Bell size={16} /></button>
        </div>
      </div>
    </nav>
  );
}