/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        cassandra: '#c084fc',
        mongodb: '#4ade80',
        mysql: '#f97316',
        neo4j: '#06b6d4',
        surface: '#131c31',
        'surface-2': '#1a2744',
        border: '#1e2a45',
        muted: '#64748b',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
