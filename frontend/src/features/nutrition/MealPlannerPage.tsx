import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Calendar as CalIcon, RefreshCw, CheckCircle2, ChevronDown, ChevronUp, AlertCircle, TrendingDown, TrendingUp, Equal } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function MealPlannerPage() {
  const queryClient = useQueryClient();
  const [expandedMeals, setExpandedMeals] = useState<string[]>([]);
  
  const today = new Date();
  const upcomingDays = Array.from({ length: 7 }).map((_, i) => {
    const d = new Date(today);
    d.setDate(today.getDate() + i);
    return d.toISOString().split('T')[0];
  });

  const { data: plans, isLoading } = useQuery({
    queryKey: ['meal-plans', upcomingDays[0], upcomingDays[6]],
    queryFn: async () => {
      const res = await api.get(`/plans/meals?start_date=${upcomingDays[0]}&end_date=${upcomingDays[6]}`);
      return res.data;
    }
  });

  const generateMutation = useMutation({
    mutationFn: async (dateStr: string) => {
      const res = await api.post(`/plans/meals/generate?target_date=${dateStr}`);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meal-plans'] });
    }
  });
  
  const completeMutation = useMutation({
    mutationFn: async (planId: string) => {
      const res = await api.post(`/plans/meals/${planId}/log`);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meal-plans'] });
      queryClient.invalidateQueries({ queryKey: ['daily-summary'] }); // Update diary
    }
  });

    const addToTodayMutation = useMutation({
    mutationFn: async (meal: any) => {
      const payload = {
        meal_name: meal.meal_name,
        meal_type: meal.meal_type,
        serving_size: meal.serving_size || "1 serving",
        calories: meal.calories,
        protein_grams: meal.protein || 0,
        carbohydrates_grams: meal.carbs || 0,
        fat_grams: meal.fats || 0,
        fiber_grams: meal.fiber || 0,
        notes: "From Meal Planner",
        consumed_at: new Date().toISOString()
      };
      const res = await api.post('/nutrition/meals', payload);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meals'] });
      queryClient.invalidateQueries({ queryKey: ['daily-summary'] });
      queryClient.invalidateQueries({ queryKey: ['today-meals'] });
      alert("Successfully added to Today's Meals!");
    }
  });

  const addToMyMealsMutation = useMutation({
    mutationFn: async (meal: any) => {
      const payload = {
        meal_name: meal.meal_name,
        meal_type: meal.meal_type,
        serving_size: meal.serving_size || "1 serving",
        calories: meal.calories,
        protein_grams: meal.protein || 0,
        carbohydrates_grams: meal.carbs || 0,
        fat_grams: meal.fats || 0,
        fiber_grams: meal.fiber || 0,
        ingredients: meal.ingredients || [],
        notes: "Saved from Meal Planner"
      };
      const res = await api.post('/nutrition/saved-meals', payload);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-meals'] });
      alert("Successfully saved to My Meals!");
    }
  });
  const toggleExpand = (mealKey: string) => {
    setExpandedMeals(prev => 
      prev.includes(mealKey) ? prev.filter(k => k !== mealKey) : [...prev, mealKey]
    );
  };

  const getTargetDiffBadge = (planned: number, target: number, unit: string, label: string) => {
    if (!target) return null;
    const diff = planned - target;
    const absDiff = Math.abs(diff);
    // Tolerance: 5% for calories, 10% for macros
    const tolerance = label === 'Calories' ? target * 0.05 : target * 0.10;
    
    if (absDiff <= tolerance) {
      return (
         <span className="flex items-center gap-1 text-[10px] uppercase font-semibold text-forest bg-forest/10 px-2 py-0.5 rounded-sm">
           <Equal className="w-3 h-3" /> Target
         </span>
      );
    }
    
    if (diff > 0) {
      return (
         <span className="flex items-center gap-1 text-[10px] uppercase font-semibold text-terracotta bg-terracotta/10 px-2 py-0.5 rounded-sm" title={`Over by ${Math.round(absDiff)}${unit}`}>
           <TrendingUp className="w-3 h-3" /> +{Math.round(absDiff)}{unit}
         </span>
      );
    }
    
    return (
       <span className="flex items-center gap-1 text-[10px] uppercase font-semibold text-charcoal bg-charcoal/10 px-2 py-0.5 rounded-sm" title={`Under by ${Math.round(absDiff)}${unit}`}>
         <TrendingDown className="w-3 h-3" /> -{Math.round(absDiff)}{unit}
       </span>
    );
  };

  if (isLoading) {
    return <div className="p-8 text-center text-stone">Loading meal planner...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 fade-in p-4 sm:p-0">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-serif text-forest flex items-center gap-3">
            <CalIcon className="w-8 h-8" /> Meal Planner
          </h1>
          <p className="text-stone mt-1">AI-generated nutrition schedules designed to hit your macros.</p>
        </div>
        <Link 
          to="/alternatives"
          className="text-sm font-medium bg-surface border border-border text-charcoal hover:border-forest hover:text-forest px-4 py-2 rounded-sm transition-colors"
        >
          Find Food Swaps
        </Link>
      </div>

      <div className="bg-surface border border-border rounded-sm shadow-sm overflow-hidden">
        <div className="divide-y divide-border">
          {upcomingDays.map((dateStr, i) => {
            const dateObj = new Date(dateStr);
            const isToday = i === 0;
            const plan = plans?.find((w: any) => w.date === dateStr);
            
            // Check if plan has major variance
            let needsAdjustment = false;
            if (plan && plan.target_calories) {
              const diff = Math.abs(plan.total_calories - plan.target_calories);
              if (diff > plan.target_calories * 0.15) needsAdjustment = true; // 15% diff is material
            }

            return (
              <div 
                key={dateStr} 
                className="p-4 sm:p-6 hover:bg-background transition-colors flex flex-col sm:flex-row sm:items-start justify-between gap-4"
              >
                <div className="flex items-start gap-4 w-full">
                  <div className={`w-14 h-14 rounded-sm flex flex-col items-center justify-center shrink-0 ${isToday ? 'bg-forest text-cream' : 'bg-background border border-border text-charcoal'}`}>
                    <span className="text-xs uppercase font-semibold">{dateObj.toLocaleDateString('en-US', { weekday: 'short' })}</span>
                    <span className="text-lg font-heading">{dateObj.getDate()}</span>
                  </div>
                  <div className="flex-grow">
                    <h3 className="font-medium text-charcoal">{isToday ? 'Today' : dateObj.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })}</h3>
                    
                    {!plan ? (
                      <p className="text-sm text-stone mt-1 italic">No meals planned yet</p>
                    ) : (
                      <div className="mt-2 space-y-4">
                        <div className="flex items-center gap-2 mb-2 flex-wrap">
                          <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-1 rounded-sm ${plan.status === 'completed' ? 'bg-forest/10 text-forest' : plan.status === 'accepted' ? 'bg-charcoal/10 text-charcoal' : 'bg-terracotta/10 text-terracotta'}`}>
                            {plan.status}
                          </span>
                          
                          {plan.status === 'generated' && (
                            <button 
                              onClick={() => generateMutation.mutate(dateStr)}
                              className="text-xs flex items-center gap-1 font-medium text-stone hover:text-forest transition-colors ml-auto"
                            >
                              <RefreshCw className="w-3 h-3" /> Regenerate
                            </button>
                          )}
                        </div>

                        {/* Nutrition Targets vs Planned */}
                        {plan.target_calories > 0 && (
                          <div className="bg-background border border-border rounded-sm p-3 grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
                             <div>
                                <span className="block text-[10px] uppercase font-semibold text-stone">Calories</span>
                                <div className="text-sm font-medium text-charcoal flex items-center justify-center gap-1">
                                   {plan.total_calories} <span className="text-xs text-stone font-normal">/ {plan.target_calories}</span>
                                </div>
                                <div className="flex justify-center mt-1">
                                  {getTargetDiffBadge(plan.total_calories, plan.target_calories, '', 'Calories')}
                                </div>
                             </div>
                             <div>
                                <span className="block text-[10px] uppercase font-semibold text-stone">Protein</span>
                                <div className="text-sm font-medium text-charcoal flex items-center justify-center gap-1">
                                   {plan.total_protein}g <span className="text-xs text-stone font-normal">/ {plan.target_protein}g</span>
                                </div>
                                <div className="flex justify-center mt-1">
                                  {getTargetDiffBadge(plan.total_protein, plan.target_protein, 'g', 'Protein')}
                                </div>
                             </div>
                             <div>
                                <span className="block text-[10px] uppercase font-semibold text-stone">Carbs</span>
                                <div className="text-sm font-medium text-charcoal flex items-center justify-center gap-1">
                                   {plan.total_carbs}g <span className="text-xs text-stone font-normal">/ {plan.target_carbs}g</span>
                                </div>
                                <div className="flex justify-center mt-1">
                                  {getTargetDiffBadge(plan.total_carbs, plan.target_carbs, 'g', 'Carbs')}
                                </div>
                             </div>
                             <div>
                                <span className="block text-[10px] uppercase font-semibold text-stone">Fats</span>
                                <div className="text-sm font-medium text-charcoal flex items-center justify-center gap-1">
                                   {plan.total_fats}g <span className="text-xs text-stone font-normal">/ {plan.target_fats}g</span>
                                </div>
                                <div className="flex justify-center mt-1">
                                  {getTargetDiffBadge(plan.total_fats, plan.target_fats, 'g', 'Fats')}
                                </div>
                             </div>
                          </div>
                        )}

                        {needsAdjustment && plan.status === 'generated' && (
                          <div className="bg-terracotta/5 border border-terracotta/20 text-terracotta p-3 rounded-sm text-xs flex gap-2 items-start">
                            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                            <div>
                              <p className="font-semibold mb-1">Target Mismatch Detected</p>
                              <p>This plan deviates significantly from your macro targets. You can edit meals, find alternatives, or regenerate the plan.</p>
                            </div>
                          </div>
                        )}
                        
                        <div className="space-y-3">
                          {plan.meals?.map((m: any, idx: number) => {
                            const mealKey = `${dateStr}-${idx}`;
                            const isMealExpanded = expandedMeals.includes(mealKey);
                            const hasLongIngredients = m.ingredients && m.ingredients.join(', ').length > 80;

                            return (
                              <div key={idx} className="border border-border p-4 rounded-sm bg-background">
                                <div className="flex justify-between items-start mb-2">
                                  <div>
                                    <span className="text-xs font-semibold uppercase tracking-wider text-forest">{m.meal_type}</span>
                                    <h4 className="font-medium text-charcoal text-base mt-0.5">{m.meal_name}</h4>
                                  </div>
                                  <div className="text-right shrink-0">
                                    <span className="block text-sm font-medium text-charcoal">{m.calories} kcal</span>
                                    <span className="block text-xs text-stone flex gap-2 justify-end">
                                      <span>P: {m.protein}g</span>
                                      <span>C: {m.carbs}g</span>
                                      <span>F: {m.fats}g</span>
                                    </span>
                                  </div>
                                </div>
                                
                                {m.ingredients && m.ingredients.length > 0 ? (
                                  <div className="mt-3">
                                    <span className="text-xs uppercase tracking-wider font-semibold text-stone block mb-1">Ingredients & Instructions</span>
                                    <div className={`text-sm text-charcoal/80 leading-relaxed ${isMealExpanded ? '' : 'line-clamp-2'}`}>
                                      <ul className="list-disc pl-4 space-y-1">
                                         {m.ingredients.map((ing: string, i: number) => (
                                           <li key={i}>{ing}</li>
                                         ))}
                                      </ul>
                                    </div>
                                    
                                                                        {hasLongIngredients && (
                                      <button 
                                        onClick={() => toggleExpand(mealKey)}
                                        className="text-xs font-medium text-forest mt-2 hover:underline flex items-center gap-1"
                                      >
                                        {isMealExpanded ? <><ChevronUp className="w-3 h-3" /> Show less</> : <><ChevronDown className="w-3 h-3" /> Show full ingredients</>}
                                      </button>
                                    )}
                                  </div>
                                ) : (
                                  <div className="mt-3 text-sm text-stone italic">Ingredient details unavailable.</div>
                                )}
                                
                                {/* Meal Actions */}
                                <div className="mt-4 pt-3 border-t border-border flex flex-wrap items-center gap-2">
                                  <button
                                    onClick={() => addToTodayMutation.mutate(m)}
                                    disabled={addToTodayMutation.isPending}
                                    className="text-xs font-medium bg-forest text-cream px-3 py-1.5 rounded-sm hover:bg-forest/90 transition-colors disabled:opacity-50"
                                  >
                                    Add to Today's Meals
                                  </button>
                                  <button
                                    onClick={() => addToMyMealsMutation.mutate(m)}
                                    disabled={addToMyMealsMutation.isPending}
                                    className="text-xs font-medium bg-charcoal text-cream px-3 py-1.5 rounded-sm hover:bg-charcoal/90 transition-colors disabled:opacity-50"
                                  >
                                    Save to My Meals
                                  </button>
                                  <Link
                                    to="/alternatives"
                                    className="text-xs font-medium bg-surface border border-border text-charcoal hover:border-forest hover:text-forest px-3 py-1.5 rounded-sm transition-colors"
                                  >
                                    Swap Food
                                  </Link>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="flex flex-col items-end gap-2 w-full sm:w-auto mt-4 sm:mt-0 shrink-0">
                  {!plan ? (
                    <button 
                      onClick={() => generateMutation.mutate(dateStr)}
                      disabled={generateMutation.isPending}
                      className="text-sm font-medium bg-background border border-border text-charcoal hover:text-forest hover:border-forest/30 px-4 py-2 rounded-sm transition-colors flex items-center justify-center gap-2 w-full disabled:opacity-50"
                    >
                      <RefreshCw className={`w-4 h-4 ${generateMutation.isPending ? 'animate-spin' : ''}`} /> Generate Plan
                    </button>
                  ) : (
                    plan.status !== 'completed' && (
                      <button 
                        onClick={() => completeMutation.mutate(plan.id)}
                        disabled={completeMutation.isPending}
                        className="flex items-center justify-center gap-2 text-sm font-medium bg-forest text-cream px-4 py-2 rounded-sm transition-colors hover:bg-forest/90 disabled:opacity-50 w-full"
                      >
                        <CheckCircle2 className="w-4 h-4" /> Log to Diary
                      </button>
                    )
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

