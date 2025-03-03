const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Simple colored console output implementation that doesn't rely on any packages
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

// Configuration
const watchDirectories = [
  'app',
  'components',
  'lib',
  'pages',
  'styles',
  'data',
  'public'
];

const ignorePatterns = [
  /node_modules/,
  /\.next/,
  /\.git/,
  /\.DS_Store/
];

let nextProcess = null;
let isRestarting = false;
let queueRestart = false;

// Check if any placeholders need to be generated first
function checkAndGeneratePlaceholders() {
  try {
    // Check if at least one of the directories has been created
    const imagesDir = path.join(process.cwd(), 'public', 'images');
    if (!fs.existsSync(path.join(imagesDir, 'maps')) || 
        !fs.existsSync(path.join(imagesDir, 'positions')) || 
        !fs.existsSync(path.join(imagesDir, 'avatars')) || 
        !fs.existsSync(path.join(imagesDir, 'icons'))) {
      colorLog('yellow', '⚠️ Placeholder images not detected. Generating placeholders...');
      execSync('npm run generate-placeholders', { stdio: 'inherit' });
      colorLog('green', '✅ Placeholders generated successfully.');
      
      // We're using placeholder images instead of real map assets
      // The copy-map-assets script has been disabled
    }
  } catch (error) {
    console.error(`${consoleColors.red}Error checking or generating placeholders:${consoleColors.reset}`, error);
  }
}

// Start the Next.js development server
function startDevServer() {
  colorLog('green', '🚀 Starting Next.js development server...');
  
  nextProcess = spawn('npm', ['run', 'dev'], { 
    stdio: ['ignore', 'pipe', 'pipe'],
    shell: true 
  });
  
  nextProcess.stdout.on('data', (data) => {
    const output = data.toString();
    process.stdout.write(output);
    
    // When the server is ready, show a nice message
    if (output.includes('ready') && output.includes('started server')) {
      colorLog('green', '\n✅ Development server is running!\n');
      colorLog('blue', '👀 Watching for changes in:');
      watchDirectories.forEach(dir => console.log(`   - ${dir}/`));
      console.log('\n' + `${consoleColors.yellow}Press Ctrl+C to stop the development server${consoleColors.reset}`);
    }
  });
  
  nextProcess.stderr.on('data', (data) => {
    process.stderr.write(data.toString());
  });
  
  nextProcess.on('close', (code) => {
    if (!isRestarting) {
      console.log(`\n${consoleColors.yellow}⛔ Development server has stopped with code: ${code}${consoleColors.reset}`);
      process.exit(code);
    }
  });
}

// Restart the Next.js development server
function restartDevServer() {
  if (isRestarting) {
    queueRestart = true;
    return;
  }
  
  isRestarting = true;
  colorLog('yellow', '\n🔄 Restarting development server due to changes...\n');
  
  if (nextProcess) {
    nextProcess.kill();
    
    // Wait a bit before starting the server again
    setTimeout(() => {
      startDevServer();
      isRestarting = false;
      
      // If another restart was requested while we were restarting, do it now
      if (queueRestart) {
        queueRestart = false;
        setTimeout(restartDevServer, 1000);
      }
    }, 1000);
  }
}

// Watch for file changes
function watchForChanges() {
  watchDirectories.forEach(dir => {
    const dirPath = path.join(process.cwd(), dir);
    
    if (fs.existsSync(dirPath)) {
      watchDirectory(dirPath);
    } else {
      // Create directory if it doesn't exist and then watch it
      try {
        fs.mkdirSync(dirPath, { recursive: true });
        colorLog('green', `Created directory: ${dir}/`);
        watchDirectory(dirPath);
      } catch (err) {
        console.error(`${consoleColors.red}Error creating directory ${dir}:${consoleColors.reset}`, err);
      }
    }
  });
}

// Watch a directory recursively
function watchDirectory(dirPath) {
  try {
    fs.watch(dirPath, { recursive: true }, (eventType, filename) => {
      if (!filename) return;
      
      const filePath = path.join(dirPath, filename);
      
      // Check if the file should be ignored
      if (ignorePatterns.some(pattern => pattern.test(filePath))) {
        return;
      }
      
      // Filter out some common temporary files
      if (filename.endsWith('~') || filename.startsWith('.#')) {
        return;
      }
      
      colorLog('yellow', `\n📝 Detected ${eventType} in: ${path.relative(process.cwd(), filePath)}`);
      restartDevServer();
    });
  } catch (err) {
    console.error(`${consoleColors.red}Error watching directory ${dirPath}:${consoleColors.reset}`, err);
  }
}

// Handle process termination
process.on('SIGINT', () => {
  colorLog('yellow', '\n👋 Stopping development server...');
  
  if (nextProcess) {
    nextProcess.kill();
  }
  
  process.exit(0);
});

// Main function
function main() {
  colorLog('green', '\n🔧 War Thunder Tactics Development Script\n');
  
  // Make sure we have placeholder images
  checkAndGeneratePlaceholders();
  
  // Start the development server
  startDevServer();
  
  // Watch for file changes
  watchForChanges();
}

// Run the main function
main(); 