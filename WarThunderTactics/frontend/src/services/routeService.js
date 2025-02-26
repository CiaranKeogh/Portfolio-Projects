import api from './api';

// Sample route data
const sampleRoutes = [
  {
    _id: '1',
    title: 'North Ridge Flanking Route',
    description: 'A strategic flanking route that allows medium tanks to bypass the central combat area and attack enemy positions from behind.',
    mapId: '1',
    map: { 
      _id: '1', 
      name: 'Advance to the Rhine' 
    },
    creator: {
      _id: 'user1',
      username: 'TankCommander'
    },
    gameMode: 'Ground Realistic',
    vehicleType: 'Medium Tank',
    difficulty: 'Medium',
    effectiveness: 4.5,
    coordinates: [
      { x: 120, y: 45 },
      { x: 135, y: 60 },
      { x: 160, y: 80 },
      { x: 200, y: 85 }
    ],
    upvotes: 42,
    downvotes: 5,
    comments: [
      {
        _id: 'c1',
        user: { _id: 'user2', username: 'StratMaster' },
        content: 'Works great with German Panther tanks!',
        createdAt: '2023-06-15T10:30:00Z'
      }
    ],
    createdAt: '2023-06-10T08:15:00Z',
    updatedAt: '2023-06-15T10:32:00Z'
  },
  {
    _id: '2',
    title: 'South Forest Ambush Path',
    description: 'A sneaky route through the forest that provides excellent cover and ambush opportunities for tank destroyers.',
    mapId: '4',
    map: { 
      _id: '4', 
      name: 'Finland' 
    },
    creator: {
      _id: 'user1',
      username: 'TankCommander'
    },
    gameMode: 'Ground Realistic',
    vehicleType: 'Tank Destroyer',
    difficulty: 'Easy',
    effectiveness: 4.8,
    coordinates: [
      { x: 75, y: 200 },
      { x: 90, y: 220 },
      { x: 110, y: 225 },
      { x: 130, y: 240 }
    ],
    upvotes: 28,
    downvotes: 2,
    comments: [],
    createdAt: '2023-07-05T14:22:00Z',
    updatedAt: '2023-07-05T14:22:00Z'
  },
  {
    _id: '3',
    title: 'Central Push Strategy',
    description: 'A direct route through the city center. Risky but can lead to quick capture of the central control point.',
    mapId: '2',
    map: { 
      _id: '2', 
      name: 'Berlin' 
    },
    creator: {
      _id: 'user3',
      username: 'StrategyMaster'
    },
    gameMode: 'Ground Arcade',
    vehicleType: 'Heavy Tank',
    difficulty: 'Hard',
    effectiveness: 3.9,
    coordinates: [
      { x: 150, y: 150 },
      { x: 160, y: 155 },
      { x: 175, y: 160 },
      { x: 190, y: 170 }
    ],
    upvotes: 67,
    downvotes: 15,
    comments: [
      {
        _id: 'c2',
        user: { _id: 'user4', username: 'TigerAce' },
        content: 'Works well with teammates, suicide mission solo.',
        createdAt: '2023-05-20T16:45:00Z'
      },
      {
        _id: 'c3',
        user: { _id: 'user5', username: 'SovietTanker' },
        content: 'Great for IS-2 with its strong frontal armor.',
        createdAt: '2023-05-21T08:12:00Z'
      }
    ],
    createdAt: '2023-05-18T11:30:00Z',
    updatedAt: '2023-05-21T08:14:00Z'
  }
];

/**
 * Get all routes
 * @returns {Promise} Promise object that resolves to an array of routes
 */
export const getRoutes = () => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      resolve(sampleRoutes);
    }, 800);
  });
};

/**
 * Get a single route by ID
 * @param {string} id - ID of the route
 * @returns {Promise} Promise object that resolves to a route object
 */
export const getRouteById = (id) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const route = sampleRoutes.find(r => r._id === id);
      
      if (route) {
        resolve(route);
      } else {
        reject(new Error('Route not found'));
      }
    }, 600);
  });
};

/**
 * Get routes by map ID
 * @param {string} mapId - ID of the map
 * @returns {Promise} Promise object that resolves to an array of routes
 */
export const getRoutesByMap = (mapId) => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const filteredRoutes = sampleRoutes.filter(route => route.mapId === mapId);
      resolve(filteredRoutes);
    }, 800);
  });
};

/**
 * Get routes by user ID
 * @param {string} userId - ID of the user
 * @returns {Promise} Promise object that resolves to an array of routes
 */
export const getRoutesByUser = (userId) => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const filteredRoutes = sampleRoutes.filter(route => route.creator._id === userId);
      resolve(filteredRoutes);
    }, 800);
  });
};

/**
 * Get top rated routes
 * @returns {Promise} Promise object that resolves to an array of routes
 */
export const getTopRatedRoutes = () => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const sortedRoutes = [...sampleRoutes].sort((a, b) => {
        const scoreA = a.upvotes - a.downvotes;
        const scoreB = b.upvotes - b.downvotes;
        return scoreB - scoreA;
      });
      resolve(sortedRoutes.slice(0, 5)); // Top 5 routes
    }, 800);
  });
};

/**
 * Get recent routes
 * @returns {Promise} Promise object that resolves to an array of routes
 */
export const getRecentRoutes = () => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const sortedRoutes = [...sampleRoutes].sort((a, b) => {
        return new Date(b.createdAt) - new Date(a.createdAt);
      });
      resolve(sortedRoutes.slice(0, 5)); // Most recent 5 routes
    }, 800);
  });
};

/**
 * Search routes
 * @param {string} searchTerm - Term to search for
 * @returns {Promise} Promise object that resolves to an array of routes
 */
export const searchRoutes = (searchTerm) => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const filteredRoutes = sampleRoutes.filter(route => 
        route.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        route.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
      resolve(filteredRoutes);
    }, 800);
  });
};

/**
 * Create a new route
 * @param {Object} routeData - Data for the new route
 * @returns {Promise} Promise object that resolves to the created route
 */
export const createRoute = (routeData) => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      // Generate a simple random ID
      const newId = Math.floor(Math.random() * 10000).toString();
      
      // Create the new route with timestamp
      const newRoute = {
        _id: newId,
        ...routeData,
        upvotes: 0,
        downvotes: 0,
        comments: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
      
      // In a real app, this would be saved to a database
      // Here we just return it
      resolve(newRoute);
    }, 1200);
  });
};

/**
 * Update an existing route
 * @param {string} id - ID of the route to update
 * @param {Object} routeData - New data for the route
 * @returns {Promise} Promise object that resolves to the updated route
 */
export const updateRoute = (id, routeData) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const routeIndex = sampleRoutes.findIndex(r => r._id === id);
      
      if (routeIndex !== -1) {
        // In a real app, this would update the database
        const updatedRoute = {
          ...sampleRoutes[routeIndex],
          ...routeData,
          updatedAt: new Date().toISOString()
        };
        
        resolve(updatedRoute);
      } else {
        reject(new Error('Route not found'));
      }
    }, 1000);
  });
};

/**
 * Delete a route
 * @param {string} id - ID of the route to delete
 * @returns {Promise} Promise object that resolves when the route is deleted
 */
export const deleteRoute = (id) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const routeIndex = sampleRoutes.findIndex(r => r._id === id);
      
      if (routeIndex !== -1) {
        // In a real app, this would delete from the database
        resolve({ success: true, message: 'Route deleted successfully' });
      } else {
        reject(new Error('Route not found'));
      }
    }, 800);
  });
};

/**
 * Vote on a route
 * @param {string} id - ID of the route to vote on
 * @param {string} voteType - Type of vote ('up' or 'down')
 * @returns {Promise} Promise object that resolves to the updated route
 */
export const voteOnRoute = (id, voteType) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const routeIndex = sampleRoutes.findIndex(r => r._id === id);
      
      if (routeIndex !== -1) {
        // In a real app, this would update the database
        const updatedRoute = { ...sampleRoutes[routeIndex] };
        
        if (voteType === 'up') {
          updatedRoute.upvotes += 1;
        } else if (voteType === 'down') {
          updatedRoute.downvotes += 1;
        }
        
        resolve(updatedRoute);
      } else {
        reject(new Error('Route not found'));
      }
    }, 500);
  });
};

/**
 * Add a comment to a route
 * @param {string} routeId - ID of the route
 * @param {Object} commentData - Data for the new comment
 * @returns {Promise} Promise object that resolves to the updated route
 */
export const addComment = (routeId, commentData) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const routeIndex = sampleRoutes.findIndex(r => r._id === routeId);
      
      if (routeIndex !== -1) {
        // Generate a simple random ID
        const newCommentId = `c${Math.floor(Math.random() * 10000)}`;
        
        // Create the new comment
        const newComment = {
          _id: newCommentId,
          ...commentData,
          createdAt: new Date().toISOString()
        };
        
        // Add comment to route
        const updatedRoute = {
          ...sampleRoutes[routeIndex],
          comments: [...sampleRoutes[routeIndex].comments, newComment],
          updatedAt: new Date().toISOString()
        };
        
        resolve(updatedRoute);
      } else {
        reject(new Error('Route not found'));
      }
    }, 800);
  });
}; 