import Link from "next/link";
import { UserPlus } from "lucide-react";

export default function SignUpPage() {
  return (
    <div
      className="min-h-screen bg-cover bg-center"
      style={{ backgroundImage: "url('/signup-bg.jpeg')" }}
    >
      {/* Overlay */}
      <div className="min-h-screen flex items-center justify-center bg-black/30 px-4">
        
        {/* Card */}
        <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-8">
          
          {/* Header */}
          <div className="flex flex-col items-center mb-6">
            <div className="w-12 h-12 flex items-center justify-center rounded-full bg-teal-500 text-white mb-2">
              <UserPlus size={22} />
            </div>
            <h1 className="text-2xl font-bold text-gray-800">
              Create Account
            </h1>
            <p className="text-sm text-gray-500">
              Sign up to get started
            </p>
          </div>

          {/* Form */}
          <form className="space-y-4">
            
            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1">
                Full Name
              </label>
              <input
                type="text"
                placeholder="John Doe"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1">
                Email
              </label>
              <input
                type="email"
                placeholder="you@example.com"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1">
                Password
              </label>
              <input
                type="password"
                placeholder="••••••••"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1">
                Confirm Password
              </label>
              <input
                type="password"
                placeholder="••••••••"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-teal-500 hover:bg-teal-600 text-white font-medium py-2 rounded-lg transition"
            >
              Sign Up
            </button>
          </form>

          {/* Footer */}
          <p className="text-center text-sm text-gray-500 mt-6">
            Already have an account?{" "}
            <Link
              href="/login"
              className="text-teal-600 font-medium hover:underline"
            >
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
