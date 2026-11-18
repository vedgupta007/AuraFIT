import { useState, useEffect } from 'react';
import { X, Play, AlertCircle, Info, Dumbbell, Wind, Loader2 } from 'lucide-react';
import api from '../../../lib/axios';

interface ExerciseGuidanceModalProps {
  exercise: any;
  workoutFocus?: string;
  onClose: () => void;
}

export default function ExerciseGuidanceModal({ exercise, workoutFocus, onClose }: ExerciseGuidanceModalProps) {
  const [guidance, setGuidance] = useState<any>(exercise?.guidance || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (exercise && !exercise.guidance) {
      setLoading(true);
      api.post('/plans/workouts/guidance', { 
        exercise_name: exercise.exercise_name,
        workout_focus: workoutFocus || "General fitness"
      })
      .then(res => setGuidance(res.data))
      .catch(() => setError("Unable to load dynamic guidance. Using fallback."))
      .finally(() => setLoading(false));
    } else if (exercise) {
      setGuidance(exercise.guidance);
    }
  }, [exercise, workoutFocus]);

  if (!exercise) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-charcoal/40 backdrop-blur-sm p-4 sm:p-6 fade-in">
      <div className="bg-surface w-full max-w-lg rounded-sm shadow-xl flex flex-col max-h-[90vh] slide-up">
        
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-border flex justify-between items-center bg-cream">
          <h2 className="text-xl font-serif text-charcoal">{exercise.exercise_name}</h2>
          <button onClick={onClose} className="p-2 text-stone hover:text-terracotta transition-colors rounded-sm">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-4 sm:p-5 overflow-y-auto space-y-6">
          <div className="flex gap-4 mb-2">
            <span className="bg-forest/10 text-forest px-3 py-1 text-xs font-semibold uppercase tracking-wider rounded-sm flex items-center gap-1">
              <Dumbbell className="w-3 h-3" /> {exercise.sets} Sets
            </span>
            <span className="bg-forest/10 text-forest px-3 py-1 text-xs font-semibold uppercase tracking-wider rounded-sm flex items-center gap-1">
              <Play className="w-3 h-3" /> {exercise.reps} Reps
            </span>
            <span className="bg-forest/10 text-forest px-3 py-1 text-xs font-semibold uppercase tracking-wider rounded-sm">
               Rest: {exercise.rest}s
            </span>
          </div>

          {loading ? (
             <div className="flex flex-col items-center justify-center p-12 text-stone">
               <Loader2 className="w-8 h-8 animate-spin text-forest mb-4" />
               <p className="text-sm font-medium">Generating guidance...</p>
             </div>
          ) : !guidance ? (
             <div className="bg-background border border-border p-4 rounded-sm text-stone italic text-sm">
               {error || "Detailed step-by-step instructions are not available for this exercise."}
             </div>
          ) : (
            <>
              {/* Media Fallback Placeholder (Could integrate real media here later) */}
              <div className="bg-background border border-border rounded-sm aspect-video flex flex-col items-center justify-center text-stone/50">
                 <Play className="w-12 h-12 mb-2" />
                 <span className="text-sm font-medium">Visual Demonstration</span>
                 <span className="text-xs">Media unavailable. Follow text guidance below.</span>
              </div>

              <div>
                <h3 className="font-semibold text-charcoal flex items-center gap-2 mb-2">
                   Starting Position
                </h3>
                <p className="text-sm text-stone leading-relaxed bg-background p-3 rounded-sm border border-border">
                  {guidance.starting_position || guidance.execution}
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-charcoal flex items-center gap-2 mb-2">
                   Execution
                </h3>
                <p className="text-sm text-stone leading-relaxed bg-background p-3 rounded-sm border border-border">
                  {guidance.execution}
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="bg-background border border-border p-3 rounded-sm">
                   <h4 className="font-semibold text-sm text-charcoal flex items-center gap-1.5 mb-1">
                     <Wind className="w-4 h-4 text-forest" /> Breathing
                   </h4>
                   <p className="text-xs text-stone">{guidance.breathing || "Breathe naturally"}</p>
                </div>
                <div className="bg-background border border-border p-3 rounded-sm">
                   <h4 className="font-semibold text-sm text-charcoal flex items-center gap-1.5 mb-1">
                     <Info className="w-4 h-4 text-forest" /> Common Mistakes
                   </h4>
                   <p className="text-xs text-stone">{guidance.common_mistakes || "None noted"}</p>
                </div>
              </div>

              <div className="bg-terracotta/5 border border-terracotta/20 p-3 rounded-sm flex items-start gap-2">
                 <AlertCircle className="w-4 h-4 text-terracotta shrink-0 mt-0.5" />
                 <p className="text-xs text-terracotta leading-relaxed">
                   <strong>Safety Note:</strong> {guidance.safety || "Stop if you feel sharp pain or discomfort in your joints."}
                 </p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}