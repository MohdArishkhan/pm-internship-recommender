import { getRepos } from "../lib/repository.js";

export const getProfile = async (req, res) => {
	try {
		const { profile } = getRepos();
		const data = await profile.get();
		res.json({ data });
	} catch (error) {
		console.error("Error fetching profile:", error);
		res.status(500).json({ error: "Internal server error" });
	}
};

export const updateProfile = async (req, res) => {
	try {
		const body = req.body;
		if (!body.name || !body.email) {
			return res.status(400).json({ error: "name and email are required" });
		}

		const cleaned = {
			name: body.name.trim(),
			email: body.email.trim(),
			skills: (body.skills || []).map((s) => s.trim()).filter(Boolean),
			interests: (body.interests || []).map((s) => s.trim()).filter(Boolean),
			desiredLocation: body.desiredLocation?.trim() || "",
			sectorPreference: body.sectorPreference?.trim() || "",
		};

		const { profile } = getRepos();
		const data = await profile.upsert(cleaned);
		res.json({ data });
	} catch (error) {
		console.error("Error updating profile:", error);
		res.status(400).json({ error: "Invalid JSON" });
	}
};
