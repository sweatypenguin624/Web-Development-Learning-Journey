import express from "express";
import cors from "cors";
import { nanoid } from "nanoid";

const app = express();
const PORT = 5002;

app.use(express.json());
app.use(cors()); // Allow requests from any device

const urlMap = new Map(); // In-memory storage for shortened URLs

// Endpoint to shorten a URL
app.post("/shorten", (req, res) => {
    try {
        const { url } = req.body;
        if (!url) {
            console.error("Error: URL is required");
            return res.status(400).json({ error: "URL is required" });
        }

        const shortId = nanoid(6);
        urlMap.set(shortId, url);

        const shortUrl = `http://192.168.38.135:${PORT}/${shortId}`;
        console.log(`Shortened URL: ${shortUrl}`);

        res.json({ shortUrl });
    } catch (error) {
        console.error("Error processing request:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

// Redirect shortened URL to original URL
app.get("/:shortId", (req, res) => {
    try {
        const originalUrl = urlMap.get(req.params.shortId);
        if (originalUrl) {
            console.log(`Redirecting ${req.params.shortId} to ${originalUrl}`);
            res.redirect(originalUrl);
        } else {
            console.error(`Error: URL not found for ${req.params.shortId}`);
            res.status(404).json({ error: "URL not found" });
        }
    } catch (error) {
        console.error("Error handling redirect:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

// Start server on all network interfaces
app.listen(PORT, "0.0.0.0", () => {
    console.log(`🚀 Server running on http://192.168.38.135:${PORT}`);
});
