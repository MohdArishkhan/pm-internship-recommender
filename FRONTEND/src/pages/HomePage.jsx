import { Link } from "react-router-dom"

export default function HomePage() {
    return (
        <main className="font-sans">
            <section className="mx-auto max-w-3xl px-6 py-16">
                <header className="mb-10">
                    <h1 className="text-balance text-3xl font-semibold tracking-tight text-slate-900 md:text-4xl">
                        Find internships that fit your skills and interests
                    </h1>
                    <p className="mt-3 text-pretty text-slate-600">
                        A lightweight recommender that matches your profile to curated internships by location, sector, and skills.
                    </p>
                </header>

                <div className="flex flex-col gap-3 sm:flex-row">
                    <Link
                        to="/dashboard"
                        className="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        Get recommendations
                    </Link>
                    <Link
                        to="/admin"
                        className="inline-flex items-center justify-center rounded-md border border-slate-200 px-4 py-2 text-slate-700 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        Admin: manage internships
                    </Link>
                </div>
            </section>
        </main>
    )
}
