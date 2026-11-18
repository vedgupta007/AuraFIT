import { useState } from 'react';
import { NavLink, Outlet, useNavigate, Link } from 'react-router-dom';
import { 
  LayoutDashboard, Calendar, FileText, Utensils, BookOpen, Apple,
  ShoppingCart, PlayCircle, Library, TrendingUp, Scale, 
  CheckSquare, MessageSquare, Search, HelpCircle, User, 
  Settings, Bell, LogOut, Menu, X, Leaf, ClipboardList, Target
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import api from '../../lib/axios';

const NAV_GROUPS = [
  {
    title: 'MAIN',
    items: [
      { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
      { name: 'My Daily Overview', path: '/daily-overview', icon: Calendar },
      { name: 'My Fitness Plan', path: '/plan', icon: FileText },
    ]
  },
  {
    title: 'NUTRITION',
    items: [
      { name: 'Nutrition Overview', path: '/nutrition', icon: Apple },
      { name: 'Meal Planner', path: '/meal-planner', icon: Utensils },
      { name: 'My Meals', path: '/meals', icon: CheckSquare },
      { name: 'Food Knowledge', path: '/knowledge', icon: BookOpen },
      { name: 'Food Alternatives', path: '/alternatives', icon: Search },
      { name: 'Grocery List', path: '/grocery', icon: ShoppingCart },
    ]
  },
  {
    title: 'FITNESS',
    items: [
      { name: 'Workout Planner', path: '/workout-planner', icon: Calendar },
      { name: 'Today\'s Workout', path: '/workout/today', icon: PlayCircle },
      { name: 'Workout Log', path: '/workouts', icon: ClipboardList },
      { name: 'Exercise Library', path: '/exercises', icon: Library },
      { name: 'Workout Progression', path: '/insights', icon: TrendingUp },
    ]
  },
  {
    title: 'TRACKING',
    items: [
      { name: 'My Goals', path: '/goals', icon: Target },
      { name: 'Progress & Measurements', path: '/progress', icon: Scale },
      { name: 'Habit Tracking', path: '/habits', icon: CheckSquare },
      { name: 'Weekly Insights', path: '/insights', icon: TrendingUp },
    ]
  },
  {
    title: 'AI',
    items: [
      { name: 'AuraAI Assistant', path: '/ai/chat', icon: MessageSquare },
      { name: 'Ask About Food', path: '/ai/food', icon: HelpCircle },
      { name: 'Ask About Workouts', path: '/ai/workouts', icon: HelpCircle },
    ]
  },
  {
    title: 'ACCOUNT',
    items: [
      { name: 'Profile', path: '/profile', icon: User },
      { name: 'Settings', path: '/settings', icon: Settings },
    ]
  }
];

export default function AppShell() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [desktopSidebarOpen, setDesktopSidebarOpen] = useState(true);
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (e) {
      // Ignore
    } finally {
      logout();
      navigate('/');
    }
  };

  return (
    <div className="h-screen flex overflow-hidden bg-cream selection:bg-forest/20 selection:text-forest">
      
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-charcoal/50 backdrop-blur-sm lg:hidden transition-opacity fade-in"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside 
        className={`fixed inset-y-0 left-0 z-50 bg-oat border-r border-forest/10 flex flex-col h-full transition-all duration-300 ease-in-out shrink-0
          ${sidebarOpen ? 'translate-x-0 w-72' : '-translate-x-full w-72'} 
          ${desktopSidebarOpen ? 'lg:translate-x-0 lg:static lg:w-72' : 'lg:-translate-x-full lg:absolute lg:w-0 lg:overflow-hidden lg:opacity-0'}
        `}
      >
        <div className="h-16 flex items-center justify-between px-6 border-b border-forest/10 bg-oat shrink-0">
          <Link to="/dashboard" className="flex items-center gap-2 outline-none group">
            <Leaf className="text-forest w-6 h-6 transition-transform group-hover:scale-110" />
            <span className="text-2xl font-heading font-semibold text-forest">AuraFIT</span>
          </Link>
          <div className="flex items-center">
            <button onClick={() => setDesktopSidebarOpen(false)} className="hidden lg:flex text-stone hover:text-forest transition-colors" title="Collapse sidebar">
              <Menu className="w-5 h-5" />
            </button>
            <button onClick={() => setSidebarOpen(false)} className="lg:hidden text-stone hover:text-forest">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto py-6 px-4 space-y-8 custom-scrollbar">
          {NAV_GROUPS.map((group, i) => (
            <div key={i}>
              <h3 className="px-3 text-xs font-semibold text-stone uppercase tracking-wider mb-2">
                {group.title}
              </h3>
              <ul className="space-y-1">
                {group.items.map((item, j) => {
                  const Icon = item.icon;
                  return (
                    <li key={j}>
                      <NavLink
                        to={item.path}
                        onClick={() => setSidebarOpen(false)}
                        className={({ isActive }) => 
                          `flex items-center gap-3 px-3 py-2 rounded-sm text-sm font-medium transition-all group ${
                            isActive 
                              ? 'bg-forest text-cream shadow-sm' 
                              : 'text-charcoal hover:bg-forest/10 hover:text-forest'
                          }`
                        }
                      >
                        <Icon className="w-4 h-4 shrink-0" />
                        <span>{item.name}</span>
                      </NavLink>
                    </li>
                  );
                })}
                {group.title === 'ACCOUNT' && (
                  <li>
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-3 py-2 rounded-sm text-sm font-medium text-terracotta hover:bg-terracotta/10 transition-all group"
                    >
                      <LogOut className="w-4 h-4 shrink-0" />
                      <span>Logout</span>
                    </button>
                  </li>
                )}
              </ul>
            </div>
          ))}
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 h-full overflow-hidden transition-all duration-300">
        
        {/* Topbar */}
        <header className="h-16 bg-cream border-b border-forest/10 flex items-center justify-between px-4 sm:px-6 lg:px-8 shrink-0 z-10 relative shadow-sm transition-all duration-300">
          <div className="flex items-center">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden text-charcoal hover:text-forest mr-4"
            >
              <Menu className="w-6 h-6" />
            </button>
            {!desktopSidebarOpen && (
              <button
                onClick={() => setDesktopSidebarOpen(true)}
                className="hidden lg:block text-charcoal hover:text-forest mr-4 transition-colors"
                title="Expand sidebar"
              >
                <Menu className="w-6 h-6" />
              </button>
            )}
            <h2 className="text-lg font-heading text-forest font-medium hidden sm:block">
              {/* Dynamic title could go here based on route */}
              Welcome back
            </h2>
          </div>
          <div className="flex items-center gap-4">
            <button className="text-stone hover:text-forest transition-colors relative">
              <Bell className="w-5 h-5" />
              <span className="absolute top-0 right-0 w-2 h-2 bg-terracotta rounded-full"></span>
            </button>
            <Link 
              to="/profile" 
              className="w-8 h-8 rounded-full bg-forest text-cream flex items-center justify-center font-medium text-sm hover:ring-2 hover:ring-forest hover:ring-offset-2 transition-all outline-none"
              title="Go to Profile"
            >
              {user?.email?.charAt(0).toUpperCase() || 'U'}
            </Link>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto bg-cream p-4 sm:p-6 lg:p-8 custom-scrollbar">
          <div className="max-w-6xl mx-auto slide-up w-full h-full">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
