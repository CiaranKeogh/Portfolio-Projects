import { maps, Map } from '@/data/maps';
import { powerPositions, PowerPosition } from '@/data/positions';
import { strategicRoutes, StrategicRoute } from '@/data/routes';

export type GameMode = 'Domination' | 'Conquest' | 'Battle';

export interface MapData {
  id: string;
  name: string;
  slug: string;
  modes: GameMode[];
  thumbnail: string;
  fullImage: string;
  description: string;
  terrainType: string;
  size: string;
  popularity: number;
  severity?: number;
}

// This will be replaced with backend data in the future
export const popularMaps: MapData[] = [
  {
    id: '1',
    name: 'Advance to the Rhine',
    slug: 'advance-to-the-rhine',
    modes: ['Domination', 'Conquest', 'Battle'],
    thumbnail: '/assets/maps/thumbnails/advance-to-the-rhine.jpg',
    fullImage: '/assets/maps/full-size/Advance to the Rhine/MapLayout_DOMINATION(ADVANCE_TO_THE_RHINE)_Advance to the Rhine.jpg',
    description: 'Urban combat through war-torn European city streets.',
    terrainType: 'Urban',
    size: 'Large',
    popularity: 98
  },
  {
    id: '2',
    name: 'Berlin',
    slug: 'berlin',
    modes: ['Domination', 'Conquest', 'Battle'],
    thumbnail: '/assets/maps/thumbnails/berlin.jpg',
    fullImage: '/assets/maps/full-size/Berlin/MapLayout_DOMINATION(BERLIN)_Berlin.jpg',
    description: 'Fight through the ruins of Berlin in this iconic WWII battle setting.',
    terrainType: 'Urban',
    size: 'Large',
    popularity: 95
  },
  {
    id: '3',
    name: 'Fulda Gap',
    slug: 'fulda-gap',
    modes: ['Domination', 'Conquest'],
    thumbnail: '/assets/maps/thumbnails/fulda-gap.jpg',
    fullImage: '/assets/maps/full-size/Fulda Gap/MapLayout_DOMINATION(FULDA_GAP)_Fulda Gap.jpg',
    description: 'Cold War scenario with rolling hills and long sight lines.',
    terrainType: 'Rural',
    size: 'Medium',
    popularity: 92
  },
  {
    id: '4',
    name: 'Ash River',
    slug: 'ash-river',
    modes: ['Battle', 'Conquest'],
    thumbnail: '/assets/maps/thumbnails/ash-river.jpg',
    fullImage: '/assets/maps/full-size/Ash River/MapLayout_DOMINATION(ASH_RIVER)_Ash River.jpg',
    description: 'Mountainous terrain with winding roads and strategic chokepoints.',
    terrainType: 'Mountainous',
    size: 'Large',
    popularity: 89
  },
  {
    id: '5',
    name: 'Eastern Europe',
    slug: 'eastern-europe',
    modes: ['Domination', 'Battle'],
    thumbnail: '/assets/maps/thumbnails/eastern-europe.jpg',
    fullImage: '/assets/maps/full-size/Eastern Europe/MapLayout_DOMINATION(EASTERN_EUROPE)_Eastern Europe.jpg',
    description: 'Mixed urban and rural environment with tactical village fighting.',
    terrainType: 'Mixed',
    size: 'Large',
    popularity: 85
  },
  {
    id: '6',
    name: 'Carpathians',
    slug: 'carpathians',
    modes: ['Domination', 'Battle'],
    thumbnail: '/assets/maps/thumbnails/carpathians.jpg',
    fullImage: '/assets/maps/full-size/Carpathians/MapLayout_DOMINATION(CARPATHIANS)_Carpathians.jpg',
    description: 'Mountain passes and snow-covered valleys provide challenging terrain.',
    terrainType: 'Mountainous',
    size: 'Large',
    popularity: 80
  }
];

// Get the top N most popular maps
export function getTopMaps(count: number): MapData[] {
  // Convert Map to MapData format
  const convertedMaps: MapData[] = maps.map(map => ({
    id: map.id,
    name: map.name,
    slug: map.id.replace('map-', ''),
    modes: map.gameModes as GameMode[],
    thumbnail: map.thumbnail,
    fullImage: map.fullImage,
    description: map.description,
    terrainType: map.terrainType,
    size: map.size,
    popularity: map.popularity
  }));
  
  return [...convertedMaps]
    .sort((a, b) => b.popularity - a.popularity)
    .slice(0, count);
}

// Get power positions for a specific map by map name
export function getPowerPositionsByMapName(mapName: string): PowerPosition[] {
  return powerPositions.filter(position => position.map === mapName);
}

// Get strategic routes for a specific map by map name
export function getStrategicRoutesByMapName(mapName: string): StrategicRoute[] {
  return strategicRoutes.filter(route => route.map === mapName);
} 