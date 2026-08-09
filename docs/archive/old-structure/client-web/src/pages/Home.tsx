import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import { getLoginUrl } from "@/const";
import { Streamdown } from 'streamdown';

/**
 * All content in this page are only for example, replace with your own feature implementation
 * When building pages, remember your instructions in Frontend Workflow, Frontend Best Practices, Design Guide and Common Pitfalls
 */
export default function Home() {
  // The userAuth hooks provides authentication state
  // To implement login/logout functionality, simply call logout() or redirect to getLoginUrl()
  let { user, loading, error, isAuthenticated, logout } = useAuth();

  // If theme is switchable in App.tsx, we can implement theme toggling like this:
  // const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-950 to-black">
      <header className="border-b border-cyan-500/20 bg-black/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-cyan-400">AI IDA</h1>
          {isAuthenticated && (
            <Button onClick={logout} variant="outline">
              Logout
            </Button>
          )}
        </div>
      </header>
      <main className="flex-1 flex items-center justify-center p-6">
        {loading ? (
          <Loader2 className="animate-spin text-cyan-400" size={48} />
        ) : isAuthenticated ? (
          <div className="text-center space-y-4">
            <h2 className="text-3xl font-bold text-white">Welcome, {user?.name}!</h2>
            <p className="text-gray-400">Navigate to Dashboard to get started</p>
          </div>
        ) : (
          <div className="text-center space-y-6">
            <h2 className="text-4xl font-bold text-cyan-400">AI IDA</h2>
            <p className="text-xl text-gray-300 max-w-md">Your Personal AI Assistant</p>
            <Button onClick={() => window.location.href = getLoginUrl()} size="lg" className="bg-cyan-600 hover:bg-cyan-700">
              Sign In
            </Button>
          </div>
        )}
      </main>
    </div>
  );
}
