export interface Map {
  id: string;
  name: string;
  thumbnail: string;
  fullImage: string;
  description: string;
  gameModes: string[];
  size: 'Small' | 'Medium' | 'Large';
  terrainType: string;
  popularity: number; // Out of 10
  viewCount: number;
  dateAdded: string;
  powerPositionsCount: number;
  strategicRoutesCount: number;
}

// Mock maps data for the homepage carousel
export const maps: Map[] = [
  {
    id: "map-1",
    name: "Advance to the Rhine",
    thumbnail: "/images/maps/thumbnails/rhine.jpg",
    fullImage: "/images/maps/rhine_full.jpg",
    description: "An urban battleground with narrow streets and multi-story buildings. Perfect for close-quarters combat and infantry support vehicles.",
    gameModes: ["Domination", "Battle", "Conquest"],
    size: "Medium",
    terrainType: "Urban",
    popularity: 9,
    viewCount: 8547,
    dateAdded: "2022-10-15",
    powerPositionsCount: 8,
    strategicRoutesCount: 12
  },
  {
    id: "map-2",
    name: "Sinai Desert",
    thumbnail: "/images/maps/thumbnails/sinai.jpg",
    fullImage: "/images/maps/sinai_full.jpg",
    description: "Open desert terrain with small villages and dunes. Excellent for long-range engagements and flanking maneuvers.",
    gameModes: ["Domination", "Battle", "Conquest", "Break"],
    size: "Large",
    terrainType: "Desert",
    popularity: 7,
    viewCount: 6329,
    dateAdded: "2022-11-03",
    powerPositionsCount: 5,
    strategicRoutesCount: 9
  },
  {
    id: "map-3",
    name: "Karelia",
    thumbnail: "/images/maps/thumbnails/karelia.jpg",
    fullImage: "/images/maps/karelia_full.jpg",
    description: "Dense forest with rocky outcroppings and narrow passages. Favors ambush tactics and defensive positions.",
    gameModes: ["Domination", "Battle"],
    size: "Small",
    terrainType: "Forest",
    popularity: 8,
    viewCount: 7123,
    dateAdded: "2022-09-22",
    powerPositionsCount: 7,
    strategicRoutesCount: 8
  },
  {
    id: "map-4",
    name: "Maginot Line",
    thumbnail: "/images/maps/thumbnails/maginot.jpg",
    fullImage: "/images/maps/maginot_full.jpg",
    description: "Rolling hills and trenches based on the historical fortification line. Mix of open fields and defensive positions.",
    gameModes: ["Domination", "Conquest", "Break"],
    size: "Large",
    terrainType: "Mixed",
    popularity: 6,
    viewCount: 5438,
    dateAdded: "2022-12-08",
    powerPositionsCount: 6,
    strategicRoutesCount: 11
  },
  {
    id: "map-5",
    name: "Berlin",
    thumbnail: "/images/maps/thumbnails/berlin.jpg",
    fullImage: "/images/maps/berlin_full.jpg",
    description: "Devastated urban environment with destroyed buildings, rubble, and tight corridors. Intense street-to-street fighting.",
    gameModes: ["Domination", "Battle", "Conquest"],
    size: "Medium",
    terrainType: "Urban",
    popularity: 8,
    viewCount: 7825,
    dateAdded: "2023-01-17",
    powerPositionsCount: 9,
    strategicRoutesCount: 13
  },
  {
    id: "map-6",
    name: "Kursk",
    thumbnail: "/images/maps/thumbnails/kursk.jpg",
    fullImage: "/images/maps/kursk_full.jpg",
    description: "Vast open plains with minimal cover, based on the historic tank battle. Long sight lines favor sniping and hull-down tactics.",
    gameModes: ["Domination", "Battle", "Conquest", "Break"],
    size: "Large",
    terrainType: "Steppe",
    popularity: 7,
    viewCount: 6214,
    dateAdded: "2023-02-25",
    powerPositionsCount: 4,
    strategicRoutesCount: 7
  }
]; 