import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import api from '../../lib/axios';
import { useAuthStore } from '../../store/authStore';
import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import Logo from '../../components/common/Logo';

const registerSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"]
});

type RegisterForm = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema)
  });
  const [serverError, setServerError] = useState('');
  const { setAccessToken, setUser } = useAuthStore();
  const navigate = useNavigate();

  const onSubmit = async (data: RegisterForm) => {
    try {
      setServerError('');
      const res = await api.post('/auth/register', {
        email: data.email,
        password: data.password
      });
      setAccessToken(res.data.access_token);
      
      const meRes = await api.get('/auth/me');
      setUser(meRes.data);
      
      navigate('/onboarding');
    } catch (err: any) {
      setServerError(err.response?.data?.detail || 'An error occurred during registration');
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 fade-in">
      <div className="w-full max-w-md bg-surface p-10 shadow-sm border border-border rounded-sm">
        <div className="text-center mb-8 flex flex-col items-center">
          <Logo iconClassName="w-8 h-8 text-forest" textClassName="text-3xl font-heading font-semibold text-forest" />
          <h2 className="mt-6 text-xl font-medium text-forest">Create your account</h2>
        </div>
        
        {serverError && (
          <div className="mb-6 p-4 bg-terracotta/10 border border-terracotta/20 text-terracotta text-sm rounded-sm">
            {serverError}
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-forest mb-1.5">Email</label>
            <input 
              type="email" 
              {...register('email')}
              className="w-full p-3 bg-background border border-border rounded-sm focus:border-forest focus:ring-1 focus:ring-forest outline-none transition-all placeholder:text-stone/60"
              placeholder="you@example.com"
            />
            {errors.email && <p className="mt-1.5 text-sm text-terracotta">{errors.email.message}</p>}
          </div>
          
          <div>
            <label className="block text-sm font-medium text-forest mb-1.5">Password</label>
            <input 
              type="password" 
              {...register('password')}
              className="w-full p-3 bg-background border border-border rounded-sm focus:border-forest focus:ring-1 focus:ring-forest outline-none transition-all"
            />
            {errors.password && <p className="mt-1.5 text-sm text-terracotta">{errors.password.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-forest mb-1.5">Confirm Password</label>
            <input 
              type="password" 
              {...register('confirmPassword')}
              className="w-full p-3 bg-background border border-border rounded-sm focus:border-forest focus:ring-1 focus:ring-forest outline-none transition-all"
            />
            {errors.confirmPassword && <p className="mt-1.5 text-sm text-terracotta">{errors.confirmPassword.message}</p>}
          </div>

          <button 
            type="submit" 
            disabled={isSubmitting}
            className="w-full py-3.5 mt-2 bg-forest text-cream font-medium rounded-sm hover:bg-forest/90 transition-colors disabled:opacity-70 outline-none focus-visible:ring-2 focus-visible:ring-forest focus-visible:ring-offset-2 focus-visible:ring-offset-surface shadow-sm"
          >
            {isSubmitting ? 'Creating account...' : 'Create Account'}
          </button>
        </form>
        
        <p className="mt-8 text-center text-sm text-stone">
          Already have an account? <Link to="/login" className="text-forest font-medium hover:underline outline-none focus-visible:ring-2 focus-visible:ring-forest rounded-sm px-1">Sign in</Link>
        </p>
      </div>
    </div>
  );
}


