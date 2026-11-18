import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Plus, Activity, Edit2, Trash2, X, TrendingDown, TrendingUp } from 'lucide-react';

export default function ProgressPage() {
  const queryClient = useQueryClient();
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    date: new Date().toISOString().slice(0, 10),
    weight_kg: '',
    body_fat_percent: '',
  });

  const { data: measurements, isLoading } = useQuery({
    queryKey: ['measurements'],
    queryFn: async () => {
      const res = await api.get('/measurements');
      return res.data;
    }
  });

  const saveMutation = useMutation({
    mutationFn: async (data: any) => {
      if (editingId) {
        return api.put(`/measurements/${editingId}`, data);
      }
      return api.post('/measurements', data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['measurements'] });
      closeModal();
    }
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => api.delete(`/measurements/${id}`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['measurements'] })
  });

  const openModal = (m?: any) => {
    if (m) {
      setEditingId(m.id);
      setFormData({
        date: m.date.slice(0, 10),
        weight_kg: m.weight_kg || '',
        body_fat_percent: m.body_fat_percent || '',
      });
    } else {
      setEditingId(null);
      setFormData({
        date: new Date().toISOString().slice(0, 10),
        weight_kg: '',
        body_fat_percent: '',
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
    const payload: any = { date: new Date(formData.date).toISOString() };
    if (formData.weight_kg) payload.weight_kg = parseFloat(formData.weight_kg);
    if (formData.body_fat_percent) payload.body_fat_percent = parseFloat(formData.body_fat_percent);
    saveMutation.mutate(payload);
  };

  const handleDelete = (id: string) => {
    if (window.confirm("Are you sure you want to delete this measurement?")) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-serif text-forest">Progress Tracking</h1>
          <p className="text-stone mt-1">Monitor your body measurements over time.</p>
        </div>
        <button
          onClick={() => openModal()}
          className="flex items-center gap-2 bg-forest text-white px-4 py-2 rounded-sm font-medium hover:bg-forest/90 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Log Measurement
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-stone">Loading...</div>
      ) : measurements?.length === 0 ? (
        <div className="bg-surface p-12 text-center rounded-sm border border-border">
          <Activity className="w-12 h-12 text-stone/50 mx-auto mb-4" />
          <h3 className="text-xl font-serif text-charcoal mb-2">No data yet</h3>
          <p className="text-stone">Start logging measurements to see trends.</p>
        </div>
      ) : (
        <div className="bg-surface border border-border rounded-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="bg-background/50 border-b border-border text-sm text-stone">
                <tr>
                  <th className="p-4 font-medium">Date</th>
                  <th className="p-4 font-medium">Weight (kg)</th>
                  <th className="p-4 font-medium">Body Fat (%)</th>
                  <th className="p-4 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {measurements?.map((m: any, i: number) => {
                  const prev = measurements[i + 1];
                  const weightDiff = prev && m.weight_kg && prev.weight_kg ? (m.weight_kg - prev.weight_kg).toFixed(1) : null;
                  
                  return (
                    <tr key={m.id} className="hover:bg-background/50 transition-colors">
                      <td className="p-4 text-charcoal">{new Date(m.date).toLocaleDateString()}</td>
                      <td className="p-4 text-charcoal flex items-center gap-2">
                        {m.weight_kg ? m.weight_kg : '--'}
                        {weightDiff && parseFloat(weightDiff) < 0 && <span className="flex text-terracotta text-xs"><TrendingDown className="w-3 h-3" /> {weightDiff}</span>}
                        {weightDiff && parseFloat(weightDiff) > 0 && <span className="flex text-forest text-xs"><TrendingUp className="w-3 h-3" /> +{weightDiff}</span>}
                      </td>
                      <td className="p-4 text-charcoal">{m.body_fat_percent ? `${m.body_fat_percent}%` : '--'}</td>
                      <td className="p-4 text-right flex justify-end gap-2">
                        <button onClick={() => openModal(m)} className="p-2 text-stone hover:text-forest transition-colors">
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button onClick={() => handleDelete(m.id)} className="p-2 text-stone hover:text-terracotta transition-colors">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-charcoal/50 flex items-center justify-center p-4 z-50">
          <div className="bg-surface rounded-sm max-w-md w-full p-6 shadow-xl">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-serif text-forest">{editingId ? 'Edit Measurement' : 'Log Measurement'}</h2>
              <button onClick={closeModal} className="text-stone hover:text-charcoal"><X className="w-5 h-5" /></button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-charcoal mb-1">Date</label>
                <input
                  required
                  type="date"
                  value={formData.date}
                  onChange={e => setFormData({ ...formData, date: e.target.value })}
                  className="w-full bg-background border border-border px-3 py-2 rounded-sm focus:border-forest outline-none transition-colors"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-charcoal mb-1">Weight (kg)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.weight_kg}
                    onChange={e => setFormData({ ...formData, weight_kg: e.target.value })}
                    className="w-full bg-background border border-border px-3 py-2 rounded-sm focus:border-forest outline-none transition-colors"
                    placeholder="e.g. 70.5"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-charcoal mb-1">Body Fat (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    value={formData.body_fat_percent}
                    onChange={e => setFormData({ ...formData, body_fat_percent: e.target.value })}
                    className="w-full bg-background border border-border px-3 py-2 rounded-sm focus:border-forest outline-none transition-colors"
                    placeholder="e.g. 15.0"
                  />
                </div>
              </div>
              
              <div className="flex gap-3 pt-4 border-t border-border">
                <button type="button" onClick={closeModal} className="flex-1 px-4 py-2 border border-border text-charcoal rounded-sm font-medium hover:bg-stone/5 transition-colors">Cancel</button>
                <button type="submit" disabled={saveMutation.isPending} className="flex-1 px-4 py-2 bg-forest text-white rounded-sm font-medium hover:bg-forest/90 transition-colors disabled:opacity-50">
                  {saveMutation.isPending ? 'Saving...' : 'Save'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}