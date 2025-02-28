export interface Activity {
  id: number;
  type: 'route_added' | 'position_shared' | 'map_rated' | 'comment_posted' | 'guide_created';
  user: string;
  avatar: string;
  content: string;
  timestamp: string;
  relatedId?: number;
  relatedType?: string;
}

export const recentActivities: Activity[] = [
  {
    id: 1,
    type: 'route_added',
    user: 'DesertFox',
    avatar: '/avatars/user1.jpg',
    content: 'Added a new route for Alaska: "Western Hills Ambush"',
    timestamp: '2 hours ago',
    relatedId: 5,
    relatedType: 'route'
  },
  {
    id: 2,
    type: 'position_shared',
    user: 'TankCommander',
    avatar: '/avatars/user2.jpg',
    content: 'Shared a power position for Sinai: "Southern Dunes Hideout"',
    timestamp: '5 hours ago',
    relatedId: 7,
    relatedType: 'position'
  },
  {
    id: 3,
    type: 'map_rated',
    user: 'ArmorAce',
    avatar: '/avatars/user3.jpg',
    content: 'Rated Fields of Poland 4.7/5 stars',
    timestamp: '12 hours ago',
    relatedId: 6,
    relatedType: 'map'
  },
  {
    id: 4,
    type: 'comment_posted',
    user: 'SteelTiger',
    avatar: '/avatars/user4.jpg',
    content: 'Great route, but be careful of snipers near the church!',
    timestamp: '1 day ago',
    relatedId: 2,
    relatedType: 'route'
  },
  {
    id: 5,
    type: 'guide_created',
    user: 'StrategyMaster',
    avatar: '/avatars/user5.jpg',
    content: 'Created a new beginner\'s guide for Eastern Europe',
    timestamp: '1 day ago',
    relatedId: 4,
    relatedType: 'guide'
  },
  {
    id: 6,
    type: 'route_added',
    user: 'PanzerPro',
    avatar: '/avatars/user6.jpg',
    content: 'Added a new route for Karelia: "Northern Forest Flanking"',
    timestamp: '2 days ago',
    relatedId: 6,
    relatedType: 'route'
  }
]; 