import express from "express";
import "dotenv/config";
import cors from "cors";
import { clerkMiddleware } from "@clerk/express";

import authRouter from "./routes/auth.routes.js";
import internshipsRouter from "./routes/internships.routes.js";
import profileRouter from "./routes/profile.routes.js";
import recommendationsRouter from "./routes/recommendations.routes.js";
import statsRouter from "./routes/stats.routes.js";

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(clerkMiddleware());

app.use(
	cors({
		origin: "http://localhost:5173",
	}),
);

// Health check route
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

app.use("/api/v1/auth", authRouter);
app.use("/api/internships", internshipsRouter);
app.use("/api/profile", profileRouter);
app.use("/api/recommendations", recommendationsRouter);
app.use("/api/stats", statsRouter);

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
	console.log(`Server is running on port ${PORT}`);
});
