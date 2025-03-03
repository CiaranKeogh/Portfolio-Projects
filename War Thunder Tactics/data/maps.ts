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
  layouts?: string[]; // Array of layout image paths
}

// Maps data for the War Thunder Tactics website
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
    strategicRoutesCount: 12,
    layouts: [
      "/images/maps/layouts/rhine_layout1.jpg",
      "/images/maps/layouts/rhine_layout2.jpg",
      "/images/maps/layouts/rhine_layout3.jpg",
      "/images/maps/layouts/rhine_layout4.jpg",
      "/images/maps/layouts/rhine_layout5.jpg",
      "/images/maps/layouts/rhine_layout6.jpg"
    ]
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
  },
  {
    id: "map-7",
    name: "Stalingrad",
    thumbnail: "/images/maps/thumbnails/stalingrad.jpg",
    fullImage: "/images/maps/stalingrad_full.jpg",
    description: "Winter urban combat in the ruins of Stalingrad. Features factory complexes, railway stations, and destroyed apartment blocks.",
    gameModes: ["Domination", "Battle", "Conquest"],
    size: "Medium",
    terrainType: "Urban",
    popularity: 9,
    viewCount: 8129,
    dateAdded: "2022-11-12",
    powerPositionsCount: 10,
    strategicRoutesCount: 14
  },
  {
    id: "map-8",
    name: "Eastern Europe",
    thumbnail: "/images/maps/thumbnails/eastern_europe.jpg",
    fullImage: "/images/maps/eastern_europe_full.jpg",
    description: "Small Eastern European town with surrounding fields. Features urban combat in narrow streets and open field engagements.",
    gameModes: ["Domination", "Battle", "Conquest"],
    size: "Medium",
    terrainType: "Mixed",
    popularity: 8,
    viewCount: 7014,
    dateAdded: "2022-12-20",
    powerPositionsCount: 8,
    strategicRoutesCount: 10
  },
  {
    id: "map-9",
    name: "Fulda Gap",
    thumbnail: "/images/maps/thumbnails/fulda.jpg",
    fullImage: "/images/maps/fulda_full.jpg",
    description: "Based on the Cold War defensive line, featuring rolling hills, small towns, and border fortifications.",
    gameModes: ["Domination", "Battle", "Conquest", "Break"],
    size: "Large",
    terrainType: "Rural",
    popularity: 7,
    viewCount: 5932,
    dateAdded: "2023-02-10",
    powerPositionsCount: 6,
    strategicRoutesCount: 9
  },
  {
    id: "map-10",
    name: "Jungle",
    thumbnail: "/images/maps/thumbnails/jungle.jpg",
    fullImage: "/images/maps/jungle_full.jpg",
    description: "Thick tropical forest with ancient temple ruins and narrow paths. Limited visibility with choke points and defensive positions.",
    gameModes: ["Domination", "Battle"],
    size: "Small",
    terrainType: "Jungle",
    popularity: 6,
    viewCount: 5213,
    dateAdded: "2023-01-28",
    powerPositionsCount: 5,
    strategicRoutesCount: 7
  },
  {
    id: "map-11",
    name: "Alaska",
    thumbnail: "/images/maps/thumbnails/karelia.jpg", // Using Karelia as a placeholder since it has snowy terrain
    fullImage: "/images/maps/karelia_full.jpg",
    description: "Snowy mountain environment with a small town and surrounding forests. Great for all types of engagements across varied terrain.",
    gameModes: ["Domination", "Battle", "Conquest"],
    size: "Medium",
    terrainType: "Winter",
    popularity: 7,
    viewCount: 5987,
    dateAdded: "2023-01-05",
    powerPositionsCount: 6,
    strategicRoutesCount: 9
  },
  {
    id: "map-12",
    name: "Abandoned Factory",
    thumbnail: "/images/maps/thumbnails/berlin.jpg", // Urban imagery as placeholder
    fullImage: "/images/maps/berlin_full.jpg",
    description: "Industrial complex with warehouses and factory buildings. Balanced mix of open areas and enclosed spaces.",
    gameModes: ["Domination", "Battle"],
    size: "Small",
    terrainType: "Industrial",
    popularity: 8,
    viewCount: 6742,
    dateAdded: "2022-10-30",
    powerPositionsCount: 7,
    strategicRoutesCount: 8
  },
  {
    id: "map-13",
    name: "White Rock Fortress",
    thumbnail: "/images/maps/thumbnails/rhine.jpg", // Using Rhine as a placeholder (urban with structures)
    fullImage: "/images/maps/rhine_full.jpg",
    description: "Ancient stone fortress on a coastal cliff. Features multiple levels, tight corridors, and defensive positions.",
    gameModes: ["Domination", "Battle"],
    size: "Small",
    terrainType: "Coastal",
    popularity: 6,
    viewCount: 4876,
    dateAdded: "2023-03-05",
    powerPositionsCount: 7,
    strategicRoutesCount: 9
  },
  {
    id: "map-14",
    name: "El Alamein",
    thumbnail: "/images/maps/thumbnails/sinai.jpg", // Using Sinai as a placeholder (desert)
    fullImage: "/images/maps/sinai_full.jpg",
    description: "North African desert with dunes, ridges, and fortified positions. Based on the historic WWII battle.",
    gameModes: ["Domination", "Battle", "Conquest", "Break"],
    size: "Large",
    terrainType: "Desert",
    popularity: 7,
    viewCount: 5824,
    dateAdded: "2023-02-18",
    powerPositionsCount: 5,
    strategicRoutesCount: 8
  },
  {
    id: "map-15",
    name: "Tunisia",
    thumbnail: "/images/maps/thumbnails/sinai.jpg", // Using Sinai as a placeholder (desert/urban mix)
    fullImage: "/images/maps/sinai_full.jpg",
    description: "North African town with surrounding desert. Features urban combat in narrow streets and open desert engagements.",
    gameModes: ["Domination", "Battle", "Conquest"],
    size: "Medium",
    terrainType: "Desert",
    popularity: 7,
    viewCount: 5931,
    dateAdded: "2022-12-15",
    powerPositionsCount: 6,
    strategicRoutesCount: 9
  },
  {
    id: "map-16",
    name: "Mozdok",
    thumbnail: "/images/maps/thumbnails/kursk.jpg", // Using Kursk as a placeholder (open fields)
    fullImage: "/images/maps/kursk_full.jpg",
    description: "Large open battlefield in the Caucasus region. Features hills, small forests, and a river crossing.",
    gameModes: ["Domination", "Battle", "Conquest", "Break"],
    size: "Large",
    terrainType: "Rural",
    popularity: 8,
    viewCount: 6752,
    dateAdded: "2022-11-20",
    powerPositionsCount: 7,
    strategicRoutesCount: 10
  },
  {
    id: "map-17",
    name: "Ash River",
    thumbnail: "/images/maps/thumbnails/karelia.jpg", // Using Karelia as a placeholder (hills and forests)
    fullImage: "/images/maps/karelia_full.jpg",
    description: "River valley with bridges, hills, and small industrial areas. Good mix of terrain types for varied gameplay.",
    gameModes: ["Domination", "Battle"],
    size: "Medium",
    terrainType: "River Valley",
    popularity: 7,
    viewCount: 6123,
    dateAdded: "2023-01-10",
    powerPositionsCount: 6,
    strategicRoutesCount: 9
  },
  {
    id: "map-18",
    name: "Port Novorossiysk",
    thumbnail: "/images/maps/thumbnails/eastern_europe.jpg", // Using Eastern Europe as a placeholder (town)
    fullImage: "/images/maps/eastern_europe_full.jpg",
    description: "Black Sea port city with docks, industrial buildings, and coastal defenses. Urban combat with open water sightlines.",
    gameModes: ["Domination", "Battle", "Conquest"],
    size: "Medium",
    terrainType: "Coastal",
    popularity: 6,
    viewCount: 5324,
    dateAdded: "2023-03-01",
    powerPositionsCount: 7,
    strategicRoutesCount: 10
  },
  {
    id: "map-19",
    name: "38th Parallel",
    thumbnail: "/images/maps/thumbnails/maginot.jpg", // Using Maginot as a placeholder (hills and varied terrain)
    fullImage: "/images/maps/maginot_full.jpg",
    description: "Korean War setting with hills, villages, and rice paddies. Features a central river with several crossing points.",
    gameModes: ["Domination", "Conquest", "Break"],
    size: "Large",
    terrainType: "Rural",
    popularity: 7,
    viewCount: 5687,
    dateAdded: "2023-02-05",
    powerPositionsCount: 8,
    strategicRoutesCount: 11
  },
  {
    id: "map-20",
    name: "Finland",
    thumbnail: "/images/maps/thumbnails/karelia.jpg", // Using Karelia as a placeholder (forest)
    fullImage: "/images/maps/karelia_full.jpg",
    description: "Winter forest with frozen lakes and small settlements. Excellent for ambush tactics and defensive positions.",
    gameModes: ["Domination", "Battle"],
    size: "Medium",
    terrainType: "Winter",
    popularity: 8,
    viewCount: 6432,
    dateAdded: "2022-10-22",
    powerPositionsCount: 7,
    strategicRoutesCount: 9
  },
  {
    id: "map-21",
    name: "Normandy",
    thumbnail: "/images/maps/thumbnails/eastern_europe.jpg", // Using Eastern Europe as a placeholder (countryside with structures)
    fullImage: "/images/maps/eastern_europe_full.jpg",
    description: "D-Day landings with beachfront, bunkers, and inland villages. A mix of open beaches and close-quarters inland fighting.",
    gameModes: ["Domination", "Battle", "Conquest", "Break"],
    size: "Large",
    terrainType: "Coastal",
    popularity: 9,
    viewCount: 7925,
    dateAdded: "2022-10-08",
    powerPositionsCount: 9,
    strategicRoutesCount: 12
  },
  {
    id: "map-22",
    name: "Vietnam",
    thumbnail: "/images/maps/thumbnails/jungle.jpg", // Using Jungle as a placeholder
    fullImage: "/images/maps/jungle_full.jpg",
    description: "Dense jungle with a central village and river crossings. Challenging visibility and lots of cover for ambush tactics.",
    gameModes: ["Domination", "Battle"],
    size: "Medium",
    terrainType: "Jungle",
    popularity: 7,
    viewCount: 6015,
    dateAdded: "2022-12-05",
    powerPositionsCount: 8,
    strategicRoutesCount: 11
  },
  {
    id: "map-23",
    name: "Carpathians",
    thumbnail: "/images/maps/thumbnails/karelia.jpg", // Using Karelia as a placeholder (mountainous terrain)
    fullImage: "/images/maps/karelia_full.jpg",
    description: "Mountain warfare in the Carpathian range. Steep slopes, valleys, and small villages create a challenging combat environment.",
    gameModes: ["Domination", "Conquest"],
    size: "Medium",
    terrainType: "Mountain",
    popularity: 7,
    viewCount: 5672,
    dateAdded: "2022-11-30",
    powerPositionsCount: 6,
    strategicRoutesCount: 8
  }
]; 