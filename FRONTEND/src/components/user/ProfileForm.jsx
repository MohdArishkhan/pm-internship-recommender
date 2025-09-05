import { useEffect, useState } from "react"

export function ProfileForm({ initialValue, onChange }) {
    const [name, setName] = useState(initialValue?.name || "")
    const [email, setEmail] = useState(initialValue?.email || "")
    const [skills, setSkills] = useState((initialValue?.skills || []).join(", "))
    const [interests, setInterests] = useState((initialValue?.interests || []).join(", "))
    const [desiredLocation, setDesiredLocation] = useState(initialValue?.desiredLocation || "")
    const [sectorPreference, setSectorPreference] = useState(initialValue?.sectorPreference || "")

    useEffect(() => {
        const profile = {
            name,
            email,
            skills: splitCSV(skills),
            interests: splitCSV(interests),
            desiredLocation,
            sectorPreference,
        }
        onChange(profile)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [name, email, skills, interests, desiredLocation, sectorPreference])

    return (
        <form className="mt-4 grid gap-4" onSubmit={(e) => e.preventDefault()}>
            <div className="grid gap-1.5">
                <label htmlFor="name" className="text-sm font-medium text-foreground">
                    Name
                </label>
                <input
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full rounded-md border border-input px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="Ada Lovelace"
                    autoComplete="name"
                />
            </div>

            <div className="grid gap-1.5">
                <label htmlFor="email" className="text-sm font-medium text-foreground">
                    Email
                </label>
                <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full rounded-md border border-input px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="ada@example.com"
                    autoComplete="email"
                />
            </div>

            <div className="grid gap-1.5">
                <label htmlFor="skills" className="text-sm font-medium text-foreground">
                    Skills (comma-separated)
                </label>
                <input
                    id="skills"
                    value={skills}
                    onChange={(e) => setSkills(e.target.value)}
                    className="w-full rounded-md border border-input px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="python, sql, data analysis"
                />
            </div>

            <div className="grid gap-1.5">
                <label htmlFor="interests" className="text-sm font-medium text-foreground">
                    Interests (comma-separated)
                </label>
                <input
                    id="interests"
                    value={interests}
                    onChange={(e) => setInterests(e.target.value)}
                    className="w-full rounded-md border border-input px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="ai, healthcare, climate"
                />
            </div>

            <div className="grid gap-1.5">
                <label htmlFor="location" className="text-sm font-medium text-foreground">
                    Desired Location
                </label>
                <input
                    id="location"
                    value={desiredLocation}
                    onChange={(e) => setDesiredLocation(e.target.value)}
                    className="w-full rounded-md border border-input px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="Remote or City/Region"
                />
            </div>

            <div className="grid gap-1.5">
                <label htmlFor="sector" className="text-sm font-medium text-foreground">
                    Sector Preference
                </label>
                <select
                    id="sector"
                    value={sectorPreference}
                    onChange={(e) => setSectorPreference(e.target.value)}
                    className="w-full rounded-md border border-input bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                >
                    <option value="">Any</option>
                    <option value="Software">Software</option>
                    <option value="Data">Data</option>
                    <option value="Design">Design</option>
                    <option value="Marketing">Marketing</option>
                    <option value="Finance">Finance</option>
                    <option value="Healthcare">Healthcare</option>
                </select>
            </div>
        </form>
    )
}

function splitCSV(s) {
    return s
        .split(",")
        .map((x) => x.trim())
        .filter(Boolean)
}
