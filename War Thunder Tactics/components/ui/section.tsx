import Link from 'next/link';
import { ReactNode } from 'react';

interface SectionProps {
  title: string;
  description?: string;
  children: ReactNode;
  viewAllLink?: string;
  viewAllText?: string;
  className?: string;
}

export function Section({ 
  title, 
  description, 
  children, 
  viewAllLink, 
  viewAllText = 'View All', 
  className = '' 
}: SectionProps) {
  return (
    <section className={`py-12 ${className}`}>
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row md:items-end md:justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold text-olive-drab mb-2">{title}</h2>
            {description && (
              <p className="text-off-white/80 max-w-2xl">{description}</p>
            )}
          </div>
          
          {viewAllLink && (
            <Link 
              href={viewAllLink} 
              className="mt-4 md:mt-0 inline-flex items-center text-burnt-orange hover:text-burnt-orange/80 transition-colors"
            >
              <span>{viewAllText}</span>
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className="h-5 w-5 ml-1" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          )}
        </div>
        
        {children}
      </div>
    </section>
  );
} 