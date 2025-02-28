const fs = require('fs');
const path = require('path');

// Base directory for images
const baseDir = path.join(process.cwd(), 'public', 'images');

// Ensure directories exist
function ensureDirectoryExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`Created directory: ${dirPath}`);
  }
}

// Generate a placeholder HTML file that displays information about the missing image
function generatePlaceholderHtml(filePath, width, height, label, bgColor = '#333333', textColor = '#ffffff') {
  const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Image Placeholder</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      width: ${width}px;
      height: ${height}px;
      background-color: ${bgColor};
      color: ${textColor};
      font-family: Arial, sans-serif;
      overflow: hidden;
    }
    .container {
      text-align: center;
      padding: 20px;
    }
    .label {
      font-size: ${Math.floor(width / 20)}px;
      font-weight: bold;
      margin-bottom: 10px;
    }
    .dimensions {
      font-size: ${Math.floor(width / 30)}px;
    }
    .border {
      position: absolute;
      top: 2px;
      left: 2px;
      right: 2px;
      bottom: 2px;
      border: 4px solid #555555;
      pointer-events: none;
    }
    .info {
      margin-top: 20px;
      font-size: 14px;
      opacity: 0.8;
    }
  </style>
</head>
<body>
  <div class="border"></div>
  <div class="container">
    <div class="label">${label}</div>
    <div class="dimensions">${width}x${height}</div>
    <div class="info">Replace with actual image</div>
  </div>
</body>
</html>
  `;
  
  // Create a text file with the .html extension next to where the image would be
  const htmlFilePath = filePath.replace(/\.(jpg|png)$/, '.html');
  
  ensureDirectoryExists(path.dirname(htmlFilePath));
  fs.writeFileSync(htmlFilePath, htmlContent);
  console.log(`Generated HTML placeholder: ${htmlFilePath}`);
  
  // Also create an empty file with the original name so that file checks don't fail
  fs.writeFileSync(filePath, 'PLACEHOLDER - Replace with actual image');
  console.log(`Generated empty placeholder: ${filePath}`);
}

// Generate SVG icon
function generateSvgIcon(filePath, name) {
  const svgContent = `<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <rect width="24" height="24" fill="#333333" />
    <rect x="2" y="2" width="20" height="20" fill="#444444" stroke="#666666" stroke-width="1" />
    <text x="12" y="12" font-family="Arial" font-size="5" text-anchor="middle" dominant-baseline="middle" fill="white">${name}</text>
    <text x="12" y="18" font-family="Arial" font-size="3" text-anchor="middle" dominant-baseline="middle" fill="white">24x24</text>
  </svg>`;
  
  ensureDirectoryExists(path.dirname(filePath));
  fs.writeFileSync(filePath, svgContent);
  console.log(`Generated SVG: ${filePath}`);
}

// Create Map Thumbnails
const mapThumbnails = [
  { name: 'rhine.jpg', label: 'Advance to the Rhine' },
  { name: 'sinai.jpg', label: 'Sinai Desert' },
  { name: 'karelia.jpg', label: 'Karelia' },
  { name: 'maginot.jpg', label: 'Maginot Line' },
  { name: 'berlin.jpg', label: 'Berlin' },
  { name: 'kursk.jpg', label: 'Kursk' },
  { name: 'eastern_europe.jpg', label: 'Eastern Europe' }
];

mapThumbnails.forEach(map => {
  const thumbnailPath = path.join(baseDir, 'maps', 'thumbnails', map.name);
  generatePlaceholderHtml(thumbnailPath, 800, 500, `Thumbnail: ${map.label}`, '#2b4c7d', '#ffffff');
  
  // Also create full map image
  const fullMapPath = path.join(baseDir, 'maps', map.name.replace('.jpg', '_full.jpg'));
  generatePlaceholderHtml(fullMapPath, 1600, 1000, `Full Map: ${map.label}`, '#2b4c7d', '#ffffff');
  
  // Simple map image for references
  const mapPath = path.join(baseDir, 'maps', map.name);
  generatePlaceholderHtml(mapPath, 1200, 800, `Map: ${map.label}`, '#2b4c7d', '#ffffff');
});

// Create additional maps needed for positions
const additionalMaps = [
  { name: 'stalingrad.jpg', label: 'Stalingrad' },
  { name: 'fulda.jpg', label: 'Fulda Gap' },
  { name: 'jungle.jpg', label: 'Jungle' }
];

additionalMaps.forEach(map => {
  const mapPath = path.join(baseDir, 'maps', map.name);
  generatePlaceholderHtml(mapPath, 1200, 800, `Map: ${map.label}`, '#2b4c7d', '#ffffff');
});

// Create Power Position images
const positionImages = [
  { name: 'kursk-hill-203-1.jpg', label: 'Kursk: Hill 203 (View 1)' },
  { name: 'kursk-hill-203-2.jpg', label: 'Kursk: Hill 203 (View 2)' },
  { name: 'stalingrad-factory-1.jpg', label: 'Stalingrad: Factory (View 1)' },
  { name: 'stalingrad-factory-2.jpg', label: 'Stalingrad: Factory (View 2)' },
  { name: 'fulda-ridge-1.jpg', label: 'Fulda: Ridge (View 1)' },
  { name: 'fulda-ridge-2.jpg', label: 'Fulda: Ridge (View 2)' },
  { name: 'jungle-island-1.jpg', label: 'Jungle: Island (View 1)' },
  { name: 'jungle-island-2.jpg', label: 'Jungle: Island (View 2)' },
  { name: 'sinai-ridge-1.jpg', label: 'Sinai: Ridge (View 1)' },
  { name: 'sinai-ridge-2.jpg', label: 'Sinai: Ridge (View 2)' }
];

positionImages.forEach(pos => {
  const posPath = path.join(baseDir, 'positions', pos.name);
  generatePlaceholderHtml(posPath, 600, 400, pos.label, '#4a6741', '#ffffff');
});

// Create Avatar images
const avatars = [
  { name: 'default.jpg', label: 'Default Avatar' },
  { name: 'commander1.jpg', label: 'Commander 1' },
  { name: 'commander2.jpg', label: 'Commander 2' },
  { name: 'commander3.jpg', label: 'Commander 3' },
  { name: 'commander4.jpg', label: 'Commander 4' },
  { name: 'commander5.jpg', label: 'Commander 5' },
  { name: 'user1.jpg', label: 'User 1' },
  { name: 'user2.jpg', label: 'User 2' },
  { name: 'user3.jpg', label: 'User 3' },
  { name: 'user4.jpg', label: 'User 4' },
  { name: 'user5.jpg', label: 'User 5' },
  { name: 'user6.jpg', label: 'User 6' },
  { name: 'user7.jpg', label: 'User 7' }
];

avatars.forEach(avatar => {
  const avatarPath = path.join(baseDir, 'avatars', avatar.name);
  generatePlaceholderHtml(avatarPath, 200, 200, avatar.label, '#603e1f', '#ffffff');
});

// Create Tank images
const tanks = [
  { name: 't-34.jpg', label: 'T-34' },
  { name: 'tiger.jpg', label: 'Tiger' },
  { name: 'sherman.jpg', label: 'Sherman' },
  { name: 'panther.jpg', label: 'Panther' },
  { name: 'is-2.jpg', label: 'IS-2' },
  { name: 'm26.jpg', label: 'M26 Pershing' },
  { name: 't-54.jpg', label: 'T-54' },
  { name: 'leopard.jpg', label: 'Leopard' },
  { name: 'abrams.jpg', label: 'Abrams' },
  { name: 't-90.jpg', label: 'T-90' }
];

tanks.forEach(tank => {
  const tankPath = path.join(baseDir, 'vehicles', 'tanks', tank.name);
  generatePlaceholderHtml(tankPath, 400, 300, tank.label, '#3a3a3a', '#ffffff');
});

// Create Aircraft images
const aircraft = [
  { name: 'bf-109.jpg', label: 'Bf-109' },
  { name: 'spitfire.jpg', label: 'Spitfire' },
  { name: 'p-51.jpg', label: 'P-51 Mustang' },
  { name: 'yak-9.jpg', label: 'Yak-9' },
  { name: 'fw-190.jpg', label: 'Fw-190' },
  { name: 'il-2.jpg', label: 'IL-2 Sturmovik' },
  { name: 'me-262.jpg', label: 'Me-262' },
  { name: 'mig-15.jpg', label: 'MiG-15' },
  { name: 'f-86.jpg', label: 'F-86 Sabre' },
  { name: 'f-4.jpg', label: 'F-4 Phantom' }
];

aircraft.forEach(ac => {
  const acPath = path.join(baseDir, 'vehicles', 'aircraft', ac.name);
  generatePlaceholderHtml(acPath, 400, 300, ac.label, '#3a3a3a', '#ffffff');
});

// Create Route images
const routes = [
  { name: 'eastern-europe-south-flank.jpg', label: 'Eastern Europe: South Flank' },
  { name: 'rhine-bridge-rush.jpg', label: 'Rhine: Bridge Rush' },
  { name: 'karelia-hill-bypass.jpg', label: 'Karelia: Hill Bypass' },
  { name: 'poland-village-sweep.jpg', label: 'Poland: Village Sweep' }
];

routes.forEach(route => {
  const routePath = path.join(baseDir, '../routes', route.name);
  generatePlaceholderHtml(routePath, 800, 600, route.label, '#3d5c3a', '#ffffff');
});

// Create icon directories
const iconDirs = [
  'tactics',
  'status',
  'navigation',
  'actions'
];

iconDirs.forEach(dir => {
  ensureDirectoryExists(path.join(baseDir, 'icons', dir));
});

// Create icon files
const icons = [
  // Tactics
  { dir: 'tactics', name: 'flanking.svg' },
  { dir: 'tactics', name: 'ambush.svg' },
  { dir: 'tactics', name: 'rush.svg' },
  { dir: 'tactics', name: 'defense.svg' },
  { dir: 'tactics', name: 'sniping.svg' },
  
  // Status
  { dir: 'status', name: 'success.svg' },
  { dir: 'status', name: 'warning.svg' },
  { dir: 'status', name: 'error.svg' },
  { dir: 'status', name: 'info.svg' },
  
  // Navigation
  { dir: 'navigation', name: 'home.svg' },
  { dir: 'navigation', name: 'maps.svg' },
  { dir: 'navigation', name: 'tactics.svg' },
  { dir: 'navigation', name: 'vehicles.svg' },
  { dir: 'navigation', name: 'profile.svg' },
  { dir: 'navigation', name: 'settings.svg' },
  
  // Actions
  { dir: 'actions', name: 'add.svg' },
  { dir: 'actions', name: 'edit.svg' },
  { dir: 'actions', name: 'delete.svg' },
  { dir: 'actions', name: 'save.svg' },
  { dir: 'actions', name: 'share.svg' },
  { dir: 'actions', name: 'like.svg' },
  { dir: 'actions', name: 'comment.svg' }
];

icons.forEach(icon => {
  const iconPath = path.join(baseDir, 'icons', icon.dir, icon.name);
  generateSvgIcon(iconPath, icon.name.replace('.svg', ''));
});

// Create hero background image
const heroPath = path.join(baseDir, '../maps', 'hero-map-background.jpg');
generatePlaceholderHtml(heroPath, 1920, 1080, 'Hero Background', '#1a2e42', '#ffffff');

console.log('All placeholder files have been generated successfully!'); 