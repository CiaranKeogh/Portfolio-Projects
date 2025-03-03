'use client';

import { useParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { maps } from '@/data/maps';
import { notFound } from 'next/navigation';

export default function MapDetailPage() {
  const params = useParams();
  const slug = params?.slug as string;
  
  // Find the map by slug (using the id prefix from the URL)
  const mapId = `map-${slug}`;
  const map = maps.find(m => m.id === mapId);
  
  // If map is not found, return 404
  if (!map) {
    notFound();
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link 
          href="/maps" 
          className="flex items-center text-olive-drab hover:text-burnt-orange transition"
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            className="h-5 w-5 mr-2" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Maps
        </Link>
      </div>
      
      <div className="bg-gunmetal rounded-lg overflow-hidden shadow-lg">
        <div className="relative h-64 md:h-96 w-full">
          <Image
            src={map.fullImage}
            alt={map.name}
            fill
            className="object-cover"
          />
        </div>
        
        <div className="p-6">
          <div className="flex flex-col md:flex-row md:justify-between md:items-start gap-4 mb-6">
            <div>
              <h1 className="text-3xl font-bold text-off-white">{map.name}</h1>
              <div className="flex flex-wrap gap-2 mt-3">
                {map.gameModes.map((mode) => (
                  <span 
                    key={mode} 
                    className="text-sm bg-olive-drab/20 text-olive-drab rounded-full px-3 py-1"
                  >
                    {mode}
                  </span>
                ))}
              </div>
            </div>
            
            <div className="flex items-center gap-3 text-off-white/80">
              <div className="text-right">
                <div className="text-sm">Size</div>
                <div className="font-medium">{map.size}</div>
              </div>
              <div className="h-10 border-r border-slate-600"></div>
              <div className="text-right">
                <div className="text-sm">Terrain</div>
                <div className="font-medium">{map.terrainType}</div>
              </div>
              <div className="h-10 border-r border-slate-600"></div>
              <div className="text-right">
                <div className="text-sm">Added</div>
                <div className="font-medium">{new Date(map.dateAdded).toLocaleDateString()}</div>
              </div>
            </div>
          </div>
          
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-off-white mb-3">Description</h2>
            <p className="text-off-white/80">{map.description}</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-deep-blue rounded-lg p-5">
              <div className="flex items-center mb-4">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-6 w-6 text-burnt-orange mr-2" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <h3 className="text-lg font-semibold text-off-white">Power Positions</h3>
              </div>
              <p className="text-off-white/80 mb-3">
                This map has {map.powerPositionsCount} known power positions.
              </p>
              <Link 
                href={`/maps/${slug}/positions`}
                className="block w-full text-center py-2 bg-burnt-orange text-off-white rounded hover:bg-opacity-90 transition"
              >
                View Power Positions
              </Link>
            </div>
            
            <div className="bg-deep-blue rounded-lg p-5">
              <div className="flex items-center mb-4">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  className="h-6 w-6 text-burnt-orange mr-2" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
                <h3 className="text-lg font-semibold text-off-white">Strategic Routes</h3>
              </div>
              <p className="text-off-white/80 mb-3">
                This map has {map.strategicRoutesCount} known strategic routes.
              </p>
              <Link 
                href={`/maps/${slug}/routes`}
                className="block w-full text-center py-2 bg-burnt-orange text-off-white rounded hover:bg-opacity-90 transition"
              >
                View Strategic Routes
              </Link>
            </div>
          </div>
          
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-off-white mb-3">Statistics</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-slate-700 rounded-lg p-4">
                <div className="text-sm text-off-white/60">Views</div>
                <div className="text-2xl font-bold text-off-white">{map.viewCount.toLocaleString()}</div>
              </div>
              <div className="bg-slate-700 rounded-lg p-4">
                <div className="text-sm text-off-white/60">Popularity</div>
                <div className="text-2xl font-bold text-off-white">{map.popularity}/10</div>
              </div>
              <div className="bg-slate-700 rounded-lg p-4">
                <div className="text-sm text-off-white/60">Added</div>
                <div className="text-2xl font-bold text-off-white">{new Date(map.dateAdded).toLocaleDateString()}</div>
              </div>
              <div className="bg-slate-700 rounded-lg p-4">
                <div className="text-sm text-off-white/60">Game Modes</div>
                <div className="text-2xl font-bold text-off-white">{map.gameModes.length}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 