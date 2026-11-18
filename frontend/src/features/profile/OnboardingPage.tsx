import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useNavigate } from 'react-router-dom';
import api from '../../lib/axios';

const onboardingSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  age: z.coerce.number().min(12).max(120),
  sex: z.enum(["M", "F", "Other"]),
  heightUnit: z.enum(["cm", "ft"]),
  height_cm: z.coerce.number().positive().max(300).optional(),
  height_ft: z.coerce.number().min(0).max(9).optional(),
  height_in: z.coerce.number().min(0).max(11).optional(),
  weight_kg: z.coerce.number().positive(),
  goal: z.enum(["lose_weight", "maintain_weight", "gain_muscle", "improve_fitness"]),
  activity_level: z.enum(["sedentary", "light", "moderate", "active", "very_active"]),
  training_experience: z.enum(["beginner", "intermediate", "advanced"]),
  preferred_workout_frequency: z.coerce.number().min(1).max(7),
  dietary_preference: z.enum(["vegetarian", "vegan", "eggetarian", "non_vegetarian", "other"]),
  allergies: z.string().optional(),
  disliked_foods: z.string().optional(),
}).superRefine((data, ctx) => {
  if (data.heightUnit === 'cm') {
    if (!data.height_cm) {
      ctx.addIssue({ code: z.ZodIssueCode.custom, message: "Required", path: ["height_cm"] });
    }
  } else {
    if (data.height_ft === undefined || data.height_ft < 1) {
      ctx.addIssue({ code: z.ZodIssueCode.custom, message: "Required", path: ["height_ft"] });
    }
    if (data.height_in === undefined || data.height_in < 0 || data.height_in > 11) {
      ctx.addIssue({ code: z.ZodIssueCode.custom, message: "Must be 0-11", path: ["height_in"] });
    }
  }
});

type OnboardingForm = z.infer<typeof onboardingSchema>;

const STEPS = [
  { id: 'welcome', title: 'Welcome to AuraFIT' },
  { id: 'basic', title: 'Basic Information', fields: ['name'] },
  { id: 'body', title: 'Body Measurements', fields: ['age', 'sex', 'heightUnit', 'height_cm', 'height_ft', 'height_in', 'weight_kg'] },
  { id: 'goal', title: 'Fitness Goal', fields: ['goal'] },
  { id: 'activity', title: 'Activity & Training', fields: ['activity_level', 'training_experience', 'preferred_workout_frequency'] },
  { id: 'diet', title: 'Diet Preferences', fields: ['dietary_preference'] },
  { id: 'allergies', title: 'Allergies & Dislikes', fields: ['allergies', 'disliked_foods'] },
  { id: 'review', title: 'Review' }
];

import { ftInToCm } from '../../utils/height';

export default function OnboardingPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [serverError, setServerError] = useState('');
  const navigate = useNavigate();
  
  const { register, handleSubmit, trigger, watch, setValue, formState: { errors, isSubmitting } } = useForm<OnboardingForm>({
    resolver: zodResolver(onboardingSchema),
    defaultValues: {
      name: '', age: 25, sex: 'M', heightUnit: 'ft', height_cm: 170, height_ft: 5, height_in: 7, weight_kg: 70,
      goal: 'improve_fitness', activity_level: 'moderate', training_experience: 'beginner',
      preferred_workout_frequency: 3, dietary_preference: 'non_vegetarian',
      allergies: '', disliked_foods: ''
    }
  });

  const formData = watch();

  const nextStep = async () => {
    const fields = STEPS[currentStep].fields;
    if (fields) {
      const isValid = await trigger(fields as any);
      if (!isValid) return;
    }
    setCurrentStep(s => Math.min(s + 1, STEPS.length - 1));
  };

  const prevStep = () => setCurrentStep(s => Math.max(s - 1, 0));

  const onSubmit = async (data: OnboardingForm) => {
    try {
      setServerError('');
      const finalHeightCm = data.heightUnit === 'cm' 
        ? data.height_cm 
        : ftInToCm(data.height_ft || 0, data.height_in || 0);
        
      const payload = {
        name: data.name,
        age: data.age,
        sex: data.sex,
        height_cm: finalHeightCm,
        weight_kg: data.weight_kg,
        goal: data.goal,
        activity_level: data.activity_level,
        training_experience: data.training_experience,
        preferred_workout_frequency: data.preferred_workout_frequency,
        dietary_preference: data.dietary_preference,
        allergies: data.allergies ? data.allergies.split(',').map(s => s.trim()).filter(Boolean) : [],
        disliked_foods: data.disliked_foods ? data.disliked_foods.split(',').map(s => s.trim()).filter(Boolean) : []
      };
      
      await api.post('/profile', payload);
      navigate('/dashboard');
    } catch (err: any) {
      setServerError(err.response?.data?.detail || 'Failed to save profile');
    }
  };

  const stepDef = STEPS[currentStep];

  return (
    <div className="min-h-screen bg-background flex flex-col items-center py-12 px-4 fade-in">
      <div className="w-full max-w-2xl bg-surface p-8 md:p-12 shadow-sm border border-border rounded-sm">
        
        {/* Progress */}
        <div className="mb-12">
          <div className="flex justify-between items-center mb-4">
            <span className="text-sm font-medium text-forest">Step {currentStep + 1} of {STEPS.length}</span>
            <span className="text-sm font-medium text-stone">{stepDef.title}</span>
          </div>
          <div className="w-full bg-border h-2 rounded-full overflow-hidden">
            <div 
              className="bg-forest h-full transition-all duration-500 ease-out" 
              style={{ width: `${((currentStep + 1) / STEPS.length) * 100}%` }}
            ></div>
          </div>
        </div>

        {serverError && (
          <div className="mb-6 p-4 bg-terracotta/10 border border-terracotta/20 text-terracotta text-sm rounded-sm">
            {serverError}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)}>
          
          <div className="min-h-[300px]">
            {currentStep === 0 && (
              <div className="text-center space-y-6 pt-8">
                <h2 className="text-4xl font-heading text-forest">Welcome to AuraFIT</h2>
                <p className="text-lg text-stone font-light">
                  We're excited to have you. To create your personalized AI fitness and nutrition plan, 
                  we need to learn a bit about your body, lifestyle, and goals.
                </p>
                <p className="text-stone">This will take about 2 minutes.</p>
              </div>
            )}

            {currentStep === 1 && (
              <div className="space-y-6">
                <h2 className="text-3xl font-heading text-forest mb-8">What should we call you?</h2>
                <div>
                  <label className="block text-sm font-medium text-forest mb-2">First Name</label>
                  <input 
                    type="text" 
                    {...register('name')}
                    className="w-full p-4 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest focus:ring-1 focus:ring-forest text-lg"
                    placeholder="e.g., Alex"
                  />
                  {errors.name && <p className="mt-2 text-sm text-terracotta">{errors.name.message}</p>}
                </div>
              </div>
            )}

            {currentStep === 2 && (
              <div className="space-y-6">
                <h2 className="text-3xl font-heading text-forest mb-8">Body Measurements</h2>
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-forest mb-2">Age</label>
                    <input type="number" {...register('age')} className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest" />
                    {errors.age && <p className="mt-1 text-sm text-terracotta">{errors.age.message}</p>}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-forest mb-2">Biological Sex</label>
                    <select {...register('sex')} className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest">
                      <option value="M">Male</option>
                      <option value="F">Female</option>
                      <option value="Other">Other</option>
                    </select>
                    {errors.sex && <p className="mt-1 text-sm text-terracotta">{errors.sex.message}</p>}
                  </div>
                  
                  <div className="col-span-2 sm:col-span-1">
                    <div className="flex justify-between items-end mb-2">
                      <label className="block text-sm font-medium text-forest">Height</label>
                      <div className="flex bg-forest/5 p-1 rounded-sm">
                        <button 
                          type="button" 
                          onClick={() => setValue('heightUnit', 'ft')}
                          className={`px-2 py-0.5 text-xs font-medium rounded-sm transition-colors ${formData.heightUnit === 'ft' ? 'bg-forest text-cream' : 'text-stone hover:text-forest'}`}
                        >
                          ft/in
                        </button>
                        <button 
                          type="button" 
                          onClick={() => setValue('heightUnit', 'cm')}
                          className={`px-2 py-0.5 text-xs font-medium rounded-sm transition-colors ${formData.heightUnit === 'cm' ? 'bg-forest text-cream' : 'text-stone hover:text-forest'}`}
                        >
                          cm
                        </button>
                      </div>
                    </div>
                    
                    {formData.heightUnit === 'cm' ? (
                      <div>
                        <input type="number" step="0.1" {...register('height_cm')} placeholder="e.g. 170" className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest" />
                        {errors.height_cm && <p className="mt-1 text-sm text-terracotta">{errors.height_cm.message}</p>}
                      </div>
                    ) : (
                      <div className="flex gap-2">
                        <div className="flex-1">
                          <input type="number" {...register('height_ft')} placeholder="ft" className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest" />
                          {errors.height_ft && <p className="mt-1 text-sm text-terracotta">{errors.height_ft.message}</p>}
                        </div>
                        <div className="flex-1">
                          <input type="number" {...register('height_in')} placeholder="in" className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest" />
                          {errors.height_in && <p className="mt-1 text-sm text-terracotta">{errors.height_in.message}</p>}
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="col-span-2 sm:col-span-1">
                    <label className="block text-sm font-medium text-forest mb-2">Weight (kg)</label>
                    <input type="number" step="0.1" {...register('weight_kg')} className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest" />
                    {errors.weight_kg && <p className="mt-1 text-sm text-terracotta">{errors.weight_kg.message}</p>}
                  </div>
                </div>
              </div>
            )}

            {currentStep === 3 && (
              <div className="space-y-6">
                <h2 className="text-3xl font-heading text-forest mb-8">What is your primary goal?</h2>
                <div className="space-y-3">
                  {[
                    { val: 'lose_weight', label: 'Lose Weight & Body Fat' },
                    { val: 'maintain_weight', label: 'Maintain Current Weight' },
                    { val: 'gain_muscle', label: 'Build Muscle & Size' },
                    { val: 'improve_fitness', label: 'Improve General Fitness & Endurance' }
                  ].map(opt => (
                    <label key={opt.val} className={`block p-4 border rounded-sm cursor-pointer transition-all ${formData.goal === opt.val ? 'border-forest bg-forest/5' : 'border-forest/20 hover:border-forest/50'}`}>
                      <div className="flex items-center">
                        <input type="radio" value={opt.val} {...register('goal')} className="mr-3 accent-forest" />
                        <span className="font-medium text-forest">{opt.label}</span>
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            )}

            {currentStep === 4 && (
              <div className="space-y-8">
                <h2 className="text-3xl font-heading text-forest mb-6">Activity & Training</h2>
                
                <div>
                  <label className="block text-sm font-medium text-forest mb-3">Daily Activity Level</label>
                  <select {...register('activity_level')} className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest">
                    <option value="sedentary">Sedentary (Office job, little movement)</option>
                    <option value="light">Lightly Active (1-3 days/week exercise)</option>
                    <option value="moderate">Moderately Active (3-5 days/week)</option>
                    <option value="active">Active (6-7 days/week)</option>
                    <option value="very_active">Very Active (Physical job or 2x training/day)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-forest mb-3">Training Experience</label>
                  <select {...register('training_experience')} className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest">
                    <option value="beginner">Beginner (New to lifting/fitness)</option>
                    <option value="intermediate">Intermediate (1-3 years consistent training)</option>
                    <option value="advanced">Advanced (3+ years consistent training)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-forest mb-3">Preferred Workout Frequency (Days/Week)</label>
                  <input type="number" min="1" max="7" {...register('preferred_workout_frequency')} className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest" />
                  {errors.preferred_workout_frequency && <p className="mt-1 text-sm text-terracotta">{errors.preferred_workout_frequency.message}</p>}
                </div>
              </div>
            )}

            {currentStep === 5 && (
              <div className="space-y-6">
                <h2 className="text-3xl font-heading text-forest mb-8">Dietary Preferences</h2>
                <div className="space-y-3">
                  {[
                    { val: 'non_vegetarian', label: 'No Restrictions (Non-Vegetarian)' },
                    { val: 'vegetarian', label: 'Vegetarian' },
                    { val: 'eggetarian', label: 'Eggetarian' },
                    { val: 'vegan', label: 'Vegan' },
                    { val: 'other', label: 'Other' }
                  ].map(opt => (
                    <label key={opt.val} className={`block p-4 border rounded-sm cursor-pointer transition-all ${formData.dietary_preference === opt.val ? 'border-forest bg-forest/5' : 'border-forest/20 hover:border-forest/50'}`}>
                      <div className="flex items-center">
                        <input type="radio" value={opt.val} {...register('dietary_preference')} className="mr-3 accent-forest" />
                        <span className="font-medium text-forest">{opt.label}</span>
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            )}

            {currentStep === 6 && (
              <div className="space-y-6">
                <h2 className="text-3xl font-heading text-forest mb-8">Allergies & Dislikes</h2>
                
                <div>
                  <label className="block text-sm font-medium text-forest mb-2">Allergies / Intolerances (Comma separated)</label>
                  <input 
                    type="text" 
                    {...register('allergies')}
                    className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest"
                    placeholder="e.g., Peanuts, Dairy, Gluten"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-forest mb-2">Disliked Foods (Comma separated)</label>
                  <input 
                    type="text" 
                    {...register('disliked_foods')}
                    className="w-full p-3 bg-background border border-border placeholder:text-stone/60 rounded-sm focus:border-forest"
                    placeholder="e.g., Mushrooms, Broccoli"
                  />
                </div>
              </div>
            )}

            {currentStep === 7 && (
              <div className="space-y-8">
                <h2 className="text-3xl font-heading text-forest mb-6">Review Your Profile</h2>
                
                <div className="grid grid-cols-2 gap-6 text-sm">
                  <div className="border-b border-border pb-4">
                    <span className="block text-stone mb-1">Name</span>
                    <span className="font-medium text-forest text-lg">{formData.name}</span>
                  </div>
                  <div className="border-b border-border pb-4">
                    <span className="block text-stone mb-1">Goal</span>
                    <span className="font-medium text-forest capitalize">{formData.goal.replace('_', ' ')}</span>
                  </div>
                  <div className="border-b border-border pb-4">
                    <span className="block text-stone mb-1">Stats</span>
                    <span className="font-medium text-forest">
                      {formData.age} yrs • {formData.sex} • {formData.weight_kg}kg • {' '}
                      {formData.heightUnit === 'cm' 
                        ? `${formData.height_cm}cm` 
                        : `${formData.height_ft}'${formData.height_in}"`}
                    </span>
                  </div>
                  <div className="border-b border-border pb-4">
                    <span className="block text-stone mb-1">Diet</span>
                    <span className="font-medium text-forest capitalize">{formData.dietary_preference.replace('_', ' ')}</span>
                  </div>
                </div>
                
                <p className="text-stone italic text-sm text-center">Ready to generate your AI fitness plan?</p>
              </div>
            )}
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-between mt-12 pt-6 border-t border-border">
            <button 
              type="button" 
              onClick={prevStep}
              disabled={currentStep === 0 || isSubmitting}
              className={`px-6 py-3 font-medium text-forest transition-opacity ${currentStep === 0 ? 'opacity-0 pointer-events-none' : 'opacity-100 hover:text-forest/70'}`}
            >
              Back
            </button>
            
            {currentStep < STEPS.length - 1 ? (
              <button 
                type="button" 
                onClick={nextStep}
                className="px-8 py-3 bg-forest text-cream font-medium rounded-sm hover:bg-forest/90 transition-colors"
              >
                Continue
              </button>
            ) : (
              <button 
                type="submit" 
                disabled={isSubmitting}
                className="px-8 py-3 bg-terracotta text-cream font-medium rounded-sm hover:bg-terracotta/90 transition-colors disabled:opacity-70"
              >
                {isSubmitting ? 'Creating Profile...' : 'Complete Setup'}
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
