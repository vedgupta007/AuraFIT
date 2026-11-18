import { Navigate, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Flame, Dumbbell, PlayCircle, ArrowRight, Activity, Target } from 'lucide-react';

export default function DashboardPlaceholder() {
  const today = new Date().toLocaleDateString('en-CA');

  const { data: profile, isLoading: isProfileLoading, isError: isProfileError } = useQuery({
    queryKey: ['profile'],
    queryFn: async () => {
      const res = await api.get('/profile');
      return res.data;
    },
    retry: false
  });

  const { data: goals, isLoading: isGoalsLoading } = useQuery({
    queryKey: ['nutrition-goals'],
    queryFn: async () => {
      const res = await api.get('/nutrition/goals');
      return res.data;
    },
    enabled: !!profile
  });

  const { data: summary, isLoading: isSummaryLoading } = useQuery({
    queryKey: ['daily-summary', today],
    queryFn: async () => {
      // Pass tz_offset_minutes
      const tzOffset = -new Date().getTimezoneOffset();
      const res = await api.get(`/nutrition/daily-summary?date=${today}&tz_offset_minutes=${tzOffset}`);
      return res.data;
    },
    enabled: !!profile
  });

  if (isProfileLoading) {
    return <div className="h-full flex items-center justify-center text-stone fade-in">Loading dashboard...</div>;
  }

  if (isProfileError) {
    return <Navigate to="/onboarding" />;
  }

  return (
    <div className="space-y-10 pb-12 fade-in">
      {/* Welcome Banner */}
      <header className="relative bg-surface border border-border rounded-lg overflow-hidden shadow-sm">
        <div className="absolute inset-0 z-0">
          <img 
            src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2053&auto=format&fit=crop" 
            alt="Healthy meal"
            className="w-full h-full object-cover opacity-15"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-surface via-surface/95 to-surface/80"></div>
        </div>
        <div className="relative z-10 p-8 sm:p-10">
          <h1 className="text-4xl font-heading text-forest mb-2">Hello, {profile?.name || 'there'}</h1>
          <p className="text-stone max-w-xl text-lg">Here is your daily wellness overview. Stay consistent, track your progress, and let AuraFIT handle the details.</p>
        </div>
      </header>

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-background border border-border p-5 rounded-sm shadow-sm transition-transform hover:-translate-y-1">
          <div className="flex justify-between items-start mb-4">
            <span className="text-stone text-sm font-medium">Calories</span>
            <Flame className="w-5 h-5 text-terracotta" />
          </div>
          <div className="text-2xl font-heading text-forest mb-1">
            {isSummaryLoading ? '...' : summary?.total_calories || 0}
            <span className="text-sm font-body text-stone"> / {isGoalsLoading ? '...' : goals?.daily_calories || 0}</span>
          </div>
          <Link to="/nutrition" className="text-xs text-forest hover:underline">View Overview</Link>
        </div>
        
        <div className="bg-background border border-border p-5 rounded-sm shadow-sm transition-transform hover:-translate-y-1">
          <div className="flex justify-between items-start mb-4">
            <span className="text-stone text-sm font-medium">Protein</span>
            <Dumbbell className="w-5 h-5 text-forest" />
          </div>
          <div className="text-2xl font-heading text-forest mb-1">
            {isSummaryLoading ? '...' : summary?.total_protein || 0}
            <span className="text-sm font-body text-stone"> / {isGoalsLoading ? '...' : goals?.daily_protein || 0}g</span>
          </div>
          <Link to="/nutrition" className="text-xs text-forest hover:underline">View Overview</Link>
        </div>

        <div className="bg-background border border-border p-5 rounded-sm shadow-sm transition-transform hover:-translate-y-1">
          <div className="flex justify-between items-start mb-4">
            <span className="text-stone text-sm font-medium">Active Goals</span>
            <Target className="w-5 h-5 text-forest" />
          </div>
          <div className="text-2xl font-heading text-forest mb-2">Track</div>
          <Link to="/goals" className="text-xs text-forest hover:underline">View Goals</Link>
        </div>

        <div className="bg-background border border-border p-5 rounded-sm shadow-sm transition-transform hover:-translate-y-1">
          <div className="flex justify-between items-start mb-4">
            <span className="text-stone text-sm font-medium">Progress</span>
            <Activity className="w-5 h-5 text-terracotta" />
          </div>
          <div className="text-2xl font-heading text-forest mb-2">Monitor</div>
          <Link to="/progress" className="text-xs text-forest hover:underline">View Progress</Link>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Nutrition Setup & Goals */}
        <section className="bg-surface border border-border p-8 rounded-sm shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
            <Target className="w-24 h-24 text-forest" />
          </div>
          <div className="flex items-center gap-3 mb-6 relative z-10">
            <div className="w-10 h-10 rounded-full bg-forest text-cream flex items-center justify-center">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-heading text-forest">Your Body Metrics</h2>
              <p className="text-sm text-stone">Based on your profile data</p>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-6 relative z-10 mb-8">
            <div>
              <div className="text-sm text-stone mb-1 font-medium">BMR</div>
              <div className="text-2xl font-heading text-charcoal">
                {isGoalsLoading ? '...' : goals?.bmr || 0} <span className="text-sm font-body text-stone font-normal">kcal</span>
              </div>
              <p className="text-xs text-stone mt-1">Basal Metabolic Rate</p>
            </div>
            <div>
              <div className="text-sm text-stone mb-1 font-medium">TDEE</div>
              <div className="text-2xl font-heading text-charcoal">
                {isGoalsLoading ? '...' : goals?.tdee || 0} <span className="text-sm font-body text-stone font-normal">kcal</span>
              </div>
              <p className="text-xs text-stone mt-1">Total Daily Energy</p>
            </div>
          </div>
          
          <div className="relative z-10 border-t border-border pt-6">
            <div className="flex justify-between items-center mb-4">
              <span className="font-medium text-charcoal">Macro Targets</span>
            </div>
            <div className="space-y-3">
               <div className="flex justify-between text-sm">
                 <span className="text-stone">Carbs (45%)</span>
                 <span className="font-medium text-charcoal">{isGoalsLoading ? '...' : goals?.daily_carbohydrates || 0}g</span>
               </div>
               <div className="flex justify-between text-sm">
                 <span className="text-stone">Protein (30%)</span>
                 <span className="font-medium text-charcoal">{isGoalsLoading ? '...' : goals?.daily_protein || 0}g</span>
               </div>
               <div className="flex justify-between text-sm">
                 <span className="text-stone">Fat (25%)</span>
                 <span className="font-medium text-charcoal">{isGoalsLoading ? '...' : goals?.daily_fat || 0}g</span>
               </div>
            </div>
          </div>
        </section>

        {/* Workout Routine */}
        <section className="bg-surface border border-border p-8 rounded-sm shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
            <PlayCircle className="w-24 h-24 text-forest" />
          </div>
          <h2 className="text-2xl font-heading text-forest mb-3 relative z-10">Workout Routine</h2>
          <p className="text-charcoal/80 text-sm mb-8 max-w-sm relative z-10 leading-relaxed">
            Track your training and progression based on your available equipment and goals.
          </p>
          <div className="flex items-center gap-4 relative z-10">
            <Link to="/workouts" className="bg-forest text-cream px-6 py-2.5 rounded-sm font-medium hover:bg-forest/90 transition-colors">
              Go to Workout Log
            </Link>
          </div>
        </section>
      </div>

      <section className="bg-forest text-cream p-8 sm:p-10 rounded-lg shadow-sm relative overflow-hidden group transition-transform hover:-translate-y-1">
        <div className="absolute top-0 right-0 w-64 h-64 bg-charcoal rounded-full filter blur-3xl opacity-30 -mr-20 -mt-20 group-hover:opacity-50 transition-opacity"></div>
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-8">
          <div>
            <h2 className="text-3xl font-heading mb-3">AuraAI Assistant</h2>
            <p className="text-cream/90 max-w-xl leading-relaxed">
              Have a question about food substitutions, a specific exercise form, or need to adapt today's meal plan? The intelligent assistant will guide you.
            </p>
          </div>
          <Link to="/ai/chat" className="bg-background text-forest hover:bg-sage/10 px-8 py-3 rounded-sm font-medium shrink-0 inline-flex items-center gap-2 transition-colors outline-none focus-visible:ring-2 focus-visible:ring-background focus-visible:ring-offset-2 focus-visible:ring-offset-forest">
            Ask AuraAI
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>
    </div>
  );
}