import React, { useState } from "react"
import { createInternship } from "../../lib/api"

export function InternshipForm({ onCreate }) {
    const [title, setTitle] = useState("")
    const [description, setDescription] = useState("")
    const [requirements, setRequirements] = useState("")
    const [location, setLocation] = useState("")
    const [sector, setSector] = useState("")

    const submit = async (e) => {
        e.preventDefault()
        if (!title || !description) return

        const payload = {
            title,
            description,
            requirements: splitCSV(requirements),
            location,
            sector: sector || "Software",
        }

        if (onCreate) await onCreate(payload)
        else await createInternship(payload)

        setTitle("")
        setDescription("")
        setRequirements("")
        setLocation("")
        setSector("")
    }

    return (
        <form className="mt-4 grid gap-3" onSubmit={submit}>
            <L label="Title">
                <input
                    className={input}
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Frontend Intern"
                />
            </L>
            <L label="Description">
                <textarea
                    className={input}
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="What you'll do..."
                    rows={4}
                />
            </L>
            <L label="Requirements (comma-separated)">
                <input
                    className={input}
                    value={requirements}
                    onChange={(e) => setRequirements(e.target.value)}
                    placeholder="react, typescript, css"
                />
            </L>
            <div className="grid gap-3 md:grid-cols-2">
                <L label="Location">
                    <input
                        className={input}
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                        placeholder="Remote / City"
                    />
                </L>
                <L label="Sector">
                    <select className={input} value={sector} onChange={(e) => setSector(e.target.value)}>
                        <option value="">Select</option>
                        <option value="Software">Software</option>
                        <option value="Data">Data</option>
                        <option value="Design">Design</option>
                        <option value="Marketing">Marketing</option>
                        <option value="Finance">Finance</option>
                        <option value="Healthcare">Healthcare</option>
                    </select>
                </L>
            </div>

            <div>
                <button className="mt-2 inline-flex items-center rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-primary">
                    Add Internship
                </button>
            </div>
        </form>
    )
}

function L({ label, children }) {
    return (
        <label className="grid gap-1.5">
            <span className="text-sm font-medium text-foreground">{label}</span>
            {children}
        </label>
    )
}

const input =
    "w-full rounded-md border border-input px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-primary"

function splitCSV(s) {
    return s
        .split(",")
        .map((x) => x.trim())
        .filter(Boolean)
}
