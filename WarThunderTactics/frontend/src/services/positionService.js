import api from './api';

// Sample position data
const samplePositions = [
  {
    _id: '1',
    title: 'Eastern Hill Sniper Spot',
    description: 'Excellent elevated position with clear lines of sight across the eastern approach. Perfect for tank destroyers.',
    mapId: '3',
    map: { 
      _id: '3', 
      name: 'Karelia' 
    },
    creator: {
      _id: 'user1',
      username: 'TankCommander'
    },
    gameMode: 'Ground Realistic',
    type: 'Sniper Spot',
    vehicleType: 'Tank Destroyer',
    effectiveness: 4.7,
    coordinates: { x: 185, y: 75 },
    upvotes: 35,
    downvotes: 3,
    comments: [
      {
        _id: 'c1',
        user: { _id: 'user4', username: 'TigerAce' },
        content: 'Great spot for German TDs with their excellent optics.',
        createdAt: '2023-06-18T09:45:00Z'
      }
    ],
    createdAt: '2023-06-12T14:30:00Z',
    updatedAt: '2023-06-18T09:47:00Z'
  },
  {
    _id: '2',
    title: 'Central Ridge Cover',
    description: 'Good hull-down position that provides cover while allowing you to engage enemies crossing the central area.',
    mapId: '1',
    map: { 
      _id: '1', 
      name: 'Advance to the Rhine' 
    },
    creator: {
      _id: 'user5',
      username: 'SniperElite'
    },
    gameMode: 'Ground Realistic',
    type: 'Hull-down Position',
    vehicleType: 'Medium Tank',
    effectiveness: 4.2,
    coordinates: { x: 150, y: 130 },
    upvotes: 54,
    downvotes: 7,
    comments: [
      {
        _id: 'c2',
        user: { _id: 'user2', username: 'StratMaster' },
        content: 'Works really well with American tanks that have good gun depression.',
        createdAt: '2023-05-25T18:15:00Z'
      }
    ],
    createdAt: '2023-05-22T11:20:00Z',
    updatedAt: '2023-05-25T18:17:00Z'
  },
  {
    _id: '3',
    title: 'Western Ambush Corner',
    description: 'Hidden spot behind debris that allows for surprise side shots on enemies moving along the western route.',
    mapId: '5',
    map: { 
      _id: '5', 
      name: 'Sinai' 
    },
    creator: {
      _id: 'user3',
      username: 'StrategyMaster'
    },
    gameMode: 'Ground Realistic',
    type: 'Ambush Spot',
    vehicleType: 'Light Tank',
    effectiveness: 4.4,
    coordinates: { x: 75, y: 145 },
    upvotes: 42,
    downvotes: 4,
    comments: [],
    createdAt: '2023-07-10T08:45:00Z',
    updatedAt: '2023-07-10T08:45:00Z'
  }
];

/**
 * Get all positions
 * @returns {Promise} Promise object that resolves to an array of positions
 */
export const getPositions = () => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      resolve(samplePositions);
    }, 800);
  });
};

/**
 * Get a single position by ID
 * @param {string} id - ID of the position
 * @returns {Promise} Promise object that resolves to a position object
 */
export const getPositionById = (id) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const position = samplePositions.find(p => p._id === id);
      
      if (position) {
        resolve(position);
      } else {
        reject(new Error('Position not found'));
      }
    }, 600);
  });
};

/**
 * Get positions by map ID
 * @param {string} mapId - ID of the map
 * @returns {Promise} Promise object that resolves to an array of positions
 */
export const getPositionsByMap = (mapId) => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const filteredPositions = samplePositions.filter(position => position.mapId === mapId);
      resolve(filteredPositions);
    }, 800);
  });
};

/**
 * Get positions by user ID
 * @param {string} userId - ID of the user
 * @returns {Promise} Promise object that resolves to an array of positions
 */
export const getPositionsByUser = (userId) => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const filteredPositions = samplePositions.filter(position => position.creator._id === userId);
      resolve(filteredPositions);
    }, 800);
  });
};

/**
 * Get top rated positions
 * @returns {Promise} Promise object that resolves to an array of positions
 */
export const getTopRatedPositions = () => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const sortedPositions = [...samplePositions].sort((a, b) => {
        const scoreA = a.upvotes - a.downvotes;
        const scoreB = b.upvotes - b.downvotes;
        return scoreB - scoreA;
      });
      resolve(sortedPositions.slice(0, 5)); // Top 5 positions
    }, 800);
  });
};

/**
 * Get recent positions
 * @returns {Promise} Promise object that resolves to an array of positions
 */
export const getRecentPositions = () => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const sortedPositions = [...samplePositions].sort((a, b) => {
        return new Date(b.createdAt) - new Date(a.createdAt);
      });
      resolve(sortedPositions.slice(0, 5)); // Most recent 5 positions
    }, 800);
  });
};

/**
 * Search positions
 * @param {string} searchTerm - Term to search for
 * @returns {Promise} Promise object that resolves to an array of positions
 */
export const searchPositions = (searchTerm) => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      const filteredPositions = samplePositions.filter(position => 
        position.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        position.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
      resolve(filteredPositions);
    }, 800);
  });
};

/**
 * Create a new position
 * @param {Object} positionData - Data for the new position
 * @returns {Promise} Promise object that resolves to the created position
 */
export const createPosition = (positionData) => {
  return new Promise((resolve) => {
    // Simulate API delay
    setTimeout(() => {
      // Generate a simple random ID
      const newId = Math.floor(Math.random() * 10000).toString();
      
      // Create the new position with timestamp
      const newPosition = {
        _id: newId,
        ...positionData,
        upvotes: 0,
        downvotes: 0,
        comments: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
      
      // In a real app, this would be saved to a database
      // Here we just return it
      resolve(newPosition);
    }, 1200);
  });
};

/**
 * Update an existing position
 * @param {string} id - ID of the position to update
 * @param {Object} positionData - New data for the position
 * @returns {Promise} Promise object that resolves to the updated position
 */
export const updatePosition = (id, positionData) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const positionIndex = samplePositions.findIndex(p => p._id === id);
      
      if (positionIndex !== -1) {
        // In a real app, this would update the database
        const updatedPosition = {
          ...samplePositions[positionIndex],
          ...positionData,
          updatedAt: new Date().toISOString()
        };
        
        resolve(updatedPosition);
      } else {
        reject(new Error('Position not found'));
      }
    }, 1000);
  });
};

/**
 * Delete a position
 * @param {string} id - ID of the position to delete
 * @returns {Promise} Promise object that resolves when the position is deleted
 */
export const deletePosition = (id) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const positionIndex = samplePositions.findIndex(p => p._id === id);
      
      if (positionIndex !== -1) {
        // In a real app, this would delete from the database
        resolve({ success: true, message: 'Position deleted successfully' });
      } else {
        reject(new Error('Position not found'));
      }
    }, 800);
  });
};

/**
 * Vote on a position
 * @param {string} id - ID of the position to vote on
 * @param {string} voteType - Type of vote ('up' or 'down')
 * @returns {Promise} Promise object that resolves to the updated position
 */
export const voteOnPosition = (id, voteType) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const positionIndex = samplePositions.findIndex(p => p._id === id);
      
      if (positionIndex !== -1) {
        // In a real app, this would update the database
        const updatedPosition = { ...samplePositions[positionIndex] };
        
        if (voteType === 'up') {
          updatedPosition.upvotes += 1;
        } else if (voteType === 'down') {
          updatedPosition.downvotes += 1;
        }
        
        resolve(updatedPosition);
      } else {
        reject(new Error('Position not found'));
      }
    }, 500);
  });
};

/**
 * Add a comment to a position
 * @param {string} positionId - ID of the position
 * @param {Object} commentData - Data for the new comment
 * @returns {Promise} Promise object that resolves to the updated position
 */
export const addComment = (positionId, commentData) => {
  return new Promise((resolve, reject) => {
    // Simulate API delay
    setTimeout(() => {
      const positionIndex = samplePositions.findIndex(p => p._id === positionId);
      
      if (positionIndex !== -1) {
        // Generate a simple random ID
        const newCommentId = `c${Math.floor(Math.random() * 10000)}`;
        
        // Create the new comment
        const newComment = {
          _id: newCommentId,
          ...commentData,
          createdAt: new Date().toISOString()
        };
        
        // Add comment to position
        const updatedPosition = {
          ...samplePositions[positionIndex],
          comments: [...samplePositions[positionIndex].comments, newComment],
          updatedAt: new Date().toISOString()
        };
        
        resolve(updatedPosition);
      } else {
        reject(new Error('Position not found'));
      }
    }, 800);
  });
}; 