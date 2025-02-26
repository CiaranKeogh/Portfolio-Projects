const mongoose = require('mongoose');

const RouteSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: [true, 'Route title is required'],
      trim: true,
      maxlength: [100, 'Title cannot exceed 100 characters']
    },
    description: {
      type: String,
      required: [true, 'Route description is required'],
      maxlength: [500, 'Description cannot exceed 500 characters']
    },
    map: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Map',
      required: [true, 'Map reference is required']
    },
    creator: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'Creator reference is required']
    },
    gameMode: {
      type: String,
      enum: ['Domination', 'Conquest', 'Battle', 'Break'],
      required: [true, 'Game mode is required']
    },
    vehicleType: {
      type: String,
      enum: ['Light Tank', 'Medium Tank', 'Heavy Tank', 'Tank Destroyer', 'SPAA', 'Any'],
      required: [true, 'Vehicle type is required']
    },
    vehicleSpecifications: {
      nation: {
        type: String,
        enum: ['USA', 'Germany', 'USSR', 'Britain', 'Japan', 'China', 'Italy', 'France', 'Sweden', 'Israel', 'Any'],
        default: 'Any'
      },
      battleRating: {
        type: String,
        default: 'Any'
      },
      specificVehicle: {
        type: String,
        default: ''
      }
    },
    // A route is a series of waypoints
    waypoints: [{
      position: {
        x: {
          type: Number,
          required: [true, 'X coordinate is required']
        },
        y: {
          type: Number,
          required: [true, 'Y coordinate is required']
        }
      },
      order: {
        type: Number,
        required: [true, 'Waypoint order is required']
      },
      timestamp: {
        type: String,
        enum: ['Early-game', 'Mid-game', 'Late-game'],
        required: [true, 'Timestamp is required']
      },
      notes: {
        type: String,
        maxlength: [200, 'Notes cannot exceed 200 characters']
      }
    }],
    // Voting and metrics
    upvotes: {
      type: Number,
      default: 0
    },
    downvotes: {
      type: Number,
      default: 0
    },
    votedBy: [{
      user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
      },
      vote: {
        type: String,
        enum: ['up', 'down']
      }
    }],
    views: {
      type: Number,
      default: 0
    },
    tags: [{
      type: String,
      trim: true
    }],
    isActive: {
      type: Boolean,
      default: true
    }
  },
  {
    timestamps: true
  }
);

// Add index for faster search
RouteSchema.index({ title: 'text', description: 'text', tags: 'text' });

module.exports = mongoose.model('Route', RouteSchema); 