const fs = require('fs');
const path = require('path');

// Simple colored console output implementation
const consoleColors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  blue: '\x1b[34m'
};

function colorLog(color, text) {
  console.log(`${consoleColors[color]}${text}${consoleColors.reset}`);
}

// Function to check if a file is an image file
function isImageFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return ext === '.jpg' || ext === '.jpeg' || ext === '.png' || ext === '.gif' || ext === '.svg';
}

// Function to recursively find image files in a directory
function findImageFiles(dir, fileList = []) {
  if (!fs.existsSync(dir)) {
    return fileList;
  }

  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    
    if (fs.statSync(filePath).isDirectory()) {
      // Skip node_modules and .next directories
      if (file !== 'node_modules' && file !== '.next') {
        findImageFiles(filePath, fileList);
      }
    } else if (isImageFile(filePath)) {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

// Main function
function main() {
  colorLog('green', '\n🔍 Checking for Map Assets in the Project\n');
  
  const projectRoot = process.cwd();
  const imageFiles = findImageFiles(projectRoot);
  
  if (imageFiles.length === 0) {
    colorLog('yellow', 'No image files found in the project.');
    process.exit(0);
  }
  
  colorLog('green', `Found ${imageFiles.length} image files in the project:\n`);
  
  // Group files by directory
  const filesByDir = {};
  
  imageFiles.forEach(file => {
    const relativePath = path.relative(projectRoot, file);
    const dir = path.dirname(relativePath);
    
    if (!filesByDir[dir]) {
      filesByDir[dir] = [];
    }
    
    filesByDir[dir].push(path.basename(file));
  });
  
  // Print files grouped by directory
  Object.keys(filesByDir).sort().forEach(dir => {
    colorLog('blue', `📁 ${dir}:`);
    filesByDir[dir].sort().forEach(file => {
      console.log(`   - ${file}`);
    });
    console.log();
  });
}

// Run the main function
main(); 