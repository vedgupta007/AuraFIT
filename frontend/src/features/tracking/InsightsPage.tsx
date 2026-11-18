import { useQuery } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Award, Activity, Calendar } from 'lucide-react';

export default function InsightsPage() {
  const { data: summary, isLoading: isSummaryLoading } = useQuery({
    queryKey: ['weekly-summary'],
    queryFn: async () => {
      const res = await api.get('/analytics/weekly-summary');
      return res.data;
    }
  });

  const { data: achievements, isLoading: isAchLoading } = useQuery({
    queryKey: ['achievements'],
    queryFn: async () => {
      // Evaluate first just to unlock any new ones
      await api.post('/achievements/evaluate');
      const res = await api.get('/achievements');
      return res.data;
    }
  });

  const { data: records, isLoading: isRecordsLoading } = useQuery({
    queryKey: ['personal-records'],
    queryFn: async () => {
      const res = await api.get('/analytics/personal-records');
      return res.data;
    }
  });

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-serif text-forest">Weekly Insights & Achievements</h1>
        <p className="text-stone mt-1">Review your performance, records, and milestones.</p>
      </div>

      {/* Summary */}
      <section>
        <h2 className="text-xl font-serif text-charcoal mb-4 flex items-center gap-2">
          <Calendar className="w-5 h-5 text-terracotta" />
          Last 7 Days
        </h2>
        {isSummaryLoading ? (
          <div className="text-stone">Loading...</div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-surface border border-border p-5 rounded-sm">
              <div className="text-sm text-stone font-medium mb-1">Workouts</div>
              <div className="text-2xl font-heading text-forest">{summary?.workouts_completed || 0}</div>
            </div>
            <div className="bg-surface border border-border p-5 rounded-sm">
              <div className="text-sm text-stone font-medium mb-1">Avg Calories</div>
              <div className="text-2xl font-heading text-terracotta">{summary?.avg_daily_calories || 0}</div>
            </div>
            <div className="bg-surface border border-border p-5 rounded-sm">
              <div className="text-sm text-stone font-medium mb-1">Avg Protein (g)</div>
              <div className="text-2xl font-heading text-forest">{summary?.avg_daily_protein || 0}</div>
            </div>
            <div className="bg-surface border border-border p-5 rounded-sm">
              <div className="text-sm text-stone font-medium mb-1">Meals Logged</div>
              <div className="text-2xl font-heading text-charcoal">{summary?.total_meals_logged || 0}</div>
            </div>
          </div>
        )}
      </section>

      {/* PRs */}
      <section>
        <h2 className="text-xl font-serif text-charcoal mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5 text-forest" />
          Personal Records
        </h2>
        {isRecordsLoading ? (
          <div className="text-stone">Loading...</div>
        ) : !records?.records || Object.keys(records.records).length === 0 ? (
          <div className="bg-surface p-8 border border-border rounded-sm text-center text-stone">
            Log exercises with weight and reps to see your records here.
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-4">
            {Object.entries(records.records).map(([name, data]: [string, any]) => (
              <div key={name} className="bg-surface border border-border p-4 rounded-sm flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-charcoal">{name}</h3>
                  <p className="text-xs text-stone mt-1">Set on {new Date(data.date).toLocaleDateString()}</p>
                </div>
                <div className="text-right">
                  <div className="text-lg font-heading text-forest">{data.max_weight} kg</div>
                  <div className="text-sm text-stone">x {data.max_reps} reps</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Achievements */}
      <section>
        <h2 className="text-xl font-serif text-charcoal mb-4 flex items-center gap-2">
          <Award className="w-5 h-5 text-terracotta" />
          Achievements
        </h2>
        {isAchLoading ? (
          <div className="text-stone">Loading...</div>
        ) : !achievements || achievements.length === 0 ? (
          <div className="bg-surface p-8 border border-border rounded-sm text-center text-stone">
            Complete workouts and log meals to start earning achievements!
          </div>
        ) : (
          <div className="grid md:grid-cols-3 gap-4">
            {achievements.map((ach: any) => (
              <div key={ach.id} className="bg-surface border border-border p-5 rounded-sm relative overflow-hidden group">
                <div className="absolute -right-4 -top-4 opacity-5 group-hover:opacity-10 transition-opacity">
                  <Award className="w-24 h-24 text-terracotta" />
                </div>
                <h3 className="font-medium text-forest relative z-10">{ach.title}</h3>
                <p className="text-sm text-stone mt-2 relative z-10">{ach.description}</p>
                <div className="text-xs text-stone/50 mt-4 relative z-10">
                  Earned {new Date(ach.earned_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
