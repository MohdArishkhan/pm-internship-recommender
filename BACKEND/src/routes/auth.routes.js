import { requireAuth } from "@clerk/express";
import { Router } from "express";
import {
	getCurrentUser,
	getUserProfile,
	updateUserProfile,
	checkAuth,
} from "../controllers/auth.controllers.js";

const authRoutes = Router();

// Public route to check auth status
authRoutes.get("/check", checkAuth);

// Protected routes
authRoutes.get("/me", requireAuth, getCurrentUser);
authRoutes.get("/profile", requireAuth, getUserProfile);
authRoutes.put("/profile", requireAuth, updateUserProfile);

// Legacy protected route (keeping for compatibility)
authRoutes.get("/protected", requireAuth, getCurrentUser);

export default authRoutes;
