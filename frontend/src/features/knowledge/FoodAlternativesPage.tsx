import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Search, Bot, AlertCircle, RefreshCw } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function FoodAlternativesPage() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  
  // To allow swapping, let's fetch today's planned meals
  const today = new Date().toISOString().split('T')[0];
  const { data: mealPlans } = useQuery({
    queryKey: ['meal-plans', today, today],
    queryFn: async () => {
      const res = await api.get(`/plans/meals?start_date=${today}&end_date=${today}`);
      return res.data;
    }
  });
  
  const todayPlan = mealPlans && mealPlans.length > 0 ? mealPlans[0] : null;

  const alternativesMutation = useMutation({
    mutationFn: async (foodName: string) => {
      const res = await api.post('/plans/meals/alternatives', { 
        food_name: foodName
      });
      return res.data;
    }
  });

  const swapMutation = useMutation({
    mutationFn: async ({ planId, oldMealIndex, newMeal }: { planId: string, oldMealIndex: number, newMeal: any }) => {
      if (!todayPlan) return;
      const updatedMeals = [...todayPlan.meals];
      updatedMeals[oldMealIndex] = {
        ...updatedMeals[oldMealIndex],
        meal_name: newMeal.meal_name,
        calories: newMeal.calories,
        protein: newMeal.protein,
        carbs: newMeal.carbs,
        fats: newMeal.fats,
        ingredients: newMeal.ingredients
      };
      
      const total_calories = updatedMeals.reduce((acc, m) => acc + (m.calories || 0), 0);
      const total_protein = updatedMeals.reduce((acc, m) => acc + (m.protein || 0), 0);
      const total_carbs = updatedMeals.reduce((acc, m) => acc + (m.carbs || 0), 0);
      const total_fats = updatedMeals.reduce((acc, m) => acc + (m.fats || 0), 0);
      const total_fiber = updatedMeals.reduce((acc, m) => acc + (m.fiber || 0), 0);

      const res = await api.patch(`/plans/meals/${planId}`, { 
        meals: updatedMeals,
        total_calories,
        total_protein,
        total_carbs,
        total_fats,
        total_fiber
      });
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meal-plans'] });
      alert("Meal successfully swapped and nutrition recalculated!");
      navigate('/meal-planner');
    }
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    alternativesMutation.mutate(query);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 fade-in p-4 sm:p-0">
      <div className="text-center mb-10">
        <div className="w-16 h-16 bg-cream rounded-full flex items-center justify-center mx-auto mb-4 border border-border shadow-sm">
          <Search className="w-8 h-8 text-forest" />
        </div>
        <h1 className="text-3xl font-serif text-charcoal mb-2">Food Alternatives</h1>
        <p className="text-stone">Find healthier swaps tailored to your allergies and preferences.</p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        <div className="md:col-span-1 space-y-6">
          <div className="bg-surface border border-border p-6 rounded-sm shadow-sm">
            <h3 className="font-serif text-lg text-forest mb-4">Quick Search</h3>
            <form onSubmit={handleSearch} className="space-y-4">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. Potato chips..."
                className="w-full bg-background border border-border px-4 py-2 rounded-sm focus:border-forest outline-none text-sm"
                disabled={alternativesMutation.isPending}
              />
              <button 
                type="submit"
                disabled={alternativesMutation.isPending || !query.trim()}
                className="w-full bg-forest text-cream px-4 py-2 rounded-sm font-medium hover:bg-forest/90 transition-colors disabled:opacity-50 flex justify-center items-center gap-2"
              >
                {alternativesMutation.isPending && <RefreshCw className="w-4 h-4 animate-spin" />}
                Find Swap
              </button>
            </form>
          </div>
          
          {todayPlan && todayPlan.meals && todayPlan.meals.length > 0 && (
            <div className="bg-surface border border-border p-6 rounded-sm shadow-sm">
              <h3 className="font-serif text-lg text-forest mb-4">Swap Today's Plan</h3>
              <div className="space-y-3">
                {todayPlan.meals.map((m: any, idx: number) => (
                  <button 
                    key={idx}
                    onClick={() => {
                      setQuery(m.meal_name);
                      alternativesMutation.mutate(m.meal_name);
                    }}
                    className="w-full text-left bg-background border border-border p-3 rounded-sm hover:border-forest/50 transition-colors text-sm"
                  >
                    <span className="block font-medium text-charcoal capitalize">{m.meal_type}</span>
                    <span className="block text-stone truncate">{m.meal_name}</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="md:col-span-2">
          {alternativesMutation.error && (
            <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta p-4 rounded-sm flex gap-3 items-start mb-6">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <p>{(alternativesMutation.error as any).response?.data?.detail || 'Failed to get alternatives.'}</p>
            </div>
          )}

          {!alternativesMutation.data && !alternativesMutation.isPending && (
            <div className="bg-surface border border-border p-12 text-center rounded-sm shadow-sm h-full flex flex-col items-center justify-center">
              <Bot className="w-12 h-12 text-stone/30 mb-4" />
              <p className="text-stone">Select a meal from your plan or search for a food to see smart alternatives.</p>
            </div>
          )}
          
          {alternativesMutation.isPending && (
            <div className="bg-surface border border-border p-12 text-center rounded-sm shadow-sm h-full flex flex-col items-center justify-center">
              <RefreshCw className="w-8 h-8 text-forest animate-spin mb-4" />
              <p className="text-stone">Analyzing your profile and generating alternatives...</p>
            </div>
          )}

          {alternativesMutation.data && (
            <div className="space-y-4 slide-up">
              <h3 className="font-serif text-xl text-charcoal mb-4 flex items-center gap-2">
                <Bot className="w-6 h-6 text-forest" /> AI Suggestions for "{query}"
              </h3>
              
              {alternativesMutation.data.map((alt: any, idx: number) => {
                // Check if this matches a meal in our today plan so we can swap it
                const matchedMealIndex = todayPlan?.meals.findIndex((m: any) => m.meal_name === query);
                const canSwap = todayPlan && matchedMealIndex !== -1 && matchedMealIndex !== undefined;

                return (
                  <div key={idx} className="bg-surface border border-border p-5 rounded-sm shadow-sm">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-lg text-forest">{alt.meal_name}</h4>
                      {canSwap && (
                        <button
                          onClick={() => swapMutation.mutate({ planId: todayPlan.id, oldMealIndex: matchedMealIndex!, newMeal: alt })}
                          disabled={swapMutation.isPending}
                          className="bg-background border border-border text-charcoal px-3 py-1.5 rounded-sm text-xs font-medium hover:border-forest hover:text-forest transition-colors"
                        >
                          Replace in Plan
                        </button>
                      )}
                    </div>
                    
                    <p className="text-sm text-charcoal mb-4">{alt.reason}</p>
                    
                    <div className="grid grid-cols-4 gap-2 mb-4 bg-background border border-border p-3 rounded-sm text-center">
                      <div>
                        <span className="block text-[10px] uppercase tracking-wider text-stone font-semibold">Calories</span>
                        <span className="text-sm font-medium text-charcoal">{alt.calories}</span>
                      </div>
                      <div>
                        <span className="block text-[10px] uppercase tracking-wider text-stone font-semibold">Protein</span>
                        <span className="text-sm font-medium text-charcoal">{alt.protein}g</span>
                      </div>
                      <div>
                        <span className="block text-[10px] uppercase tracking-wider text-stone font-semibold">Carbs</span>
                        <span className="text-sm font-medium text-charcoal">{alt.carbs}g</span>
                      </div>
                      <div>
                        <span className="block text-[10px] uppercase tracking-wider text-stone font-semibold">Fats</span>
                        <span className="text-sm font-medium text-charcoal">{alt.fats}g</span>
                      </div>
                    </div>
                    
                    <div>
                      <span className="block text-xs font-semibold uppercase tracking-wider text-stone mb-1">Ingredients</span>
                      <p className="text-sm text-charcoal/80">{alt.ingredients?.join(', ')}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
