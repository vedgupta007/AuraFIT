import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { FileText, Target, Utensils, Dumbbell, AlertCircle, RefreshCw, CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function FitnessPlanPage() {
  const queryClient = useQueryClient();
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const { data: profile, isLoading: profileLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: async () => {
      const res = await api.get('/profile');
      return res.data;
    }
  });

  const { data: plan, isLoading: planLoading,  } = useQuery({
    queryKey: ['fitness-strategy'],
    queryFn: async () => {
      const res = await api.get('/plans/strategy');
      return res.data;
    },
    retry: false
  });

  const generateMutation = useMutation({
    mutationFn: async () => {
      setErrorMsg(null);
      const res = await api.post('/plans/strategy/generate');
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fitness-strategy'] });
    },
    onError: (err: any) => {
      setErrorMsg(err.response?.data?.detail || "Failed to generate plan.");
    }
  });

  const acceptMutation = useMutation({
    mutationFn: async (id: string) => {
      const res = await api.patch(`/plans/strategy/${id}`, { status: 'accepted' });
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fitness-strategy'] });
    }
  });

  if (profileLoading || planLoading) {
    return (
      <div className="p-8 flex justify-center items-center h-full">
        <div className="animate-pulse flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-4 border-forest border-t-transparent rounded-full animate-spin"></div>
          <p className="text-stone font-medium">Loading your plan...</p>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="p-8 max-w-4xl mx-auto text-center">
        <AlertCircle className="w-12 h-12 text-terracotta mx-auto mb-4" />
        <h2 className="text-2xl font-serif text-charcoal mb-2">Profile Incomplete</h2>
        <p className="text-stone mb-4">Please complete your profile to generate a personalized fitness plan.</p>
        <Link to="/profile" className="inline-block bg-forest text-cream px-4 py-2 rounded-sm font-medium hover:bg-forest/90 transition-colors">
          Go to Profile
        </Link>
      </div>
    );
  }

  const isGenerating = generateMutation.isPending;

  return (
    <div className="max-w-4xl mx-auto space-y-6 fade-in p-4 sm:p-0">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
        <div className="flex items-center gap-3">
          <FileText className="w-8 h-8 text-forest" />
          <div>
            <h1 className="text-3xl font-serif text-charcoal">My Fitness Plan</h1>
            <p className="text-stone mt-1">Generated based on your profile and goals.</p>
          </div>
        </div>
        {plan && (
          <div className="flex gap-2">
            <button
              onClick={() => generateMutation.mutate()}
              disabled={isGenerating}
              className="flex items-center gap-2 bg-background border border-border text-stone px-4 py-2 rounded-sm text-sm font-medium hover:text-charcoal transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${isGenerating ? 'animate-spin' : ''}`} />
              Regenerate
            </button>
            {plan.status === 'generated' && (
              <button
                onClick={() => acceptMutation.mutate(plan.id)}
                disabled={acceptMutation.isPending}
                className="flex items-center gap-2 bg-forest text-cream px-4 py-2 rounded-sm text-sm font-medium hover:bg-forest/90 transition-colors disabled:opacity-50"
              >
                <CheckCircle2 className="w-4 h-4" />
                Accept Plan
              </button>
            )}
          </div>
        )}
      </div>

      {errorMsg && (
        <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta p-4 rounded-sm mb-6 flex gap-3 items-start">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <p>{errorMsg}</p>
        </div>
      )}

      {!plan ? (
        <div className="bg-surface border border-border p-12 text-center rounded-sm shadow-sm">
          <Target className="w-12 h-12 text-stone/50 mx-auto mb-4" />
          <h2 className="text-xl font-serif text-charcoal mb-2">No Active Plan</h2>
          <p className="text-stone mb-6 max-w-md mx-auto">
            You haven't generated a personalized fitness plan yet. AuraAI will craft a specific strategy based on your profile goals ({profile.goal?.replace('_', ' ')}).
          </p>
          <button
            onClick={() => generateMutation.mutate()}
            disabled={isGenerating}
            className="inline-flex items-center gap-2 bg-forest text-cream px-6 py-3 rounded-sm font-medium hover:bg-forest/90 transition-colors disabled:opacity-50"
          >
            {isGenerating ? (
              <><RefreshCw className="w-5 h-5 animate-spin" /> Analyzing Profile...</>
            ) : (
              'Generate My Plan'
            )}
          </button>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-6">
          {plan.status === 'generated' && (
            <div className="md:col-span-2 bg-cream border border-forest/30 p-4 rounded-sm flex items-center justify-between">
              <span className="text-forest font-medium text-sm flex items-center gap-2">
                <Target className="w-4 h-4" /> Please review your new generated strategy. Accept it to make it your active plan.
              </span>
            </div>
          )}

          {/* The Strategy */}
          <div className="bg-surface border border-border p-6 rounded-sm shadow-sm md:col-span-2 relative">
            <h2 className="text-xl font-serif text-forest flex items-center gap-2 mb-4">
              <Target className="w-5 h-5" /> The Strategy
            </h2>
            <p className="text-charcoal leading-relaxed whitespace-pre-wrap">
              {plan.strategy_text}
            </p>
          </div>

          {/* Nutrition Protocol */}
          <div className="bg-surface border border-border p-6 rounded-sm shadow-sm">
            <h2 className="text-xl font-serif text-forest flex items-center gap-2 mb-4">
              <Utensils className="w-5 h-5" /> Nutrition Protocol
            </h2>
            <div className="space-y-4">
              <p className="text-charcoal/80 text-sm leading-relaxed whitespace-pre-wrap">
                {plan.nutrition_protocol}
              </p>
              <div className="pt-4 border-t border-border">
                <Link to="/meal-planner" className="text-sm font-medium text-forest hover:underline">Go to Meal Planner &rarr;</Link>
              </div>
            </div>
          </div>

          {/* Training Protocol */}
          <div className="bg-surface border border-border p-6 rounded-sm shadow-sm">
            <h2 className="text-xl font-serif text-forest flex items-center gap-2 mb-4">
              <Dumbbell className="w-5 h-5" /> Training Protocol
            </h2>
            <div className="space-y-4">
              <p className="text-charcoal/80 text-sm leading-relaxed whitespace-pre-wrap">
                {plan.training_protocol}
              </p>
              <div className="pt-4 border-t border-border">
                <Link to="/workout-planner" className="text-sm font-medium text-forest hover:underline">Go to Workout Planner &rarr;</Link>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
