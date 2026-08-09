import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [showCursor, setShowCursor] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => setShowCursor(prev => !prev), 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-4 animate-fadeIn" style={{ fontFamily: 'Courier New, monospace' }}>
      {/* Header - VS Code Style */}
      <div className="border-2 border-[#3b82f6] p-4 bg-[#0a0e1a] rounded-sm">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <span className="text-[#3b82f6] text-xs ml-2">AI IDA Dashboard v2.0.0</span>
        </div>
        <div className="text-[#06b6d4] text-sm leading-relaxed font-mono">
          <div>Welcome back to AI IDA Control Panel!</div>
          <div className="mt-2 text-[#888] text-xs">
            <div>🤖 AI Assistant Status: <span className="text-green-500">Online</span></div>
            <div>📊 System Health: <span className="text-green-500">Optimal</span></div>
            <div>⚡ Performance: <span className="text-green-500">Peak</span></div>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Left Panel - Stats */}
        <div className="lg:col-span-1 space-y-4">
          {/* Stat Cards */}
          <div className="border-2 border-[#3b82f6] p-4 bg-[#0a0e1a] rounded-sm">
            <div className="text-[#3b82f6] text-xs mb-2 font-mono">$ Interactions</div>
            <div className="text-[#06b6d4] text-2xl font-bold font-mono">1,247</div>
            <div className="text-[#666] text-xs mt-1 font-mono">+12% this week</div>
          </div>

          <div className="border-2 border-[#06b6d4] p-4 bg-[#0a0e1a] rounded-sm">
            <div className="text-[#06b6d4] text-xs mb-2 font-mono">$ Memory Usage</div>
            <div className="text-[#3b82f6] text-2xl font-bold font-mono">2.4 GB</div>
            <div className="text-[#666] text-xs mt-1 font-mono">75% of 3.2 GB</div>
          </div>

          <div className="border-2 border-[#3b82f6] p-4 bg-[#0a0e1a] rounded-sm">
            <div className="text-[#3b82f6] text-xs mb-2 font-mono">$ Active Plugins</div>
            <div className="text-[#06b6d4] text-2xl font-bold font-mono">8</div>
            <div className="text-[#666] text-xs mt-1 font-mono">Weather, Browser, Voice...</div>
          </div>

          <div className="border-2 border-[#06b6d4] p-4 bg-[#0a0e1a] rounded-sm">
            <div className="text-[#06b6d4] text-xs mb-2 font-mono">$ Agent Status</div>
            <div className="text-[#06b6d4] text-2xl font-bold font-mono">🟢 Online</div>
            <div className="text-[#666] text-xs mt-1 font-mono">Uptime: 99.8%</div>
          </div>
        </div>

        {/* Right Panel - Activity */}
        <div className="lg:col-span-2 space-y-4">
          {/* Recent Activity */}
          <div className="border-2 border-[#3b82f6] p-4 bg-[#0a0e1a] rounded-sm">
            <div className="text-[#3b82f6] text-xs mb-3 font-mono">$ Recent Activity</div>
            <div className="space-y-2 text-[#888] text-xs font-mono">
              <div><span className="text-[#06b6d4]">1m ago</span>   Updated system config</div>
              <div><span className="text-[#06b6d4]">8m ago</span>   Processed user query</div>
              <div><span className="text-[#06b6d4]">2d ago</span>   Added new plugin</div>
              <div><span className="text-[#06b6d4]">1w ago</span>   System maintenance</div>
              <div className="text-[#666]">... /more in history</div>
            </div>
          </div>

          {/* What's New */}
          <div className="border-2 border-[#06b6d4] p-4 bg-[#0a0e1a] rounded-sm">
            <div className="text-[#06b6d4] text-xs mb-3 font-mono">$ What's new</div>
            <div className="space-y-2 text-[#888] text-xs font-mono">
              <div><span className="text-[#3b82f6]">/</span>new voice commands available</div>
              <div><span className="text-[#3b82f6]">/</span>neural network visualization improved</div>
              <div><span className="text-[#3b82f6]">/</span>streaming responses enabled</div>
              <div><span className="text-[#3b82f6]">/</span>multi-language support expanded</div>
              <div className="text-[#666]">... /help for more</div>
            </div>
          </div>
        </div>
      </div>

      {/* Terminal Input */}
      <div className="border-2 border-[#3b82f6] p-3 bg-[#0a0e1a] rounded-sm">
        <div className="space-y-3">
          <div className="text-[#888] text-xs font-mono">
            <span className="text-[#06b6d4]">&gt;</span>
            <span className="text-[#888]"> </span>
            <span className="text-[#3b82f6]">python</span>
            <span className="text-[#888]"> "run_ida_dashboard"</span>
            <span className={showCursor ? 'bg-[#3b82f6] text-[#0a0e1a]' : ''}>_</span>
          </div>
        </div>
      </div>
    </div>
  );
}
