/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html", // Flask Jinja templates
        "./static/js/**/*.js",   // JS files in static
        "./static/css/**/*.css", // CSS files in static
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'), // For better form styling 
    ],
}