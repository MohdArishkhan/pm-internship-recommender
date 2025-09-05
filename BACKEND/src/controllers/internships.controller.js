import { prisma } from "../lib/prisma.js";

export const getInternships = async (req, res) => {
	try {
		const data = await prisma.internship.findMany({
			orderBy: { createdAt: "desc" },
		});
		res.json({ data });
	} catch (error) {
		console.error("Error fetching internships:", error);
		res.status(500).json({ error: "Internal server error" });
	}
};

export const createInternship = async (req, res) => {
	try {
		const { title, description, requirements, location, sector } = req.body;

		if (!title || !description || !location || !sector) {
			return res.status(400).json({ error: "Missing required fields" });
		}

		const reqs = Array.isArray(requirements)
			? requirements
			: (requirements || "")
					.split(/[|;,]/)
					.map((s) => s.trim())
					.filter(Boolean);

		const created = await prisma.internship.create({
			data: {
				title: title.trim(),
				description: description.trim(),
				requirements: reqs,
				location: location.trim(),
				sector: sector.trim(),
			},
		});

		res.status(201).json({ data: created });
	} catch (error) {
		console.error("Error creating internship:", error);
		res.status(500).json({ error: "Internal server error" });
	}
};

export const getInternshipById = async (req, res) => {
	const id = parseInt(req.params.id);
	if (!id || isNaN(id)) {
		return res.status(400).json({ error: "Invalid ID" });
	}

	try {
		const item = await prisma.internship.findUnique({ where: { id } });
		if (!item) {
			return res.status(404).json({ error: "Not found" });
		}
		res.json({ data: item });
	} catch (error) {
		console.error("Error fetching internship:", error);
		res.status(500).json({ error: "Internal server error" });
	}
};

export const updateInternship = async (req, res) => {
	const id = parseInt(req.params.id);
	if (!id || isNaN(id)) {
		return res.status(400).json({ error: "Invalid ID" });
	}

	try {
		const patch = req.body;

		// Validate or sanitize patch fields if necessary here
		const updated = await prisma.internship.update({
			where: { id },
			data: patch,
		});

		res.json({ data: updated });
	} catch (error) {
		if (error.code === "P2025") {
			// Prisma error code for record not found on update
			return res.status(404).json({ error: "Not found" });
		}
		console.error("Error updating internship:", error);
		res.status(400).json({ error: "Invalid JSON or update failed" });
	}
};

export const deleteInternship = async (req, res) => {
	const id = parseInt(req.params.id);
	if (!id || isNaN(id)) {
		return res.status(400).json({ error: "Invalid ID" });
	}

	try {
		await prisma.internship.delete({ where: { id } });
		res.json({ ok: true });
	} catch (error) {
		if (error.code === "P2025") {
			// Record not found
			return res.status(404).json({ error: "Not found" });
		}
		console.error("Error deleting internship:", error);
		res.status(400).json({ error: "Delete failed" });
	}
};

export const uploadInternshipsCSV = async (req, res) => {
	try {
		const csvText = req.body;

		if (!csvText || typeof csvText !== "string") {
			return res.status(400).json({ error: "Invalid CSV data" });
		}

		// Simple CSV parsing (you might want to use a proper CSV parser like papaparse)
		const lines = csvText.trim().split("\n");
		const headers = lines[0].split(",").map((h) => h.trim().toLowerCase());

		const requiredHeaders = [
			"title",
			"description",
			"requirements",
			"location",
			"sector",
		];
		const missingHeaders = requiredHeaders.filter((h) => !headers.includes(h));

		if (missingHeaders.length > 0) {
			return res.status(400).json({
				error: `Missing required headers: ${missingHeaders.join(", ")}`,
			});
		}

		let createdCount = 0;

		for (let i = 1; i < lines.length; i++) {
			const values = lines[i].split(",").map((v) => v.trim());
			const row = {};

			headers.forEach((header, index) => {
				row[header] = values[index] || "";
			});

			if (row.title && row.description && row.location && row.sector) {
				const reqs = row.requirements
					? row.requirements
							.split(/[|;]/)
							.map((s) => s.trim())
							.filter(Boolean)
					: [];

				await prisma.internship.create({
					data: {
						title: row.title,
						description: row.description,
						requirements: reqs,
						location: row.location,
						sector: row.sector,
					},
				});
				createdCount++;
			}
		}

		res.json({
			message: `Successfully uploaded ${createdCount} internships`,
			count: createdCount,
		});
	} catch (error) {
		console.error("Error uploading CSV:", error);
		res.status(500).json({ error: "Internal server error" });
	}
};
