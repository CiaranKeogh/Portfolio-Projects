'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { maps } from '@/data/maps';
import { notFound } from 'next/navigation';
import { getPowerPositionsByMapName, getStrategicRoutesByMapName } from '@/lib/map-utils';
import { PowerPosition } from '@/data/positions';
import { StrategicRoute } from '@/data/routes';

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

  // Get positions and routes for this map
  const positions = getPowerPositionsByMapName(map.name);
  const routes = getStrategicRoutesByMapName(map.name);
  
  // Handle case where there are no positions or routes
  const hasPositions = positions.length > 0;
  const hasRoutes = routes.length > 0;
  
  // Define available layouts
  const layouts = map.layouts || [map.fullImage];
  const totalLayouts = layouts.length;
  
  // State for map layout selection
  const [currentLayout, setCurrentLayout] = useState<number>(0);
  
  // Navigate to previous layout
  const prevLayout = () => {
    setCurrentLayout((prev) => (prev === 0 ? totalLayouts - 1 : prev - 1));
  };
  
  // Navigate to next layout
  const nextLayout = () => {
    setCurrentLayout((prev) => (prev === totalLayouts - 1 ? 0 : prev + 1));
  };
  
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
      
      {/* Map Information Header */}
      <div className="bg-gunmetal/90 rounded-lg p-6 mb-6 shadow-lg">
        <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-3xl font-bold text-off-white">{map.name}</h1>
              {map.gameModes.map((mode) => (
                <span 
                  key={mode} 
                  className="text-xs bg-olive-drab/20 text-olive-drab rounded-full px-2 py-0.5"
                >
                  {mode}
                </span>
              ))}
            </div>
            <p className="text-off-white/80 mt-2">{map.description}</p>
          </div>
          
          <div className="flex items-center gap-4 text-off-white/80 shrink-0">
            <div className="text-right">
              <div className="text-sm">Size</div>
              <div className="font-medium">{map.size}</div>
            </div>
            <div className="h-10 border-r border-slate-600"></div>
            <div className="text-right">
              <div className="text-sm">Terrain</div>
              <div className="font-medium">{map.terrainType}</div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Three-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column - Power Positions */}
        <div className="lg:col-span-3 order-3 lg:order-1">
          <div className="bg-deep-blue/40 rounded-lg p-4 shadow-md h-full flex flex-col">
            <div className="flex items-center mb-6">
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
              <h2 className="text-xl font-semibold text-off-white">Power Positions</h2>
            </div>
            
            {hasPositions ? (
              <div className="space-y-4 flex-grow">
                {positions.map((position) => (
                  <PowerPositionCard key={position.id} position={position} />
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-off-white/60 flex-grow">
                <p>No power positions have been added for this map yet.</p>
                <p className="mt-2 text-sm">Check back later!</p>
              </div>
            )}
            
            {/* Add Position Button */}
            <button className="w-full mt-4 bg-burnt-orange hover:bg-burnt-orange/90 text-off-white font-medium py-2 px-4 rounded transition-colors flex items-center justify-center">
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className="h-5 w-5 mr-2" 
                viewBox="0 0 20 20" 
                fill="currentColor"
              >
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Add Position
            </button>
          </div>
        </div>
        
        {/* Middle Column - Map Display */}
        <div className="lg:col-span-6 order-1 lg:order-2">
          <div className="bg-gunmetal rounded-lg overflow-hidden shadow-lg">
            <div className="relative">
              {/* Map Navigation - Left */}
              <button
                className="absolute left-2 top-1/2 -translate-y-1/2 z-10 bg-deep-blue/80 hover:bg-deep-blue text-off-white w-10 h-10 rounded-full flex items-center justify-center transition-colors"
                aria-label="Previous layout"
                onClick={prevLayout}
                disabled={totalLayouts <= 1}
                style={{ opacity: totalLayouts <= 1 ? 0.5 : 1 }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </button>
              
              {/* Map Display */}
              <div className="relative h-[600px] w-full">
                <Image
                  src={layouts[currentLayout]}
                  alt={`${map.name} - Layout ${currentLayout + 1}`}
                  fill
                  className="object-cover"
                  priority
                />
              </div>
              
              {/* Map Navigation - Right */}
              <button
                className="absolute right-2 top-1/2 -translate-y-1/2 z-10 bg-deep-blue/80 hover:bg-deep-blue text-off-white w-10 h-10 rounded-full flex items-center justify-center transition-colors"
                aria-label="Next layout"
                onClick={nextLayout}
                disabled={totalLayouts <= 1}
                style={{ opacity: totalLayouts <= 1 ? 0.5 : 1 }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </button>
              
              {/* Layout indicator */}
              <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-10 bg-deep-blue/70 px-3 py-1 rounded-full text-off-white text-sm">
                {totalLayouts > 1 ? (
                  <span>
                    Layout {currentLayout + 1} of {totalLayouts}
                    {map.id === "map-1" && (
                      <span className="ml-2 text-xs text-off-white/80">
                        {currentLayout === 0 && "- Domination"}
                        {currentLayout === 1 && "- Battle"}
                        {currentLayout === 2 && "- Conquest"}
                        {currentLayout === 3 && "- Break"}
                        {currentLayout === 4 && "- Tank Realistic"}
                        {currentLayout === 5 && "- Air Realistic"}
                      </span>
                    )}
                  </span>
                ) : (
                  <span>Map Layout</span>
                )}
              </div>
            </div>
          </div>
        </div>
        
        {/* Right Column - Strategic Routes */}
        <div className="lg:col-span-3 order-2 lg:order-3">
          <div className="bg-deep-blue/40 rounded-lg p-4 shadow-md h-full flex flex-col">
            <div className="flex items-center mb-6">
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className="h-6 w-6 text-burnt-orange mr-2" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
              <h2 className="text-xl font-semibold text-off-white">Strategic Routes</h2>
            </div>
            
            {hasRoutes ? (
              <div className="space-y-4 flex-grow">
                {routes.map((route) => (
                  <RouteCard key={route.id} route={route} />
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-off-white/60 flex-grow">
                <p>No strategic routes have been added for this map yet.</p>
                <p className="mt-2 text-sm">Check back later!</p>
              </div>
            )}
            
            {/* Add Route Button */}
            <button className="w-full mt-4 bg-burnt-orange hover:bg-burnt-orange/90 text-off-white font-medium py-2 px-4 rounded transition-colors flex items-center justify-center">
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className="h-5 w-5 mr-2" 
                viewBox="0 0 20 20" 
                fill="currentColor"
              >
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Add Route
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Power Position Card Component
function PowerPositionCard({ position }: { position: PowerPosition }) {
  return (
    <div className="bg-gunmetal/60 rounded-lg overflow-hidden hover:bg-gunmetal/80 transition-colors">
      <div className="relative h-28">
        <Image 
          src={position.screenshots[0] || position.mapImage} 
          alt={position.name}
          fill
          className="object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-gunmetal/90 to-transparent"></div>
        <div className="absolute bottom-2 left-2 right-2">
          <h3 className="text-off-white font-medium text-sm line-clamp-1">{position.name}</h3>
        </div>
      </div>
      <div className="p-3">
        <p className="text-off-white/70 text-xs line-clamp-2 mb-2">{position.description}</p>
        <div className="flex justify-between items-center text-xs">
          <div className="flex items-center text-off-white/60">
            <svg 
              className="h-3 w-3 mr-1" 
              fill="currentColor" 
              viewBox="0 0 20 20"
            >
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
            </svg>
            Cover: {position.coverLevel}/5
          </div>
          <div className="flex gap-1">
            {position.suitableVehicles.slice(0, 2).map((vehicle, i) => (
              <span key={i} className="bg-deep-blue/40 px-2 py-1 rounded text-xs text-off-white/80">
                {vehicle.split(' ')[0]}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// Strategic Route Card Component
function RouteCard({ route }: { route: StrategicRoute }) {
  return (
    <div className="bg-gunmetal/60 rounded-lg overflow-hidden hover:bg-gunmetal/80 transition-colors">
      <div className="relative h-28">
        <Image 
          src={route.mapImage} 
          alt={route.name}
          fill
          className="object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-gunmetal/90 to-transparent"></div>
        <div className="absolute bottom-2 left-2 right-2">
          <h3 className="text-off-white font-medium text-sm line-clamp-1">{route.name}</h3>
        </div>
      </div>
      <div className="p-3">
        <p className="text-off-white/70 text-xs line-clamp-2 mb-2">{route.description}</p>
        <div className="flex justify-between items-center text-xs">
          <div className="flex items-center text-off-white/60">
            <svg 
              className="h-3 w-3 mr-1" 
              fill="currentColor" 
              viewBox="0 0 20 20"
            >
              <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            {route.successRate}% Success
          </div>
          <div className="flex gap-1">
            <span className="bg-deep-blue/40 px-2 py-1 rounded text-xs text-off-white/80">
              {route.difficulty}
            </span>
            <span className="bg-burnt-orange/40 px-2 py-1 rounded text-xs text-off-white/80">
              {route.vehicleType}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
} 