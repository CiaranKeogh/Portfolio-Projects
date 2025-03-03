const fs = require('fs');
const path = require('path');

// Function to ensure directory exists
function ensureDirectoryExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

// Function to create a placeholder HTML file
function createPlaceholderHtml(filePath, title, description, dimensions) {
  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} - Placeholder</title>
  <style>
    body {
      font-family: sans-serif;
      background-color: #f0f0f0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .placeholder {
      width: ${dimensions.width}px;
      height: ${dimensions.height}px;
      background-color: #333;
      color: white;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 20px;
      box-sizing: border-box;
    }
    h1 {
      margin: 0 0 20px 0;
    }
    p {
      margin: 0;
    }
  </style>
</head>
<body>
  <div class="placeholder">
    <h1>${title}</h1>
    <p>${description}</p>
    <p>${dimensions.width}x${dimensions.height}</p>
  </div>
</body>
</html>
  `;

  fs.writeFileSync(filePath, htmlContent);
  console.log(`Created placeholder HTML: ${filePath}`);
}

// Function to create an empty image file
function createEmptyImageFile(filePath) {
  // Create an empty file
  fs.writeFileSync(filePath, '');
  console.log(`Created empty image file: ${filePath}`);
}

// Maps
const mapThumbnails = [
  'rhine.jpg',
  'sinai.jpg',
  'karelia.jpg',
  'maginot.jpg',
  'berlin.jpg',
  'kursk.jpg',
  'eastern_europe.jpg',
  'fulda.jpg',
  'jungle.jpg'
];

// Add additional maps (could be different) - these are the full size versions
const additionalMapImages = [
  'rhine_full.jpg',
  'sinai_full.jpg',
  'karelia_full.jpg', 
  'maginot_full.jpg',
  'berlin_full.jpg',
  'kursk_full.jpg',
  'eastern_europe_full.jpg',
  'fulda_full.jpg',
  'jungle_full.jpg',
  'stalingrad.jpg', // Additional map not in thumbnails
  'hero-map-background.jpg' // Background for hero section
];

// Power position images
const powerPositionImages = [
  'kursk-hill-203-1.jpg',
  'kursk-hill-203-2.jpg',
  'stalingrad-factory-1.jpg',
  'stalingrad-factory-2.jpg',
  'fulda-ridge-1.jpg',
  'fulda-ridge-2.jpg',
  'jungle-island-1.jpg',
  'jungle-island-2.jpg',
  'sinai-ridge-1.jpg',
  'sinai-ridge-2.jpg'
];

// Avatar images
const avatarImages = [
  'default.jpg',
  'commander1.jpg',
  'commander2.jpg',
  'commander3.jpg',
  'commander4.jpg',
  'commander5.jpg',
  'user1.jpg',
  'user2.jpg',
  'user3.jpg',
  'user4.jpg',
  'user5.jpg',
  'user6.jpg',
  'user7.jpg'
];

// Tank images
const tankImages = [
  't-34.jpg',
  'tiger.jpg',
  'sherman.jpg',
  'is-2.jpg',
  'panther.jpg',
  'm26.jpg',
  'leopard.jpg',
  'abrams.jpg',
  't-54.jpg',
  't-90.jpg'
];

// Aircraft images
const aircraftImages = [
  'bf-109.jpg',
  'spitfire.jpg',
  'p-51.jpg',
  'fw-190.jpg',
  'il-2.jpg',
  'yak-9.jpg',
  'me-262.jpg',
  'f-86.jpg',
  'mig-15.jpg',
  'f-4.jpg'
];

// Route images
const routeImages = [
  'rhine-bridge-rush.jpg',
  'eastern-europe-south-flank.jpg',
  'karelia-hill-bypass.jpg',
  'poland-village-sweep.jpg'
];

// Icon files in SVG format
const iconFiles = {
  tactics: ['ambush.svg', 'defense.svg', 'flanking.svg', 'rush.svg', 'sniping.svg'],
  status: ['error.svg', 'info.svg', 'success.svg', 'warning.svg'],
  navigation: ['home.svg', 'maps.svg', 'profile.svg', 'settings.svg', 'tactics.svg', 'vehicles.svg'],
  actions: ['add.svg', 'comment.svg', 'delete.svg', 'edit.svg', 'like.svg', 'save.svg', 'share.svg']
};

// Generate image placeholders
function generateImagePlaceholders() {
  // Map thumbnails
  const thumbnailsDir = path.join('public', 'images', 'maps', 'thumbnails');
  ensureDirectoryExists(thumbnailsDir);
  
  mapThumbnails.forEach(filename => {
    const htmlPath = path.join(thumbnailsDir, `${path.basename(filename, path.extname(filename))}.html`);
    const imagePath = path.join(thumbnailsDir, filename);
    
    createPlaceholderHtml(
      htmlPath,
      `Map Thumbnail: ${filename}`,
      'Replace with actual map thumbnail',
      { width: 800, height: 500 }
    );
    
    createEmptyImageFile(imagePath);
  });
  
  // Map images
  const mapsDir = path.join('public', 'images', 'maps');
  ensureDirectoryExists(mapsDir);
  
  additionalMapImages.forEach(filename => {
    const htmlPath = path.join(mapsDir, `${path.basename(filename, path.extname(filename))}.html`);
    const imagePath = path.join(mapsDir, filename);
    
    createPlaceholderHtml(
      htmlPath,
      `Map Image: ${filename}`,
      'Replace with actual map image',
      { width: 1200, height: 800 }
    );
    
    createEmptyImageFile(imagePath);
  });
  
  // Power position images
  const positionsDir = path.join('public', 'images', 'positions');
  ensureDirectoryExists(positionsDir);
  
  powerPositionImages.forEach(filename => {
    const htmlPath = path.join(positionsDir, `${path.basename(filename, path.extname(filename))}.html`);
    const imagePath = path.join(positionsDir, filename);
    
    createPlaceholderHtml(
      htmlPath,
      `Position Image: ${filename}`,
      'Replace with actual position screenshot',
      { width: 1000, height: 750 }
    );
    
    createEmptyImageFile(imagePath);
  });
  
  // Avatar images
  const avatarsDir = path.join('public', 'images', 'avatars');
  ensureDirectoryExists(avatarsDir);
  
  avatarImages.forEach(filename => {
    const htmlPath = path.join(avatarsDir, `${path.basename(filename, path.extname(filename))}.html`);
    const imagePath = path.join(avatarsDir, filename);
    
    createPlaceholderHtml(
      htmlPath,
      `Avatar: ${filename}`,
      'Replace with actual avatar image',
      { width: 200, height: 200 }
    );
    
    createEmptyImageFile(imagePath);
  });
  
  // Tank images
  const tanksDir = path.join('public', 'images', 'vehicles', 'tanks');
  ensureDirectoryExists(tanksDir);
  
  tankImages.forEach(filename => {
    const htmlPath = path.join(tanksDir, `${path.basename(filename, path.extname(filename))}.html`);
    const imagePath = path.join(tanksDir, filename);
    
    createPlaceholderHtml(
      htmlPath,
      `Tank: ${filename}`,
      'Replace with actual tank image',
      { width: 400, height: 300 }
    );
    
    createEmptyImageFile(imagePath);
  });
  
  // Aircraft images
  const aircraftDir = path.join('public', 'images', 'vehicles', 'aircraft');
  ensureDirectoryExists(aircraftDir);
  
  aircraftImages.forEach(filename => {
    const htmlPath = path.join(aircraftDir, `${path.basename(filename, path.extname(filename))}.html`);
    const imagePath = path.join(aircraftDir, filename);
    
    createPlaceholderHtml(
      htmlPath,
      `Aircraft: ${filename}`,
      'Replace with actual aircraft image',
      { width: 400, height: 300 }
    );
    
    createEmptyImageFile(imagePath);
  });
  
  // Route images
  const routesDir = path.join('public', 'routes');
  ensureDirectoryExists(routesDir);
  
  routeImages.forEach(filename => {
    const htmlPath = path.join(routesDir, `${path.basename(filename, path.extname(filename))}.html`);
    const imagePath = path.join(routesDir, filename);
    
    createPlaceholderHtml(
      htmlPath,
      `Route: ${filename}`,
      'Replace with actual route image',
      { width: 1200, height: 800 }
    );
    
    createEmptyImageFile(imagePath);
  });
  
  // Icons
  for (const [category, icons] of Object.entries(iconFiles)) {
    const iconsDir = path.join('public', 'images', 'icons', category);
    ensureDirectoryExists(iconsDir);
    
    icons.forEach(filename => {
      const filePath = path.join(iconsDir, filename);
      
      // Simple SVG placeholder
      const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
        <rect width="24" height="24" fill="#ccc" />
        <text x="12" y="12" font-family="sans-serif" font-size="8" text-anchor="middle" alignment-baseline="middle" fill="#333">
          ${filename}
        </text>
      </svg>`;
      
      fs.writeFileSync(filePath, svgContent);
      console.log(`Created placeholder SVG: ${filePath}`);
    });
  }
  
  console.log('All placeholder images have been generated successfully.');
}

// Execute the function to generate placeholders
generateImagePlaceholders(); 