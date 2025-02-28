# War Thunder Tactics

A community-driven website for War Thunder players to share, view, and vote on optimal routes, power positions, and strategies for the Realistic Battles Ground game mode.

## Features

- Interactive map system with high-resolution War Thunder battle maps
- Community-contributed tactics and strategies
- Vehicle-specific routes and power positions
- Upvoting system for the best tactics
- User accounts for contributing and saving favorite tactics

## Tech Stack

- **Frontend**: Next.js, React, TypeScript
- **Styling**: Tailwind CSS, Shadcn UI
- **State Management**: React Context API
- **Deployment**: Vercel (planned)

## Project Structure

```
war-thunder-tactics/
├── app/                  # Next.js App Router
├── components/           # React components
│   ├── home/             # Homepage-specific components
│   ├── maps/             # Map-related components
│   ├── tactics/          # Tactics-related components
│   └── ui/               # Reusable UI components
├── lib/                  # Utility functions and data
├── public/               # Static assets
│   └── assets/
│       └── maps/         # Map images
└── ...
```

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```
3. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Map Naming Convention

Map images follow this naming convention:
```
MapLayout_MODE NAME(MAP LAYOUT)_MAP NAME
```

## License

This project is not affiliated with Gaijin Entertainment. War Thunder is a trademark of Gaijin Entertainment. 