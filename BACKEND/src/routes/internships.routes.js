import express from "express";
import {
	getInternships,
	createInternship,
	getInternshipById,
	updateInternship,
	deleteInternship,
	uploadInternshipsCSV,
} from "../controllers/internships.controller.js";

const router = express.Router();

router.get("/", getInternships);
router.post("/", createInternship);
router.get("/:id", getInternshipById);
router.patch("/:id", updateInternship);
router.delete("/:id", deleteInternship);
router.post("/upload", express.text(), uploadInternshipsCSV);

export default router;
