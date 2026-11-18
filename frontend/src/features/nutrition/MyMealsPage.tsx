import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Plus, Calendar as CalIcon, ChevronLeft, ChevronRight, CheckCircle2, Bookmark, Flame, Edit2, Trash2 } from 'lucide-react';
import MealFormModal from './components/MealFormModal';

export default function MyMealsPage() {
  const queryClient = useQueryClient();
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingMeal, setEditingMeal] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'diary' | 'saved'>('diary');

  const { data: meals, isLoading } = useQuery({
    queryKey: ['meals', selectedDate],
    queryFn: async () => {
      const start = new Date(selectedDate);
      start.setHours(0, 0, 0, 0);
      const end = new Date(selectedDate);
      end.setHours(23, 59, 59, 999);
      
      const res = await api.get(`/nutrition/meals?limit=100&start_date=${start.toISOString()}&end_date=${end.toISOString()}`);
      return res.data;
    }
  });

  const { data: savedMeals, isLoading: isSavedLoading } = useQuery({
    queryKey: ['saved-meals'],
    queryFn: async () => {
      const res = await api.get('/nutrition/saved-meals');
      return res.data;
    },
    enabled: activeTab === 'saved'
  });

  const { data: summary } = useQuery({
    queryKey: ['daily-summary', selectedDate],
    queryFn: async () => {
      const tzOffset = -new Date().getTimezoneOffset();
      const res = await api.get(`/nutrition/daily-summary?date=${selectedDate}&tz_offset_minutes=${tzOffset}`);
      return res.data;
    }
  });

  const { data: goals } = useQuery({
    queryKey: ['nutrition-goals'],
    queryFn: async () => {
      const res = await api.get('/nutrition/goals');
      return res.data;
    }
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      if (activeTab === 'diary') {
        await api.delete(`/nutrition/meals/${id}`);
      } else {
        await api.delete(`/nutrition/saved-meals/${id}`);
      }
    },
    onSuccess: () => {
      if (activeTab === 'diary') {
        queryClient.invalidateQueries({ queryKey: ['meals'] });
        queryClient.invalidateQueries({ queryKey: ['daily-summary'] });
        queryClient.invalidateQueries({ queryKey: ['today-meals'] });
      } else {
        queryClient.invalidateQueries({ queryKey: ['saved-meals'] });
      }
    }
  });

  const addToTodayMutation = useMutation({
    mutationFn: async (meal: any) => {
      const payload = {
        meal_name: meal.meal_name,
        meal_type: meal.meal_type,
        serving_size: meal.serving_size || "1 serving",
        calories: meal.calories,
        protein_grams: meal.protein_grams || 0,
        carbohydrates_grams: meal.carbohydrates_grams || 0,
        fat_grams: meal.fat_grams || 0,
        fiber_grams: meal.fiber_grams || 0,
        notes: "Added from Saved Meals",
        consumed_at: new Date().toISOString()
      };
      const res = await api.post('/nutrition/meals', payload);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meals'] });
      queryClient.invalidateQueries({ queryKey: ['daily-summary'] });
      queryClient.invalidateQueries({ queryKey: ['today-meals'] });
      alert("Successfully added to Today's Diary!");
    }
  });

  const adjustDate = (days: number) => {
    const d = new Date(selectedDate);
    d.setDate(d.getDate() + days);
    setSelectedDate(d.toISOString().split('T')[0]);
  };

  if (isLoading && !meals) {
    return <div className="p-8 text-center text-stone">Loading...</div>;
  }

  return (
    <div className="p-4 sm:p-8 max-w-7xl mx-auto fade-in space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-serif text-forest">My Meals</h1>
          <p className="text-stone mt-1">Manage and track your nutrition history.</p>
        </div>
        <button 
          onClick={() => { setEditingMeal(null); setIsModalOpen(true); }}
          className="flex items-center gap-2 px-4 py-2 bg-forest text-cream font-medium rounded-sm hover:bg-forest/90 transition-colors w-full sm:w-auto justify-center"
        >
          <Plus className="w-4 h-4" /> Add Meal
        </button>
      </div>

      <div className="flex border-b border-border mb-4">
        <button 
          onClick={() => setActiveTab('diary')} 
          className={`px-4 py-2 font-medium text-sm transition-colors ${activeTab === 'diary' ? 'border-b-2 border-forest text-forest' : 'text-stone hover:text-charcoal'}`}
        >
          Food Diary
        </button>
        <button 
          onClick={() => setActiveTab('saved')} 
          className={`px-4 py-2 font-medium text-sm transition-colors ${activeTab === 'saved' ? 'border-b-2 border-forest text-forest' : 'text-stone hover:text-charcoal'}`}
        >
          Saved Meals
        </button>
      </div>

      {activeTab === 'diary' ? (
        <>
          <div className="bg-surface rounded-sm shadow-sm border border-border p-4 sm:p-6 flex flex-col md:flex-row gap-6 items-center justify-between">
            <div className="flex items-center gap-3 w-full md:w-auto justify-between md:justify-start">
              <button onClick={() => adjustDate(-1)} className="p-2 border border-border rounded-sm text-stone hover:bg-background hover:text-forest transition-colors">
                <ChevronLeft className="w-5 h-5" />
              </button>
              <div className="flex items-center gap-2 text-charcoal font-medium bg-background px-4 py-2 rounded-sm border border-border">
                <CalIcon className="w-4 h-4 text-forest" />
                <input 
                  type="date" 
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  className="bg-transparent border-none outline-none font-sans text-sm"
                />
              </div>
              <button onClick={() => adjustDate(1)} className="p-2 border border-border rounded-sm text-stone hover:bg-background hover:text-forest transition-colors">
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
            
            <div className="grid grid-cols-2 md:flex items-center gap-4 md:gap-8 w-full md:w-auto justify-around">
              <div className="text-center md:text-left">
                <div className="text-xs text-stone mb-1 uppercase tracking-wider font-semibold">Calories</div>
                <div className="font-heading text-forest text-xl">{summary?.total_calories || 0} <span className="text-stone text-xs font-sans">/ {goals?.daily_calories || '-'} kcal</span></div>
              </div>
              <div className="text-center md:text-left">
                <div className="text-xs text-stone mb-1 uppercase tracking-wider font-semibold">Protein</div>
                <div className="font-heading text-charcoal text-lg">{summary?.total_protein || 0}g <span className="text-stone text-xs font-sans">/ {goals?.daily_protein || '-'}g</span></div>
              </div>
              <div className="text-center md:text-left">
                <div className="text-xs text-stone mb-1 uppercase tracking-wider font-semibold">Carbs</div>
                <div className="font-heading text-charcoal text-lg">{summary?.total_carbohydrates || 0}g</div>
              </div>
              <div className="text-center md:text-left">
                <div className="text-xs text-stone mb-1 uppercase tracking-wider font-semibold">Fats</div>
                <div className="font-heading text-charcoal text-lg">{summary?.total_fats || 0}g</div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            {meals?.length === 0 ? (
              <div className="text-center p-12 bg-surface border border-border rounded-sm shadow-sm text-stone">
                <div className="w-12 h-12 bg-background border border-border rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle2 className="w-6 h-6 text-stone/50" />
                </div>
                <h3 className="font-medium text-charcoal mb-1">No meals logged yet</h3>
                <p className="text-sm max-w-sm mx-auto mb-4">You haven't logged any food for this date. Add a meal or track from your planner.</p>
                <button 
                  onClick={() => setIsModalOpen(true)}
                  className="text-sm font-medium text-forest hover:underline"
                >
                  Log your first meal
                </button>
              </div>
            ) : (
              meals?.map((meal: any) => (
                <div key={meal.id} className="bg-surface border border-border p-4 sm:p-5 rounded-sm shadow-sm hover:border-forest/30 transition-colors group">
                  <div className="flex flex-col sm:flex-row justify-between items-start gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-xs font-semibold uppercase tracking-wider text-forest bg-forest/10 px-2 py-0.5 rounded-sm">{meal.meal_type}</span>
                        <h3 className="font-medium text-charcoal text-lg">{meal.meal_name}</h3>
                      </div>
                      <p className="text-sm text-stone flex items-center gap-1.5 mb-2">
                        {meal.serving_size}
                        {new Date(meal.consumed_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) !== '12:00 AM' && (
                          <span className="text-xs opacity-75">
                            &bull; {new Date(meal.consumed_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </span>
                        )}
                      </p>
                      
                      <div className="flex gap-4 text-xs font-medium bg-background border border-border w-max px-3 py-1.5 rounded-sm mt-3">
                        <span className="text-forest flex items-center gap-1"><Flame className="w-3 h-3" /> {meal.calories} kcal</span>
                        <span className="text-charcoal border-l border-border pl-4">P: {meal.protein_grams}g</span>
                        <span className="text-charcoal">C: {meal.carbohydrates_grams}g</span>
                        <span className="text-charcoal">F: {meal.fat_grams}g</span>
                      </div>
                      {meal.notes && (
                        <p className="text-sm text-stone/80 mt-3 italic border-l-2 border-border pl-3">{meal.notes}</p>
                      )}
                    </div>
                    
                    <div className="flex items-center gap-2 w-full sm:w-auto border-t border-border sm:border-0 pt-3 sm:pt-0 mt-3 sm:mt-0 justify-end opacity-100 sm:opacity-0 group-hover:opacity-100 transition-opacity">
                      <button 
                        onClick={() => { setEditingMeal(meal); setIsModalOpen(true); }}
                        className="p-1.5 text-stone hover:text-forest hover:bg-forest/10 rounded-sm transition-colors"
                        title="Edit Meal"
                      >
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button 
                        onClick={() => { if (window.confirm('Delete this meal?')) deleteMutation.mutate(meal.id); }}
                        className="p-1.5 text-stone hover:text-terracotta hover:bg-terracotta/10 rounded-sm transition-colors"
                        title="Delete Meal"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      ) : (
        <div className="space-y-4">
          {isSavedLoading ? (
            <div className="p-8 text-center text-stone">Loading saved meals...</div>
          ) : savedMeals?.length === 0 ? (
            <div className="text-center p-12 bg-surface border border-border rounded-sm shadow-sm text-stone">
              <Bookmark className="w-12 h-12 text-stone/50 mx-auto mb-4" />
              <h3 className="font-medium text-charcoal mb-1">No Saved Meals</h3>
              <p className="text-sm max-w-sm mx-auto mb-4">You can save your favorite meals from the Meal Planner for quick logging later.</p>
            </div>
          ) : (
            savedMeals?.map((meal: any) => (
              <div key={meal.id} className="bg-surface border border-border p-4 sm:p-5 rounded-sm shadow-sm hover:border-forest/30 transition-colors group">
                <div className="flex flex-col sm:flex-row justify-between items-start gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-1">
                      <span className="text-xs font-semibold uppercase tracking-wider text-forest bg-forest/10 px-2 py-0.5 rounded-sm">{meal.meal_type}</span>
                      <h3 className="font-medium text-charcoal text-lg">{meal.meal_name}</h3>
                    </div>
                    <p className="text-sm text-stone mb-2">{meal.serving_size}</p>
                    
                    {meal.ingredients && meal.ingredients.length > 0 && (
                      <ul className="text-xs text-stone mb-3 list-disc pl-4 line-clamp-2">
                        {meal.ingredients.map((ing: string, idx: number) => (
                          <li key={idx}>{ing}</li>
                        ))}
                      </ul>
                    )}
                    
                    <div className="flex gap-4 text-xs font-medium bg-background border border-border w-max px-3 py-1.5 rounded-sm">
                      <span className="text-forest flex items-center gap-1"><Flame className="w-3 h-3" /> {meal.calories} kcal</span>
                      <span className="text-charcoal border-l border-border pl-4">P: {meal.protein_grams}g</span>
                      <span className="text-charcoal">C: {meal.carbohydrates_grams}g</span>
                      <span className="text-charcoal">F: {meal.fat_grams}g</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2 w-full sm:w-auto border-t border-border sm:border-0 pt-3 sm:pt-0 mt-3 sm:mt-0 justify-end">
                    <button 
                      onClick={() => addToTodayMutation.mutate(meal)}
                      disabled={addToTodayMutation.isPending}
                      className="text-xs font-medium bg-forest text-cream px-3 py-1.5 rounded-sm transition-colors hover:bg-forest/90 disabled:opacity-50"
                    >
                      Log Today
                    </button>
                    <button 
                      onClick={() => { if (window.confirm('Delete this saved meal?')) deleteMutation.mutate(meal.id); }}
                      className="p-1.5 text-stone hover:text-terracotta hover:bg-terracotta/10 rounded-sm transition-colors"
                      title="Delete Saved Meal"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

            {isModalOpen && (
        <MealFormModal 
          isOpen={isModalOpen} 
          onClose={() => { setIsModalOpen(false); setEditingMeal(null); }} 
          onSubmit={async (data: any) => {
            const dt = new Date(selectedDate);
            const now = new Date();
            dt.setHours(now.getHours(), now.getMinutes());
            
            if (editingMeal) {
              await api.patch(`/nutrition/meals/${editingMeal.id}`, { ...data, consumed_at: dt.toISOString() });
            } else {
              await api.post(`/nutrition/meals`, { ...data, consumed_at: dt.toISOString() });
            }
            queryClient.invalidateQueries({ queryKey: ['meals'] });
            queryClient.invalidateQueries({ queryKey: ['daily-summary'] });
            queryClient.invalidateQueries({ queryKey: ['today-meals'] });
            setIsModalOpen(false);
            setEditingMeal(null);
          }}
          initialData={editingMeal}
          title={editingMeal ? "Edit Meal" : "Add Meal"}
        />
      )}
    </div>
  );
}
