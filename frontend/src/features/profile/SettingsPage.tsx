import { useState, useEffect } from 'react';


import { Save, Bell, Activity } from 'lucide-react';

export default function SettingsPage() {
  
  const [success, setSuccess] = useState(false);
  const [formData, setFormData] = useState({
    workout_reminders: false,
    meal_reminders: false,
    weekly_summary: true,
    preferred_units: 'metric',
  });

  // Mocked or minimal setting fetch (to not over-engineer the backend right now)
  useEffect(() => {
    const saved = localStorage.getItem('aurafit_settings');
    if (saved) {
      try {
        setFormData(JSON.parse(saved));
      } catch (e) {}
    }
  }, []);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem('aurafit_settings', JSON.stringify(formData));
    setSuccess(true);
    setTimeout(() => setSuccess(false), 3000);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-serif text-forest">Settings & Preferences</h1>
        <p className="text-stone mt-1">Manage your reminders and app experience.</p>
      </div>

      <form onSubmit={handleSave} className="space-y-8">
        <section className="bg-surface border border-border p-8 rounded-sm">
          <h2 className="text-xl font-serif text-charcoal mb-6 flex items-center gap-2">
            <Bell className="w-5 h-5 text-terracotta" />
            Notifications & Reminders
          </h2>
          
          <div className="space-y-4">
            <label className="flex items-start gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.workout_reminders}
                onChange={(e) => setFormData({ ...formData, workout_reminders: e.target.checked })}
                className="mt-1 h-4 w-4 text-forest border-border rounded focus:ring-forest bg-background"
              />
              <div>
                <div className="font-medium text-charcoal">Workout Reminders</div>
                <div className="text-sm text-stone">Get reminded to log your workouts and stay consistent.</div>
              </div>
            </label>

            <label className="flex items-start gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.meal_reminders}
                onChange={(e) => setFormData({ ...formData, meal_reminders: e.target.checked })}
                className="mt-1 h-4 w-4 text-forest border-border rounded focus:ring-forest bg-background"
              />
              <div>
                <div className="font-medium text-charcoal">Meal Logging Reminders</div>
                <div className="text-sm text-stone">Reminders to log your breakfast, lunch, and dinner.</div>
              </div>
            </label>

            <label className="flex items-start gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.weekly_summary}
                onChange={(e) => setFormData({ ...formData, weekly_summary: e.target.checked })}
                className="mt-1 h-4 w-4 text-forest border-border rounded focus:ring-forest bg-background"
              />
              <div>
                <div className="font-medium text-charcoal">Weekly Summary Email</div>
                <div className="text-sm text-stone">Receive a weekly digest of your fitness and nutrition progress.</div>
              </div>
            </label>
          </div>
        </section>

        <section className="bg-surface border border-border p-8 rounded-sm">
          <h2 className="text-xl font-serif text-charcoal mb-6 flex items-center gap-2">
            <Activity className="w-5 h-5 text-forest" />
            App Preferences
          </h2>
          
          <div>
            <label className="block text-sm font-medium text-charcoal mb-2">Preferred Units</label>
            <select
              value={formData.preferred_units}
              onChange={(e) => setFormData({ ...formData, preferred_units: e.target.value })}
              className="w-full bg-background border border-border px-3 py-2.5 rounded-sm focus:border-forest outline-none transition-colors"
            >
              <option value="metric">Metric (kg, cm, ml)</option>
              <option value="imperial">Imperial (lbs, in, fl oz) - Coming Soon</option>
            </select>
          </div>
        </section>

        <div className="flex justify-end items-center gap-4">
          {success && <span className="text-forest text-sm font-medium">Settings saved successfully!</span>}
          <button type="submit" className="flex items-center gap-2 bg-forest text-cream px-8 py-3 rounded-sm font-medium hover:bg-forest/90 transition-colors">
            <Save className="w-5 h-5" />
            Save Preferences
          </button>
        </div>
      </form>
    </div>
  );
}
