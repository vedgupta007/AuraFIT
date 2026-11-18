import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Calendar as CalIcon, Activity, RefreshCw, CheckCircle2, ChevronDown, ChevronUp, Info } from 'lucide-react';
import ExerciseGuidanceModal from './components/ExerciseGuidanceModal';

export default function WorkoutPlannerPage() {
  const queryClient = useQueryClient();
  const [expandedWorkouts, setExpandedWorkouts] = useState<string[]>([]);
  const [selectedExercise, setSelectedExercise] = useState<any | null>(null);
  
  const today = new Date();
  const upcomingDays = Array.from({ length: 7 }).map((_, i) => {
    const d = new Date(today);
    d.setDate(today.getDate() + i);
    return d.toISOString().split('T')[0];
  });

  const { data: plans, isLoading } = useQuery({
    queryKey: ['workout-plans', upcomingDays[0], upcomingDays[6]],
    queryFn: async () => {
      const res = await api.get(`/plans/workouts?start_date=${upcomingDays[0]}&end_date=${upcomingDays[6]}`);
      return res.data;
    }
  });

  const generateMutation = useMutation({
    mutationFn: async (dateStr: string) => {
      const res = await api.post(`/plans/workouts/generate?target_date=${dateStr}`);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workout-plans'] });
    }
  });
  
  const completeMutation = useMutation({
    mutationFn: async (planId: string) => {
      const res = await api.post(`/plans/workouts/${planId}/complete`);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workout-plans'] });
      queryClient.invalidateQueries({ queryKey: ['workouts'] }); // Update diary
    }
  });

  const toggleExpand = (dateStr: string) => {
    setExpandedWorkouts(prev => 
      prev.includes(dateStr) ? prev.filter(d => d !== dateStr) : [...prev, dateStr]
    );
  };

  if (isLoading) {
    return <div className="p-8 text-center text-stone">Loading planner...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 fade-in p-4 sm:p-0">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-serif text-forest flex items-center gap-3">
            <CalIcon className="w-8 h-8" /> Workout Planner
          </h1>
          <p className="text-stone mt-1">AI-generated training schedules tailored to your strategy.</p>
        </div>
      </div>

      <div className="bg-surface border border-border rounded-sm shadow-sm overflow-hidden">
        <div className="divide-y divide-border">
          {upcomingDays.map((dateStr, i) => {
            const dateObj = new Date(dateStr);
            const isToday = i === 0;
            const plan = plans?.find((w: any) => w.date === dateStr);
            const isExpanded = expandedWorkouts.includes(dateStr);

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
                      <p className="text-sm text-stone mt-1 italic">Rest day / No workout scheduled</p>
                    ) : (
                      <div className="mt-2 w-full">
                        <div className="flex items-center justify-between gap-2 mb-1 w-full">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-1 rounded-sm ${plan.status === 'completed' ? 'bg-forest/10 text-forest' : plan.status === 'accepted' ? 'bg-charcoal/10 text-charcoal' : 'bg-terracotta/10 text-terracotta'}`}>
                              {plan.status}
                            </span>
                            <span className="text-charcoal font-medium">{plan.workout_title}</span>
                          </div>
                          
                          <div className="flex items-center gap-2 shrink-0">
                            {plan.status === 'generated' && (
                              <button 
                                onClick={() => generateMutation.mutate(dateStr)}
                                className="p-1.5 text-stone hover:text-forest hover:bg-forest/10 rounded-sm"
                                title="Regenerate"
                              >
                                <RefreshCw className="w-4 h-4" />
                              </button>
                            )}
                            {plan.status !== 'completed' && (
                              <button 
                                onClick={() => completeMutation.mutate(plan.id)}
                                disabled={completeMutation.isPending}
                                className="hidden sm:flex items-center gap-1 text-sm font-medium bg-forest text-cream px-3 py-1.5 rounded-sm transition-colors hover:bg-forest/90 disabled:opacity-50"
                              >
                                <CheckCircle2 className="w-4 h-4" /> Complete
                              </button>
                            )}
                          </div>
                        </div>
                        
                        <p className="text-xs text-stone mb-4">{plan.focus} &bull; ~{plan.estimated_duration_minutes} min</p>
                        
                        <div className="space-y-2 w-full max-w-2xl">
                          {plan.exercises?.slice(0, isExpanded ? plan.exercises.length : 3).map((ex: any, idx: number) => (
                            <div key={idx} className="bg-background border border-border rounded-sm p-3 flex justify-between items-center group">
                               <div className="flex items-center gap-2 text-sm text-charcoal">
                                  <Activity className="w-4 h-4 text-forest shrink-0" />
                                  <span className="font-medium whitespace-normal break-words">{ex.exercise_name}</span>
                                  <span className="text-stone hidden sm:inline">&bull; {ex.sets}x{ex.reps}</span>
                               </div>
                               <button 
                                  onClick={() => setSelectedExercise(ex)}
                                  className="text-xs font-medium text-stone hover:text-forest flex items-center gap-1 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity whitespace-nowrap shrink-0 ml-2"
                               >
                                  <Info className="w-3 h-3" /> Guidance
                               </button>
                            </div>
                          ))}
                          
                          {plan.exercises?.length > 3 && (
                            <button 
                              onClick={() => toggleExpand(dateStr)}
                              className="text-xs font-medium text-forest hover:underline flex items-center gap-1 mt-2 w-full justify-center sm:justify-start"
                            >
                              {isExpanded ? (
                                <><ChevronUp className="w-3 h-3" /> Show fewer</>
                              ) : (
                                <><ChevronDown className="w-3 h-3" /> Show all {plan.exercises.length} exercises</>
                              )}
                            </button>
                          )}
                        </div>
                        
                        {/* Mobile complete button */}
                        {plan.status !== 'completed' && (
                          <button 
                            onClick={() => completeMutation.mutate(plan.id)}
                            disabled={completeMutation.isPending}
                            className="w-full sm:hidden mt-4 flex items-center justify-center gap-1 text-sm font-medium bg-forest text-cream px-3 py-2 rounded-sm transition-colors hover:bg-forest/90 disabled:opacity-50"
                          >
                            <CheckCircle2 className="w-4 h-4" /> Mark Complete
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                </div>
                
                {/* Generate Button state if no plan */}
                {!plan && (
                  <div className="w-full sm:w-auto mt-4 sm:mt-0 flex justify-end">
                    <button 
                      onClick={() => generateMutation.mutate(dateStr)}
                      disabled={generateMutation.isPending}
                      className="text-sm font-medium bg-background border border-border text-charcoal hover:text-forest hover:border-forest/30 px-3 py-1.5 rounded-sm transition-colors flex items-center gap-1 disabled:opacity-50 w-full sm:w-auto justify-center"
                    >
                      <RefreshCw className={`w-3 h-3 ${generateMutation.isPending ? 'animate-spin' : ''}`} /> Generate
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      <ExerciseGuidanceModal 
        exercise={selectedExercise} 
        onClose={() => setSelectedExercise(null)} 
      />
    </div>
  );
}