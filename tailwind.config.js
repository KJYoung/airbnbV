/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html", "./templates/**/*.html"],
  theme: {
    extend: {
      spacing: {
        "25vh" : "25vh",
        "50vh" : "50vh",
        "75vh" : "75vh",
      },
      borderRadius: {
        "vxl" : "1.5rem"
      }
    },
  },
  plugins: [],
}
