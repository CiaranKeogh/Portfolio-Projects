export interface PowerPosition {
  id: string;
  name: string;
  map: string;
  mapImage: string;
  description: string;
  coordinates: {
    x: number;
    y: number;
  };
  coverLevel: number; // 1-5 rating
  suitableVehicles: string[];
  videoGuideUrl?: string;
  screenshots: string[];
  upvotes: number;
  views: number;
  dateAdded: string;
  addedBy: string;
}

// Mock power positions data for the homepage
export const powerPositions: PowerPosition[] = [
  {
    id: "position-1",
    name: "Hill 203 Overlook",
    map: "Kursk",
    mapImage: "/images/maps/kursk.jpg",
    description: "This elevated position provides clear line of sight to both the southern and eastern approach, perfect for long-range engagements. Natural depressions offer hull-down opportunities.",
    coordinates: {
      x: 65,
      y: 42
    },
    coverLevel: 4,
    suitableVehicles: ["Heavy Tank", "Tank Destroyer", "Medium Tank"],
    videoGuideUrl: "/videos/kursk-hill-203.mp4",
    screenshots: [
      "/images/positions/kursk-hill-203-1.jpg",
      "/images/positions/kursk-hill-203-2.jpg"
    ],
    upvotes: 342,
    views: 2156,
    dateAdded: "2023-04-15",
    addedBy: "TankCommander"
  },
  {
    id: "position-2",
    name: "Factory Ruins",
    map: "Stalingrad",
    mapImage: "/images/maps/stalingrad.jpg",
    description: "These ruins provide excellent cover while allowing you to control the central corridor of the map. Multiple firing positions let you adapt as the battle progresses.",
    coordinates: {
      x: 38,
      y: 57
    },
    coverLevel: 5,
    suitableVehicles: ["Medium Tank", "Light Tank", "Tank Destroyer"],
    screenshots: [
      "/images/positions/stalingrad-factory-1.jpg",
      "/images/positions/stalingrad-factory-2.jpg"
    ],
    upvotes: 289,
    views: 1872,
    dateAdded: "2023-05-22",
    addedBy: "RedArmy"
  },
  {
    id: "position-3",
    name: "North Ridge",
    map: "Fulda Gap",
    mapImage: "/images/maps/fulda.jpg",
    description: "This ridge offers a commanding view of the northern approaches and allows for long-range engagement of vehicles crossing the open fields. Retreat paths available to the west.",
    coordinates: {
      x: 23,
      y: 18
    },
    coverLevel: 3,
    suitableVehicles: ["Tank Destroyer", "Medium Tank", "SPAA"],
    videoGuideUrl: "/videos/fulda-north-ridge.mp4",
    screenshots: [
      "/images/positions/fulda-ridge-1.jpg",
      "/images/positions/fulda-ridge-2.jpg"
    ],
    upvotes: 215,
    views: 1453,
    dateAdded: "2023-06-08",
    addedBy: "NATOFan"
  },
  {
    id: "position-4",
    name: "Island Stronghold",
    map: "Jungle",
    mapImage: "/images/maps/jungle.jpg",
    description: "This central island controls all water crossings and provides excellent firing positions toward both spawns. Dense vegetation offers concealment for ambushes.",
    coordinates: {
      x: 50,
      y: 50
    },
    coverLevel: 5,
    suitableVehicles: ["Light Tank", "Medium Tank", "Tank Destroyer"],
    screenshots: [
      "/images/positions/jungle-island-1.jpg",
      "/images/positions/jungle-island-2.jpg"
    ],
    upvotes: 198,
    views: 1289,
    dateAdded: "2023-07-03",
    addedBy: "JungleAce"
  },
  {
    id: "position-5",
    name: "Desert Ridge",
    map: "Sinai",
    mapImage: "/images/maps/sinai.jpg",
    description: "This elevated dune provides excellent visibility across the central portion of the map. Limited cover means you need to use hull-down techniques effectively.",
    coordinates: {
      x: 62,
      y: 35
    },
    coverLevel: 2,
    suitableVehicles: ["Tank Destroyer", "Medium Tank", "Heavy Tank"],
    videoGuideUrl: "/videos/sinai-ridge.mp4",
    screenshots: [
      "/images/positions/sinai-ridge-1.jpg",
      "/images/positions/sinai-ridge-2.jpg"
    ],
    upvotes: 175,
    views: 1102,
    dateAdded: "2023-08-12",
    addedBy: "DesertFox"
  }
]; 