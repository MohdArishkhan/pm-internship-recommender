import { useEffect, useState } from "react"
import { ProfileForm } from "../components/user/ProfileForm"
import { RecommendationsList } from "../components/user/RecommendationsList"
import { useProfile, saveProfile } from "../lib/api"

export default function DashboardPage() {
    const { profile: serverProfile } = useProfile()
    const [profile, setProfile] = useState(null)

    useEffect(() => {
        if (serverProfile && !profile) setProfile(serverProfile)
    }, [serverProfile, profile])

    const handleProfileChange = async (next) => {
        setProfile(next)
        try {
            await saveProfile(next)
        } catch (e) {
            // ignore transient errors for now
        }
    }

    return (
        <main className="mx-auto max-w-6xl px-6 py-10 font-sans">
            <h1 className="text-2xl font-semibold text-foreground">Your Dashboard</h1>
            <p className="mt-1 text-muted-foreground">Update your profile and get personalized internship recommendations.</p>

            <div className="mt-8 grid gap-8 md:grid-cols-2">
                <section aria-labelledby="profile-heading" className="rounded-lg border border-border p-5">
                    <h2 id="profile-heading" className="text-lg font-medium text-foreground">
                        Profile
                    </h2>
                    <ProfileForm initialValue={profile || undefined} onChange={handleProfileChange} />
                </section>

                <section aria-labelledby="recs-heading" className="rounded-lg border border-border p-5">
                    <h2 id="recs-heading" className="text-lg font-medium text-foreground">
                        Recommendations
                    </h2>
                    <RecommendationsList profile={profile || undefined} />
                </section>
            </div>
        </main>
    )
}
