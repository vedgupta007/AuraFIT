import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../lib/axios';
import { Save, AlertCircle, CheckCircle } from 'lucide-react';

const emptyStringToUndefined = (val: unknown) => {
  if (val === '' || val === null || val === undefined) return undefined;
  const num = Number(val);
  return isNaN(num) ? undefined : num;
};

const profileSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  age: z.preprocess(emptyStringToUndefined, z.number({ required_error: "Age is required" }).min(12, "Must be at least 12").max(120, "Must be under 120")),
  sex: z.enum(["M", "F", "Other"], { required_error: "Please select your sex" }),
  height_cm: z.preprocess(emptyStringToUndefined, z.number({ required_error: "Height is required" }).positive("Must be positive").max(300, "Too high")),
  weight_kg: z.preprocess(emptyStringToUndefined, z.number({ required_error: "Weight is required" }).positive("Must be positive")),
  goal: z.enum(["lose_weight", "maintain_weight", "gain_muscle", "improve_fitness"]),
  activity_level: z.enum(["sedentary", "light", "moderate", "active", "very_active"]),
  training_experience: z.enum(["beginner", "intermediate", "advanced"]),
  preferred_workout_frequency: z.preprocess(emptyStringToUndefined, z.number({ required_error: "Frequency is required" }).min(1).max(7)),
  dietary_preference: z.enum(["vegetarian", "vegan", "eggetarian", "non_vegetarian", "other"]),
  allergies: z.string().optional(),
  disliked_foods: z.string().optional(),
});

type ProfileFormInputValues = {
  name: string;
  age: number | string;
  sex: "M" | "F" | "Other";
  height_cm: number | string;
  weight_kg: number | string;
  goal: "lose_weight" | "maintain_weight" | "gain_muscle" | "improve_fitness";
  activity_level: "sedentary" | "light" | "moderate" | "active" | "very_active";
  training_experience: "beginner" | "intermediate" | "advanced";
  preferred_workout_frequency: number | string;
  dietary_preference: "vegetarian" | "vegan" | "eggetarian" | "non_vegetarian" | "other";
  allergies?: string;
  disliked_foods?: string;
};

export default function ProfilePage() {
  const queryClient = useQueryClient();
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: async () => {
      const res = await api.get('/profile');
      return res.data;
    }
  });

  const { register, handleSubmit, reset, formState: { errors } } = useForm<ProfileFormInputValues>({
    resolver: zodResolver(profileSchema) as any,
    defaultValues: {
      name: '',
      age: '' as any,
      sex: 'M',
      height_cm: '' as any,
      weight_kg: '' as any,
      goal: 'maintain_weight',
      activity_level: 'moderate',
      training_experience: 'beginner',
      preferred_workout_frequency: '' as any,
      dietary_preference: 'non_vegetarian',
      allergies: '',
      disliked_foods: ''
    }
  });

  useEffect(() => {
    if (profile) {
      reset({
        name: profile.name || '',
        age: profile.age ?? ('' as any),
        sex: profile.sex || 'M',
        height_cm: profile.height_cm ?? ('' as any),
        weight_kg: profile.weight_kg ?? ('' as any),
        goal: profile.goal || 'maintain_weight',
        activity_level: profile.activity_level || 'moderate',
        training_experience: profile.training_experience || 'beginner',
        preferred_workout_frequency: profile.preferred_workout_frequency ?? ('' as any),
        dietary_preference: profile.dietary_preference || 'non_vegetarian',
        allergies: (profile.allergies || []).join(', '),
        disliked_foods: (profile.disliked_foods || []).join(', ')
      });
    }
  }, [profile, reset]);

  const updateMutation = useMutation({
    mutationFn: async (data: any) => {
      const res = await api.put('/profile', data);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile'] });
      queryClient.invalidateQueries({ queryKey: ['nutrition-goals'] });
      setSuccessMsg('Profile and preferences updated successfully!');
      setTimeout(() => setSuccessMsg(''), 4000);
    },
    onError: (err: any) => {
      setErrorMsg(err.response?.data?.detail || 'Failed to update profile');
      setTimeout(() => setErrorMsg(''), 4000);
    }
  });

  const onSubmit = (data: any) => {
    const payload = {
      ...data,
      allergies: data.allergies ? data.allergies.split(',').map((s: string) => s.trim()).filter(Boolean) : [],
      disliked_foods: data.disliked_foods ? data.disliked_foods.split(',').map((s: string) => s.trim()).filter(Boolean) : []
    };
    updateMutation.mutate(payload);
  };

  if (isLoading) {
    return (
      <div className="p-8 flex justify-center items-center h-full">
        <div className="animate-pulse flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-4 border-forest border-t-transparent rounded-full animate-spin"></div>
          <p className="text-stone font-medium">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-4xl mx-auto fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-heading font-semibold text-forest">Edit Profile & Nutrition Preferences</h1>
        <p className="text-stone mt-1">Update your details to recalculate your BMR, TDEE, and daily nutrition targets.</p>
      </div>

      {successMsg && (
        <div className="mb-6 p-4 bg-forest/10 border border-forest/20 text-forest text-sm rounded-sm flex items-center gap-2">
          <CheckCircle className="w-4 h-4" />
          {successMsg}
        </div>
      )}

      {errorMsg && (
        <div className="mb-6 p-4 bg-terracotta/10 border border-terracotta/20 text-terracotta text-sm rounded-sm flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          {errorMsg}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8 bg-surface p-8 rounded-sm border border-border shadow-sm">
        
        {/* Basic Info */}
        <section>
          <h2 className="text-xl font-heading text-forest mb-4 border-b border-border pb-2">Basic Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-forest mb-1.5">First Name</label>
              <input type="text" {...register('name')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors" />
              {errors.name && <p className="text-terracotta text-xs mt-1">{errors.name.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-forest mb-1.5">Age</label>
              <input type="number" {...register('age')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors" />
              {errors.age && <p className="text-terracotta text-xs mt-1">{errors.age.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-forest mb-1.5">Biological Sex (for BMR)</label>
              <select {...register('sex')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors">
                <option value="M">Male</option>
                <option value="F">Female</option>
                <option value="Other">Other</option>
              </select>
              {errors.sex && <p className="text-terracotta text-xs mt-1">{errors.sex.message}</p>}
            </div>
          </div>
        </section>

        {/* Body Metrics */}
        <section>
          <h2 className="text-xl font-heading text-forest mb-4 border-b border-border pb-2">Body Metrics</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-forest mb-1.5">Height (cm)</label>
              <input type="number" step="0.1" {...register('height_cm')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors" />
              {errors.height_cm && <p className="text-terracotta text-xs mt-1">{errors.height_cm.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-forest mb-1.5">Weight (kg)</label>
              <input type="number" step="0.1" {...register('weight_kg')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors" />
              {errors.weight_kg && <p className="text-terracotta text-xs mt-1">{errors.weight_kg.message}</p>}
            </div>
          </div>
        </section>

        {/* Fitness & Activity */}
        <section>
          <h2 className="text-xl font-heading text-forest mb-4 border-b border-border pb-2">Activity & Goals</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-forest mb-1.5">Primary Goal</label>
              <select {...register('goal')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors">
                <option value="lose_weight">Lose Weight</option>
                <option value="maintain_weight">Maintain Weight</option>
                <option value="gain_muscle">Gain Muscle</option>
                <option value="improve_fitness">Improve Fitness</option>
              </select>
              {errors.goal && <p className="text-terracotta text-xs mt-1">{errors.goal.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-forest mb-1.5">Daily Activity Level</label>
              <select {...register('activity_level')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors">
                <option value="sedentary">Sedentary (Little/no exercise)</option>
                <option value="light">Lightly Active (1-3 days/week)</option>
                <option value="moderate">Moderately Active (3-5 days/week)</option>
                <option value="active">Active (6-7 days/week)</option>
                <option value="very_active">Very Active (Physical job / 2x training)</option>
              </select>
              {errors.activity_level && <p className="text-terracotta text-xs mt-1">{errors.activity_level.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-forest mb-1.5">Training Experience</label>
              <select {...register('training_experience')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors">
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-forest mb-1.5">Preferred Workouts / Week</label>
              <input type="number" min="1" max="7" {...register('preferred_workout_frequency')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors" />
              {errors.preferred_workout_frequency && <p className="text-terracotta text-xs mt-1">{errors.preferred_workout_frequency.message}</p>}
            </div>
          </div>
        </section>

        {/* Dietary Preferences */}
        <section>
          <h2 className="text-xl font-heading text-forest mb-4 border-b border-border pb-2">Dietary Preferences</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-forest mb-1.5">Diet Type</label>
              <select {...register('dietary_preference')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors">
                <option value="non_vegetarian">Non-Vegetarian</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="eggetarian">Eggetarian</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-forest mb-1.5">Allergies (comma separated)</label>
              <input type="text" placeholder="e.g. Peanuts, Shellfish" {...register('allergies')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors" />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-forest mb-1.5">Disliked Foods (comma separated)</label>
              <input type="text" placeholder="e.g. Mushrooms, Olives" {...register('disliked_foods')} className="w-full h-11 px-3 bg-background border border-border rounded-sm focus:border-forest outline-none transition-colors" />
            </div>
          </div>
        </section>

        <div className="pt-4 flex justify-end">
          <button 
            type="submit" 
            disabled={updateMutation.isPending}
            className="flex items-center gap-2 px-6 py-3 bg-forest text-cream font-medium rounded-sm hover:bg-forest/90 transition-colors disabled:opacity-70"
          >
            {updateMutation.isPending ? 'Saving...' : (
              <>
                <Save className="w-4 h-4" /> Save Profile
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
