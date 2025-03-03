/**
 * CLEANUP SCRIPTS
 * 
 * This script removes unnecessary files and scripts from the project.
 * It updates the package.json file to remove references to deleted scripts.
 * 
 * NOTE: THIS SCRIPT SHOULD BE DELETED AFTER RUNNING ONCE
 * 
 * It does not delete itself, so you should manually delete it after running.
 */

const fs = require('fs');
const path = require('path');

// ANSI color codes for console output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function colorLog(message, color = 'reset') {
  console.log(colors[color] + message + colors.reset);
}

// Scripts that are one-time use or redundant
const scriptsToRemove = [
  // Asset import/copy scripts (one-time operations)
  'scripts/copy-map-assets.js',
  'scripts/check-map-assets.js',
  'scripts/import-map-assets.js',
  'scripts/replace-map-assets.js',
  
  // The cleanup script we just ran (meta-cleanup)
  'scripts/cleanup-codebase.js'
];

// Scripts to keep (don't remove these)
const scriptsToKeep = [
  'scripts/dev-watch.js',            // Main development utility
  'scripts/start-project.js',        // Important for starting the project
  'scripts/cleanup-unused-images.js', // Useful for ongoing maintenance
  'scripts/generate-placeholders-simple.js' // Used for generating placeholders
];

// Update package.json to remove scripts that reference the removed files
function updatePackageJson() {
  const packageJsonPath = path.join(process.cwd(), 'package.json');
  
  try {
    // Read the package.json file
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    
    // Scripts to remove from package.json
    const scriptsToRemoveFromJson = [
      'copy-map-assets',
      'check-map-assets',
      'import-map-assets',
      'replace-map-assets',
      'cleanup-codebase'
    ];
    
    // Remove the scripts
    let removedScripts = 0;
    scriptsToRemoveFromJson.forEach(script => {
      if (packageJson.scripts[script]) {
        delete packageJson.scripts[script];
        removedScripts++;
        colorLog(`✅ Removed '${script}' from package.json scripts`, 'green');
      }
    });
    
    // Write the updated package.json
    fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
    colorLog(`Updated package.json, removed ${removedScripts} scripts`, 'green');
  } catch (error) {
    colorLog(`❌ Error updating package.json: ${error.message}`, 'red');
  }
}

// Count of files deleted
let totalRemoved = 0;
let totalFailures = 0;

// Process scripts to remove
colorLog('Starting cleanup of scripts...', 'blue');
scriptsToRemove.forEach(file => {
  const filePath = path.join(process.cwd(), file);
  
  try {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      colorLog(`✅ Removed: ${file}`, 'green');
      totalRemoved++;
    } else {
      colorLog(`⚠️ File not found: ${file}`, 'yellow');
    }
  } catch (error) {
    colorLog(`❌ Error removing ${file}: ${error.message}`, 'red');
    totalFailures++;
  }
});

// Update package.json
colorLog('\nUpdating package.json...', 'blue');
updatePackageJson();

// Final summary
colorLog('\n=== Cleanup Summary ===', 'magenta');
colorLog(`Total scripts removed: ${totalRemoved}`, totalRemoved > 0 ? 'green' : 'yellow');
colorLog(`Failed operations: ${totalFailures}`, totalFailures > 0 ? 'red' : 'green');
colorLog('========================', 'magenta'); 