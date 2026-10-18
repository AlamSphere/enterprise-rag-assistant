import React, { useState } from 'react';
import { MessageSquare, Send, Shield, User, Database, Sparkles, Plus } from 'lucide-react';

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I am your Enterprise Knowledge Assistant. Ask me anything about company policies, HR leave guidelines, or expense claims.',
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
        throw new Error(`Server returned status ${response.status}`);
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
          content: `⚠️ API Error: ${err.message}. Ensure FastAPI is running on http://127.0.0.1:8000!`,
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Sidebar */}
      <div className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between hidden md:flex">
        <div>
          <div className="p-4 border-b border-slate-800 flex items-center space-x-3">
            <div className="bg-indigo-600 p-2 rounded-lg text-white">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h1 className="font-bold text-sm tracking-wide">Enterprise RAG</h1>
              <p className="text-xs text-slate-400">Knowledge Assistant</p>
            </div>
          </div>

          <div className="p-4">
            <button 
              onClick={() => setMessages([{ role: 'assistant', content: 'New chat started. How can I help you today?', sources: [] }])}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium py-2.5 px-4 rounded-xl flex items-center justify-center space-x-2 transition shadow-lg shadow-indigo-600/20"
            >
              <Plus className="w-4 h-4" />
              <span>New Chat</span>
            </button>
          </div>

          <div className="px-4 py-2">
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2 flex items-center space-x-1">
              <Shield className="w-3 h-3 text-indigo-400" />
              <span>Demo User Role</span>
            </label>
            <select
              value={userRole}
              onChange={(e) => setUserRole(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 text-slate-200 text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            >
              <option value="employee">Employee</option>
              <option value="hr">HR Specialist</option>
              <option value="finance">Finance Team</option>
              <option value="admin">Administrator</option>
            </select>
          </div>
        </div>

        <div className="p-4 border-t border-slate-800 text-xs text-slate-400 flex items-center justify-between">
          <span>Hugging Face + Python RAG</span>
          <span className="inline-block w-2 h-2 rounded-full bg-emerald-500"></span>
        </div>
      </div>

      {/* Main Workspace */}
      <div className="flex-1 flex flex-col h-full bg-slate-950">
        <header className="h-16 border-b border-slate-800 flex items-center justify-between px-6 bg-slate-900/50 backdrop-blur">
          <div className="flex items-center space-x-2">
            <span className="text-sm font-semibold text-slate-300">Active Role:</span>
            <span className="bg-indigo-500/10 text-indigo-400 text-xs font-medium px-2.5 py-1 rounded-full border border-indigo-500/20 uppercase tracking-wider">
              {userRole}
            </span>
          </div>
          <div className="text-xs text-slate-400">
            PDA College • AI & ML Portfolio Project
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex items-start space-x-4 max-w-3xl mx-auto ${
                msg.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-indigo-400 border border-slate-700'
                }`}
              >
                {msg.role === 'user' ? <User className="w-4 h-4" /> : <Sparkles className="w-4 h-4" />}
              </div>

              <div
                className={`p-4 rounded-2xl text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white rounded-tr-none'
                    : 'bg-slate-900 text-slate-200 border border-slate-800 rounded-tl-none shadow-sm'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>

                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-slate-800/80 flex flex-wrap gap-2">
                    <span className="text-xs text-slate-400 flex items-center space-x-1">
                      <Database className="w-3 h-3 text-indigo-400" />
                      <span>Sources:</span>
                    </span>
                    {msg.sources.map((src, sIdx) => (
                      <span
                        key={sIdx}
                        className="bg-slate-800 hover:bg-slate-700 text-indigo-300 text-xs px-2 py-0.5 rounded border border-slate-700"
                      >
                        📄 {src.title || src.id}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-start space-x-4 max-w-3xl mx-auto">
              <div className="w-8 h-8 rounded-full bg-slate-800 text-indigo-400 border border-slate-700 flex items-center justify-center shrink-0">
                <Sparkles className="w-4 h-4 animate-spin" />
              </div>
              <div className="p-4 rounded-2xl bg-slate-900 text-slate-400 border border-slate-800 text-sm">
                Searching documents & generating grounded response with Hugging Face...
              </div>
            </div>
          )}
        </div>

        <div className="p-4 md:p-6 bg-slate-950 border-t border-slate-800">
          <form onSubmit={handleSend} className="max-w-3xl mx-auto relative flex items-center">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about company policies, leave rules, or expense claims..."
              className="w-full bg-slate-900 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm rounded-2xl py-4 pl-4 pr-14 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="absolute right-2.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 text-white p-2.5 rounded-xl transition"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
          <div className="text-center mt-2">
            <p className="text-[11px] text-slate-500">
              Enterprise RAG Assistant • Role-Based Access Control Enabled • Powered by Hugging Face & Python
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
