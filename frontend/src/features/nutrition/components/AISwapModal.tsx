import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../../lib/axios';
import { Bot, RefreshCw, X, AlertCircle } from 'lucide-react';

type AISwapModalProps = {
  isOpen: boolean;
  onClose: () => void;
  meal: any;
};

export default function AISwapModal({ isOpen, onClose, meal }: AISwapModalProps) {
  const [reason, setReason] = useState('');
  const [result, setResult] = useState<{message: string, success: boolean} | null>(null);
  const queryClient = useQueryClient();

  const swapMutation = useMutation({
    mutationFn: async (userMessage: string) => {
      const prompt = `I want to swap the food in my tracked meal ID ${meal.id} (${meal.meal_name}). Reason: ${userMessage}. Use the swap_meal_food tool to replace it with a suitable alternative from the database.`;
      const res = await api.post('/ai/chat', { message: prompt });
      return res.data;
    },
    onSuccess: (data) => {
      const toolEvent = data.tool_events?.find((t: any) => t.tool_name === 'swap_meal_food');
      if (toolEvent && toolEvent.success) {
        setResult({ success: true, message: toolEvent.data?.message || 'Successfully swapped meal!' });
        queryClient.invalidateQueries({ queryKey: ['all-meals'] });
        queryClient.invalidateQueries({ queryKey: ['meals'] });
        queryClient.invalidateQueries({ queryKey: ['daily-summary'] });
        
        setTimeout(() => {
          onClose();
          setResult(null);
          setReason('');
        }, 2000);
      } else {
        setResult({ success: false, message: toolEvent?.error_message || data.message || 'Swap could not be completed.' });
      }
    },
    onError: () => {
      setResult({ success: false, message: 'Server communication failed.' });
    }
  });

  if (!isOpen || !meal) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-charcoal/50 backdrop-blur-sm fade-in">
      <div className="bg-surface rounded-md shadow-lg w-full max-w-md overflow-hidden flex flex-col">
        <div className="flex justify-between items-center p-4 border-b border-border bg-cream">
          <h2 className="text-lg font-heading font-semibold text-forest flex items-center gap-2">
            <Bot className="w-5 h-5 text-terracotta" /> AI Swap
          </h2>
          <button onClick={() => { onClose(); setResult(null); setReason(''); }} className="text-stone hover:text-charcoal transition-colors outline-none focus-visible:ring-2 rounded-sm p-1">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="p-6">
          <p className="text-sm text-stone mb-4">
            Current food: <span className="font-semibold text-charcoal">{meal.meal_name}</span>
          </p>
          
          {result ? (
            <div className={`p-4 rounded-sm border ${result.success ? 'bg-forest/10 border-forest/20 text-forest' : 'bg-terracotta/10 border-terracotta/20 text-terracotta'} mb-4 flex gap-2 items-start`}>
               {result.success ? <Bot className="w-5 h-5 shrink-0" /> : <AlertCircle className="w-5 h-5 shrink-0" />}
               <p className="text-sm">{result.message}</p>
            </div>
          ) : (
            <>
              <label className="block text-sm font-medium text-forest mb-2">
                Why do you want to swap? (Optional)
              </label>
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                placeholder="e.g. I want something vegetarian, I don't have this right now..."
                className="w-full bg-background border border-border rounded-sm p-3 focus:border-forest outline-none resize-none text-sm text-charcoal mb-4"
                rows={3}
                disabled={swapMutation.isPending}
              />
              
              <div className="flex justify-end gap-3">
                <button 
                  onClick={onClose}
                  disabled={swapMutation.isPending}
                  className="px-4 py-2 text-sm font-medium text-charcoal hover:bg-stone/10 rounded-sm transition-colors outline-none focus-visible:ring-2"
                >
                  Cancel
                </button>
                <button 
                  onClick={() => swapMutation.mutate(reason || 'Find a suitable alternative with similar macros.')}
                  disabled={swapMutation.isPending}
                  className="flex items-center gap-2 px-4 py-2 bg-forest text-cream text-sm font-medium rounded-sm hover:bg-forest/90 transition-colors outline-none focus-visible:ring-2 disabled:opacity-50"
                >
                  {swapMutation.isPending ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Bot className="w-4 h-4" />}
                  {swapMutation.isPending ? 'Swapping...' : 'Swap with AI'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
