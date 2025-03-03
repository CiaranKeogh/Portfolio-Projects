"use client";

import React, { useState } from 'react';
import Image from 'next/image';
import { maps, Map } from '@/data/maps';

export function MapCarousel() {
  const [activeIndex, setActiveIndex] = useState(0);
  
  const nextSlide = () => {
    setActiveIndex((current) => (current === maps.length - 1 ? 0 : current + 1));
  };
  
  const prevSlide = () => {
    setActiveIndex((current) => (current === 0 ? maps.length - 1 : current - 1));
  };
  
  const goToSlide = (index: number) => {
    setActiveIndex(index);
  };
  
  return (
    <section className="py-16 bg-deep-blue/10">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-off-white mb-4">
            Popular Maps
          </h2>
          <p className="text-off-white/80 max-w-2xl mx-auto">
            Explore our detailed map database with community-created power positions,
            strategic routes, and tactical tips for War Thunder's most played battlegrounds.
          </p>
        </div>
        
        <div className="relative overflow-hidden rounded-xl border border-deep-blue/30">
          <div 
            className="flex transition-transform duration-700 ease-in-out"
            style={{ transform: `translateX(-${activeIndex * 100}%)` }}
          >
            {maps.map((map: Map, index: number) => (
              <div key={map.id} className="min-w-full">
                <div className="grid grid-cols-1 md:grid-cols-2 bg-gunmetal/80">
                  {/* Map thumbnail */}
                  <div className="relative h-64 md:h-96">
                    <div className="absolute inset-0 z-10">
                      <Image 
                        src={map.thumbnail} 
                        alt={`${map.name} map thumbnail`}
                        width={800}
                        height={500}
                        className="w-full h-full object-cover"
                        priority={index === 0}
                      />
                    </div>
                    <div className="absolute bottom-4 left-4 z-20">
                      <span className="text-off-white text-lg font-medium px-4 py-2 bg-deep-blue/60 rounded-lg">
                        {map.name}
                      </span>
                    </div>
                  </div>
                  
                  {/* Map details */}
                  <div className="p-6 md:p-8 flex flex-col">
                    <div className="mb-4">
                      <h3 className="text-2xl font-bold text-off-white mb-2">{map.name}</h3>
                      
                      <div className="flex flex-wrap gap-2 mb-4">
                        {map.gameModes.map((mode, modeIndex) => (
                          <span 
                            key={modeIndex} 
                            className="bg-deep-blue/60 text-off-white text-xs px-3 py-1 rounded-full"
                          >
                            {mode}
                          </span>
                        ))}
                      </div>
                      
                      <p className="text-off-white/80 mb-6">{map.description}</p>
                      
                      <div className="grid grid-cols-3 gap-2 mb-6">
                        <div className="border border-deep-blue/30 rounded p-3 text-center">
                          <div className="text-burnt-orange font-semibold text-lg">
                            {map.size}
                          </div>
                          <div className="text-off-white/60 text-xs">Size</div>
                        </div>
                        <div className="border border-deep-blue/30 rounded p-3 text-center">
                          <div className="text-burnt-orange font-semibold text-lg">
                            {map.terrainType}
                          </div>
                          <div className="text-off-white/60 text-xs">Terrain</div>
                        </div>
                        <div className="border border-deep-blue/30 rounded p-3 text-center">
                          <div className="text-burnt-orange font-semibold text-lg flex items-center justify-center">
                            <span>{map.popularity}</span>
                            <span className="text-xs text-off-white/80 ml-1">/10</span>
                          </div>
                          <div className="text-off-white/60 text-xs">Popularity</div>
                        </div>
                      </div>
                      
                      <div className="flex justify-between items-center text-off-white/60 text-sm mb-6">
                        <div>
                          <svg 
                            xmlns="http://www.w3.org/2000/svg" 
                            className="h-4 w-4 inline mr-1" 
                            viewBox="0 0 20 20" 
                            fill="currentColor"
                          >
                            <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                            <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                          </svg>
                          {map.viewCount.toLocaleString()} views
                        </div>
                        <div>
                          <div className="flex">
                            <div className="flex items-center mr-3">
                              <svg 
                                xmlns="http://www.w3.org/2000/svg" 
                                className="h-4 w-4 inline mr-1 text-olive-drab" 
                                viewBox="0 0 20 20" 
                                fill="currentColor"
                              >
                                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                              </svg>
                              {map.powerPositionsCount}
                            </div>
                            <div className="flex items-center">
                              <svg 
                                xmlns="http://www.w3.org/2000/svg" 
                                className="h-4 w-4 inline mr-1 text-burnt-orange" 
                                viewBox="0 0 20 20" 
                                fill="currentColor"
                              >
                                <path fillRule="evenodd" d="M9.293 2.293a1 1 0 011.414 0l7 7A1 1 0 0117 11h-1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-3a1 1 0 00-1-1H9a1 1 0 00-1 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-6H3a1 1 0 01-.707-1.707l7-7z" clipRule="evenodd" />
                              </svg>
                              {map.strategicRoutesCount}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-auto">
                      <a 
                        href={`/maps/${map.id}`} 
                        className="inline-block w-full bg-burnt-orange hover:bg-burnt-orange/90 text-off-white font-medium py-3 px-4 rounded text-center transition-colors"
                      >
                        Explore Map
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          {/* Navigation arrows */}
          <button 
            onClick={prevSlide}
            className="absolute left-4 top-1/2 -translate-y-1/2 bg-deep-blue/80 hover:bg-deep-blue text-off-white w-10 h-10 rounded-full flex items-center justify-center transition-colors z-10"
            aria-label="Previous slide"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          </button>
          
          <button 
            onClick={nextSlide}
            className="absolute right-4 top-1/2 -translate-y-1/2 bg-deep-blue/80 hover:bg-deep-blue text-off-white w-10 h-10 rounded-full flex items-center justify-center transition-colors z-10"
            aria-label="Next slide"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
            </svg>
          </button>
          
          {/* Indicators */}
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex space-x-2">
            {maps.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                className={`w-3 h-3 rounded-full transition-all ${
                  index === activeIndex 
                    ? 'bg-burnt-orange w-6' 
                    : 'bg-off-white/40 hover:bg-off-white/60'
                }`}
                aria-label={`Go to slide ${index + 1}`}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
} 