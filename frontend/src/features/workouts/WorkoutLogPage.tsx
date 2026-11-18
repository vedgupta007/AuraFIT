import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Plus, Trash2, Calendar, Activity, Edit2, X, Copy, Dumbbell } from 'lucide-react';

export default function WorkoutLogPage() {
  const queryClient = useQueryClient();
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  
  const [formData, setFormData] = useState({
    title: '',
    started_at: new Date().toISOString().slice(0, 16),
    notes: '',
  });
  
  const [exercises, setExercises] = useState<any[]>([]);

  const { data: workouts, isLoading } = useQuery({
    queryKey: ['workouts'],
    queryFn: async () => {
      const res = await api.get('/workouts');
      return res.data;
    }
  });

  const saveMutation = useMutation({
    mutationFn: async (data: any) => {
      if (editingId) {
        return api.put(`/workouts/${editingId}`, data);
      }
      return api.post('/workouts', data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workouts'] });
      queryClient.invalidateQueries({ queryKey: ['personal-records'] });
      queryClient.invalidateQueries({ queryKey: ['weekly-summary'] });
      closeModal();
    }
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => api.delete(`/workouts/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workouts'] });
      queryClient.invalidateQueries({ queryKey: ['personal-records'] });
      queryClient.invalidateQueries({ queryKey: ['weekly-summary'] });
    }
  });

  const openModal = (workout?: any, isDuplicate = false) => {
    if (workout) {
      setEditingId(isDuplicate ? null : workout.id);
      setFormData({
        title: isDuplicate ? `${workout.title} (Copy)` : workout.title,
        started_at: isDuplicate ? new Date().toISOString().slice(0, 16) : workout.started_at.slice(0, 16),
        notes: workout.notes || '',
      });
      setExercises(workout.exercises || []);
    } else {
      setEditingId(null);
      setFormData({
        title: '',
        started_at: new Date().toISOString().slice(0, 16),
        notes: '',
      });
      setExercises([]);
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingId(null);
    setExercises([]);
  };

  const handleAddExercise = () => {
    setExercises([...exercises, { exercise_name: '', sets: 0, reps: 0, weight_kg: '' }]);
  };

  const handleExerciseChange = (index: number, field: string, value: any) => {
    const updated = [...exercises];
    updated[index] = { ...updated[index], [field]: value };
    setExercises(updated);
  };

  const handleRemoveExercise = (index: number) => {
    const updated = exercises.filter((_, i) => i !== index);
    setExercises(updated);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const isoDate = new Date(formData.started_at).toISOString();
    
    const cleanedExercises = exercises.filter(ex => ex.exercise_name.trim() !== '').map(ex => ({
      ...ex,
      sets: parseInt(ex.sets) || 0,
      reps: parseInt(ex.reps) || 0,
      weight_kg: ex.weight_kg ? parseFloat(ex.weight_kg) : null
    }));

    saveMutation.mutate({
      ...formData,
      started_at: isoDate,
      exercises: cleanedExercises
    });
  };

  const handleDelete = (id: string) => {
    if (window.confirm("Are you sure you want to delete this workout?")) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-serif text-forest">Workout Log</h1>
          <p className="text-stone mt-1">Track your training and progression.</p>
        </div>
        <button
          onClick={() => openModal()}
          className="flex items-center gap-2 bg-forest text-cream px-5 py-2.5 rounded-sm font-medium hover:bg-forest/90 transition-colors shrink-0"
        >
          <Plus className="w-5 h-5" />
          Log Workout
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-stone">Loading workouts...</div>
      ) : workouts?.length === 0 ? (
        <div className="bg-surface p-12 text-center rounded-sm border border-border">
          <Activity className="w-12 h-12 text-stone/50 mx-auto mb-4" />
          <h3 className="text-xl font-serif text-charcoal mb-2">No workouts yet</h3>
          <p className="text-stone mb-6">Start logging your training to track your progress.</p>
          <button
            onClick={() => openModal()}
            className="inline-flex items-center gap-2 bg-forest text-cream px-4 py-2 rounded-sm font-medium hover:bg-forest/90 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Log First Workout
          </button>
        </div>
      ) : (
        <div className="grid gap-4">
          {workouts?.map((w: any) => (
            <div key={w.id} className="bg-surface border border-border p-5 rounded-sm hover:border-forest/30 transition-colors">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
                <div>
                  <h3 className="text-xl font-serif text-charcoal">{w.title}</h3>
                  <div className="flex items-center gap-4 mt-2 text-sm text-stone">
                    <span className="flex items-center gap-1"><Calendar className="w-4 h-4" /> {new Date(w.started_at).toLocaleDateString()}</span>
                    <span className="flex items-center gap-1"><Activity className="w-4 h-4" /> {w.exercises?.length || 0} exercises</span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button onClick={() => openModal(w, true)} className="p-2 text-stone hover:text-forest transition-colors rounded-sm hover:bg-forest/5" title="Duplicate/Repeat Workout">
                    <Copy className="w-4 h-4" />
                  </button>
                  <button onClick={() => openModal(w)} className="p-2 text-stone hover:text-forest transition-colors rounded-sm hover:bg-forest/5" title="Edit">
                    <Edit2 className="w-4 h-4" />
                  </button>
                  <button onClick={() => handleDelete(w.id)} disabled={deleteMutation.isPending} className="p-2 text-stone hover:text-terracotta transition-colors rounded-sm hover:bg-terracotta/5" title="Delete">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
              
              {w.notes && <p className="text-sm text-charcoal/80 mb-4 bg-background p-3 rounded-sm">{w.notes}</p>}
              
              {w.exercises && w.exercises.length > 0 && (
                <div className="mt-4 border-t border-border pt-4">
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                    {w.exercises.map((ex: any, idx: number) => (
                      <div key={idx} className="bg-background p-3 rounded-sm border border-border/50 text-sm flex items-center gap-3">
                        <Dumbbell className="w-4 h-4 text-forest shrink-0" />
                        <div>
                          <div className="font-medium text-charcoal">{ex.exercise_name}</div>
                          <div className="text-stone mt-0.5">
                            {ex.sets} sets × {ex.reps} reps {ex.weight_kg ? `@ ${ex.weight_kg}kg` : ''}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-charcoal/50 backdrop-blur-sm flex items-center justify-center p-4 z-50 overflow-y-auto">
          <div className="bg-surface rounded-sm max-w-2xl w-full p-6 shadow-xl my-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-serif text-forest">{editingId ? 'Edit Workout' : 'Log Workout'}</h2>
              <button onClick={closeModal} className="text-stone hover:text-charcoal transition-colors p-1"><X className="w-5 h-5" /></button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-charcoal mb-1">Workout Title *</label>
                  <input
                    required
                    type="text"
                    value={formData.title}
                    onChange={e => setFormData({ ...formData, title: e.target.value })}
                    className="w-full bg-background border border-border px-3 py-2 rounded-sm focus:border-forest focus:ring-1 focus:ring-forest outline-none transition-colors"
                    placeholder="e.g. Upper Body Power"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-charcoal mb-1">Date & Time *</label>
                  <input
                    required
                    type="datetime-local"
                    value={formData.started_at}
                    onChange={e => setFormData({ ...formData, started_at: e.target.value })}
                    className="w-full bg-background border border-border px-3 py-2 rounded-sm focus:border-forest focus:ring-1 focus:ring-forest outline-none transition-colors"
                  />
                </div>
              </div>
              
              <div>
                <div className="flex justify-between items-center mb-2">
                  <label className="block text-sm font-medium text-charcoal">Exercises</label>
                  <button type="button" onClick={handleAddExercise} className="text-xs font-medium text-forest hover:underline flex items-center gap-1">
                    <Plus className="w-3 h-3" /> Add Exercise
                  </button>
                </div>
                
                {exercises.length === 0 ? (
                  <div className="text-sm text-stone bg-background p-4 rounded-sm border border-border text-center">
                    No exercises added. Add an exercise to track sets and reps.
                  </div>
                ) : (
                  <div className="space-y-3">
                    {exercises.map((ex, idx) => (
                      <div key={idx} className="flex flex-col sm:flex-row gap-3 bg-background p-3 rounded-sm border border-border items-start sm:items-center">
                        <input 
                          type="text" 
                          required
                          placeholder="Exercise name"
                          value={ex.exercise_name}
                          onChange={(e) => handleExerciseChange(idx, 'exercise_name', e.target.value)}
                          className="flex-1 bg-surface border border-border px-2 py-1.5 text-sm rounded-sm focus:border-forest outline-none w-full sm:w-auto"
                        />
                        <div className="flex gap-2 w-full sm:w-auto">
                          <input 
                            type="number" 
                            placeholder="Sets"
                            required min="0"
                            value={ex.sets}
                            onChange={(e) => handleExerciseChange(idx, 'sets', e.target.value)}
                            className="w-16 bg-surface border border-border px-2 py-1.5 text-sm rounded-sm focus:border-forest outline-none"
                          />
                          <input 
                            type="number" 
                            placeholder="Reps"
                            required min="0"
                            value={ex.reps}
                            onChange={(e) => handleExerciseChange(idx, 'reps', e.target.value)}
                            className="w-16 bg-surface border border-border px-2 py-1.5 text-sm rounded-sm focus:border-forest outline-none"
                          />
                          <input 
                            type="number" 
                            placeholder="kg"
                            step="0.5" min="0"
                            value={ex.weight_kg}
                            onChange={(e) => handleExerciseChange(idx, 'weight_kg', e.target.value)}
                            className="w-20 bg-surface border border-border px-2 py-1.5 text-sm rounded-sm focus:border-forest outline-none"
                          />
                          <button type="button" onClick={() => handleRemoveExercise(idx)} className="p-1.5 text-stone hover:text-terracotta ml-auto sm:ml-0">
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-charcoal mb-1">Notes (Optional)</label>
                <textarea
                  value={formData.notes}
                  onChange={e => setFormData({ ...formData, notes: e.target.value })}
                  className="w-full bg-background border border-border px-3 py-2 rounded-sm focus:border-forest focus:ring-1 focus:ring-forest outline-none transition-colors"
                  rows={2}
                  placeholder="How did you feel during this workout?"
                ></textarea>
              </div>
              
              <div className="flex gap-3 pt-4 border-t border-border">
                <button type="button" onClick={closeModal} className="flex-1 px-4 py-2 border border-border text-charcoal rounded-sm font-medium hover:bg-stone/5 transition-colors">Cancel</button>
                <button type="submit" disabled={saveMutation.isPending} className="flex-1 px-4 py-2 bg-forest text-cream rounded-sm font-medium hover:bg-forest/90 transition-colors disabled:opacity-50">
                  {saveMutation.isPending ? 'Saving...' : 'Save Workout'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}