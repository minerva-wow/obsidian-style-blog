/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/blog/**/*.html",  // 这样就能扫描到 blog 文件夹下所有的 html 文件
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}