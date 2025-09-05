import { useRecommendations } from "../../lib/api"

export function RecommendationsList({ profile }) {
    const { recommendations, isLoading, error } = useRecommendations(profile)

    if (!profile) {
        return (
            <div className="mt-4 rounded-md bg-muted p-4 text-sm text-foreground/80">
                Add your profile details to see recommendations.
            </div>
        )
    }

    if (isLoading) return <p className="mt-4 text-sm text-muted-foreground">Loading recommendations…</p>
    if (error) return <p className="mt-4 text-sm text-destructive">Failed to load recommendations.</p>
    if (recommendations.length === 0) {
        return <p className="mt-4 text-sm text-muted-foreground">No matches found. Try broadening your filters.</p>
    }

    return (
        <ul className="mt-4 grid gap-4">
            {recommendations.slice(0, 8).map((rec) => (
                <li key={rec.id} className="rounded-lg border border-border p-4">
                    <div className="flex items-start justify-between gap-4">
                        <div>
                            <h3 className="text-base font-semibold text-foreground">{rec.title}</h3>
                            <p className="text-sm text-muted-foreground">
                                {rec.location} • {rec.sector}
                            </p>
                        </div>
                        <span
                            className="rounded-md bg-green-100 px-2 py-1 text-xs font-medium text-green-700"
                            aria-label={`Match score ${rec.score}`}
                        >
                            Match {rec.score}
                        </span>
                    </div>
                    <p className="mt-2 text-sm text-foreground/90">{rec.description}</p>
                    <div className="mt-3 flex flex-wrap gap-2">
                        {rec.requirements.map((r) => (
                            <span key={r} className="rounded-md bg-muted px-2 py-1 text-xs text-foreground/80">
                                {r}
                            </span>
                        ))}
                    </div>
                </li>
            ))}
        </ul>
    )
}
