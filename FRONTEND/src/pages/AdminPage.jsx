import { useInternships, deleteInternship, createInternship } from "../lib/api"
import { InternshipForm } from "../components/admin/InternshipForm"
import { CsvUpload } from "../components/admin/CSVUpload"

export default function AdminPage() {
    const { internships, mutate } = useInternships()

    const remove = async (id) => {
        await deleteInternship(id)
        mutate()
    }

    const handleCreate = async (payload) => {
        await createInternship(payload)
        mutate()
    }

    return (
        <main className="mx-auto max-w-6xl px-6 py-10 font-sans">
            <header className="mb-6">
                <h1 className="text-2xl font-semibold text-foreground">Admin</h1>
                <p className="text-muted-foreground">Add internships manually or upload via CSV.</p>
            </header>

            <div className="grid gap-6 md:grid-cols-2">
                <div className="rounded-lg border border-border p-5">
                    <h2 className="text-lg font-medium text-foreground">Add New Internship</h2>
                    <InternshipForm onCreate={handleCreate} />
                </div>
                <div className="rounded-lg border border-border p-5">
                    <h2 className="text-lg font-medium text-foreground">Bulk Upload (CSV)</h2>
                    <CsvUpload />
                </div>
            </div>

            <section className="mt-8">
                <h2 className="text-lg font-medium text-foreground">Current Internships</h2>
                <ul className="mt-4 divide-y divide-border rounded-lg border border-border">
                    {internships.map((i) => (
                        <li key={i.id} className="flex items-start justify-between gap-4 p-4">
                            <div>
                                <h3 className="font-medium text-foreground">{i.title}</h3>
                                <p className="text-sm text-muted-foreground">
                                    {i.location} • {i.sector}
                                </p>
                                <p className="mt-1 text-sm text-foreground/90">{i.description}</p>
                                <div className="mt-2 flex flex-wrap gap-2">
                                    {i.requirements.map((r) => (
                                        <span key={r} className="rounded-md bg-muted px-2 py-1 text-xs text-foreground/80">
                                            {r}
                                        </span>
                                    ))}
                                </div>
                            </div>
                            <button
                                onClick={() => remove(i.id)}
                                className="rounded-md border border-border px-3 py-1 text-sm text-foreground/90 hover:bg-muted"
                                aria-label={`Remove ${i.title}`}
                            >
                                Remove
                            </button>
                        </li>
                    ))}
                    {internships.length === 0 && <li className="p-4 text-sm text-muted-foreground">No internships yet.</li>}
                </ul>
            </section>
        </main>
    )
}
