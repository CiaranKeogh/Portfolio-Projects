/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'olive-drab': '#4A5D23',     // Primary color
        'gunmetal': '#2A3439',       // Secondary color
        'burnt-orange': '#CC5500',   // Accent color
        'off-white': '#E8ECEF',      // Neutral base
        'deep-blue': '#1A3C5A',      // Support color
      },
    },
  },
  plugins: [],
} 