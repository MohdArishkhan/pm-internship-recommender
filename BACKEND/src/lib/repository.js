import { getPrisma } from "./prisma.js";

// Type definitions as comments for JavaScript
// Internship = {
//   id: string
//   title: string
//   description?: string
//   requirements: string[]
//   location: string
//   sector: string
//   createdAt?: string
//   updatedAt?: string
// }

// UserProfile = {
//   id?: string
//   name: string
//   email: string
//   skills: string[]
//   interests: string[]
//   desiredLocation?: string
//   sectorPreference?: string
//   updatedAt?: string
// }

// Interface: InternshipRepo {
//   list(): Promise<Internship[]>
//   create(data: Omit<Internship, "id" | "createdAt" | "updatedAt">): Promise<Internship>
// }

// Interface: ProfileRepo {
//   get(): Promise<UserProfile | null>
//   upsert(p: Omit<UserProfile, "id" | "updatedAt">): Promise<UserProfile>
// }

// ------- In-memory fallback (no envs required) -------
const memInternships = [];
let memProfile = null;

function uid() {
	return Math.random().toString(36).slice(2, 10);
}

const MemoryInternshipRepo = {
	async list() {
		return memInternships;
	},
	async create(data) {
		const now = new Date().toISOString();
		const item = { id: uid(), createdAt: now, updatedAt: now, ...data };
		memInternships.unshift(item);
		return item;
	},
};

const MemoryProfileRepo = {
	async get() {
		return memProfile;
	},
	async upsert(p) {
		const now = new Date().toISOString();
		if (!memProfile) {
			memProfile = { id: "me", updatedAt: now, ...p };
		} else {
			memProfile = { ...memProfile, ...p, updatedAt: now };
		}
		return memProfile;
	},
};

// ------- Prisma-backed repos (enabled when DATABASE_URL exists) -------
const PrismaInternshipRepo = {
	async list() {
		const prisma = await getPrisma();
		const rows = await prisma.internship.findMany({
			orderBy: { createdAt: "desc" },
		});
		return rows.map((r) => ({
			id: r.id,
			title: r.title,
			description: r.description ?? undefined,
			requirements: r.requirements ?? [],
			location: r.location,
			sector: r.sector,
			createdAt: r.createdAt?.toISOString?.() ?? undefined,
			updatedAt: r.updatedAt?.toISOString?.() ?? undefined,
		}));
	},
	async create(data) {
		const prisma = await getPrisma();
		const r = await prisma.internship.create({
			data: {
				title: data.title,
				description: data.description ?? null,
				requirements: data.requirements ?? [],
				location: data.location,
				sector: data.sector,
			},
		});
		return {
			id: r.id,
			title: r.title,
			description: r.description ?? undefined,
			requirements: r.requirements ?? [],
			location: r.location,
			sector: r.sector,
			createdAt: r.createdAt?.toISOString?.(),
			updatedAt: r.updatedAt?.toISOString?.(),
		};
	},
};

const PrismaProfileRepo = {
	async get() {
		const prisma = await getPrisma();
		const r = await prisma.userProfile.findFirst();
		if (!r) return null;
		return {
			id: r.id,
			name: r.name,
			email: r.email,
			skills: r.skills ?? [],
			interests: r.interests ?? [],
			desiredLocation: r.desiredLocation ?? undefined,
			sectorPreference: r.sectorPreference ?? undefined,
			updatedAt: r.updatedAt?.toISOString?.(),
		};
	},
	async upsert(p) {
		const prisma = await getPrisma();
		const existing = await prisma.userProfile.findFirst();
		const r = existing
			? await prisma.userProfile.update({
					where: { id: existing.id },
					data: {
						name: p.name,
						email: p.email,
						skills: p.skills ?? [],
						interests: p.interests ?? [],
						desiredLocation: p.desiredLocation ?? null,
						sectorPreference: p.sectorPreference ?? null,
					},
				})
			: await prisma.userProfile.create({
					data: {
						name: p.name,
						email: p.email,
						skills: p.skills ?? [],
						interests: p.interests ?? [],
						desiredLocation: p.desiredLocation ?? null,
						sectorPreference: p.sectorPreference ?? null,
					},
				});
		return {
			id: r.id,
			name: r.name,
			email: r.email,
			skills: r.skills ?? [],
			interests: r.interests ?? [],
			desiredLocation: r.desiredLocation ?? undefined,
			sectorPreference: r.sectorPreference ?? undefined,
			updatedAt: r.updatedAt?.toISOString?.(),
		};
	},
};

// ------- Public factory -------
export function getRepos() {
	const usePrisma = Boolean(process.env.DATABASE_URL);
	if (usePrisma) {
		return { internships: PrismaInternshipRepo, profile: PrismaProfileRepo };
	}
	return { internships: MemoryInternshipRepo, profile: MemoryProfileRepo };
}
