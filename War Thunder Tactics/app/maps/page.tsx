'use client';

import { useState } from 'react';
import { maps } from '@/data/maps';
import { MapData } from '@/lib/map-utils';
import { MapCard } from '@/components/maps/map-card';

export default function MapsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterMode, setFilterMode] = useState<string>('');
  
  // Extract unique game modes for filter
  const gameModes = Array.from(new Set(maps.flatMap(map => map.gameModes)));
  
  // Filter maps based on search and filter criteria
  const filteredMaps = maps.filter(map => {
    const matchesSearch = searchTerm === '' || 
      map.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      map.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesMode = filterMode === '' || map.gameModes.includes(filterMode);
    
    return matchesSearch && matchesMode;
  });

  // Convert Map to MapData format for MapCard
  const convertToMapData = (map: typeof maps[0]): MapData => {
    return {
      id: map.id,
      name: map.name,
      slug: map.id.replace('map-', ''),
      modes: map.gameModes as any,
      thumbnail: map.thumbnail,
      fullImage: map.fullImage,
      description: map.description,
      popularity: map.popularity
    };
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-off-white">War Thunder Maps</h1>
      
      <div className="mb-8 bg-gunmetal rounded-lg p-6 shadow-md">
        <div className="flex flex-col md:flex-row gap-4 mb-4">
          <div className="flex-1">
            <label htmlFor="search" className="block text-off-white mb-2">Search Maps</label>
            <input
              type="text"
              id="search"
              placeholder="Search by name or description..."
              className="w-full p-2 rounded bg-slate-700 text-off-white border border-slate-600 focus:ring-2 focus:ring-burnt-orange focus:border-transparent"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div>
            <label htmlFor="mode" className="block text-off-white mb-2">Game Mode</label>
            <select
              id="mode"
              className="w-full p-2 rounded bg-slate-700 text-off-white border border-slate-600 focus:ring-2 focus:ring-burnt-orange focus:border-transparent"
              value={filterMode}
              onChange={(e) => setFilterMode(e.target.value)}
            >
              <option value="">All Modes</option>
              {gameModes.map(mode => (
                <option key={mode} value={mode}>{mode}</option>
              ))}
            </select>
          </div>
        </div>
        
        <div className="flex justify-between items-center">
          <p className="text-off-white">
            Showing {filteredMaps.length} of {maps.length} maps
          </p>
          <button 
            className="px-4 py-2 rounded bg-burnt-orange text-off-white hover:bg-opacity-90 transition"
            onClick={() => {
              setSearchTerm('');
              setFilterMode('');
            }}
          >
            Reset Filters
          </button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredMaps.length > 0 ? (
          filteredMaps.map(map => (
            <MapCard key={map.id} map={convertToMapData(map)} />
          ))
        ) : (
          <div className="col-span-full text-center py-12">
            <h3 className="text-xl text-off-white mb-2">No maps found</h3>
            <p className="text-off-white/70">Try adjusting your search or filters</p>
          </div>
        )}
      </div>
    </div>
  );
} 