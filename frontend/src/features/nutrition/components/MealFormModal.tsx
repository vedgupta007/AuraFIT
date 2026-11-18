import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { X } from 'lucide-react';
import { useEffect } from 'react';

const numericField = z.preprocess(
  (val) => (val === "" || val === undefined || val === null || (typeof val === 'number' && isNaN(val)) ? undefined : Number(val)),
  z.number({ required_error: "Required", invalid_type_error: "Invalid number" }).min(0, "Must be >= 0")
);

const optionalNumericField = z.preprocess(
  (val) => (val === "" || val === undefined || val === null || (typeof val === 'number' && isNaN(val)) ? 0 : Number(val)),
  z.number({ invalid_type_error: "Invalid number" }).min(0, "Must be >= 0")
);

const mealSchema = z.object({
  meal_type: z.enum(['breakfast', 'lunch', 'dinner', 'snack']),
  meal_name: z.string().min(1, 'Meal name is required').max(100),
  consumed_at: z.string(),
  serving_size: z.string().min(1, 'Serving size is required'),
  calories: numericField,
  protein_grams: numericField,
  carbohydrates_grams: optionalNumericField,
  fat_grams: optionalNumericField,
  fiber_grams: optionalNumericField,
  notes: z.string().max(500).optional(),
});

type MealFormValues = z.infer<typeof mealSchema>;

// The form state before Zod transforms the strings to numbers
type MealFormInputValues = {
  meal_type: "breakfast" | "lunch" | "dinner" | "snack";
  meal_name: string;
  consumed_at: string;
  serving_size: string;
  calories: number | string;
  protein_grams: number | string;
  carbohydrates_grams: number | string;
  fat_grams: number | string;
  fiber_grams: number | string;
  notes?: string;
};

interface MealFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: MealFormValues) => Promise<void>;
  initialData?: any;
  title: string;
}

export default function MealFormModal({ isOpen, onClose, onSubmit, initialData, title }: MealFormModalProps) {
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<MealFormInputValues>({
    resolver: zodResolver(mealSchema) as any,
    defaultValues: {
      meal_type: 'breakfast',
      consumed_at: '',
      calories: '',
      protein_grams: '',
      carbohydrates_grams: '',
      fat_grams: '',
      fiber_grams: '',
    }
  });

  const getLocalDatetimeLocal = (dateObj: Date) => {
    const tzOffsetMs = dateObj.getTimezoneOffset() * 60000;
    return new Date(dateObj.getTime() - tzOffsetMs).toISOString().slice(0, 16);
  };

  useEffect(() => {
    if (initialData) {
      // Partial updates logic: strip out null or undefined to avoid overwriting valid fields
      const safeData = { ...initialData };
      if (safeData.notes === null || safeData.notes === undefined) {
          delete safeData.notes;
      }
      
      reset({
        ...safeData,
        consumed_at: getLocalDatetimeLocal(new Date(initialData.consumed_at)),
        // Map any 0s back to '' if desired, or keep as is. The user requested: "When editing an existing meal: Display its saved numeric values correctly."
        // We leave them as numbers, RHF will display them.
      });
    } else {
      reset({
        meal_type: 'breakfast',
        consumed_at: getLocalDatetimeLocal(new Date()),
        calories: '',
        protein_grams: '',
        carbohydrates_grams: '',
        fat_grams: '',
        fiber_grams: '',
      });
    }
  }, [initialData, reset, isOpen]);

  if (!isOpen) return null;

  const handleFormSubmit = async (data: any) => {
    const dateObj = new Date(data.consumed_at);
    const utcDate = dateObj.toISOString();
    await onSubmit({ ...data, consumed_at: utcDate });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-charcoal/50 backdrop-blur-sm fade-in">
      <div className="bg-surface rounded-md shadow-lg w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-surface p-4 border-b border-border flex justify-between items-center z-10">
          <h2 className="text-xl font-heading font-semibold text-forest">{title}</h2>
          <button onClick={onClose} className="p-1 hover:bg-stone/10 rounded-sm outline-none focus-visible:ring-2 focus-visible:ring-forest text-stone hover:text-charcoal transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <form onSubmit={handleSubmit(handleFormSubmit)} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-sm font-medium text-charcoal">Meal Type <span className="text-terracotta">*</span></label>
              <select {...register('meal_type')} className="w-full h-10 px-3 rounded-sm border border-border bg-surface text-charcoal focus:outline-none focus:ring-2 focus:ring-forest">
                <option value="breakfast">Breakfast</option>
                <option value="lunch">Lunch</option>
                <option value="dinner">Dinner</option>
                <option value="snack">Snack</option>
              </select>
              {errors.meal_type && <p className="text-xs text-terracotta">{errors.meal_type.message as string}</p>}
            </div>
            
            <div className="space-y-1">
              <label className="text-sm font-medium text-charcoal">Date & Time <span className="text-terracotta">*</span></label>
              <input type="datetime-local" {...register('consumed_at')} className="w-full h-10 px-3 rounded-sm border border-border bg-surface text-charcoal focus:outline-none focus:ring-2 focus:ring-forest" />
              {errors.consumed_at && <p className="text-xs text-terracotta">{errors.consumed_at.message as string}</p>}
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium text-charcoal">Meal Name <span className="text-terracotta">*</span></label>
            <input type="text" placeholder="e.g. Avocado Toast" {...register('meal_name')} className="w-full h-10 px-3 rounded-sm border border-border bg-surface text-charcoal focus:outline-none focus:ring-2 focus:ring-forest" />
            {errors.meal_name && <p className="text-xs text-terracotta">{errors.meal_name.message as string}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-sm font-medium text-charcoal">Serving Size <span className="text-terracotta">*</span></label>
              <input type="text" placeholder="e.g. 2 slices" {...register('serving_size')} className="w-full h-10 px-3 rounded-sm border border-border bg-surface text-charcoal focus:outline-none focus:ring-2 focus:ring-forest" />
              {errors.serving_size && <p className="text-xs text-terracotta">{errors.serving_size.message as string}</p>}
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium text-charcoal">Calories (kcal) <span className="text-terracotta">*</span></label>
              <input type="number" placeholder="Enter calories" {...register('calories')} className="w-full h-10 px-3 rounded-sm border border-border bg-surface text-charcoal focus:outline-none focus:ring-2 focus:ring-forest" />
              {errors.calories && <p className="text-xs text-terracotta">{errors.calories.message as string}</p>}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-sm font-medium text-charcoal">Protein (g) <span className="text-terracotta">*</span></label>
              <input type="number" step="0.1" placeholder="Enter protein" {...register('protein_grams')} className="w-full h-10 px-3 rounded-sm border border-border bg-surface text-charcoal focus:outline-none focus:ring-2 focus:ring-forest" />
              {errors.protein_grams && <p className="text-xs text-terracotta">{errors.protein_grams.message as string}</p>}
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium text-charcoal">Carbs (g) <span className="text-stone font-normal text-xs">(optional)</span></label>
              <input type="number" step="0.1" placeholder="Enter carbohydrates" {...register('carbohydrates_grams')} className="w-full h-10 px-3 rounded-sm border border-border bg-surface text-charcoal focus:outline-none focus:ring-2 focus:ring-forest" />
              {errors.carbohydrates_grams && <p className="text-xs text-terracotta">{errors.carbohydrates_grams.message as string}</p>}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-sm font-medium text-charcoal">Fat (g) <span className="text-stone font-normal text-xs">(optional)</span></label>
              <input type="number" step="0.1" placeholder="Enter fat" {...register('fat_grams')} className="w-full h-10 px-3 rounded-sm border border-border bg-surface text-charcoal focus:outline-none focus:ring-2 focus:ring-forest" />
              {errors.fat_grams && <p className="text-xs text-terracotta">{errors.fat_grams.message as string}</p>}
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium text-charcoal">Fiber (g) <span className="text-stone font-normal text-xs">(optional)</span></label>
              <input type="number" step="0.1" placeholder="Enter fiber" {...register('fiber_grams')} className="w-full h-10 px-3 rounded-sm border border-border bg-surface text-charcoal focus:outline-none focus:ring-2 focus:ring-forest" />
              {errors.fiber_grams && <p className="text-xs text-terracotta">{errors.fiber_grams.message as string}</p>}
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium text-charcoal">Notes <span className="text-stone font-normal text-xs">(optional)</span></label>
            <textarea {...register('notes')} className="w-full p-3 rounded-sm border border-border bg-surface text-charcoal focus:outline-none focus:ring-2 focus:ring-forest min-h-[80px]"></textarea>
            {errors.notes && <p className="text-xs text-terracotta">{errors.notes.message as string}</p>}
          </div>

          <div className="pt-4 flex justify-end gap-3">
            <button type="button" onClick={onClose} className="px-4 py-2 font-medium text-charcoal hover:bg-stone/10 rounded-sm transition-colors outline-none focus-visible:ring-2 focus-visible:ring-forest">
              Cancel
            </button>
            <button type="submit" disabled={isSubmitting} className="px-6 py-2 bg-forest text-cream font-medium rounded-sm hover:bg-forest/90 transition-colors disabled:opacity-50 outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-forest">
              {isSubmitting ? 'Saving...' : 'Save Meal'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
