import { getRepos } from "../lib/repository.js";
import { getRecommendations } from "../lib/recommender.js";

export const getRecommendationsForProfile = async (req, res) => {
	try {
		const p = req.body;
		const { internships } = getRepos();
		const items = await internships.list();
		const ranked = getRecommendations(p, items);
		res.json({ data: ranked });
	} catch (error) {
		console.error("Error generating recommendations:", error);
		res.status(400).json({ error: "Invalid JSON" });
	}
};
