import { useQuery } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Calendar, Activity, Flame, Dumbbell, Target, CheckCircle2, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function DailyOverviewPage() {
  const today = new Date().toISOString().split('T')[0];

  const { data: profile, isLoading: isProfileLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: async () => {
      const res = await api.get('/profile');
      return res.data;
    }
  });

  const { data: summary, isLoading: isSummaryLoading } = useQuery({
    queryKey: ['daily-summary', today],
    queryFn: async () => {
      const tzOffset = -new Date().getTimezoneOffset();
      const res = await api.get(`/nutrition/daily-summary?date=${today}&tz_offset_minutes=${tzOffset}`);
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

  const { data: mealPlan } = useQuery({
    queryKey: ['planned-meals', today],
    queryFn: async () => {
      const res = await api.get(`/plans/meals?start_date=${today}&end_date=${today}`);
      return res.data && res.data.length > 0 ? res.data[0] : null;
    }
  });

  const { data: workoutPlan } = useQuery({
    queryKey: ['today-workout'],
    queryFn: async () => {
      const res = await api.get('/plans/workouts/today');
      return res.data;
    },
    retry: false
  });

  if (isProfileLoading || isSummaryLoading) {
    return <div className="p-8 text-center text-stone">Loading your daily overview...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 fade-in p-4 sm:p-0">
      <header className="bg-surface border border-border p-8 rounded-sm shadow-sm relative overflow-hidden">
        <div className="relative z-10">
          <div className="flex items-center gap-3 text-stone mb-2">
            <Calendar className="w-5 h-5 text-forest" />
            <span className="font-medium">{new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}</span>
          </div>
          <h1 className="text-3xl font-serif text-charcoal mb-2">Today's Overview</h1>
          <p className="text-stone">Your personalized snapshot for the day.</p>
        </div>
      </header>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Nutrition Overview */}
        <section className="bg-surface border border-border p-6 rounded-sm shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-serif text-forest flex items-center gap-2">
              <Flame className="w-5 h-5" /> Nutrition Status
            </h2>
            <Link to="/meal-planner" className="text-sm font-medium text-stone hover:text-forest transition-colors underline">Meal Planner</Link>
          </div>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-charcoal font-medium">Calories Eaten</span>
                <span className="text-stone">{summary?.total_calories || 0} / {goals?.daily_calories || 0} kcal</span>
              </div>
              <div className="h-2 bg-background rounded-full overflow-hidden border border-border">
                <div 
                  className="h-full bg-terracotta transition-all duration-500"
                  style={{ width: `${Math.min(((summary?.total_calories || 0) / (goals?.daily_calories || 1)) * 100, 100)}%` }}
                ></div>
              </div>
            </div>
          </div>
          <div className="mt-6 pt-4 border-t border-border">
            <h3 className="text-sm font-medium text-stone mb-3 uppercase tracking-wider flex justify-between">
              <span>Today's Planned Meals</span>
              {mealPlan && (
                <span className={`px-2 py-0.5 rounded-sm text-[10px] ${mealPlan.status === 'completed' ? 'bg-forest/10 text-forest' : 'bg-charcoal/10 text-charcoal'}`}>
                  {mealPlan.status}
                </span>
              )}
            </h3>
            {mealPlan && mealPlan.meals && mealPlan.meals.length > 0 ? (
              <ul className="space-y-2">
                {mealPlan.meals.map((m: any, idx: number) => (
                  <li key={idx} className="flex justify-between text-sm bg-background p-2 rounded-sm border border-border text-charcoal">
                    <span className="capitalize">{m.meal_type}: {m.meal_name}</span>
                    <span className="font-medium text-forest">{m.calories} kcal</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-sm text-stone italic bg-background p-3 rounded-sm border border-border">
                No meals planned for today. <Link to="/meal-planner" className="text-forest hover:underline">Generate a plan.</Link>
              </div>
            )}
          </div>
        </section>

        {/* Workout Overview */}
        <section className="bg-surface border border-border p-6 rounded-sm shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-serif text-forest flex items-center gap-2">
              <Activity className="w-5 h-5" /> Today's Training
            </h2>
            <Link to="/workout/today" className="text-sm font-medium text-stone hover:text-forest transition-colors underline">View Details</Link>
          </div>
          
          <div className="space-y-4">
            {workoutPlan ? (
              <div className="bg-background border border-border p-4 rounded-sm">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h3 className="font-medium text-charcoal">{workoutPlan.workout_title}</h3>
                    <p className="text-sm text-stone mt-1">{workoutPlan.focus}</p>
                  </div>
                  {workoutPlan.status === 'completed' && <CheckCircle2 className="w-5 h-5 text-forest" />}
                </div>
                <div className="flex items-center gap-4 text-xs text-stone mt-4 pt-3 border-t border-border">
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> ~{workoutPlan.estimated_duration_minutes} min</span>
                  <span className="flex items-center gap-1"><Dumbbell className="w-3 h-3" /> {workoutPlan.exercises?.length || 0} exercises</span>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 bg-background border border-border rounded-sm">
                <Dumbbell className="w-8 h-8 text-stone/50 mx-auto mb-2" />
                <p className="text-charcoal font-medium">No workout scheduled</p>
                <p className="text-stone text-sm mb-4">Rest day or haven't generated yet?</p>
                <Link to="/workout-planner" className="inline-block bg-forest text-cream px-4 py-2 rounded-sm text-sm font-medium hover:bg-forest/90">
                  Plan Workout
                </Link>
              </div>
            )}
          </div>
        </section>

        {/* Profile/Goals Alignment */}
        <section className="bg-surface border border-border p-6 rounded-sm shadow-sm md:col-span-2">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-serif text-forest flex items-center gap-2">
              <Target className="w-5 h-5" /> Active Objective
            </h2>
            <Link to="/plan" className="text-sm font-medium text-stone hover:text-forest transition-colors underline">View Strategy</Link>
          </div>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-background border border-border p-4 rounded-sm">
              <span className="text-xs text-stone uppercase tracking-wider font-semibold block mb-1">Primary Goal</span>
              <span className="text-charcoal font-medium capitalize">{profile?.goal?.replace('_', ' ') || 'Not Set'}</span>
            </div>
            <div className="bg-background border border-border p-4 rounded-sm">
              <span className="text-xs text-stone uppercase tracking-wider font-semibold block mb-1">Activity Level</span>
              <span className="text-charcoal font-medium capitalize">{profile?.activity_level?.replace('_', ' ') || 'Not Set'}</span>
            </div>
            <div className="bg-background border border-border p-4 rounded-sm">
              <span className="text-xs text-stone uppercase tracking-wider font-semibold block mb-1">Dietary Preference</span>
              <span className="text-charcoal font-medium capitalize">{profile?.dietary_preference?.replace('_', ' ') || 'Not Set'}</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}