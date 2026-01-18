Open index.html in a browser (double-click or use file:// path).

Recommended: upload the entire `static_site` folder to GitHub Pages, Netlify or any static host to get a public URL.

Local file URL example (Windows):
file:///C:/Users/asus/Downloads/RegenWave_Real/static_site/index.html

Files:
- index.html (welcome)
- app.html (main analyzer; client-side only)
- styles.css (styles)
- metadata.json (dataset copy)

Notes:
- Client-side app checks filename against embedded metadata and draws charts using Chart.js.
- Server-side features (server plotting, server validation logs) are not present in this static build.
