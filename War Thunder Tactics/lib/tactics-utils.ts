export type VehicleType = 
  | 'Light Tank' 
  | 'Medium Tank' 
  | 'Heavy Tank' 
  | 'Tank Destroyer' 
  | 'SPAA' 
  | 'SPFA';

export interface TacticData {
  id: string;
  title: string;
  slug: string;
  mapId: string;
  mapName: string;
  description: string;
  vehicleTypes: VehicleType[];
  author: string;
  authorId: string;
  createdAt: string;
  upvotes: number;
  downvotes: number;
  thumbnail: string;
  previewImage: string;
}

// This will be replaced with backend data in the future
export const featuredTactics: TacticData[] = [
  {
    id: '1',
    title: 'North Flank Push on Berlin',
    slug: 'north-flank-push-berlin',
    mapId: '2',
    mapName: 'Berlin',
    description: 'Use the northern urban area to secure a strong flank position while avoiding the central killzone.',
    vehicleTypes: ['Medium Tank', 'Light Tank'],
    author: 'TankCommander',
    authorId: 'user1',
    createdAt: '2023-10-15',
    upvotes: 284,
    downvotes: 23,
    thumbnail: '/assets/maps/thumbnails/berlin.jpg',
    previewImage: '/assets/maps/full-size/Berlin/MapLayout_DOMINATION(BERLIN)_Berlin.jpg'
  },
  {
    id: '2',
    title: 'Fulda Ridge Sniping Spots',
    slug: 'fulda-ridge-sniping',
    mapId: '3',
    mapName: 'Fulda Gap',
    description: 'A collection of the best hull-down positions to control the central valley from the ridgelines.',
    vehicleTypes: ['Tank Destroyer', 'Heavy Tank'],
    author: 'SniperElite',
    authorId: 'user2',
    createdAt: '2023-11-02',
    upvotes: 197,
    downvotes: 12,
    thumbnail: '/assets/maps/thumbnails/fulda-gap.jpg',
    previewImage: '/assets/maps/full-size/Fulda Gap/MapLayout_DOMINATION(FULDA_GAP)_Fulda Gap.jpg'
  },
  {
    id: '3',
    title: 'Rhine Urban Brawling',
    slug: 'rhine-urban-brawling',
    mapId: '1',
    mapName: 'Advance to the Rhine',
    description: 'Dominate close-quarters combat in the city center using aggressive flanking maneuvers.',
    vehicleTypes: ['Light Tank', 'Medium Tank'],
    author: 'UrbanWarrior',
    authorId: 'user3',
    createdAt: '2023-12-05',
    upvotes: 176,
    downvotes: 18,
    thumbnail: '/assets/maps/thumbnails/advance-to-the-rhine.jpg',
    previewImage: '/assets/maps/full-size/Advance to the Rhine/MapLayout_DOMINATION(ADVANCE_TO_THE_RHINE)_Advance to the Rhine.jpg'
  },
  {
    id: '4',
    title: 'Eastern Europe Village Control',
    slug: 'eastern-europe-village-control',
    mapId: '5',
    mapName: 'Eastern Europe',
    description: 'Methodical approach to securing and holding the village against infantry and armor threats.',
    vehicleTypes: ['Heavy Tank', 'SPAA'],
    author: 'StrategyMaster',
    authorId: 'user4',
    createdAt: '2023-09-22',
    upvotes: 152,
    downvotes: 8,
    thumbnail: '/assets/maps/thumbnails/eastern-europe.jpg',
    previewImage: '/assets/maps/full-size/Eastern Europe/MapLayout_DOMINATION(EASTERN_EUROPE)_Eastern Europe.jpg'
  }
];

// Get featured tactics, sorted by upvote ratio
export function getFeaturedTactics(count: number): TacticData[] {
  return [...featuredTactics]
    .sort((a, b) => {
      const ratioA = a.upvotes / (a.upvotes + a.downvotes);
      const ratioB = b.upvotes / (b.upvotes + b.downvotes);
      return ratioB - ratioA;
    })
    .slice(0, count);
} 