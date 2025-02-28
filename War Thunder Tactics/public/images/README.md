# Image Assets Directory

This directory contains all image assets for the War Thunder Tactics application.

## Directory Structure

- `/maps/` - Map background images
  - `/thumbnails/` - Smaller thumbnail versions of maps for listings
- `/positions/` - Strategic position images for each map
- `/avatars/` - User and commander profile avatars
- `/vehicles/` - Vehicle images
  - `/tanks/` - Tank images
  - `/aircraft/` - Aircraft images
- `/icons/` - UI icons
  - `/tactics/` - Tactical approach icons
  - `/status/` - Status indicator icons
  - `/navigation/` - Navigation menu icons
  - `/actions/` - Action button icons

## Image Guidelines

### File Formats
- Use `.jpg` for photographs and complex images with many colors
- Use `.png` for images that require transparency
- Use `.svg` for icons and graphics that need to scale

### Dimensions
- Map thumbnails: 800x500px
- Position images: 600x400px
- Avatars: 200x200px (square)
- Vehicle images: 400x300px
- Icons: 24x24px (SVG preferred)

### Naming Conventions
- Use lowercase letters
- Use hyphens instead of spaces
- Be descriptive but concise
- Include map name for position images (e.g., `kursk-hill-203-1.jpg`)

### Optimization
- Compress all images appropriately before adding to the repository
- Keep file sizes under 200KB for better performance
- Consider using WebP format for production

## Placeholder Files

Placeholder text files are included in each directory to indicate what images are needed. Replace these with actual images before deployment. 