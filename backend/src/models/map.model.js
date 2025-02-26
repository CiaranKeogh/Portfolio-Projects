const mongoose = require('mongoose');

const MapSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Map name is required'],
      unique: true,
      trim: true
    },
    description: {
      type: String,
      required: [true, 'Map description is required']
    },
    imageUrl: {
      type: String,
      required: [true, 'Map image URL is required']
    },
    thumbnailUrl: {
      type: String,
      required: [true, 'Map thumbnail URL is required']
    },
    dimensions: {
      width: {
        type: Number,
        required: [true, 'Map width is required']
      },
      height: {
        type: Number,
        required: [true, 'Map height is required']
      }
    },
    gameModes: [{
      type: String,
      enum: ['Domination', 'Conquest', 'Battle', 'Break'],
      required: [true, 'At least one game mode is required']
    }],
    objectives: [{
      type: {
        type: String,
        enum: ['capture', 'defend', 'spawn'],
        required: [true, 'Objective type is required']
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
      name: {
        type: String,
        required: [true, 'Objective name is required']
      },
      gameMode: {
        type: String,
        enum: ['Domination', 'Conquest', 'Battle', 'Break'],
        required: [true, 'Game mode for objective is required']
      }
    }],
    isActive: {
      type: Boolean,
      default: true
    },
    versionHistory: [{
      version: {
        type: String,
        required: [true, 'Version number is required']
      },
      changes: {
        type: String,
        required: [true, 'Description of changes is required']
      },
      releaseDate: {
        type: Date,
        default: Date.now
      }
    }]
  },
  {
    timestamps: true
  }
);

// Add index for faster search by name
MapSchema.index({ name: 'text' });

module.exports = mongoose.model('Map', MapSchema); 