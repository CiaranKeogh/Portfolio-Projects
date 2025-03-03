const fs = require('fs');
const path = require('path');

// Helper function for colored console output
function colorLog(message, type = 'info') {
  const colors = {
    success: '\x1b[32m', // green
    info: '\x1b[36m',    // cyan
    warning: '\x1b[33m', // yellow
    error: '\x1b[31m',   // red
    reset: '\x1b[0m'     // reset
  };
  
  console.log(`${colors[type]}${message}${colors.reset}`);
}

// Define source directory with imported maps
const SOURCE_DIR = path.join('assets', 'imported-maps');

// Define target directories
const TARGET_MAPS_DIR = path.join('public', 'images', 'maps');
const TARGET_THUMBNAILS_DIR = path.join('public', 'images', 'maps', 'thumbnails');

// Map the imported asset folders to the map names in our codebase
const mapNameMapping = {
  // Required maps from maps.ts
  'advance_to_the_rhine': { 
    targetName: 'rhine',
    displayName: 'Advance to the Rhine',
    sourceModes: ['Conquest1', 'Battle']
  },
  'sinai_desert': { // Not in our imports, will use el_alamein as replacement
    replacement: 'el_alamein',
    targetName: 'sinai',
    displayName: 'Sinai Desert',
    sourceModes: ['Conquest1', 'Battle']
  },
  'karelia': {
    targetName: 'karelia', 
    displayName: 'Karelia',
    sourceModes: ['Conquest1', 'Domination']
  },
  'maginot_line': { 
    targetName: 'maginot',
    displayName: 'Maginot Line',
    sourceModes: ['Conquest1', 'Battle']
  },
  'berlin': { 
    targetName: 'berlin',
    displayName: 'Berlin',
    sourceModes: ['Conquest1', 'Battle']
  },
  'fire_arc': { // This is used for Kursk in our codebase
    targetName: 'kursk',
    displayName: 'Kursk',
    sourceModes: ['Conquest1', 'Battle']
  },
  // Additional maps for other components
  'eastern_europe': {
    targetName: 'eastern_europe',
    displayName: 'Eastern Europe',
    sourceModes: ['Conquest1', 'Battle']
  },
  'fulda_gap': {
    targetName: 'fulda',
    displayName: 'Fulda Gap',
    sourceModes: ['Conquest1', 'Battle']
  },
  'jungle': {
    targetName: 'jungle',
    displayName: 'Jungle',
    sourceModes: ['Conquest1', 'Battle']
  },
  'stalingrad': { // Not in our imports, will use berlin as replacement
    replacement: 'berlin',
    targetName: 'stalingrad',
    displayName: 'Stalingrad',
    sourceModes: ['Conquest1', 'Battle']
  }
};

// Function to ensure a directory exists
function ensureDirectoryExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    try {
      fs.mkdirSync(dirPath, { recursive: true });
      colorLog(`Created directory: ${dirPath}`, 'success');
    } catch (error) {
      colorLog(`Failed to create directory ${dirPath}: ${error.message}`, 'error');
      return false;
    }
  }
  return true;
}

// Function to copy a file
function copyFile(source, target) {
  try {
    fs.copyFileSync(source, target);
    colorLog(`Copied: ${path.basename(source)} -> ${target}`, 'success');
    return true;
  } catch (error) {
    colorLog(`Failed to copy ${source}: ${error.message}`, 'error');
    return false;
  }
}

// Process a map folder and copy assets to the appropriate locations
function processMapFolder(sourceFolder, mapping) {
  // Handle replacements (if a map isn't available, use another one)
  const actualSourceFolder = mapping.replacement 
    ? path.join(SOURCE_DIR, mapping.replacement) 
    : path.join(SOURCE_DIR, sourceFolder);
  
  if (!fs.existsSync(actualSourceFolder)) {
    colorLog(`Source folder not found: ${actualSourceFolder}`, 'error');
    return false;
  }
  
  let successCount = 0;
  
  // Get all files in the source folder
  const files = fs.readdirSync(actualSourceFolder);
  
  // Find appropriate files for thumbnail and full image
  let thumbnailSource = null;
  let fullImageSource = null;
  
  // Try to find the specific mode files mentioned in the mapping
  mapping.sourceModes.forEach(mode => {
    const modePattern = new RegExp(`MapLayout_${mode}_`, 'i');
    const matchingFile = files.find(file => modePattern.test(file) && file.endsWith('.jpg'));
    
    if (matchingFile && !thumbnailSource) {
      thumbnailSource = path.join(actualSourceFolder, matchingFile);
    } else if (matchingFile && !fullImageSource) {
      fullImageSource = path.join(actualSourceFolder, matchingFile);
    }
  });
  
  // If we couldn't find specific modes, just use any available map layout files
  if (!thumbnailSource) {
    const anyMapFile = files.find(file => file.startsWith('MapLayout_') && file.endsWith('.jpg'));
    if (anyMapFile) {
      thumbnailSource = path.join(actualSourceFolder, anyMapFile);
    }
  }
  
  if (!fullImageSource && thumbnailSource !== null) {
    // Use the same file for both if we only found one
    fullImageSource = thumbnailSource;
  }
  
  if (!thumbnailSource) {
    colorLog(`No suitable image files found in ${actualSourceFolder}`, 'warning');
    return false;
  }
  
  // Copy thumbnail
  const thumbnailTarget = path.join(TARGET_THUMBNAILS_DIR, `${mapping.targetName}.jpg`);
  if (copyFile(thumbnailSource, thumbnailTarget)) {
    successCount++;
  }
  
  // Copy full image
  const fullImageTarget = path.join(TARGET_MAPS_DIR, `${mapping.targetName}_full.jpg`);
  if (copyFile(fullImageSource, fullImageTarget)) {
    successCount++;
  }
  
  colorLog(`Processed ${mapping.displayName}: ${successCount} files copied`, 'info');
  return successCount > 0;
}

// Function to update the maps.ts file with the new display names if needed
function updateMapsData() {
  const mapsFilePath = path.join('data', 'maps.ts');
  
  if (!fs.existsSync(mapsFilePath)) {
    colorLog(`Maps data file not found: ${mapsFilePath}`, 'warning');
    return false;
  }
  
  try {
    let mapsContent = fs.readFileSync(mapsFilePath, 'utf8');
    
    // We don't need to update the map names in this case
    // This function is here for future extensions if needed
    
    return true;
  } catch (error) {
    colorLog(`Failed to update maps data: ${error.message}`, 'error');
    return false;
  }
}

// Main function
async function main() {
  colorLog('Starting Map Assets Replacement', 'info');
  
  // Check if source directory exists
  if (!fs.existsSync(SOURCE_DIR)) {
    colorLog(`Source directory not found: ${SOURCE_DIR}`, 'error');
    return;
  }
  
  // Ensure target directories exist
  if (!ensureDirectoryExists(TARGET_MAPS_DIR) || !ensureDirectoryExists(TARGET_THUMBNAILS_DIR)) {
    return;
  }
  
  // Process each map folder
  let processedCount = 0;
  
  for (const [sourceFolder, mapping] of Object.entries(mapNameMapping)) {
    if (processMapFolder(sourceFolder, mapping)) {
      processedCount++;
    }
  }
  
  colorLog(`Replacement complete. Processed ${processedCount} out of ${Object.keys(mapNameMapping).length} maps`, 'success');
  
  // Update maps data if needed
  updateMapsData();
}

// Execute the main function
main().catch(error => {
  colorLog(`Unhandled error: ${error.message}`, 'error');
  process.exit(1);
}); 