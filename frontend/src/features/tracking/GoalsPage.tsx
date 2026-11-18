import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Plus, Target, CheckCircle2, Circle, Edit2, Trash2, X } from 'lucide-react';

export default function GoalsPage() {
  const queryClient = useQueryClient();
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    goal_type: 'lose_weight',
    start_date: new Date().toISOString().slice(0, 10),
  });

  const { data: goals, isLoading } = useQuery({
    queryKey: ['goals'],
    queryFn: async () => {
      const res = await api.get('/goals');
      return res.data;
    }
  });

  const saveMutation = useMutation({
    mutationFn: async (data: any) => {
      if (editingId) {
        return api.put(`/goals/${editingId}`, data);
      }
      return api.post('/goals', data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['goals'] });
      closeModal();
    }
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => api.delete(`/goals/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['goals'] })
  });

  const toggleStatusMutation = useMutation({
    mutationFn: async ({ id, status }: { id: string, status: string }) => api.put(`/goals/${id}`, { status }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['goals'] })
  });

  const openModal = (goal?: any) => {
    if (goal) {
      setEditingId(goal.id);
      setFormData({
        title: goal.title,
        goal_type: goal.goal_type,
        start_date: goal.start_date.slice(0, 10),
      });
    } else {
      setEditingId(null);
      setFormData({
        title: '',
        goal_type: 'lose_weight',
        start_date: new Date().toISOString().slice(0, 10),
      });
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingId(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const isoDate = new Date(formData.start_date).toISOString();
    saveMutation.mutate({
      ...formData,
      start_date: isoDate,
    });
  };

  const handleDelete = (id: string) => {
    if (window.confirm("Are you sure you want to delete this goal?")) {
      deleteMutation.mutate(id);
    }
  };

  const activeGoals = goals?.filter((g: any) => g.status === 'active') || [];
  const completedGoals = goals?.filter((g: any) => g.status === 'completed') || [];

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-serif text-forest">My Goals</h1>
          <p className="text-stone mt-1">Set targets and track your milestones.</p>
        </div>
        <button
          onClick={() => openModal()}
          className="flex items-center gap-2 bg-forest text-white px-4 py-2 rounded-sm font-medium hover:bg-forest/90 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Add Goal
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-stone">Loading goals...</div>
      ) : (
        <div className="space-y-8">
          <section>
            <h2 className="text-xl font-serif text-charcoal mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-terracotta" />
              Active Goals
            </h2>
            {activeGoals.length === 0 ? (
              <div className="bg-surface p-8 text-center rounded-sm border border-border">
                <p className="text-stone">No active goals. Time to set one!</p>
              </div>
            ) : (
              <div className="grid gap-4">
                {activeGoals.map((goal: any) => (
                  <div key={goal.id} className="bg-surface border border-border p-5 rounded-sm flex items-start gap-4">
                    <button 
                      onClick={() => toggleStatusMutation.mutate({ id: goal.id, status: 'completed' })}
                      className="mt-1 text-stone hover:text-forest transition-colors"
                    >
                      <Circle className="w-6 h-6" />
                    </button>
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-charcoal">{goal.title}</h3>
                      <p className="text-sm text-stone mt-1 capitalize">{goal.goal_type.replace('_', ' ')}</p>
                      <p className="text-xs text-stone/70 mt-2">Started: {new Date(goal.start_date).toLocaleDateString()}</p>
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => openModal(goal)} className="p-2 text-stone hover:text-forest transition-colors">
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button onClick={() => handleDelete(goal.id)} className="p-2 text-stone hover:text-terracotta transition-colors">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>

          {completedGoals.length > 0 && (
            <section>
              <h2 className="text-xl font-serif text-charcoal mb-4 flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-forest" />
                Completed
              </h2>
              <div className="grid gap-4 opacity-75">
                {completedGoals.map((goal: any) => (
                  <div key={goal.id} className="bg-surface border border-border p-5 rounded-sm flex items-start gap-4">
                    <button 
                      onClick={() => toggleStatusMutation.mutate({ id: goal.id, status: 'active' })}
                      className="mt-1 text-forest"
                    >
                      <CheckCircle2 className="w-6 h-6" />
                    </button>
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-charcoal line-through">{goal.title}</h3>
                      <p className="text-sm text-stone mt-1 capitalize">{goal.goal_type.replace('_', ' ')}</p>
                    </div>
                    <button onClick={() => handleDelete(goal.id)} className="p-2 text-stone hover:text-terracotta transition-colors">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-charcoal/50 flex items-center justify-center p-4 z-50">
          <div className="bg-surface rounded-sm max-w-md w-full p-6 shadow-xl">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-serif text-forest">{editingId ? 'Edit Goal' : 'Add Goal'}</h2>
              <button onClick={closeModal} className="text-stone hover:text-charcoal"><X className="w-5 h-5" /></button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-charcoal mb-1">Goal Title</label>
                <input
                  required
                  type="text"
                  value={formData.title}
                  onChange={e => setFormData({ ...formData, title: e.target.value })}
                  className="w-full bg-background border border-border px-3 py-2 rounded-sm focus:border-forest outline-none transition-colors"
                  placeholder="e.g., Run 5km under 25 mins"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-charcoal mb-1">Type</label>
                <select
                  value={formData.goal_type}
                  onChange={e => setFormData({ ...formData, goal_type: e.target.value })}
                  className="w-full bg-background border border-border px-3 py-2 rounded-sm focus:border-forest outline-none transition-colors"
                >
                  <option value="lose_weight">Lose Weight</option>
                  <option value="gain_muscle">Gain Muscle</option>
                  <option value="improve_strength">Improve Strength</option>
                  <option value="improve_endurance">Improve Endurance</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-charcoal mb-1">Start Date</label>
                <input
                  required
                  type="date"
                  value={formData.start_date}
                  onChange={e => setFormData({ ...formData, start_date: e.target.value })}
                  className="w-full bg-background border border-border px-3 py-2 rounded-sm focus:border-forest outline-none transition-colors"
                />
              </div>
              
              <div className="flex gap-3 pt-4 border-t border-border">
                <button type="button" onClick={closeModal} className="flex-1 px-4 py-2 border border-border text-charcoal rounded-sm font-medium hover:bg-stone/5 transition-colors">Cancel</button>
                <button type="submit" disabled={saveMutation.isPending} className="flex-1 px-4 py-2 bg-forest text-white rounded-sm font-medium hover:bg-forest/90 transition-colors disabled:opacity-50">
                  {saveMutation.isPending ? 'Saving...' : 'Save Goal'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}