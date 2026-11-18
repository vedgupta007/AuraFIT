import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Search, Activity, Filter, X, ChevronDown, ChevronUp } from 'lucide-react';

export default function ExerciseLibraryPage() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [equipment, setEquipment] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [page, setPage] = useState(1);
  const [showFilters, setShowFilters] = useState(false);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  
  const [appliedSearch, setAppliedSearch] = useState('');
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setAppliedSearch(search);
    setPage(1);
  };
  
  const clearFilters = () => {
    setCategory('');
    setEquipment('');
    setDifficulty('');
    setSearch('');
    setAppliedSearch('');
    setPage(1);
  };
  
  const buildQueryParams = () => {
    const params = new URLSearchParams();
    if (appliedSearch) params.append('search', appliedSearch);
    if (category) params.append('category', category);
    if (equipment) params.append('equipment', equipment);
    if (difficulty) params.append('difficulty', difficulty);
    params.append('page', page.toString());
    params.append('limit', '12');
    return params.toString();
  };

  const { data, isLoading, isError } = useQuery({
    queryKey: ['exercises', appliedSearch, category, equipment, difficulty, page],
    queryFn: async (): Promise<any> => {
      const res = await api.get(`/exercises?${buildQueryParams()}`);
      return res.data;
    },
    placeholderData: (prev) => prev
  });

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  return (
    <div className="p-4 sm:p-8 max-w-7xl mx-auto fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-heading font-semibold text-forest">Exercise Library</h1>
        <p className="text-stone mt-1">Discover exercises with step-by-step instructions and muscle targets.</p>
      </div>

      <div className="flex flex-col xl:flex-row gap-6 mb-8">
        <div className="flex-1">
          <form onSubmit={handleSearch} className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-stone w-5 h-5" />
            <input 
              type="text" 
              placeholder="Search for exercises (e.g., Squats, Plank)..."
              className="w-full pl-10 pr-4 py-3 bg-surface border border-border rounded-sm focus:border-forest outline-none transition-colors shadow-sm"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <button type="submit" className="hidden">Search</button>
          </form>
        </div>
        
        <button 
          onClick={() => setShowFilters(!showFilters)}
          className="xl:hidden flex items-center gap-2 px-4 py-3 bg-surface border border-border rounded-sm font-medium text-forest justify-center"
        >
          <Filter className="w-4 h-4" /> Filters
        </button>
        
        <div className={`xl:flex items-center gap-4 ${showFilters ? 'flex flex-col' : 'hidden'}`}>
          <select 
            value={category} 
            onChange={(e) => { setCategory(e.target.value); setPage(1); }}
            className="w-full xl:w-auto px-4 py-3 bg-surface border border-border rounded-sm text-charcoal outline-none focus:border-forest"
          >
            <option value="">All Categories</option>
            <option value="Strength">Strength</option>
            <option value="Cardio">Cardio</option>
            <option value="Core">Core</option>
            <option value="Mobility">Mobility</option>
            <option value="Flexibility">Flexibility</option>
          </select>
          
          <select 
            value={difficulty} 
            onChange={(e) => { setDifficulty(e.target.value); setPage(1); }}
            className="w-full xl:w-auto px-4 py-3 bg-surface border border-border rounded-sm text-charcoal outline-none focus:border-forest"
          >
            <option value="">All Difficulties</option>
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>

          <select 
            value={equipment} 
            onChange={(e) => { setEquipment(e.target.value); setPage(1); }}
            className="w-full xl:w-auto px-4 py-3 bg-surface border border-border rounded-sm text-charcoal outline-none focus:border-forest"
          >
            <option value="">Any Equipment</option>
            <option value="Bodyweight">Bodyweight</option>
            <option value="Dumbbells">Dumbbells</option>
            <option value="Barbell">Barbell</option>
            <option value="Machine">Machine</option>
            <option value="Cable Machine">Cable Machine</option>
            <option value="Resistance Band">Resistance Band</option>
          </select>
          
          {(category || difficulty || equipment || appliedSearch) && (
            <button onClick={clearFilters} className="text-sm text-terracotta hover:underline flex items-center gap-1">
              <X className="w-4 h-4" /> Clear
            </button>
          )}
        </div>
      </div>

      {isError ? (
        <div className="bg-terracotta/10 text-terracotta p-6 rounded-sm border border-terracotta/20 text-center">
          <p>Failed to load exercises. Please try again later.</p>
        </div>
      ) : isLoading && !data ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1,2,3,4].map(i => (
            <div key={i} className="h-48 bg-surface animate-pulse rounded-sm border border-border"></div>
          ))}
        </div>
      ) : data?.items.length === 0 ? (
        <div className="text-center py-16 bg-surface border border-border rounded-sm">
          <Activity className="w-12 h-12 text-stone mx-auto mb-4 opacity-50" />
          <h3 className="text-xl font-heading text-forest mb-2">No exercises found</h3>
          <p className="text-stone max-w-md mx-auto">We couldn't find any exercises matching your search criteria. Try adjusting your filters.</p>
          <button onClick={clearFilters} className="mt-6 px-6 py-2 bg-forest text-cream rounded-sm">Reset Filters</button>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {data?.items.map((ex: any) => (
              <div key={ex.id} className="bg-surface border border-border rounded-sm shadow-sm hover:shadow-md transition-shadow">
                <div 
                  className="p-6 cursor-pointer"
                  onClick={() => toggleExpand(ex.id)}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <span className="text-xs font-semibold uppercase tracking-wider text-stone mb-1 block">{ex.category} • {ex.difficulty}</span>
                      <h3 className="text-xl font-heading text-forest">{ex.name}</h3>
                    </div>
                    {expandedId === ex.id ? (
                      <ChevronUp className="w-5 h-5 text-stone" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-stone" />
                    )}
                  </div>
                  
                  <p className="text-charcoal text-sm mb-4 line-clamp-2">{ex.description}</p>
                  
                  <div className="flex flex-wrap gap-2 text-xs">
                    <span className="bg-forest/10 text-forest px-2 py-1 rounded-sm font-medium border border-forest/20">
                      Muscle: {ex.primary_muscle}
                    </span>
                    <span className="bg-stone/10 text-charcoal px-2 py-1 rounded-sm border border-border">
                      Equipment: {ex.equipment}
                    </span>
                  </div>
                </div>

                {expandedId === ex.id && (
                  <div className="px-6 pb-6 pt-2 border-t border-border bg-stone/5 fade-in">
                    <div className="mb-4">
                      <h4 className="text-sm font-semibold text-forest mb-2 uppercase tracking-wider">Instructions</h4>
                      <ol className="list-decimal pl-5 space-y-1 text-sm text-charcoal">
                        {ex.instructions.map((step: string, i: number) => (
                          <li key={i} className="pl-1">{step}</li>
                        ))}
                      </ol>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm mt-4 pt-4 border-t border-border">
                      {ex.sets_recommendation && (
                        <div>
                          <span className="block text-stone text-xs uppercase tracking-wide">Rec. Sets</span>
                          <span className="font-medium">{ex.sets_recommendation}</span>
                        </div>
                      )}
                      {ex.reps_recommendation && (
                        <div>
                          <span className="block text-stone text-xs uppercase tracking-wide">Rec. Reps</span>
                          <span className="font-medium">{ex.reps_recommendation}</span>
                        </div>
                      )}
                      {ex.duration_seconds && (
                        <div>
                          <span className="block text-stone text-xs uppercase tracking-wide">Duration</span>
                          <span className="font-medium">{ex.duration_seconds}s</span>
                        </div>
                      )}
                    </div>

                    {ex.safety_notes && (
                      <div className="mt-4 p-3 bg-terracotta/10 border border-terracotta/20 rounded-sm">
                        <h4 className="text-xs font-bold text-terracotta uppercase tracking-wide mb-1">Safety Note</h4>
                        <p className="text-sm text-terracotta/90">{ex.safety_notes}</p>
                      </div>
                    )}
                  </div>
                )}
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


