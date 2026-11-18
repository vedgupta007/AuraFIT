import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Search, Apple, Filter, X, Bot } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function FoodLibraryPage() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [diet, setDiet] = useState('');
  const [page, setPage] = useState(1);
  const [showFilters, setShowFilters] = useState(false);
  
  // Create search state applied on submit/delay to prevent bouncing
  const [appliedSearch, setAppliedSearch] = useState('');
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setAppliedSearch(search);
    setPage(1);
  };
  
  const clearFilters = () => {
    setCategory('');
    setDiet('');
    setSearch('');
    setAppliedSearch('');
    setPage(1);
  };
  
  const buildQueryParams = () => {
    const params = new URLSearchParams();
    if (appliedSearch) params.append('search', appliedSearch);
    if (category) params.append('category', category);
    if (diet === 'vegetarian') params.append('is_vegetarian', 'true');
    if (diet === 'vegan') params.append('is_vegan', 'true');
    if (diet === 'eggetarian') params.append('is_eggetarian', 'true');
    params.append('page', page.toString());
    params.append('limit', '12');
    return params.toString();
  };

  const { data, isLoading, isError } = useQuery({
    queryKey: ['foods', appliedSearch, category, diet, page],
    queryFn: async (): Promise<any> => {
      const res = await api.get(`/foods?${buildQueryParams()}`);
      return res.data;
    },
    placeholderData: (prev) => prev
  });

  return (
    <div className="p-4 sm:p-8 max-w-7xl mx-auto fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-heading font-semibold text-forest">Food Knowledge Base</h1>
        <p className="text-stone mt-1">Browse our verified database of foods and nutritional values.</p>
      </div>

      <div className="flex flex-col md:flex-row gap-6 mb-8">
        <div className="flex-1">
          <form onSubmit={handleSearch} className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-stone w-5 h-5" />
            <input 
              type="text" 
              placeholder="Search for foods (e.g., Paneer, Apple)..."
              className="w-full pl-10 pr-4 py-3 bg-surface border border-border rounded-sm focus:border-forest outline-none transition-colors shadow-sm"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <button type="submit" className="hidden">Search</button>
          </form>
        </div>
        
        <button 
          onClick={() => setShowFilters(!showFilters)}
          className="md:hidden flex items-center gap-2 px-4 py-3 bg-surface border border-border rounded-sm font-medium text-forest justify-center"
        >
          <Filter className="w-4 h-4" /> Filters
        </button>
        
        <div className={`md:flex items-center gap-4 ${showFilters ? 'flex flex-col' : 'hidden'}`}>
          <select 
            value={category} 
            onChange={(e) => { setCategory(e.target.value); setPage(1); }}
            className="w-full md:w-auto px-4 py-3 bg-surface border border-border rounded-sm text-charcoal outline-none focus:border-forest"
          >
            <option value="">All Categories</option>
            <option value="Grains">Grains</option>
            <option value="Fruits">Fruits</option>
            <option value="Vegetables">Vegetables</option>
            <option value="Dairy">Dairy</option>
            <option value="Meat">Meat</option>
            <option value="Eggs">Eggs</option>
            <option value="Legumes">Legumes</option>
            <option value="Nuts and Seeds">Nuts and Seeds</option>
          </select>
          
          <select 
            value={diet} 
            onChange={(e) => { setDiet(e.target.value); setPage(1); }}
            className="w-full md:w-auto px-4 py-3 bg-surface border border-border rounded-sm text-charcoal outline-none focus:border-forest"
          >
            <option value="">Any Diet</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="eggetarian">Eggetarian</option>
          </select>
          
          {(category || diet || appliedSearch) && (
            <button onClick={clearFilters} className="text-sm text-terracotta hover:underline flex items-center gap-1">
              <X className="w-4 h-4" /> Clear
            </button>
          )}
        </div>
      </div>

      {isError ? (
        <div className="bg-terracotta/10 text-terracotta p-6 rounded-sm border border-terracotta/20 text-center">
          <p>Failed to load foods. Please try again later.</p>
        </div>
      ) : isLoading && !data ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {[1,2,3,4,5,6].map(i => (
            <div key={i} className="h-48 bg-surface animate-pulse rounded-sm border border-border"></div>
          ))}
        </div>
      ) : data?.items.length === 0 ? (
        <div className="text-center py-16 bg-surface border border-border rounded-sm">
          <Apple className="w-12 h-12 text-stone mx-auto mb-4 opacity-50" />
          <h3 className="text-xl font-heading text-forest mb-2">No foods found</h3>
          <p className="text-stone max-w-md mx-auto">We couldn't find any foods matching your search criteria. Try adjusting your filters.</p>
          <button onClick={clearFilters} className="mt-6 px-6 py-2 bg-forest text-cream rounded-sm">Reset Filters</button>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mb-8">
            {data?.items.map((food: any) => (
              <div key={food.id} className="bg-surface border border-border p-6 rounded-sm shadow-sm hover:shadow-md transition-shadow group">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <span className="text-xs font-semibold uppercase tracking-wider text-stone mb-1 block">{food.category}</span>
                    <h3 className="text-xl font-heading text-forest group-hover:text-terracotta transition-colors">{food.name}</h3>
                  </div>
                  {food.is_vegetarian && !food.is_vegan && (
                    <span className="w-3 h-3 rounded-full bg-forest flex-shrink-0" title="Vegetarian"></span>
                  )}
                  {food.is_vegan && (
                    <span className="w-3 h-3 rounded-full bg-forest flex-shrink-0" title="Vegan"></span>
                  )}
                  {food.is_eggetarian && !food.is_vegetarian && !food.is_vegan && (
                    <span className="w-3 h-3 rounded-full bg-terracotta flex-shrink-0" title="Eggetarian"></span>
                  )}
                  {!food.is_vegetarian && !food.is_vegan && !food.is_eggetarian && (
                    <span className="w-3 h-3 rounded-full bg-charcoal flex-shrink-0" title="Non-Vegetarian"></span>
                  )}
                </div>
                
                <div className="mb-4">
                  <div className="text-sm text-stone mb-2">Serving: {food.serving_size} {food.serving_unit}</div>
                  <div className="flex gap-4">
                    <div>
                      <div className="text-lg font-semibold text-charcoal">{food.calories}</div>
                      <div className="text-xs text-stone uppercase tracking-wide">kcal</div>
                    </div>
                    <div>
                      <div className="text-lg font-semibold text-charcoal">{food.protein}</div>
                      <div className="text-xs text-stone uppercase tracking-wide">Protein (g)</div>
                    </div>
                    <div>
                      <div className="text-lg font-semibold text-charcoal">{food.carbohydrates}</div>
                      <div className="text-xs text-stone uppercase tracking-wide">Carbs (g)</div>
                    </div>
                  </div>
                </div>
                
                <div className="pt-4 border-t border-border flex justify-between items-center text-sm">
                  <span className="text-stone">
                    Fat: {food.fat}g | Fiber: {food.fiber}g
                  </span>
                  {food.allergens?.length > 0 && (
                    <span className="text-terracotta font-medium text-xs bg-terracotta/10 px-2 py-1 rounded-sm">
                      {food.allergens.join(', ')}
                    </span>
                  )}
                </div>
                <div className="mt-4 pt-4 border-t border-border flex justify-end">
                  <Link to={`/ai/chat?food_id=${food.id}`} className="flex items-center gap-2 text-xs font-medium text-forest hover:text-terracotta transition-colors">
                    <Bot className="w-4 h-4" /> Ask AI about this food
                  </Link>
                </div>
              </div>
            ))}
          </div>
          
          {/* Pagination */}
          {data && data.pages > 1 && (
            <div className="flex justify-center items-center gap-4 pt-4">
              <button 
                disabled={page === 1}
                onClick={() => setPage(p => p - 1)}
                className="px-4 py-2 border border-border rounded-sm text-forest disabled:opacity-50 font-medium"
              >
                Previous
              </button>
              <span className="text-stone text-sm">Page {page} of {data.pages}</span>
              <button 
                disabled={page === data.pages}
                onClick={() => setPage(p => p + 1)}
                className="px-4 py-2 border border-border rounded-sm text-forest disabled:opacity-50 font-medium"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}





