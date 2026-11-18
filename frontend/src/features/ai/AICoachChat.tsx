import { useState, useRef, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Send, Bot, User as UserIcon, RefreshCw, AlertCircle, Wrench, ChevronRight, Plus, MessageSquare, Trash2 } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

type ToolEvent = {
  tool_name: string;
  success: boolean;
  data?: any;
  error_message?: string;
};

interface AISection {
  title?: string;
  items: string[];
}

interface StructuredAIResponse {
  answer: string;
  sections: AISection[];
  response_type: string;
  citations_or_sources: string[];
}

type Message = {
  id: string;
  role: 'user' | 'model';
  content: string;
  structured_data?: StructuredAIResponse;
  tool_events?: ToolEvent[];
  created_at: string;
};

export default function AICoachChat() {
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  
  const queryClient = useQueryClient();
  const { user } = useAuthStore();

  const { data: convHistory } = useQuery({
    queryKey: ['ai-conversations'],
    queryFn: async () => {
      const res = await api.get('/ai/conversations');
      return res.data;
    }
  });

  // Auto-load latest conversation if exists
  useEffect(() => {
    if (convHistory && convHistory.length > 0 && !conversationId) {
      loadConversation(convHistory[0].id);
    }
  }, [convHistory]);

  const loadConversation = async (id: string) => {
    try {
      const res = await api.get(`/ai/conversations/${id}`);
      setConversationId(id);
      
      // Transform db messages
      const msgs = res.data.messages.map((m: any, i: number) => ({
        id: `msg-${i}`,
        role: m.role,
        content: m.content,
        structured_data: m.structured_data,
        tool_events: m.tool_events,
        created_at: m.created_at
      }));
      setMessages(msgs);
      setTimeout(scrollToBottom, 50);
    } catch (e) {
      console.error("Failed to load conversation", e);
    }
  };

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      const res = await api.delete(`/ai/conversations/${id}`);
      return res.data;
    },
    onSuccess: (_, deletedId) => {
      queryClient.invalidateQueries({ queryKey: ['ai-conversations'] });
      if (conversationId === deletedId) {
        setConversationId('new');
        setMessages([]);
      }
    },
    onError: () => {
      alert('Failed to delete conversation. Please try again.');
    }
  });

  const handleDelete = () => {
    if (!conversationId || conversationId === 'new') return;
    if (window.confirm('Are you sure you want to delete this chat?')) {
      deleteMutation.mutate(conversationId);
    }
  };

  const chatMutation = useMutation({
    mutationFn: async (messageText: string) => {
      const payload: any = { message: messageText };
      if (conversationId && conversationId !== 'new') payload.conversation_id = conversationId;
      
      const res = await api.post('/ai/chat', payload);
      return res.data;
    },
    onSuccess: (data) => {
      if (!conversationId || conversationId === 'new') {
        setConversationId(data.conversation_id);
        queryClient.invalidateQueries({ queryKey: ['ai-conversations'] });
      }
      
      setMessages(prev => [...prev, {
        id: `msg-${Date.now()}`,
        role: 'model',
        content: data.message,
        structured_data: data.structured_data,
        tool_events: data.tool_events,
        created_at: new Date().toISOString()
      }]);
      
      // If tools mutated data (like swap_meal_food), invalidate nutrition caches
      if (data.tool_events?.some((t: ToolEvent) => t.tool_name === 'swap_meal_food' && t.success)) {
        queryClient.invalidateQueries({ queryKey: ['all-meals'] });
        queryClient.invalidateQueries({ queryKey: ['meals'] });
        queryClient.invalidateQueries({ queryKey: ['daily-summary'] });
      }
      
      setTimeout(scrollToBottom, 50);
    },
    onError: () => {
      setMessages(prev => [...prev, {
        id: `msg-${Date.now()}`,
        role: 'model',
        content: "Sorry, I encountered an error communicating with the server. Please check your connection or provider configuration.",
        created_at: new Date().toISOString()
      }]);
      setTimeout(scrollToBottom, 50);
    }
  });

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || chatMutation.isPending) return;

    const userText = input.trim();
    setInput('');
    
    setMessages(prev => [...prev, {
      id: `msg-user-${Date.now()}`,
      role: 'user',
      content: userText,
      created_at: new Date().toISOString()
    }]);
    
    setTimeout(scrollToBottom, 50);
    chatMutation.mutate(userText);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const renderToolEvent = (tool: ToolEvent, idx: number) => {
    if (!tool.success) {
      return (
        <div key={idx} className="flex items-center gap-2 text-xs text-terracotta bg-terracotta/10 px-3 py-2 rounded-sm mb-2">
          <AlertCircle className="w-3 h-3" />
          <span>Failed to use {tool.tool_name}: {tool.error_message}</span>
        </div>
      );
    }
    
    let message = `Used tool: ${tool.tool_name}`;
    if (tool.tool_name === 'search_foods') {
      const count = tool.data?.results?.length || 0;
      message = `Searched foods: Found ${count} matching items.`;
    } else if (tool.tool_name === 'swap_meal_food') {
      message = tool.data?.message || 'Successfully swapped meal food.';
    } else if (tool.tool_name === 'search_exercises') {
      const count = tool.data?.results?.length || 0;
      message = `Searched exercises: Found ${count} matching items.`;
    }

    return (
      <div key={idx} className="flex items-center gap-2 text-xs text-forest bg-forest/10 px-3 py-2 rounded-sm mb-2 border border-forest/20">
        <Wrench className="w-3 h-3" />
        <span>{message}</span>
      </div>
    );
  };

  const renderStructuredMessage = (data: StructuredAIResponse) => {
    return (
      <div className="space-y-4">
        {data.answer && (
          <p className="leading-relaxed">{data.answer}</p>
        )}
        
        {data.sections && data.sections.length > 0 && (
          <div className="space-y-3 mt-4">
            {data.sections.map((section, sIdx) => (
              <div key={sIdx} className="bg-surface border border-border p-3 rounded-sm">
                {section.title && (
                  <h4 className="font-heading font-medium text-forest mb-2 border-b border-border pb-1">{section.title}</h4>
                )}
                {section.items && section.items.length > 0 && (
                  <ul className="space-y-2">
                    {section.items.map((item, iIdx) => (
                      <li key={iIdx} className="flex items-start gap-2 text-sm text-charcoal">
                        <ChevronRight className="w-4 h-4 text-terracotta flex-shrink-0 mt-0.5" />
                        <span dangerouslySetInnerHTML={{ __html: item.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        )}
        
        {data.citations_or_sources && data.citations_or_sources.length > 0 && (
          <div className="mt-4 pt-3 border-t border-border">
            <p className="text-xs text-stone font-medium mb-1">Sources & Context:</p>
            <ul className="list-disc pl-4 text-xs text-stone space-y-1">
              {data.citations_or_sources.map((cite, cIdx) => (
                <li key={cIdx}>{cite}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] max-w-4xl mx-auto p-4 sm:p-8 fade-in">
      <div className="mb-6 flex-shrink-0 flex flex-col md:flex-row md:items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-heading font-semibold text-forest flex items-center gap-3">
            <Bot className="w-8 h-8 text-terracotta" /> AI Coach
          </h1>
          <p className="text-stone mt-1">Your personal nutrition and fitness assistant, powered by your exact targets.</p>
        </div>
        
        <div className="flex flex-wrap items-center gap-3">
          {convHistory && convHistory.length > 0 && (
            <div className="flex items-center gap-2">
              <div className="relative">
                <MessageSquare className="w-4 h-4 text-stone absolute left-3 top-1/2 -translate-y-1/2" />
                <select
                  value={conversationId === 'new' ? 'new' : (conversationId || '')}
                  onChange={(e) => {
                    if (e.target.value === 'new') {
                      setConversationId('new');
                      setMessages([]);
                    } else if (e.target.value) {
                      loadConversation(e.target.value);
                    }
                  }}
                  className="bg-surface border border-border text-sm text-charcoal py-2 pl-9 pr-8 rounded-sm outline-none focus:border-forest appearance-none min-w-[200px]"
                  style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 24 24\' stroke=\'%23a8a29e\'%3E%3Cpath stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'2\' d=\'M19 9l-7 7-7-7\'%3E%3C/path%3E%3C/svg%3E")', backgroundRepeat: 'no-repeat', backgroundPosition: 'right 0.5rem center', backgroundSize: '1em' }}
                >
                  <option value="new">-- Start New --</option>
                  {convHistory.map((c: any) => (
                    <option key={c.id} value={c.id}>{c.title || 'AI Coach Chat'}</option>
                  ))}
                </select>
              </div>
              
              {conversationId && conversationId !== 'new' && (
                <button
                  onClick={handleDelete}
                  disabled={deleteMutation.isPending}
                  className="p-2 text-stone hover:text-terracotta hover:bg-terracotta/10 rounded-sm transition-colors border border-transparent hover:border-terracotta/20"
                  title="Delete this conversation"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              )}
            </div>
          )}
          <button 
            onClick={() => {
              setConversationId('new');
              setMessages([]);
              setTimeout(() => inputRef.current?.focus(), 50);
            }}
            className="flex items-center gap-2 bg-background border border-border hover:border-forest text-charcoal px-3 py-2 rounded-sm text-sm font-medium transition-colors outline-none focus-visible:ring-2 focus-visible:ring-forest"
          >
            <Plus className="w-4 h-4" /> New Chat
          </button>
        </div>
      </div>

      <div className="flex-1 bg-surface border border-border rounded-sm shadow-sm flex flex-col overflow-hidden relative">
        
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
          {messages.length === 0 && !chatMutation.isPending && (
            <div className="h-full flex flex-col items-center justify-center text-center text-stone">
              <Bot className="w-16 h-16 text-forest/20 mb-4" />
              <p className="text-lg font-medium text-forest mb-2">Hello, {user?.email?.split('@')[0] || 'there'}!</p>
              <p className="max-w-md text-sm">I have access to your fitness goals, dietary preferences, and macro targets. How can I help you today?</p>
              
              <div className="mt-8 flex flex-wrap gap-2 justify-center max-w-lg">
                {['What should I eat for breakfast?', 'Suggest a high protein vegetarian meal', 'Find a dumbbell exercise for my chest'].map(suggestion => (
                  <button 
                    key={suggestion}
                    onClick={() => { setInput(suggestion); }}
                    className="text-xs bg-background border border-border px-3 py-2 rounded-sm text-charcoal hover:border-forest transition-colors"
                  >
                    "{suggestion}"
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="space-y-6">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {msg.role === 'model' && (
                  <div className="w-8 h-8 rounded-full bg-forest text-cream flex items-center justify-center flex-shrink-0 self-end">
                    <Bot className="w-4 h-4" />
                  </div>
                )}
                
                <div className={`max-w-[85%] ${msg.role === 'user' ? 'order-1' : 'order-2'}`}>
                  {msg.tool_events && msg.tool_events.length > 0 && (
                    <div className="mb-2">
                      {msg.tool_events.map((t, idx) => renderToolEvent(t, idx))}
                    </div>
                  )}
                  <div className={`p-4 rounded-sm text-sm whitespace-pre-wrap leading-relaxed shadow-sm
                    ${msg.role === 'user' ? 'bg-forest text-cream' : 'bg-background border border-border text-charcoal'}`
                  }>
                    {msg.structured_data 
                      ? renderStructuredMessage(msg.structured_data) 
                      : msg.content}
                  </div>
                </div>

                {msg.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-terracotta text-cream flex items-center justify-center flex-shrink-0 self-end order-2">
                    <UserIcon className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}
          </div>
          
          {chatMutation.isPending && (
            <div className="flex gap-4 justify-start fade-in">
              <div className="w-8 h-8 rounded-full bg-forest text-cream flex items-center justify-center flex-shrink-0 self-end">
                <Bot className="w-4 h-4" />
              </div>
              <div className="max-w-[85%] order-2">
                <div className="p-4 rounded-sm bg-background border border-border text-charcoal shadow-sm flex items-center gap-2">
                  <RefreshCw className="w-4 h-4 text-forest animate-spin" />
                  <span className="text-sm text-stone">Thinking...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-background border-t border-border">
          <form onSubmit={handleSubmit} className="flex gap-3 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about meals, exercises, or alternatives..."
              className="w-full bg-surface border border-border rounded-sm py-3 pl-4 pr-12 focus:border-forest outline-none resize-none min-h-[50px] max-h-[150px] text-sm text-charcoal"
              rows={1}
              disabled={chatMutation.isPending}
            />
            <button
              type="submit"
              disabled={!input.trim() || chatMutation.isPending}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-2 text-forest hover:bg-forest/10 rounded-sm disabled:opacity-50 transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
          <div className="text-center mt-2">
            <span className="text-[10px] text-stone uppercase tracking-wider">AI can make mistakes. Verify nutrition totals.</span>
          </div>
        </div>
      </div>
    </div>
  );
}