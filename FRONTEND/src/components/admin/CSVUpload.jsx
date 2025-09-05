import React from "react"
import { uploadCSV } from "../../lib/api"

export function CsvUpload({ onBulkAdd }) {
    const parse = async (file) => {
        const text = await file.text()
        await uploadCSV(text)
    }

    const onChange = (e) => {
        const f = e.target.files?.[0]
        if (f) parse(f)
    }

    return (
        <div className="mt-4">
            <input
                type="file"
                accept=".csv,text/csv"
                onChange={onChange}
                aria-label="Upload CSV"
                className="block w-full text-sm text-foreground/90 file:mr-4 file:rounded-md file:border-0 file:bg-blue-600 file:px-4 file:py-2 file:text-white hover:file:bg-blue-700"
            />
            <p className="mt-2 text-xs text-muted-foreground">
                Expected columns: title, description, requirements, location, sector. Use commas to separate columns and delimit
                requirements with commas, semicolons, pipes, or slashes.
            </p>
        </div>
    )
}
