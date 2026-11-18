import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import React, { useEffect, useState } from 'react';
import api from './lib/axios';
import axios from 'axios';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import LandingPage from './features/auth/LandingPage';
import LoginPage from './features/auth/LoginPage';
import RegisterPage from './features/auth/RegisterPage';
import OnboardingPage from './features/profile/OnboardingPage';
import DashboardPlaceholder from './features/dashboard/DashboardPlaceholder';
import AppShell from './components/layout/AppShell';
import DailyOverviewPage from './features/dashboard/DailyOverviewPage';
import FitnessPlanPage from './features/dashboard/FitnessPlanPage';
import MealPlannerPage from './features/nutrition/MealPlannerPage';
import FoodAlternativesPage from './features/knowledge/FoodAlternativesPage';
import GroceryListPage from './features/nutrition/GroceryListPage';
import WorkoutPlannerPage from './features/workouts/WorkoutPlannerPage';
import TodayWorkoutPage from './features/workouts/TodayWorkoutPage';
import ProfilePage from './features/profile/ProfilePage';
import SettingsPage from './features/profile/SettingsPage';
import NutritionOverview from './features/nutrition/NutritionOverview';
import MyMealsPage from './features/nutrition/MyMealsPage';
import FoodLibraryPage from './features/knowledge/FoodLibraryPage';
import ExerciseLibraryPage from './features/workouts/ExerciseLibraryPage';
import WorkoutLogPage from './features/workouts/WorkoutLogPage';
import GoalsPage from './features/tracking/GoalsPage';
import ProgressPage from './features/tracking/ProgressPage';
import InsightsPage from './features/tracking/InsightsPage';
import AICoachChat from './features/ai/AICoachChat';
import { GlobalErrorBoundary } from './components/common/ErrorBoundary';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? <Navigate to="/dashboard" replace /> : <>{children}</>;
}

function App() {
  const { setAuth, logout } = useAuthStore();
  const [isInitializing, setIsInitializing] = useState(true);
  const [initError, setInitError] = useState<string | null>(null);

  const initAuth = async () => {
    if (import.meta.env.DEV) console.log("[DIAGNOSTIC] Auth initialization started");
    setIsInitializing(true);
    setInitError(null);
    try {
      const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
      if (import.meta.env.DEV) console.log("[DIAGNOSTIC] Attempting refresh");
      
      const refreshRes = await axios.post(`${baseURL}/auth/refresh`, {}, { withCredentials: true });
      const token = refreshRes.data?.access_token;
      
      if (import.meta.env.DEV) console.log("[DIAGNOSTIC] Token present:", !!token);
      
      if (!token) {
        throw new Error("No valid token format returned from server");
      }
      useAuthStore.getState().setAccessToken(token);

      if (import.meta.env.DEV) console.log("[DIAGNOSTIC] Fetching /auth/me");
      const res = await api.get('/auth/me');
      
      if (import.meta.env.DEV) console.log("[DIAGNOSTIC] /auth/me status:", res.status);
      
      if (!res.data || !res.data.id || !res.data.email) {
        throw new Error("Invalid user data format returned from server");
      }
      
      setAuth(res.data, token);
      if (import.meta.env.DEV) console.log("[DIAGNOSTIC] Auth initialization successful");
      
    } catch (e: any) {
      if (import.meta.env.DEV) console.log("[DIAGNOSTIC] Auth initialization failed:", e.message);
      if (e.response && (e.response.status === 401 || e.response.status === 403)) {
        if (import.meta.env.DEV) console.log("[DIAGNOSTIC] Clearing session due to 401/403");
        logout();
      } else {
        const errorMessage = e.response?.data?.detail || e.message || "Unable to connect to the server.";
        setInitError(`Connection failed: ${errorMessage}`);
      }
    } finally {
      if (import.meta.env.DEV) console.log("[DIAGNOSTIC] Auth initialization ended");
      setIsInitializing(false);
    }
  };

  useEffect(() => {
    initAuth();
  }, [setAuth, logout]);

  if (isInitializing) {
    return <div className="min-h-screen bg-cream flex items-center justify-center text-forest font-medium">Loading AuraFIT...</div>;
  }

  if (initError) {
    return (
      <div className="min-h-screen bg-cream flex flex-col items-center justify-center p-4">
        <div className="bg-surface p-8 rounded-sm shadow-sm max-w-md w-full text-center border border-border">
          <h2 className="text-2xl font-heading text-forest mb-4">Connection Error</h2>
          <p className="text-stone mb-6 text-sm">{initError}</p>
          <button
            onClick={initAuth}
            className="bg-forest text-cream px-6 py-2 rounded-sm font-medium hover:bg-forest/90 transition-colors"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <GlobalErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <Router>
          <Routes>
            <Route path="/" element={<PublicRoute><LandingPage /></PublicRoute>} />
            <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
            <Route path="/register" element={<PublicRoute><RegisterPage /></PublicRoute>} />
            
            <Route path="/onboarding" element={<ProtectedRoute><OnboardingPage /></ProtectedRoute>} />
            
            {/* Authenticated App Shell Routes */}
            <Route element={<ProtectedRoute><AppShell /></ProtectedRoute>}>
              <Route path="/dashboard" element={<DashboardPlaceholder />} />
              
              {/* Main */}
                            <Route path="/daily-overview" element={<DailyOverviewPage />} />
              <Route path="/plan" element={<FitnessPlanPage />} />
              
              {/* Nutrition */}
              <Route path="/meal-planner" element={<MealPlannerPage />} />
              <Route path="/alternatives" element={<FoodAlternativesPage />} />
              <Route path="/grocery" element={<GroceryListPage />} />
              <Route path="/nutrition" element={<NutritionOverview />} />
              <Route path="/meals" element={<MyMealsPage />} />
              <Route path="/knowledge" element={<FoodLibraryPage />} />
              {/* Fitness */}
              <Route path="/workout-planner" element={<WorkoutPlannerPage />} />
              <Route path="/workout/today" element={<TodayWorkoutPage />} />
              <Route path="/exercises" element={<ExerciseLibraryPage />} />
              <Route path="/workouts" element={<WorkoutLogPage />} />
              {/* Tracking */}
              <Route path="/goals" element={<GoalsPage />} />
              <Route path="/progress" element={<ProgressPage />} />
              <Route path="/insights" element={<InsightsPage />} />
              {/* AI */}
              <Route path="/ai/chat" element={<AICoachChat />} />
              <Route path="/ai/food" element={<AICoachChat />} />
              <Route path="/ai/workouts" element={<AICoachChat />} />
              
              {/* Account */}
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>
            
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </QueryClientProvider>
    </GlobalErrorBoundary>
  );
}

export default App;
