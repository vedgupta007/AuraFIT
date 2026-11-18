import { Link } from 'react-router-dom';
import { ArrowRight, Target, Activity, ChefHat, Brain, Compass, LineChart, ShieldCheck } from 'lucide-react';
import Logo from '../../components/common/Logo';

export default function LandingPage() {
  const featureCategories = [
    {
      title: "Nutrition",
      icon: <ChefHat className="w-5 h-5 text-forest" />,
      features: [
        { name: "Nutrition Overview", desc: "Understand your daily energy and macronutrient balance." },
        { name: "Meal Planner", desc: "Plan your meals ahead of time with exact macro targets." },
        { name: "My Meals", desc: "Save and quickly log your favorite customized recipes." },
        { name: "Food Knowledge", desc: "Learn about the nutritional value of what you eat." },
        { name: "Food Alternatives", desc: "Find healthier swaps for your favorite cravings." },
        { name: "Grocery List", desc: "Automatically generate shopping lists from your meal plans." }
      ]
    },
    {
      title: "Fitness",
      icon: <Activity className="w-5 h-5 text-forest" />,
      features: [
        { name: "Workout Planner", desc: "Create training routines that fit your schedule." },
        { name: "Today's Workout", desc: "A clear view of your daily exercises and sets." },
        { name: "Exercise Library", desc: "Browse a database of movements with proper form guidelines." },
        { name: "Workout Progression", desc: "Track weight and reps to ensure progressive overload." }
      ]
    },
    {
      title: "Progress",
      icon: <LineChart className="w-5 h-5 text-forest" />,
      features: [
        { name: "Progress Tracking", desc: "Visualize your journey with detailed charts." },
        { name: "Weight & Measurements", desc: "Log body metrics safely and consistently." },
        { name: "Habit Tracking", desc: "Build sustainable daily routines for water and sleep." },
        { name: "Weekly Insights", desc: "Review your consistency and adjust your targets." }
      ]
    },
    {
      title: "AI",
      icon: <Brain className="w-5 h-5 text-forest" />,
      features: [
        { name: "AuraAI Assistant", desc: "Your personal guide to navigating fitness and nutrition." },
        { name: "Ask About Food", desc: "Get instant answers about ingredients and meal balance." },
        { name: "Ask About Workouts", desc: "Troubleshoot your training routine and exercise selection." }
      ]
    },
    {
      title: "Account",
      icon: <ShieldCheck className="w-5 h-5 text-forest" />,
      features: [
        { name: "Profile & Preferences", desc: "Set your dietary restrictions and biometric data." },
        { name: "Notifications", desc: "Manage how and when AuraFIT reminds you." },
        { name: "Settings", desc: "Control your privacy and account preferences." }
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border bg-background sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          <Logo />
          <div className="flex items-center gap-6">
            <a href="#features" className="text-sm font-medium text-stone hover:text-forest transition-colors hidden sm:block outline-none focus-visible:ring-2 focus-visible:ring-forest rounded-sm px-1">Features</a>
            <a href="#knowledge" className="text-sm font-medium text-stone hover:text-forest transition-colors hidden sm:block outline-none focus-visible:ring-2 focus-visible:ring-forest rounded-sm px-1">Approach</a>
            <Link to="/login" className="text-sm font-medium text-charcoal hover:text-forest transition-colors outline-none focus-visible:ring-2 focus-visible:ring-forest rounded-sm px-1">
              Log in
            </Link>
            <Link to="/register" className="text-sm font-medium bg-forest text-cream px-5 py-2.5 rounded-sm hover:bg-forest/90 transition-all shadow-sm outline-none focus-visible:ring-2 focus-visible:ring-forest focus-visible:ring-offset-2 focus-visible:ring-offset-background">
              Sign up
            </Link>
          </div>
        </div>
      </nav>

      <main>
        {/* A. HERO SECTION */}
        <section className="relative overflow-hidden pt-16 pb-20 lg:pt-24 lg:pb-32 bg-surface">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
              <div className="max-w-xl slide-up">
                <h2 className="text-5xl lg:text-6xl font-heading text-forest leading-tight mb-6">
                  Understand your body.<br />
                  Eat with purpose.<br />
                  Train with direction.
                </h2>
                <p className="text-lg text-charcoal/80 mb-8 leading-relaxed">
                  AuraFIT is your personalized fitness and nutrition platform. Build a sustainable routine designed for your real life, with practical guidance and smart tracking.
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <Link to="/register" className="inline-flex justify-center items-center gap-2 bg-forest text-cream px-8 py-4 rounded-sm font-medium hover:bg-forest/90 transition-all group shadow-sm outline-none focus-visible:ring-2 focus-visible:ring-forest focus-visible:ring-offset-2 focus-visible:ring-offset-background">
                    Start My Fitness Journey
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </Link>
                  <a href="#features" className="inline-flex justify-center items-center gap-2 bg-transparent border border-border text-charcoal px-8 py-4 rounded-sm font-medium hover:bg-background transition-all outline-none focus-visible:ring-2 focus-visible:ring-forest focus-visible:ring-offset-2 focus-visible:ring-offset-surface">
                    Explore Features
                  </a>
                </div>
              </div>

              {/* High Quality Hero Imagery - Natural Food Photography */}
              <div className="relative h-[400px] sm:h-[500px] lg:h-[600px] rounded-lg overflow-hidden bg-background border border-border slide-up stagger-1 shadow-sm">
                <img
                  src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2053&auto=format&fit=crop"
                  alt="A balanced, nutritious meal containing fresh vegetables, legumes, and healthy fats in warm daylight"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>
        </section>

        {/* B. WHAT IS AURAFIT? */}
        <section id="knowledge" className="py-24 bg-background border-b border-border">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center slide-up stagger-2">
            <div className="inline-flex items-center justify-center p-3 bg-sage/50 rounded-full mb-6">
              <Compass className="w-6 h-6 text-forest" />
            </div>
            <h2 className="text-4xl font-heading text-forest mb-6">A balanced approach.</h2>
            <p className="text-lg text-charcoal/80 leading-relaxed mb-16 max-w-2xl mx-auto">
              We believe that sustainable health comes from understanding, not just blind adherence. AuraFIT helps you build a practical relationship with food and fitness.
            </p>
            <div className="grid md:grid-cols-3 gap-8 text-left">
              <div className="bg-surface p-8 border border-border rounded-sm">
                <Target className="w-8 h-8 text-terracotta mb-6" />
                <h3 className="font-heading text-xl text-forest mb-3">Energy Balance</h3>
                <p className="text-stone text-sm leading-relaxed">Understand calories, macronutrients, and portion awareness without obsessive tracking or rigid diets.</p>
              </div>
              <div className="bg-surface p-8 border border-border rounded-sm">
                <ChefHat className="w-8 h-8 text-terracotta mb-6" />
                <h3 className="font-heading text-xl text-forest mb-3">Food Quality</h3>
                <p className="text-stone text-sm leading-relaxed">Learn how meal composition, dietary preferences, and healthier substitutions influence your daily goals.</p>
              </div>
              <div className="bg-surface p-8 border border-border rounded-sm">
                <Activity className="w-8 h-8 text-terracotta mb-6" />
                <h3 className="font-heading text-xl text-forest mb-3">Consistent Training</h3>
                <p className="text-stone text-sm leading-relaxed">Discover how workout consistency, progressive overload, and recovery adapt to your lifestyle constraints.</p>
              </div>
            </div>
          </div>
        </section>

        {/* C. ALL FEATURES */}
        <section id="features" className="py-24 bg-surface">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-heading text-forest mb-4">What you'll be able to do with AuraFIT</h2>
              <p className="text-stone text-lg max-w-2xl mx-auto">
                Explore the complete set of tools and features we are building to support your fitness and nutrition journey.
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featureCategories.map((category, idx) => (
                <div key={idx} className="bg-background border border-border rounded-sm p-6 shadow-sm">
                  <div className="flex items-center gap-3 mb-6 pb-4 border-b border-border">
                    <div className="p-2 bg-sage/30 rounded-sm">
                      {category.icon}
                    </div>
                    <h3 className="font-heading text-xl text-forest font-medium">{category.title}</h3>
                  </div>
                  <ul className="space-y-5">
                    {category.features.map((feat, fIdx) => (
                      <li key={fIdx}>
                        <h4 className="text-sm font-semibold text-charcoal mb-1">{feat.name}</h4>
                        <p className="text-sm text-stone leading-relaxed">{feat.desc}</p>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* D. FINAL CTA */}
        <section className="py-24 bg-background border-t border-border text-center">
          <div className="max-w-2xl mx-auto px-4">
            <h2 className="text-4xl font-heading text-forest mb-8 leading-tight">Build a plan around your real life.</h2>
            <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
              <Link to="/register" className="w-full sm:w-auto bg-forest text-cream px-8 py-4 rounded-sm font-medium hover:bg-forest/90 transition-colors shadow-sm outline-none focus-visible:ring-2 focus-visible:ring-forest focus-visible:ring-offset-2 focus-visible:ring-offset-background">
                Create Free Account
              </Link>
              <Link to="/login" className="w-full sm:w-auto text-charcoal bg-surface border border-border hover:bg-border/50 px-8 py-4 font-medium transition-colors outline-none focus-visible:ring-2 focus-visible:ring-forest rounded-sm">
                Log In to Your Account
              </Link>
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-surface border-t border-border py-8 text-center text-stone text-sm">
        <p>&copy; {new Date().getFullYear()} AuraFIT. All rights reserved.</p>
      </footer>
    </div>
  );
}

