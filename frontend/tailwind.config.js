/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#4f46e5", // indigo-600
        accent: "#0ea5e9", // sky-500
      },
    },
  },
  plugins: [],
}