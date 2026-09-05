/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ['"Noto Serif SC"', 'serif'],
      },
      colors: {
        primary: '#8b7355',
        secondary: '#5c4a3d',
        paper: '#fdfbf7',
        ink: '#3e3a39',
        border: '#e8dcc4',
      },
    },
  },
  plugins: [],
}