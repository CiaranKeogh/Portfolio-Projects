const mongoose = require('mongoose');

const PositionSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: [true, 'Position title is required'],
      trim: true,
      maxlength: [100, 'Title cannot exceed 100 characters']
    },
    description: {
      type: String,
      required: [true, 'Position description is required'],
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
    type: {
      type: String,
      enum: ['Sniping Spot', 'Cover Position', 'Ambush Point', 'Capping Position', 'Artillery Position', 'Other'],
      required: [true, 'Position type is required']
    },
    gameMode: {
      type: String,
      enum: ['Domination', 'Conquest', 'Battle', 'Break', 'Any'],
      required: [true, 'Game mode is required']
    },
    // Effectiveness ratings for different vehicle types
    effectiveness: {
      lightTank: {
        type: Number,
        min: 0,
        max: 10,
        default: 5
      },
      mediumTank: {
        type: Number,
        min: 0,
        max: 10,
        default: 5
      },
      heavyTank: {
        type: Number,
        min: 0,
        max: 10,
        default: 5
      },
      tankDestroyer: {
        type: Number,
        min: 0,
        max: 10,
        default: 5
      },
      spaa: {
        type: Number,
        min: 0,
        max: 10,
        default: 5
      }
    },
    // Line of sight information
    lineOfSight: {
      range: {
        type: Number, // in meters
        required: [true, 'Range is required']
      },
      coverage: {
        type: Number, // percentage of map visible
        min: 0,
        max: 100,
        required: [true, 'Coverage percentage is required']
      },
      coveragePoints: [{
        x: {
          type: Number,
          required: [true, 'X coordinate is required']
        },
        y: {
          type: Number,
          required: [true, 'Y coordinate is required']
        }
      }], // Polygon of visible area
    },
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
PositionSchema.index({ title: 'text', description: 'text', tags: 'text' });

module.exports = mongoose.model('Position', PositionSchema); 