import { prisma } from "../lib/prisma.js";

// GET /api/stats
export const getStats = async (req, res) => {
	try {
		const items = await prisma.internship.findMany({
			orderBy: { createdAt: "desc" },
		});

		const bySector = {};
		const byLocation = {};

		for (const i of items) {
			bySector[i.sector] = (bySector[i.sector] || 0) + 1;
			byLocation[i.location] = (byLocation[i.location] || 0) + 1;
		}

		res.json({ data: { bySector, byLocation, total: items.length } });
	} catch (error) {
		console.error("Error fetching stats:", error);
		res.status(500).json({ error: "Internal server error" });
	}
};
