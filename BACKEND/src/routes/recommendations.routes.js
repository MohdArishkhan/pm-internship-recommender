import express from "express";
import { getRecommendationsForProfile } from "../controllers/recommendations.controller.js";

const router = express.Router();

router.post("/", getRecommendationsForProfile);

export default router;
