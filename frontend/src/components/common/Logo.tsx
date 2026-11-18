import { Leaf } from 'lucide-react';
import { Link } from 'react-router-dom';

interface LogoProps {
  to?: string;
  className?: string;
  iconClassName?: string;
  textClassName?: string;
}

export default function Logo({ 
  to = '/', 
  className = '', 
  iconClassName = 'w-6 h-6 text-forest', 
  textClassName = 'text-2xl font-heading font-semibold text-forest' 
}: LogoProps) {
  return (
    <Link 
      to={to} 
      className={`flex items-center gap-2 group outline-none rounded-sm focus-visible:ring-2 focus-visible:ring-forest ${className}`}
    >
      <Leaf className={`${iconClassName} group-hover:scale-110 transition-transform`} />
      <span className={textClassName}>AuraFIT</span>
    </Link>
  );
}
