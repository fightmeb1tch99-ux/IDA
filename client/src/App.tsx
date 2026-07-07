import { Toaster } from "@/components/ui/sonner";
 import DashboardLayout from "@/components/DashboardLayout";
 import { TooltipProvider } from "@/components/ui/tooltip";
 import NotFound from "@/pages/NotFound";
 import { Route, Switch } from "wouter";
 import ErrorBoundary from "./components/ErrorBoundary";
 import { ThemeProvider } from "./contexts/ThemeContext";
 import Home from "./pages/Home";
 import Dashboard from "./pages/Dashboard";
 import Chat from "./pages/Chat";
 import History from "./pages/History";
 import Plugins from "./pages/Plugins";
 import Settings from "./pages/Settings";
import NeuralNetwork from "./pages/NeuralNetwork";
import VoiceVisualizer from "./components/VoiceVisualizer";
import Login from "./pages/Login";
 
 function Router() {
   // IDA Dashboard with DashboardLayout
   return (
     <Switch>
       <Route path={"/login"} component={Login} />
       <Route path={"/"} component={Home} />
       <Route path={"/dashboard"}>
         {() => (
           <DashboardLayout>
             <Dashboard />
           </DashboardLayout>
         )}
       </Route>
       <Route path={"/chat"}>
         {() => (
           <DashboardLayout>
             <Chat />
           </DashboardLayout>
         )}
       </Route>
       <Route path={"/history"}>
         {() => (
           <DashboardLayout>
             <History />
           </DashboardLayout>
         )}
       </Route>
       <Route path={"/plugins"}>
         {() => (
           <DashboardLayout>
             <Plugins />
           </DashboardLayout>
         )}
       </Route>
       <Route path={"/settings"}>
        {() => (
          <DashboardLayout>
            <Settings />
          </DashboardLayout>
        )}
      </Route>
      <Route path={"/neural"}>
        {() => (
          <DashboardLayout>
            <NeuralNetwork />
          </DashboardLayout>
        )}
      </Route>
      <Route path={"/voice"}>
        {() => (
          <DashboardLayout>
            <VoiceVisualizer />
          </DashboardLayout>
        )}
      </Route>
      <Route path={"/"} component={Home} />
      <Route path={"/404"} component={NotFound} />
       {/* Final fallback route */}
       <Route component={NotFound} />
     </Switch>
   );
 }

// NOTE: About Theme
// - First choose a default theme according to your design style (dark or light bg), than change color palette in index.css
//   to keep consistent foreground/background color across components
// - If you want to make theme switchable, pass `switchable` ThemeProvider and use `useTheme` hook

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider
        defaultTheme="light"
        // switchable
      >
        <TooltipProvider>
          <Toaster />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
