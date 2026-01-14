import Input from '../components/ui/Input'
import Button from '../components/ui/Button'



export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-8">
        
        {/* Heading */}
        <h1 className="text-2xl font-bold text-gray-900 mb-2 text-center">
          Welcome Back
        </h1>
        <p className="text-gray-500 text-sm text-center mb-6">
          Please sign in to your account
        </p>

        {/* Form */}
        <form className="space-y-4">
          <Input
            label="Email"
            type="email"
            placeholder="you@example.com"
          />

          <Input
            label="Password"
            type="password"
            placeholder="Password@123"
          />

          <Button className="w-full">
            Sign In
          </Button>
        </form>

        {/* Footer */}
        <p className="text-xs text-gray-500 text-center mt-6">
          
        </p>
      </div>
    </div>
  );
}
