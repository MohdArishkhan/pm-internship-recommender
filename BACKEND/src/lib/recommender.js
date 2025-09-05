function scoreMatch(p, i) {
	let score = 0;
	if (
		p.desiredLocation &&
		i.location.toLowerCase().includes(p.desiredLocation.toLowerCase())
	)
		score += 3;
	if (
		p.sectorPreference &&
		i.sector.toLowerCase() === p.sectorPreference.toLowerCase()
	)
		score += 3;

	const skillSet = new Set((p.skills || []).map((s) => s.toLowerCase()));
	for (const req of i.requirements) {
		if (skillSet.has(req.toLowerCase())) score += 1;
	}

	for (const interest of p.interests || []) {
		const q = interest.toLowerCase();
		if (
			i.title.toLowerCase().includes(q) ||
			i.description.toLowerCase().includes(q)
		) {
			score += 1;
		}
	}
	return score;
}

export function getRecommendations(p, items) {
	const ranked = items
		.map((i) => ({
			...i,
			description: i.description || "",
			requirements: i.requirements || [],
			score: scoreMatch(p, {
				title: i.title,
				description: i.description || "",
				requirements: i.requirements || [],
				location: i.location,
				sector: i.sector,
			}),
		}))
		.filter((x) => x.score > 0)
		.sort((a, b) => b.score - a.score);
	return ranked;
}

export function calculateRecommendationScore(profile, internship) {
	return scoreMatch(profile, internship);
}
