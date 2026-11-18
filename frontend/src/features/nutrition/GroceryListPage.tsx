import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../../lib/axios';
import { ShoppingCart, CheckCircle2, Circle, AlertCircle, Plus, Trash2 } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

export default function GroceryListPage() {
  const { user } = useAuthStore();
  const today = new Date();
  
  // Look 7 days ahead
  const endDate = new Date(today);
  endDate.setDate(today.getDate() + 7);

  const { data: meals, isLoading } = useQuery({
    queryKey: ['planned-meals-week', today.toISOString().split('T')[0], endDate.toISOString().split('T')[0]],
    queryFn: async () => {
      const start = new Date(today);
      start.setHours(0, 0, 0, 0);
      const end = new Date(endDate);
      end.setHours(23, 59, 59, 999);
      const res = await api.get(`/plans/meals?&start_date=${start.toISOString()}&end_date=${end.toISOString()}`);
      return res.data;
    }
  });

  const [items, setItems] = useState<{id: string, name: string, checked: boolean, custom: boolean}[]>([]);
  const [newItemName, setNewItemName] = useState('');

  // Load from local storage and sync with meals
  useEffect(() => {
    if (!meals || !user) return;
    
    const storageKey = `aurafit_grocery_${user.id}`;
    const saved = localStorage.getItem(storageKey);
    let currentItems: any[] = saved ? JSON.parse(saved) : [];

    // Extract ingredients from meals (assuming meal_name implies the main ingredients for now, or just list the meals)
    const mealNames = Array.from(new Set(meals.flatMap((p: any) => p.meals.map((m: any) => m.meal_name))));
    
    // Add any new meals that aren't in the list
    mealNames.forEach((name: any) => {
      if (!currentItems.find(i => i.name === name && !i.custom)) {
        currentItems.push({ id: `meal-${name}-${Date.now()}`, name, checked: false, custom: false });
      }
    });

    setItems(currentItems);
  }, [meals, user]);

  const saveItems = (newItems: any[]) => {
    setItems(newItems);
    if (user) {
      localStorage.setItem(`aurafit_grocery_${user.id}`, JSON.stringify(newItems));
    }
  };

  const toggleCheck = (id: string) => {
    saveItems(items.map(item => item.id === id ? { ...item, checked: !item.checked } : item));
  };

  const removeCustomItem = (id: string) => {
    saveItems(items.filter(item => item.id !== id));
  };

  const handleAddItem = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newItemName.trim()) return;
    saveItems([...items, { id: `custom-${Date.now()}`, name: newItemName.trim(), checked: false, custom: true }]);
    setNewItemName('');
  };

  const clearChecked = () => {
    saveItems(items.filter(item => !item.checked));
  };

  if (isLoading) {
    return <div className="p-8 text-center text-stone">Generating grocery list...</div>;
  }

  const unchecked = items.filter(i => !i.checked);
  const checked = items.filter(i => i.checked);

  return (
    <div className="max-w-3xl mx-auto space-y-6 fade-in p-4 sm:p-0">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div>
          <h1 className="text-3xl font-serif text-forest flex items-center gap-3">
            <ShoppingCart className="w-8 h-8" /> Grocery List
          </h1>
          <p className="text-stone mt-1">Generated from your upcoming 7-day meal plan.</p>
        </div>
        {checked.length > 0 && (
          <button 
            onClick={clearChecked}
            className="text-sm font-medium text-terracotta hover:underline bg-terracotta/10 px-3 py-1.5 rounded-sm"
          >
            Clear Checked
          </button>
        )}
      </div>

      <div className="bg-surface border border-border p-4 sm:p-6 rounded-sm shadow-sm">
        <form onSubmit={handleAddItem} className="flex gap-2 mb-6">
          <input 
            type="text" 
            placeholder="Add custom item..." 
            value={newItemName}
            onChange={e => setNewItemName(e.target.value)}
            className="flex-1 bg-background border border-border px-4 py-2 rounded-sm focus:border-forest outline-none transition-colors"
          />
          <button type="submit" className="bg-forest text-cream px-4 py-2 rounded-sm hover:bg-forest/90 transition-colors flex items-center gap-2">
            <Plus className="w-4 h-4" /> Add
          </button>
        </form>

        {items.length === 0 ? (
          <div className="text-center py-12 text-stone">
            <AlertCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p>Your list is empty. Log some future meals or add items manually!</p>
          </div>
        ) : (
          <div className="space-y-6">
            {unchecked.length > 0 && (
              <ul className="space-y-2">
                {unchecked.map(item => (
                  <li key={item.id} className="flex items-center justify-between p-3 bg-background border border-border rounded-sm hover:border-forest/30 transition-colors group">
                    <button onClick={() => toggleCheck(item.id)} className="flex items-center gap-3 flex-1 text-left">
                      <Circle className="w-5 h-5 text-stone group-hover:text-forest transition-colors" />
                      <span className="text-charcoal font-medium">{item.name}</span>
                    </button>
                    {item.custom && (
                      <button onClick={() => removeCustomItem(item.id)} className="text-stone hover:text-terracotta p-1">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            )}

            {checked.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wider text-stone mb-3 px-1">Completed</h3>
                <ul className="space-y-2 opacity-60">
                  {checked.map(item => (
                    <li key={item.id} className="flex items-center justify-between p-3 bg-background border border-border rounded-sm text-stone line-through">
                      <button onClick={() => toggleCheck(item.id)} className="flex items-center gap-3 flex-1 text-left">
                        <CheckCircle2 className="w-5 h-5 text-forest" />
                        <span>{item.name}</span>
                      </button>
                      {item.custom && (
                        <button onClick={() => removeCustomItem(item.id)} className="hover:text-terracotta p-1">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
