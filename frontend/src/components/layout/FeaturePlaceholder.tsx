import { useLocation } from 'react-router-dom';
import { Construction } from 'lucide-react';

export default function FeaturePlaceholder() {
  const location = useLocation();
  
  // Format the path to a readable title
  const title = location.pathname
    .replace('/', '')
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ') || 'Feature';

  return (
    <div className="h-[80vh] flex flex-col items-center justify-center text-center px-4 animate-in fade-in">
      <div className="w-20 h-20 bg-forest/5 rounded-full flex items-center justify-center mb-6">
        <Construction className="w-10 h-10 text-forest" />
      </div>
      <h1 className="text-4xl font-heading text-forest mb-4">{title}</h1>
      <p className="text-stone max-w-md mx-auto leading-relaxed">
        This feature is part of a future implementation phase. 
        It will be built following our incremental roadmap to ensure a high-quality, personalized experience.
      </p>
      <div className="mt-8 px-4 py-2 bg-surface border border-border rounded-sm text-sm text-charcoal font-medium inline-block">
        Path: <code className="text-terracotta">{location.pathname}</code>
      </div>
    </div>
  );
}
