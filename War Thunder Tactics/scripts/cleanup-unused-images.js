const fs = require('fs');
const path = require('path');

// Color logging helper
function colorLog(color, message) {
  const colors = {
    reset: "\x1b[0m",
    red: "\x1b[31m",
    green: "\x1b[32m",
    yellow: "\x1b[33m",
    blue: "\x1b[34m",
    magenta: "\x1b[35m",
    cyan: "\x1b[36m",
  };
  
  console.log(colors[color] + message + colors.reset);
}

// Get the list of referenced map images from data files
function getReferencedMapImages() {
  const referencedImages = new Set();
  
  try {
    // Check maps.ts
    const mapsData = fs.readFileSync(path.join(__dirname, '../data/maps.ts'), 'utf8');
    const mapsMatches = mapsData.match(/\/images\/maps\/[^"'\s]+/g) || [];
    mapsMatches.forEach(match => referencedImages.add(match.replace('/images/maps/', '')));

    // Check positions.ts
    const positionsData = fs.readFileSync(path.join(__dirname, '../data/positions.ts'), 'utf8');
    const positionsMatches = positionsData.match(/\/images\/maps\/[^"'\s]+/g) || [];
    positionsMatches.forEach(match => referencedImages.add(match.replace('/images/maps/', '')));

    // Check routes.ts
    const routesData = fs.readFileSync(path.join(__dirname, '../data/routes.ts'), 'utf8');
    const routesMatches = routesData.match(/\/images\/maps\/[^"'\s]+/g) || [];
    routesMatches.forEach(match => referencedImages.add(match.replace('/images/maps/', '')));

    // Check any other potential references
    // For example, in components files if needed
    
  } catch (error) {
    colorLog('red', `Error reading data files: ${error.message}`);
  }
  
  return referencedImages;
}

// Main function to clean up unused images
function cleanupUnusedImages() {
  const mapsDir = path.join(__dirname, '../public/images/maps');
  const thumbnailsDir = path.join(mapsDir, 'thumbnails');
  const referencedImages = getReferencedMapImages();
  
  colorLog('cyan', '=== Cleaning up unused map images ===');
  colorLog('yellow', 'Referenced images found in code:');
  console.log(Array.from(referencedImages).join(', '));
  
  // Process main maps directory
  try {
    const mainDirFiles = fs.readdirSync(mapsDir).filter(file => {
      const filePath = path.join(mapsDir, file);
      return fs.statSync(filePath).isFile(); // Only include files, not directories
    });
    
    colorLog('yellow', '\nChecking main maps directory:');
    let removedCount = 0;
    
    mainDirFiles.forEach(file => {
      // Skip HTML placeholder files
      if (file.endsWith('.html')) return;
      
      // Skip empty files (they're placeholders)
      const filePath = path.join(mapsDir, file);
      const stats = fs.statSync(filePath);
      if (stats.size === 0) return;
      
      // Check if file is referenced
      const fileIsReferenced = Array.from(referencedImages).some(ref => file === ref);
      
      // Special case for files like hero-map-background.jpg that aren't directly referenced
      const isSpecialFile = file === 'hero-map-background.jpg';
      
      if (!fileIsReferenced && !isSpecialFile) {
        // This file is not referenced and not a special case, so we should remove it
        try {
          colorLog('red', `Removing unused file: ${file}`);
          fs.unlinkSync(filePath);
          removedCount++;
        } catch (error) {
          colorLog('red', `Error removing file ${file}: ${error.message}`);
        }
      } else if (!fileIsReferenced && isSpecialFile) {
        colorLog('yellow', `Keeping special file: ${file}`);
      } else {
        colorLog('green', `Keeping referenced file: ${file}`);
      }
    });
    
    if (removedCount === 0) {
      colorLog('green', 'No unused files found in main maps directory.');
    } else {
      colorLog('green', `Removed ${removedCount} unused files from main maps directory.`);
    }
    
    // Handle malformed filenames (like stalingrad.jpgl)
    mainDirFiles.forEach(file => {
      if (file.match(/\.[a-z]+l$/i)) { // Files ending with something like .jpgl
        const filePath = path.join(mapsDir, file);
        try {
          colorLog('red', `Removing malformed filename: ${file}`);
          fs.unlinkSync(filePath);
        } catch (error) {
          colorLog('red', `Error removing file ${file}: ${error.message}`);
        }
      }
    });
    
  } catch (error) {
    colorLog('red', `Error processing main maps directory: ${error.message}`);
  }
  
  // Process thumbnails directory
  try {
    if (fs.existsSync(thumbnailsDir)) {
      const thumbnailFiles = fs.readdirSync(thumbnailsDir);
      
      colorLog('yellow', '\nChecking thumbnails directory:');
      let removedThumbCount = 0;
      
      thumbnailFiles.forEach(file => {
        // Skip HTML placeholder files and placeholder.txt
        if (file.endsWith('.html') || file === 'placeholder.txt') return;
        
        // Skip empty files (they're placeholders)
        const filePath = path.join(thumbnailsDir, file);
        const stats = fs.statSync(filePath);
        if (stats.size === 0) return;
        
        // Check if file is referenced
        const thumbName = 'thumbnails/' + file;
        const fileIsReferenced = Array.from(referencedImages).some(ref => thumbName === ref);
        
        if (!fileIsReferenced) {
          try {
            colorLog('red', `Removing unused thumbnail: ${file}`);
            fs.unlinkSync(filePath);
            removedThumbCount++;
          } catch (error) {
            colorLog('red', `Error removing thumbnail ${file}: ${error.message}`);
          }
        } else {
          colorLog('green', `Keeping referenced thumbnail: ${file}`);
        }
      });
      
      if (removedThumbCount === 0) {
        colorLog('green', 'No unused files found in thumbnails directory.');
      } else {
        colorLog('green', `Removed ${removedThumbCount} unused files from thumbnails directory.`);
      }
    }
  } catch (error) {
    colorLog('red', `Error processing thumbnails directory: ${error.message}`);
  }
  
  colorLog('cyan', '\n=== Cleanup complete ===');
}

// Run the cleanup
cleanupUnusedImages(); 