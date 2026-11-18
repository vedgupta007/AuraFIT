import { 
  LayoutDashboard, Apple, BookOpen, Library, MessageSquare, HelpCircle, User, CheckSquare,
  Utensils, Search, Calendar, PlayCircle, TrendingUp, Activity, Scale, ShoppingCart, Droplets, Moon
} from 'lucide-react';

export type FeatureStatus = 'implemented' | 'coming_soon' | 'beta';

export interface Feature {
  id: string;
  name: string;
  description: string;
  icon: any;
  path: string;
  status: FeatureStatus;
  enabled: boolean;
  group: 'MAIN' | 'NUTRITION' | 'FITNESS' | 'TRACKING' | 'AI' | 'ACCOUNT';
}

export const FEATURE_REGISTRY: Feature[] = [
  // MAIN
  { id: 'dashboard', name: 'Dashboard', description: 'Your daily wellness overview', icon: LayoutDashboard, path: '/dashboard', status: 'implemented', enabled: true, group: 'MAIN' },
  { id: 'daily-overview', name: 'My Daily Overview', description: 'Detailed view of your day', icon: Calendar, path: '/daily-overview', status: 'coming_soon', enabled: true, group: 'MAIN' },
  { id: 'fitness-plan', name: 'My Fitness Plan', description: 'Your active fitness plan', icon: Activity, path: '/plan', status: 'coming_soon', enabled: true, group: 'MAIN' },
  
  // NUTRITION
  { id: 'nutrition-overview', name: 'Nutrition Overview', description: 'Track calories and macros', icon: Apple, path: '/nutrition', status: 'implemented', enabled: true, group: 'NUTRITION' },
  { id: 'meal-planner', name: 'Meal Planner', description: 'Plan your weekly meals', icon: Utensils, path: '/meal-planner', status: 'coming_soon', enabled: true, group: 'NUTRITION' },
  { id: 'my-meals', name: 'My Meals', description: 'Log and save custom meals', icon: CheckSquare, path: '/meals', status: 'implemented', enabled: true, group: 'NUTRITION' },
  { id: 'food-library', name: 'Food Library', description: 'Browse nutritional database', icon: BookOpen, path: '/knowledge', status: 'implemented', enabled: true, group: 'NUTRITION' },
  { id: 'food-alternatives', name: 'Food Alternatives', description: 'Find healthier swaps', icon: Search, path: '/alternatives', status: 'coming_soon', enabled: true, group: 'NUTRITION' },
  { id: 'grocery-list', name: 'Grocery List', description: 'Generated shopping lists', icon: ShoppingCart, path: '/grocery', status: 'coming_soon', enabled: true, group: 'NUTRITION' },
  
  // FITNESS
  { id: 'workout-planner', name: 'Workout Planner', description: 'Schedule your training', icon: Calendar, path: '/workout-planner', status: 'coming_soon', enabled: true, group: 'FITNESS' },
  { id: 'todays-workout', name: "Today's Workout", description: 'Execute your daily routine', icon: PlayCircle, path: '/workout/today', status: 'coming_soon', enabled: true, group: 'FITNESS' },
  { id: 'exercise-library', name: 'Exercise Library', description: 'Browse movements and form', icon: Library, path: '/exercises', status: 'implemented', enabled: true, group: 'FITNESS' },
  { id: 'workout-progression', name: 'Workout Progression', description: 'Track strength gains', icon: TrendingUp, path: '/progression', status: 'coming_soon', enabled: true, group: 'FITNESS' },
  
  // TRACKING
  { id: 'progress', name: 'Progress', description: 'Overall fitness progress', icon: Activity, path: '/progress', status: 'coming_soon', enabled: true, group: 'TRACKING' },
  { id: 'measurements', name: 'Weight & Measurements', description: 'Track body metrics', icon: Scale, path: '/measurements', status: 'coming_soon', enabled: true, group: 'TRACKING' },
  { id: 'habits', name: 'Habit Tracking', description: 'Monitor daily habits', icon: CheckSquare, path: '/habits', status: 'coming_soon', enabled: true, group: 'TRACKING' },
  { id: 'insights', name: 'Weekly Insights', description: 'Analytics and trends', icon: TrendingUp, path: '/insights', status: 'coming_soon', enabled: true, group: 'TRACKING' },
  { id: 'water', name: 'Water Intake', description: 'Track daily hydration', icon: Droplets, path: '/water', status: 'coming_soon', enabled: true, group: 'TRACKING' },
  { id: 'sleep', name: 'Sleep', description: 'Track sleep patterns', icon: Moon, path: '/sleep', status: 'coming_soon', enabled: true, group: 'TRACKING' },

  // AI
  { id: 'ai-chat', name: 'AuraAI Assistant', description: 'General fitness and nutrition help', icon: MessageSquare, path: '/ai/chat', status: 'implemented', enabled: true, group: 'AI' },
  { id: 'ai-food', name: 'Ask About Food', description: 'Specific nutrition inquiries', icon: HelpCircle, path: '/ai/food', status: 'implemented', enabled: true, group: 'AI' },
  { id: 'ai-workout', name: 'Ask About Workouts', description: 'Specific training inquiries', icon: HelpCircle, path: '/ai/workouts', status: 'implemented', enabled: true, group: 'AI' },
  
  // ACCOUNT
  { id: 'profile', name: 'Profile', description: 'Manage preferences', icon: User, path: '/profile', status: 'implemented', enabled: true, group: 'ACCOUNT' }
];

export function getFeaturesByGroup(group: Feature['group']) {
  return FEATURE_REGISTRY.filter(f => f.group === group && f.enabled);
}

export function getFeature(id: string) {
  return FEATURE_REGISTRY.find(f => f.id === id);
}
