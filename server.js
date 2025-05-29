const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8000;

// Serve static files from the root directory
app.use(express.static('.'));

// Handle specific routes for HTML files
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Route for the main village map
app.get('/map', (req, res) => {
    res.sendFile(path.join(__dirname, 'complete-1000-villages-map.html'));
});

// Route for the database-powered map
app.get('/database-map', (req, res) => {
    res.sendFile(path.join(__dirname, 'database-powered-villages-map-fixed.html'));
});

// Route for the transformation game
app.get('/game', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'visualization', 'village-transformation-game.html'));
});

// Route for project overview
app.get('/overview', (req, res) => {
    res.sendFile(path.join(__dirname, 'PROJECT-OVERVIEW.md'));
});

// Route for API to serve village data
app.get('/api/villages', (req, res) => {
    res.sendFile(path.join(__dirname, 'india-villages-map-data.json'));
});

// Route for discovery report
app.get('/api/kaithal-discovery', (req, res) => {
    res.sendFile(path.join(__dirname, 'docs', 'kaithal-pilot', 'kaithal-discovery-report.json'));
});

// Handle markdown files with proper content type
app.get('*.md', (req, res) => {
    res.type('text/plain');
    res.sendFile(path.join(__dirname, req.path));
});

// Handle JSON files with proper content type
app.get('*.json', (req, res) => {
    res.type('application/json');
    res.sendFile(path.join(__dirname, req.path));
});

// Fallback for any other routes - serve index page or 404
app.get('*', (req, res) => {
    // Try to serve the requested file directly
    const filePath = path.join(__dirname, req.path);
    res.sendFile(filePath, (err) => {
        if (err) {
            res.status(404).send(`
                <html>
                <head><title>Indian Rural Transformation Strategy</title></head>
                <body>
                    <h1>🇮🇳 Indian Rural Transformation Strategy</h1>
                    <p>File not found. Available resources:</p>
                    <ul>
                        <li><a href="/map">🗺️ Complete Village Map</a></li>
                        <li><a href="/database-map">🗄️ Database-Powered Map</a></li>
                        <li><a href="/game">🎮 Village Transformation Game</a></li>
                        <li><a href="/overview">📋 Project Overview</a></li>
                        <li><a href="/api/villages">📊 Village Data API</a></li>
                    </ul>
                    <p><a href="https://github.com/tenhundredtrees/transitions">📂 View on GitHub</a></p>
                </body>
                </html>
            `);
        }
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Indian Villages Resilience Mapping server running on port ${PORT}`);
    console.log(`🌐 Local: http://localhost:${PORT}`);
    console.log(`🗺️ Village Map: http://localhost:${PORT}/map`);
    console.log(`🎮 Transformation Game: http://localhost:${PORT}/game`);
});

module.exports = app;
