import Image from 'next/image';
import Link from 'next/link';
import { TacticData } from '@/lib/tactics-utils';

interface TacticCardProps {
  tactic: TacticData;
  featured?: boolean;
}

export function TacticCard({ tactic, featured = false }: TacticCardProps) {
  const upvoteRatio = Math.round((tactic.upvotes / (tactic.upvotes + tactic.downvotes)) * 100);
  
  return (
    <Link href={`/tactics/${tactic.slug}`} className="group">
      <div className={`bg-gunmetal rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300 ${featured ? 'border-2 border-burnt-orange' : ''}`}>
        <div className="relative h-48 md:h-56 w-full">
          {/* Fallback image if thumbnail is not available */}
          <div className="absolute inset-0 bg-deep-blue flex items-center justify-center">
            <span className="text-off-white text-lg font-semibold">{tactic.title}</span>
          </div>
          
          {/* Tactic preview image */}
          {tactic.previewImage && (
            <Image 
              src={tactic.previewImage}
              alt={tactic.title}
              fill
              className="object-cover group-hover:scale-105 transition-transform duration-300"
            />
          )}
          
          {/* Map name badge */}
          <div className="absolute top-3 left-3 bg-gunmetal/80 rounded-full px-3 py-1">
            <span className="text-off-white text-xs">{tactic.mapName}</span>
          </div>
          
          {/* Upvote ratio badge */}
          <div className="absolute top-3 right-3 bg-olive-drab rounded-full px-2 py-1 flex items-center space-x-1">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-4 w-4 text-off-white" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
            </svg>
            <span className="text-off-white text-xs font-medium">{upvoteRatio}%</span>
          </div>
          
          {/* Title overlay */}
          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-gunmetal/90 to-transparent p-4">
            <h3 className="text-off-white text-xl font-bold line-clamp-1">{tactic.title}</h3>
          </div>
        </div>
        
        <div className="p-4">
          <div className="flex flex-wrap gap-2 mb-3">
            {tactic.vehicleTypes.map((type) => (
              <span 
                key={type} 
                className="text-xs bg-deep-blue/30 text-off-white rounded-full px-2 py-1"
              >
                {type}
              </span>
            ))}
          </div>
          
          <p className="text-off-white/80 text-sm line-clamp-2">{tactic.description}</p>
          
          <div className="mt-4 flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-full bg-olive-drab flex items-center justify-center">
                <span className="text-off-white text-xs">{tactic.author.charAt(0)}</span>
              </div>
              <span className="text-off-white/80 text-xs">{tactic.author}</span>
            </div>
            
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-1">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-4 w-4 text-burnt-orange" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                </svg>
                <span className="text-burnt-orange text-xs font-medium">{tactic.upvotes}</span>
              </div>
              
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
      </div>
    </Link>
  );
} 