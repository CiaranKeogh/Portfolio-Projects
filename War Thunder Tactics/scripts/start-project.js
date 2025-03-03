const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// Simple colored console output implementation
const consoleColors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m'
};

function colorLog(color, text) {
  console.log(`${consoleColors[color]}${text}${consoleColors.reset}`);
}

// Function to check if placeholder images are generated
function checkPlaceholders() {
  const imagesDir = path.join(process.cwd(), 'public', 'images');
  return fs.existsSync(path.join(imagesDir, 'maps')) && 
         fs.existsSync(path.join(imagesDir, 'positions')) && 
         fs.existsSync(path.join(imagesDir, 'avatars')) && 
         fs.existsSync(path.join(imagesDir, 'icons'));
}

// Main function to start the project
function startProject() {
  // Display welcome message
  colorLog('magenta', '\n========================================================');
  colorLog('magenta', '    WAR THUNDER TACTICS - PROJECT STARTUP SCRIPT');
  colorLog('magenta', '========================================================\n');
  
  // Step 1: Check and generate placeholders if needed
  colorLog('cyan', '📁 Checking placeholder images...');
  if (!checkPlaceholders()) {
    colorLog('yellow', '⚠️ Placeholder images not detected. Generating...');
    try {
      execSync('npm run generate-placeholders', { stdio: 'inherit' });
      colorLog('green', '✅ Placeholders generated successfully.\n');
    } catch (error) {
      colorLog('red', '❌ Error generating placeholders!');
      console.error(error);
      process.exit(1);
    }
  } else {
    colorLog('green', '✅ Placeholder images already exist.\n');
  }
  
  // Step 2: Start the development server
  colorLog('cyan', '🚀 Starting the development server...');
  colorLog('blue', 'The server will start in a moment. You can access the application at:');
  colorLog('green', '👉 http://localhost:3000\n');
  
  // Show additional instructions
  colorLog('yellow', 'ℹ️ Instructions:');
  colorLog('yellow', '  - Press Ctrl+C to stop the server');
  colorLog('yellow', '  - The application uses placeholder images');
  colorLog('yellow', '  - Any changes to the code will automatically refresh the browser\n');
  
  // Start the Next.js development server
  const nextProcess = spawn('npx', ['next', 'dev'], { 
    stdio: 'inherit',
    shell: true
  });
  
  // Handle process termination
  nextProcess.on('close', (code) => {
    if (code !== 0) {
      colorLog('red', `\n❌ Next.js development server exited with code ${code}`);
    } else {
      colorLog('green', '\n✅ Next.js development server shut down successfully');
    }
  });
  
  // Handle SIGINT (Ctrl+C)
  process.on('SIGINT', () => {
    colorLog('yellow', '\n🛑 Stopping the development server...');
    nextProcess.kill('SIGINT');
    setTimeout(() => {
      process.exit(0);
    }, 1000);
  });
}

// Run the main function
startProject(); 