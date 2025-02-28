import Image from 'next/image';
import Link from 'next/link';
import { MapData } from '@/lib/map-utils';

interface MapCardProps {
  map: MapData;
}

export function MapCard({ map }: MapCardProps) {
  return (
    <Link href={`/maps/${map.slug}`} className="group">
      <div className="bg-gunmetal rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300">
        <div className="relative h-48 w-full">
          {/* Fallback image if thumbnail is not available */}
          <div className="absolute inset-0 bg-deep-blue flex items-center justify-center">
            <span className="text-off-white text-lg font-semibold">{map.name}</span>
          </div>
          
          {/* Map thumbnail */}
          {map.thumbnail && (
            <Image 
              src={map.fullImage} // Using fullImage for now since we don't have thumbnails yet
              alt={map.name}
              fill
              className="object-cover group-hover:scale-105 transition-transform duration-300"
            />
          )}
          
          {/* Map name overlay */}
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-gunmetal/90 to-transparent p-4">
            <h3 className="text-off-white text-xl font-bold">{map.name}</h3>
          </div>
        </div>
        
        <div className="p-4">
          <div className="flex flex-wrap gap-2 mb-3">
            {map.modes.map((mode) => (
              <span 
                key={mode} 
                className="text-xs bg-olive-drab/20 text-olive-drab rounded-full px-2 py-1"
              >
                {mode}
              </span>
            ))}
          </div>
          
          <p className="text-off-white/80 text-sm line-clamp-2">{map.description}</p>
          
          <div className="mt-4 flex justify-between items-center">
            <span className="text-burnt-orange font-medium text-sm">View Tactics</span>
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-5 w-5 text-burnt-orange transform group-hover:translate-x-1 transition-transform" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </div>
      </div>
    </Link>
  );
} 