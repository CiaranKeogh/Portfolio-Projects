export interface CommunityStatItem {
  label: string;
  value: string;
}

export interface CommunityActivity {
  userName: string;
  userAvatar: string;
  time: string;
  action: string;
  link: string;
}

export interface Contributor {
  name: string;
  avatar: string;
  contributions: number;
  score: number; // Combined score for ranking
}

export interface CommunityStats {
  stats: CommunityStatItem[];
  recentActivity: CommunityActivity[];
  topContributors: Contributor[];
}

// Mock community data for the homepage
export const communityStats: CommunityStats = {
  stats: [
    {
      label: "Active Users",
      value: "12.5K+"
    },
    {
      label: "Routes Shared",
      value: "876"
    },
    {
      label: "Power Positions",
      value: "452"
    },
    {
      label: "Tips & Guides",
      value: "1.2K+"
    }
  ],
  recentActivity: [
    {
      userName: "TankCommander",
      userAvatar: "/images/avatars/user1.jpg",
      time: "2 hours ago",
      action: "Added a new power position 'Ridge Overlook' on the Fulda Gap map",
      link: "/positions/position-45"
    },
    {
      userName: "DesertFox",
      userAvatar: "/images/avatars/user2.jpg",
      time: "5 hours ago",
      action: "Shared a new strategic route 'North Flank Push' for Berlin",
      link: "/routes/route-92"
    },
    {
      userName: "StalingradVet",
      userAvatar: "/images/avatars/user3.jpg",
      time: "Yesterday",
      action: "Published a new guide: 'Advanced Hull-Down Techniques for Heavy Tanks'",
      link: "/guides/guide-27"
    },
    {
      userName: "TigerAce",
      userAvatar: "/images/avatars/user4.jpg",
      time: "2 days ago",
      action: "Updated the 'Factory Control' route on Advance to the Rhine with new waypoints",
      link: "/routes/route-38"
    },
    {
      userName: "RedArmy",
      userAvatar: "/images/avatars/user5.jpg",
      time: "3 days ago",
      action: "Added a video demonstration for the 'Hill 203' power position on Kursk",
      link: "/positions/position-12"
    }
  ],
  topContributors: [
    {
      name: "TankCommander",
      avatar: "/images/avatars/user1.jpg",
      contributions: 87,
      score: 1250
    },
    {
      name: "DesertFox",
      avatar: "/images/avatars/user2.jpg",
      contributions: 64,
      score: 980
    },
    {
      name: "StalingradVet",
      avatar: "/images/avatars/user3.jpg",
      contributions: 52,
      score: 820
    },
    {
      name: "TigerAce",
      avatar: "/images/avatars/user4.jpg",
      contributions: 45,
      score: 760
    },
    {
      name: "RedArmy",
      avatar: "/images/avatars/user5.jpg",
      contributions: 38,
      score: 690
    },
    {
      name: "StrategyMaster",
      avatar: "/images/avatars/user6.jpg",
      contributions: 32,
      score: 580
    },
    {
      name: "PanzerElite",
      avatar: "/images/avatars/user7.jpg",
      contributions: 29,
      score: 520
    }
  ]
}; 