import React from 'react';
import { PowerPositionCard } from './PowerPositionCard';
import { powerPositions } from '@/data/positions';

export function PowerPositionsSection() {
  // Only show the first 3 positions on the homepage
  const featuredPositions = powerPositions.slice(0, 3);
  
  return (
    <section className="py-16 bg-gunmetal/20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-off-white mb-4">
            Top Power Positions
          </h2>
          <p className="text-off-white/80 max-w-2xl mx-auto">
            Discover the best strategic positions on each map that give you an advantage over your enemies. 
            These positions offer superior firing angles, cover, and tactical advantages.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuredPositions.map((position) => (
            <PowerPositionCard key={position.id} position={position} />
          ))}
        </div>
        
        <div className="mt-12 text-center">
          <a 
            href="/positions" 
            className="bg-burnt-orange hover:bg-burnt-orange/90 text-off-white font-bold py-3 px-8 rounded-lg inline-flex items-center transition-colors"
          >
            View All Power Positions
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-5 w-5 ml-2" 
              viewBox="0 0 20 20" 
              fill="currentColor"
            >
              <path fillRule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </a>
        </div>
      </div>
    </section>
  );
} 