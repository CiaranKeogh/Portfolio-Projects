import React from 'react';
import Link from 'next/link';
import { PowerPosition } from '@/data/positions';

interface PowerPositionCardProps {
  position: PowerPosition;
}

export function PowerPositionCard({ position }: PowerPositionCardProps) {
  return (
    <div className="bg-gunmetal/90 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1">
      <div className="relative h-48">
        {/* Using a colored background instead of actual image */}
        <div className="absolute inset-0 bg-olive-drab/60 flex items-center justify-center">
          <span className="text-off-white text-lg font-medium">{position.map}</span>
        </div>
        
        {/* Map and cover level overlay */}
        <div className="absolute top-0 left-0 right-0 p-3 flex justify-between items-center">
          <span className="bg-deep-blue/80 text-off-white text-sm px-3 py-1 rounded-full">
            {position.map}
          </span>
          <div className="flex items-center">
            <span className="text-off-white text-xs mr-1">Cover:</span>
            <div className="flex">
              {Array.from({ length: 5 }).map((_, i) => (
                <svg 
                  key={i}
                  xmlns="http://www.w3.org/2000/svg" 
                  className={`h-4 w-4 ${i < position.coverLevel ? 'text-burnt-orange' : 'text-off-white/30'}`}
                  viewBox="0 0 20 20" 
                  fill="currentColor"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              ))}
            </div>
          </div>
        </div>
      </div>
      
      <div className="p-4">
        <h3 className="text-xl font-bold text-off-white mb-2">{position.name}</h3>
        
        <div className="mb-3">
          <h4 className="text-sm text-off-white/70 mb-1">Suitable Vehicles:</h4>
          <div className="flex flex-wrap gap-1">
            {position.suitableVehicles.map((vehicle, idx) => (
              <span 
                key={idx}
                className="bg-olive-drab/60 text-off-white text-xs px-2 py-1 rounded"
              >
                {vehicle}
              </span>
            ))}
          </div>
        </div>
        
        <p className="text-off-white/80 text-sm mb-4">{position.description}</p>
        
        <Link href={`/positions/${position.id}`}>
          <button className="w-full bg-deep-blue hover:bg-deep-blue/90 text-off-white font-medium py-2 px-4 rounded transition-colors">
            View Position
          </button>
        </Link>
      </div>
    </div>
  );
} 