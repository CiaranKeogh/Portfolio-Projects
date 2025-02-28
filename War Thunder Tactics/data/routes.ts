export interface Route {
  id: number;
  name: string;
  map: string;
  mapImage: string;
  createdBy: string;
  successRate: number;
  upvotes: number;
  recommendedVehicles: string[];
  description: string;
}

export const topRoutes: Route[] = [
  {
    id: 1,
    name: "South Flank Push",
    map: "Eastern Europe",
    mapImage: "/routes/eastern-europe-south-flank.jpg",
    createdBy: "TankAce420",
    successRate: 78,
    upvotes: 342,
    recommendedVehicles: ["Light Tanks", "Fast Medium Tanks"],
    description: "Quick flanking route to surprise enemy side shooters. Avoid open areas and stick to buildings."
  },
  {
    id: 2,
    name: "Central Bridge Rush",
    map: "Advance to the Rhine",
    mapImage: "/routes/rhine-bridge-rush.jpg",
    createdBy: "StealthSniper",
    successRate: 65,
    upvotes: 287,
    recommendedVehicles: ["Medium Tanks", "Heavy Tanks"],
    description: "Direct push to the central bridge with team support. Provides early map control."
  },
  {
    id: 3,
    name: "Hill Bypass",
    map: "Karelia",
    mapImage: "/routes/karelia-hill-bypass.jpg",
    createdBy: "GeneralPatton",
    successRate: 82,
    upvotes: 456,
    recommendedVehicles: ["Light Tanks", "Medium Tanks"],
    description: "Sneaky route behind the eastern hill that allows for rear shots on enemies watching the usual approach."
  },
  {
    id: 4,
    name: "Village Sweep",
    map: "Fields of Poland",
    mapImage: "/routes/poland-village-sweep.jpg",
    createdBy: "DezertFox",
    successRate: 70,
    upvotes: 312,
    recommendedVehicles: ["Medium Tanks", "Tank Destroyers"],
    description: "Systematic clearing of the village buildings from south to north, providing safe progression."
  }
];

export interface StrategicRoute {
  id: string;
  name: string;
  map: string;
  mapImage: string;
  description: string;
  vehicleType: string;
  gameMode: string;
  successRate: number;
  timeToExecute: number; // in minutes
  waypoints: string[];
  recommendedVehicles: string[];
  upvotes: number;
  dateAdded: string;
  addedBy: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
}

// Mock strategic routes data for the homepage
export const strategicRoutes: StrategicRoute[] = [
  {
    id: "route-1",
    name: "Northern Flanking Route",
    map: "Maginot Line",
    mapImage: "/images/maps/maginot.jpg",
    description: "A stealthy northern route that bypasses the main combat areas, allowing for surprise attacks on cap points or enemy spawns.",
    vehicleType: "Light Tank",
    gameMode: "Domination",
    successRate: 78,
    timeToExecute: 3,
    waypoints: [
      "Start at the northern spawn",
      "Move through the forest at A3, staying in cover",
      "Cross the open field at B5 using smoke if detected",
      "Position at the rocks near C7 to engage enemies at the capture point",
      "Push to capture point when teammates apply pressure from the center"
    ],
    recommendedVehicles: [
      "M18 Hellcat",
      "BT-7",
      "Puma",
      "EBR"
    ],
    upvotes: 427,
    dateAdded: "2023-05-12",
    addedBy: "SpeedDemon",
    difficulty: "Medium"
  },
  {
    id: "route-2",
    name: "Urban Corridor Push",
    map: "Berlin",
    mapImage: "/images/maps/berlin.jpg",
    description: "A coordinated push through the urban corridor with strong points for defense and hull-down positions.",
    vehicleType: "Medium Tank",
    gameMode: "Battle",
    successRate: 65,
    timeToExecute: 5,
    waypoints: [
      "Group up near the collapsed buildings at D5",
      "Advance along the main street using buildings for cover",
      "Set up positions at the intersection near F7",
      "Cover teammates as they push toward the enemy spawn",
      "Hold the gained territory and repel counter-attacks"
    ],
    recommendedVehicles: [
      "T-34-85",
      "Sherman Jumbo",
      "Panther D",
      "Centurion Mk.1"
    ],
    upvotes: 352,
    dateAdded: "2023-06-18",
    addedBy: "UrbanTactician",
    difficulty: "Medium"
  },
  {
    id: "route-3",
    name: "Ridge Line Control",
    map: "Karelia",
    mapImage: "/images/maps/karelia.jpg",
    description: "Take control of the central ridge to dominate sight lines and control the flow of battle.",
    vehicleType: "Heavy Tank",
    gameMode: "Conquest",
    successRate: 83,
    timeToExecute: 4,
    waypoints: [
      "Advance quickly to the base of the ridge at C4",
      "Climb the ridge using the path at C5",
      "Set up hull-down position at the top of ridge D6",
      "Control both capture points from elevated position",
      "Rotate to defend against flankers when needed"
    ],
    recommendedVehicles: [
      "Tiger H1",
      "IS-2",
      "T29",
      "Conqueror"
    ],
    upvotes: 498,
    dateAdded: "2023-04-03",
    addedBy: "RidgeMaster",
    difficulty: "Easy"
  },
  {
    id: "route-4",
    name: "Desert Flanking Maneuver",
    map: "Sinai",
    mapImage: "/images/maps/sinai.jpg",
    description: "Use the dunes for cover as you execute a wide flanking maneuver to surprise the enemy team.",
    vehicleType: "Light Tank",
    gameMode: "Domination",
    successRate: 71,
    timeToExecute: 2,
    waypoints: [
      "Start at the eastern spawn point",
      "Move south behind the large dunes to avoid detection",
      "Cross the dry riverbed at G7",
      "Position behind the enemy at the western capture point",
      "Engage from unexpected angle, causing confusion"
    ],
    recommendedVehicles: [
      "AMX-13",
      "PT-76",
      "M41 Walker Bulldog",
      "Type 62"
    ],
    upvotes: 315,
    dateAdded: "2023-07-22",
    addedBy: "DesertRaider",
    difficulty: "Medium"
  },
  {
    id: "route-5",
    name: "Village Control Strategy",
    map: "Eastern Europe",
    mapImage: "/images/maps/eastern_europe.jpg",
    description: "Take control of the village and use buildings for cover while dominating the central capture point.",
    vehicleType: "Medium Tank",
    gameMode: "Domination",
    successRate: 75,
    timeToExecute: 6,
    waypoints: [
      "Advance to the outskirts of the village at D4",
      "Secure the large building at E5 for cover",
      "Control the roads leading to the central capture point",
      "Rotate between positions to avoid artillery",
      "Support teammates pushing to secure the capture point"
    ],
    recommendedVehicles: [
      "T-44",
      "M26 Pershing",
      "Panther G",
      "Centurion Mk.3"
    ],
    upvotes: 382,
    dateAdded: "2023-08-05",
    addedBy: "VillageCommander",
    difficulty: "Hard"
  }
]; 