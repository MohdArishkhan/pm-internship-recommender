import useSWR, { mutate } from "swr";

const fetcher = async (input, init) => {
	const res = await fetch(input, {
		...init,
		headers: {
			"content-type": "application/json",
			...(init?.headers || {}),
		},
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({}));
		throw new Error(err.error || `Request failed: ${res.status}`);
	}
	return res.json();
};

// Auth
export function useAuthCheck() {
	const { data, error, isLoading } = useSWR("/api/v1/auth/check", fetcher);
	return { authStatus: data || null, error, isLoading };
}

export function useCurrentUser() {
	const { data, error, isLoading } = useSWR("/api/v1/auth/me", fetcher);
	return { user: data?.data || null, error, isLoading };
}

export function useUserProfile() {
	const { data, error, isLoading } = useSWR("/api/v1/auth/profile", fetcher);
	return { userProfile: data?.data || null, error, isLoading };
}

export async function updateUserProfile(profileData) {
	await fetcher("/api/v1/auth/profile", {
		method: "PUT",
		body: JSON.stringify(profileData),
	});
	await mutate("/api/v1/auth/profile");
}

// Internships
export function useInternships() {
	const { data, error, isLoading, mutate } = useSWR(
		"/api/internships",
		fetcher,
	);
	return {
		internships: data?.data || [],
		error,
		isLoading,
		mutate,
	};
}

export function useInternship(id) {
	const { data, error, isLoading } = useSWR(
		id ? `/api/internships/${id}` : null,
		fetcher,
	);
	return { internship: data?.data || null, error, isLoading };
}

export async function createInternship(payload) {
	await fetcher("/api/internships", {
		method: "POST",
		body: JSON.stringify(payload),
	});
	await mutate("/api/internships");
}

export async function updateInternship(id, payload) {
	await fetcher(`/api/internships/${id}`, {
		method: "PATCH",
		body: JSON.stringify(payload),
	});
	await mutate("/api/internships");
	await mutate(`/api/internships/${id}`);
}

export async function deleteInternship(id) {
	await fetcher(`/api/internships/${id}`, { method: "DELETE" });
	await mutate("/api/internships");
}

export async function uploadCSV(text) {
	const res = await fetch("/api/internships/upload", {
		method: "POST",
		headers: { "content-type": "text/csv" },
		body: text,
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({}));
		throw new Error(err.error || "Upload failed");
	}
	await mutate("/api/internships");
}

// Profile
export function useProfile() {
	const { data, error, isLoading } = useSWR("/api/profile", fetcher);
	return { profile: data?.data || null, error, isLoading };
}

export async function saveProfile(profileData) {
	await fetcher("/api/profile", {
		method: "PUT",
		body: JSON.stringify(profileData),
	});
	await mutate("/api/profile");
}

// Recommendations
export function useRecommendations(profileData) {
	const key = profileData ? ["/api/recommendations", profileData] : null;
	const { data, error, isLoading } = useSWR(key, ([url, body]) =>
		fetcher(url, { method: "POST", body: JSON.stringify(body) }),
	);
	return { recommendations: data?.data || [], error, isLoading };
}

// Stats
export function useStats() {
	const { data, error, isLoading } = useSWR("/api/stats", fetcher);
	return { stats: data?.data || null, error, isLoading };
}
