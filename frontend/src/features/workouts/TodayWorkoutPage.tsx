import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { PlayCircle, Calendar, CheckCircle2, Clock, Activity, Info } from 'lucide-react';
import { Link } from 'react-router-dom';
import ExerciseGuidanceModal from './components/ExerciseGuidanceModal';

export default function TodayWorkoutPage() {
  const queryClient = useQueryClient();
  const [selectedExercise, setSelectedExercise] = useState<any | null>(null);

  const { data: plan, isLoading } = useQuery({
    queryKey: ['today-workout'],
    queryFn: async () => {
      try {
        const res = await api.get('/plans/workouts/today');
        return res.data;
      } catch (e: any) {
        if (e.response?.status === 404) return null;
        throw e;
      }
    },
    retry: false
  });

  const completeMutation = useMutation({
    mutationFn: async (planId: string) => {
      const res = await api.post(`/plans/workouts/${planId}/complete`);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['today-workout'] });
      queryClient.invalidateQueries({ queryKey: ['workouts'] });
    }
  });

  if (isLoading) {
    return <div className="p-8 text-center text-stone">Loading today's session...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8 fade-in p-4 sm:p-0">
      <div className="text-center mb-10">
        <div className="w-16 h-16 bg-cream rounded-full flex items-center justify-center mx-auto mb-4 border border-border shadow-sm">
          <PlayCircle className="w-8 h-8 text-forest" />
        </div>
        <h1 className="text-3xl font-serif text-charcoal mb-2">Today's Session</h1>
        <p className="text-stone">{new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}</p>
      </div>

      {!plan ? (
        <div className="bg-surface p-12 text-center rounded-sm border border-border shadow-sm">
          <Calendar className="w-12 h-12 text-stone/50 mx-auto mb-4" />
          <h3 className="text-xl font-serif text-charcoal mb-2">No Workout Scheduled</h3>
          <p className="text-stone mb-6 max-w-sm mx-auto">Take a rest day, or head to the Workout Planner to generate a session.</p>
          <Link 
            to="/workout-planner"
            className="inline-flex items-center gap-2 bg-forest text-cream px-5 py-2.5 rounded-sm font-medium hover:bg-forest/90 transition-colors"
          >
            Go to Workout Planner
          </Link>
        </div>
      ) : (
        <div className="bg-surface border border-border rounded-sm shadow-sm overflow-hidden">
          <div className="p-6 border-b border-border bg-background flex flex-col sm:flex-row justify-between items-start gap-4">
            <div>
              <div className="flex items-center gap-3 mb-1 flex-wrap">
                <h2 className="text-2xl font-serif text-charcoal">{plan.workout_title}</h2>
                <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-1 rounded-sm ${plan.status === 'completed' ? 'bg-forest/10 text-forest' : plan.status === 'accepted' ? 'bg-charcoal/10 text-charcoal' : 'bg-terracotta/10 text-terracotta'}`}>
                  {plan.status}
                </span>
              </div>
              <p className="text-stone">{plan.focus}</p>
            </div>
            
            <div className="flex items-center gap-4 text-sm text-stone bg-surface px-4 py-2 border border-border rounded-sm w-full sm:w-auto shrink-0 justify-center">
              <span className="flex items-center gap-1.5 font-medium"><Clock className="w-4 h-4" /> ~{plan.estimated_duration_minutes} min</span>
            </div>
          </div>

          <div className="p-6">
            <h3 className="font-semibold text-charcoal mb-4 uppercase tracking-wider text-xs">Exercises ({plan.exercises?.length || 0})</h3>
            
            <div className="space-y-3">
              {plan.exercises?.map((ex: any, idx: number) => (
                <div key={idx} className="bg-background border border-border rounded-sm p-4 hover:border-forest/50 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3 group">
                  <div className="flex items-start sm:items-center gap-3">
                    <div className="w-8 h-8 rounded-sm bg-forest/10 text-forest flex items-center justify-center font-bold text-sm shrink-0">
                      {idx + 1}
                    </div>
                    <div>
                      <h4 className="font-medium text-charcoal flex items-center gap-2 whitespace-normal break-words">{ex.exercise_name}</h4>
                      <div className="flex gap-3 text-xs text-stone mt-1">
                        <span className="flex items-center gap-1"><Activity className="w-3 h-3" /> {ex.sets} sets &times; {ex.reps} reps</span>
                        {ex.rest > 0 && <span>&bull; {ex.rest}s rest</span>}
                      </div>
                    </div>
                  </div>
                  
                  <button 
                    onClick={() => setSelectedExercise(ex)}
                    className="text-sm font-medium text-forest border border-forest/30 bg-forest/5 px-3 py-1.5 rounded-sm hover:bg-forest/10 transition-colors flex items-center gap-1 justify-center w-full sm:w-auto shrink-0"
                  >
                    <Info className="w-4 h-4" /> Guidance
                  </button>
                </div>
              ))}
            </div>

            {plan.status !== 'completed' && (
              <div className="mt-8 pt-6 border-t border-border flex justify-end">
                <button 
                  onClick={() => completeMutation.mutate(plan.id)}
                  disabled={completeMutation.isPending}
                  className="w-full sm:w-auto flex justify-center items-center gap-2 bg-forest text-cream px-8 py-3 rounded-sm font-medium hover:bg-forest/90 transition-colors disabled:opacity-50"
                >
                  <CheckCircle2 className="w-5 h-5" /> Mark Workout Complete
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      <ExerciseGuidanceModal 
        exercise={selectedExercise} 
        onClose={() => setSelectedExercise(null)} 
      />
    </div>
  );
}