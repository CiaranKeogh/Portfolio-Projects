"use client";

import React, { useState } from 'react';
import Image from 'next/image';
import { strategicRoutes, StrategicRoute } from '@/data/routes';

export function StrategicRoutesSection() {
  const [activeRoute, setActiveRoute] = useState<StrategicRoute>(strategicRoutes[0]);
  
  return (
    <section className="py-16 bg-deep-blue/20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-off-white mb-4">
            Strategic Routes
          </h2>
          <p className="text-off-white/80 max-w-2xl mx-auto">
            Follow proven paths to victory with our curated collection of strategic routes.
            Each route is designed to maximize your team's chances of success.
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          {/* Route selection sidebar */}
          <div className="lg:col-span-2">
            <h3 className="text-xl font-semibold text-off-white mb-4">Popular Routes</h3>
            <div className="space-y-3">
              {strategicRoutes.slice(0, 5).map((route: StrategicRoute) => (
                <div 
                  key={route.id}
                  onClick={() => setActiveRoute(route)}
                  className={`p-4 rounded-lg cursor-pointer transition-colors ${
                    activeRoute.id === route.id 
                      ? 'bg-olive-drab text-off-white' 
                      : 'bg-gunmetal/60 text-off-white/80 hover:bg-gunmetal/80'
                  }`}
                >
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="font-medium">{route.name}</h4>
                    <span className="text-xs px-2 py-1 rounded-full bg-deep-blue/60">
                      {route.map}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center text-xs">
                    <span>
                      <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        className="h-4 w-4 inline mr-1" 
                        viewBox="0 0 20 20" 
                        fill="currentColor"
                      >
                        <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6z" />
                      </svg>
                      {route.vehicleType}
                    </span>
                    <span>
                      <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        className="h-4 w-4 inline mr-1" 
                        viewBox="0 0 20 20" 
                        fill="currentColor"
                      >
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                      </svg>
                      {route.timeToExecute} min
                    </span>
                    <span>
                      <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        className="h-4 w-4 inline mr-1" 
                        viewBox="0 0 20 20" 
                        fill="currentColor"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                      {route.successRate}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-6">
              <a 
                href="/routes" 
                className="inline-block w-full bg-deep-blue hover:bg-deep-blue/90 text-off-white font-medium py-3 px-4 rounded text-center transition-colors"
              >
                Browse All Routes
              </a>
            </div>
          </div>
          
          {/* Route details */}
          <div className="lg:col-span-3 bg-gunmetal/80 rounded-xl overflow-hidden">
            <div className="relative h-64 md:h-80">
              {/* Using actual map image */}
              <div className="absolute inset-0">
                <Image 
                  src={activeRoute.mapImage} 
                  alt={`${activeRoute.map} map for ${activeRoute.name} route`}
                  width={800}
                  height={500}
                  className="w-full h-full object-cover"
                />
              </div>
              
              {/* Bottom gradient for text readability */}
              <div className="absolute inset-x-0 bottom-0 h-32 bg-gradient-to-t from-gunmetal/90 to-transparent z-10"></div>
              
              <div className="absolute bottom-0 left-0 right-0 p-6 z-20">
                <h3 className="text-2xl font-bold text-off-white mb-1">{activeRoute.name}</h3>
                <p className="text-off-white/90 text-sm">{activeRoute.map}</p>
              </div>
            </div>
            
            <div className="p-6">
              <div className="flex flex-wrap gap-2 mb-4">
                <span className="bg-olive-drab/60 text-off-white text-xs px-3 py-1 rounded-full">
                  {activeRoute.gameMode}
                </span>
                <span className="bg-deep-blue/60 text-off-white text-xs px-3 py-1 rounded-full">
                  {activeRoute.vehicleType}
                </span>
                <span className="bg-burnt-orange/60 text-off-white text-xs px-3 py-1 rounded-full">
                  {activeRoute.successRate}% Success Rate
                </span>
              </div>
              
              <p className="text-off-white/80 mb-6">{activeRoute.description}</p>
              
              <div className="space-y-3">
                <h4 className="text-md font-semibold text-off-white">Key Waypoints:</h4>
                <ol className="list-decimal list-inside text-off-white/80 space-y-2">
                  {activeRoute.waypoints.map((waypoint: string, idx: number) => (
                    <li key={idx} className="pl-2">{waypoint}</li>
                  ))}
                </ol>
              </div>
              
              <div className="mt-6">
                <a 
                  href={`/routes/${activeRoute.id}`}
                  className="inline-flex items-center bg-burnt-orange hover:bg-burnt-orange/90 text-off-white font-medium py-2 px-4 rounded transition-colors"
                >
                  View Detailed Route
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
          </div>
        </div>
      </div>
    </section>
  );
} 