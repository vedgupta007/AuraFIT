import { useQuery, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { ChefHat, Flame, Droplets, Dumbbell, Activity, Plus } from 'lucide-react';
import { useState } from 'react';
import MealFormModal from './components/MealFormModal';

export default function NutritionOverview() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const queryClient = useQueryClient();
  
  // Use local date formatted as YYYY-MM-DD
  const todayDate = new Date();
  const today = todayDate.toLocaleDateString('en-CA');
  const tzOffset = -todayDate.getTimezoneOffset();
  
  const { data: summary, isLoading, isError, refetch } = useQuery({
    queryKey: ['daily-summary', today],
    queryFn: async () => {
      const res = await api.get(`/nutrition/daily-summary?date=${today}&tz_offset_minutes=${tzOffset}`);
      return res.data;
    }
  });

  const { data: meals } = useQuery({
    queryKey: ['meals', today],
    queryFn: async () => {
      const startOfDay = new Date();
      startOfDay.setHours(0,0,0,0);
      const endOfDay = new Date();
      endOfDay.setHours(23,59,59,999);
      
      const res = await api.get(`/nutrition/meals?start_date=${startOfDay.toISOString()}&end_date=${endOfDay.toISOString()}`);
      return res.data;
    }
  });

  const handleAddMeal = async (data: any) => {
    await api.post('/nutrition/meals', data);
    queryClient.invalidateQueries({ queryKey: ['daily-summary'] });
    queryClient.invalidateQueries({ queryKey: ['meals'] });
    queryClient.invalidateQueries({ queryKey: ['all-meals'] });
  };

  if (isLoading) {
    return (
      <div className="p-8 flex justify-center items-center h-full">
        <div className="animate-pulse flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-4 border-forest border-t-transparent rounded-full animate-spin"></div>
          <p className="text-stone font-medium">Loading your nutrition data...</p>
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-8">
        <div className="bg-terracotta/10 text-terracotta p-4 rounded-sm border border-terracotta/20">
          <p className="font-medium">Failed to load nutrition data.</p>
          <button onClick={() => refetch()} className="mt-2 text-sm underline outline-none focus-visible:ring-2">Try again</button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-7xl mx-auto fade-in">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-heading font-semibold text-forest">Nutrition Overview</h1>
          <p className="text-stone mt-1">Your daily macros and energy balance for today.</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2 px-4 py-2 bg-forest text-cream font-medium rounded-sm hover:bg-forest/90 transition-colors outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-forest"
        >
          <Plus className="w-4 h-4" /> Add Meal
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <div className="bg-surface p-6 rounded-sm shadow-sm border border-border flex flex-col items-center text-center">
          <div className="w-12 h-12 bg-forest/10 rounded-full flex items-center justify-center mb-3">
            <Flame className="w-6 h-6 text-terracotta" />
          </div>
          <span className="text-sm font-medium text-stone uppercase tracking-wider">Calories</span>
          <span className="text-3xl font-heading font-semibold text-forest mt-1">{summary?.total_calories || 0}</span>
          <span className="text-xs text-stone mt-1">kcal</span>
        </div>

        <div className="bg-surface p-6 rounded-sm shadow-sm border border-border flex flex-col items-center text-center">
          <div className="w-12 h-12 bg-forest/10 rounded-full flex items-center justify-center mb-3">
            <Dumbbell className="w-6 h-6 text-forest" />
          </div>
          <span className="text-sm font-medium text-stone uppercase tracking-wider">Protein</span>
          <span className="text-3xl font-heading font-semibold text-forest mt-1">{summary?.total_protein || 0}</span>
          <span className="text-xs text-stone mt-1">g</span>
        </div>

        <div className="bg-surface p-6 rounded-sm shadow-sm border border-border flex flex-col items-center text-center">
          <div className="w-12 h-12 bg-forest/10 rounded-full flex items-center justify-center mb-3">
            <Activity className="w-6 h-6 text-forest" />
          </div>
          <span className="text-sm font-medium text-stone uppercase tracking-wider">Carbs</span>
          <span className="text-3xl font-heading font-semibold text-forest mt-1">{summary?.total_carbohydrates || 0}</span>
          <span className="text-xs text-stone mt-1">g</span>
        </div>

        <div className="bg-surface p-6 rounded-sm shadow-sm border border-border flex flex-col items-center text-center">
          <div className="w-12 h-12 bg-forest/10 rounded-full flex items-center justify-center mb-3">
            <Droplets className="w-6 h-6 text-forest" />
          </div>
          <span className="text-sm font-medium text-stone uppercase tracking-wider">Fat</span>
          <span className="text-3xl font-heading font-semibold text-forest mt-1">{summary?.total_fat || 0}</span>
          <span className="text-xs text-stone mt-1">g</span>
        </div>

        <div className="bg-surface p-6 rounded-sm shadow-sm border border-border flex flex-col items-center text-center">
          <div className="w-12 h-12 bg-forest/10 rounded-full flex items-center justify-center mb-3">
            <ChefHat className="w-6 h-6 text-forest" />
          </div>
          <span className="text-sm font-medium text-stone uppercase tracking-wider">Fiber</span>
          <span className="text-3xl font-heading font-semibold text-forest mt-1">{summary?.total_fiber || 0}</span>
          <span className="text-xs text-stone mt-1">g</span>
        </div>
      </div>

      <div className="bg-surface rounded-sm shadow-sm border border-border">
        <div className="p-6 border-b border-border">
          <h2 className="text-lg font-heading font-semibold text-forest">Today's Meals</h2>
        </div>
        <div className="p-6">
          {(!meals || meals.length === 0) ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-cream rounded-full flex items-center justify-center mx-auto mb-4">
                <ChefHat className="w-8 h-8 text-stone/50" />
              </div>
              <h3 className="text-lg font-medium text-charcoal">No meals logged yet</h3>
              <p className="text-stone mt-1 max-w-sm mx-auto">Start tracking your nutrition to see your daily breakdown.</p>
              <button 
                onClick={() => setIsModalOpen(true)}
                className="mt-4 px-4 py-2 bg-cream text-forest font-medium rounded-sm border border-border hover:bg-forest/5 transition-colors outline-none focus-visible:ring-2 focus-visible:ring-forest"
              >
                Log your first meal
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {meals.map((meal: any) => (
                <div key={meal.id} className="flex flex-col sm:flex-row justify-between items-start sm:items-center p-4 border border-border rounded-sm hover:border-forest/30 transition-colors">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold uppercase tracking-wider text-terracotta bg-terracotta/10 px-2 py-0.5 rounded-full">
                        {meal.meal_type}
                      </span>
                      <h4 className="font-medium text-charcoal">{meal.meal_name}</h4>
                    </div>
                    <p className="text-sm text-stone mt-1">
                      {meal.serving_size} • {new Date(meal.consumed_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </p>
                  </div>
                  <div className="mt-4 sm:mt-0 flex gap-4 text-sm">
                    <div className="text-center">
                      <span className="block font-semibold text-forest">{meal.calories}</span>
                      <span className="text-xs text-stone">kcal</span>
                    </div>
                    <div className="text-center">
                      <span className="block font-semibold text-charcoal">{meal.protein_grams}g</span>
                      <span className="text-xs text-stone">P</span>
                    </div>
                    <div className="text-center">
                      <span className="block font-semibold text-charcoal">{meal.carbohydrates_grams}g</span>
                      <span className="text-xs text-stone">C</span>
                    </div>
                    <div className="text-center">
                      <span className="block font-semibold text-charcoal">{meal.fat_grams}g</span>
                      <span className="text-xs text-stone">F</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <MealFormModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onSubmit={handleAddMeal}
        title="Log a Meal"
      />
    </div>
  );
}
