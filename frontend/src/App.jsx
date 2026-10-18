import React, { useState } from 'react';
import { MessageSquare, Send, ShieldAlert, UserCheck, Search, Filter, BotMessageSquare, Sparkles } from 'lucide-react';

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'System Initialized. Awaiting proprietary context query.',
      sources: []
    }
  ]);
  const [input, setInput] = useState('');
  const [userRole, setUserRole] = useState('employee');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userQuery = input;
    const userMessage = { role: 'user', content: userQuery, sources: [] };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: userQuery,
          user_role: userRole,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server Exception: ${response.status}`);
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `⚠️ API Exception: ${err.message}. Backend offline.`,
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-black text-slate-200 antialiased" style={{ fontFamily: '"Inter", sans-serif' }}>
      {/* Human-designed Sidebar: Ultra-minimal */}
      <div className="w-72 bg-[#111111] border-r border-[#222222] flex flex-col justify-between p-6">
        <div>
          {/* Custom Branding Detail */}
          <div className="flex items-center space-x-3 mb-12">
            <div className="bg-[#222222] p-2.5 rounded-xl border border-[#333333]">
              <Filter className="w-6 h-6 text-emerald-400" />
            </div>
            <div>
              <h1 className="text-xl font-medium text-white tracking-tight">Kore_RAG</h1>
              <p className="text-[13px] text-slate-500 font-light">Authenticated Knowledge Access</p>
            </div>
          </div>

          {/* New Chat Button: Subtle & Architectural */}
          <button 
            onClick={() => setMessages([{ role: 'assistant', content: 'New context session initialized.', sources: [] }])}
            className="w-full bg-[#181818] border border-[#333333] hover:border-emerald-500/40 text-slate-200 text-sm font-medium py-3 px-5 rounded-2xl flex items-center justify-between transition-all"
          >
            <span>Initialize Session</span>
            <span className="text-xl font-extralight text-emerald-400">+</span>
          </button>

          {/* Role Controls: High contrast & Custom */}
          <div className="mt-12 space-y-4">
            <div className="flex items-center justify-between">
                <label className="text-xs font-semibold text-slate-500 uppercase tracking-widest block flex items-center space-x-1.5">
                  <ShieldAlert className="w-4 h-4 text-emerald-500" />
                  <span>Access Level</span>
                </label>
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-lg shadow-emerald-500/20"></div>
            </div>
            <select
              value={userRole}
              onChange={(e) => setUserRole(e.target.value)}
              className="w-full bg-[#181818] border border-[#333333] text-slate-100 text-sm rounded-xl p-3.5 focus:ring-1 focus:ring-emerald-500 focus:outline-none appearance-none font-medium"
              style={{ backgroundImage: "url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22%23475569%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpolyline%20points%3D%226%209%2012%2015%2018%209%22%3E%3C%2Fpolyline%3E%3C%2Fsvg%3E')", backgroundRepeat: 'no-repeat', backgroundPosition: 'right 1rem center', backgroundSize: '1em' }}
            >
              <option value="employee">Employee (Level 1)</option>
              <option value="hr">HR Specialist (Level 3)</option>
              <option value="finance">Finance Team (Level 3)</option>
              <option value="admin">Administrator (Level 5)</option>
            </select>
            <p className="text-[12px] text-slate-600 font-light px-1">
              Determines cryptographic access to indexed vector space.
            </p>
          </div>
        </div>

        {/* Sidebar Footer: Clean & Brutalist */}
        <div className="text-[12px] text-slate-700 border-t border-[#222222] pt-4 font-light">
          Kore Enterprise AI • RAG_v1.0.3
        </div>
      </div>

      {/* Main Workspace: Clean & Focused */}
      <div className="flex-1 flex flex-col h-full bg-black">
        <header className="h-20 border-b border-[#222222] flex items-center justify-between px-8 bg-black/80 backdrop-blur-sm z-10">
          <div className="flex items-center space-x-3">
            <UserCheck className="w-5 h-5 text-emerald-500" />
            <span className="text-sm font-light text-slate-400">Authenticated:</span>
            <span className="text-sm font-semibold text-white uppercase tracking-wider">
              {userRole}
            </span>
          </div>
          <div className="text-xs text-slate-600 font-light">
            PDA College • Architecture Assessment
          </div>
        </header>

        {/* Chat History: Custom Bubble Design */}
        <div className="flex-1 overflow-y-auto p-6 md:p-10 space-y-10">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex items-start max-w-4xl mx-auto ${
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {/* Message Bubble: Asymmetric & Grounded */}
              <div
                className={`p-6 text-sm leading-relaxed max-w-[85%] font-grotesque ${
                  msg.role === 'user'
                    ? 'bg-[#181818] text-white rounded-3xl rounded-br-lg border border-[#333333]'
                    : 'bg-[#111111] text-slate-200 rounded-3xl rounded-bl-lg border border-[#222222]'
                }`}
                style={{ fontFamily: '"SF Pro Text", sans-serif' }}
              >
                <div className="flex items-center space-x-2.5 mb-3 text-xs text-slate-500">
                    {msg.role === 'user' ? <UserCheck className="w-4 h-4 text-emerald-500" /> : <BotMessageSquare className="w-4 h-4" />}
                    <span className='font-light tracking-wide'>{msg.role === 'user' ? 'AUTHENTICATED USER' : 'KORE KNOWLEDGE ASSISTANT'}</span>
                </div>
                
                <p className="whitespace-pre-wrap">{msg.content}</p>

                {/* Citations: Minimalist List */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-5 pt-4 border-t border-[#222222] space-y-1.5">
                    <span className="text-xs text-slate-600 flex items-center space-x-1.5 font-light">
                      <Search className="w-3.5 h-3.5" />
                      <span>Context Sources:</span>
                    </span>
                    {msg.sources.map((src, sIdx) => (
                      <span
                        key={sIdx}
                        className="block text-xs text-emerald-400 font-medium hover:text-emerald-300 transition cursor-default"
                        title={`Department: ${src.department}`}
                      >
                        » {src.title || src.id}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-start max-w-4xl mx-auto justify-start">
              <div className="p-6 rounded-3xl rounded-bl-lg bg-[#111111] text-slate-400 border border-[#222222] text-sm font-light">
                <Sparkles className="w-4 h-4 animate-spin text-emerald-500 inline mr-2" />
                Querying context & generating grounded response...
              </div>
            </div>
          )}
        </div>

        {/* Message Input: Seamless Integration */}
        <div className="p-6 md:p-8 bg-black">
          <form onSubmit={handleSend} className="max-w-4xl mx-auto relative flex items-center group">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Query enterprise knowledge base (Level 1 policies, claims)..."
              className="w-full bg-[#111111] border border-[#222222] text-slate-100 placeholder-slate-700 text-sm rounded-2xl py-4.5 pl-5 pr-16 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 group-hover:border-[#333333] transition-all font-light"
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="absolute right-3.5 bg-[#181818] border border-[#333333] hover:border-emerald-500 hover:text-emerald-500 disabled:opacity-40 text-slate-500 p-3 rounded-xl transition-all"
            >
              <Send className="w-4.5 h-4.5" />
            </button>
          </form>
          <div className="text-center mt-3">
            <p className="text-[11px] text-slate-700 font-extralight tracking-wider">
              KORE Proprietary RAG • Role-Based Access Enforcement Enabled
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
