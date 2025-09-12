import React, { useState, useEffect } from "react";
import "./Registration.css";
import { useNavigate } from "react-router-dom";
import translations from "../utility/Languages";
import Select from "react-select";
import axios from "axios";

const languageOptions = [
	{ value: "en", label: "English" },
	{ value: "hi", label: "हिन्दी (Hindi)" },
	{ value: "bn", label: "বাংলা (Bengali)" },
	{ value: "ta", label: "தமிழ் (Tamil)" },
	{ value: "te", label: "తెలుగు (Telugu)" },
	{ value: "mr", label: "मराठी (Marathi)" },
	{ value: "gu", label: "ગુજરાતી (Gujarati)" },
	{ value: "kn", label: "ಕನ್ನಡ (Kannada)" },
	{ value: "ml", label: "മലയാളം (Malayalam)" },
	{ value: "or", label: "ଓଡ଼ିଆ (Odia)" },
	{ value: "pa", label: "ਪੰਜਾਬੀ (Punjabi)" },
	{ value: "as", label: "অসমীয়া (Assamese)" },
	{ value: "ur", label: "اردو (Urdu)" },
	{ value: "ks", label: "کٲشُر (Kashmiri)" },
	{ value: "sd", label: "سنڌي (Sindhi)" },
	{ value: "sa", label: "संस्कृत (Sanskrit)" },
	{ value: "ne", label: "नेपाली (Nepali)" },
	{ value: "kok", label: "कोंकणी (Konkani)" },
	{ value: "mai", label: "मैथिली (Maithili)" },
	{ value: "mni", label: "ꯃꯤꯇꯩ ꯂꯣꯟ (Manipuri/Meitei)" },
	{ value: "doi", label: "डोगरी (Dogri)" },
	{ value: "bho", label: "भोजपुरी (Bhojpuri)" },
	{ value: "sant", label: "ᱥᱟᱱᱛᱟᱲᱤ (Santali)" },
];

const RegistrationForm = () => {
	const navigate = useNavigate();

	const [formData, setFormData] = useState({
		education: "",
		sector: "",
		skills: [],
		location: "",
	});

	const [language, setLanguage] = useState(languageOptions[0]);

	const [locationOptions, setLocationOptions] = useState([]);
	const [educationOptions, setEducationOptions] = useState([]);
	const [sectorOptions, setSectorOptions] = useState([]);
	const [skillsOptions, setSkillsOptions] = useState([]);
	const [isLoading, setIsLoading] = useState(false);

	const handleLanguageChange = (selectedOption) => {
		setLanguage(selectedOption);
		console.log("Selected language:", selectedOption.value);
	};

	// Initial education + location fetch
	useEffect(() => {
		const fetchInitialData = async () => {
			try {
				const [eduRes, locRes] = await Promise.all([
					axios.get("http://localhost:8000/api/education"),
					axios.get("http://localhost:8000/api/location"),
				]);
				setEducationOptions(
					Array.isArray(eduRes.data) ? eduRes.data : [eduRes.data],
				);
				setLocationOptions(
					Array.isArray(locRes.data) ? locRes.data : [locRes.data],
				);
			} catch (err) {
				console.error("Error fetching initial data:", err);
			}
		};

		fetchInitialData();
	}, []);

	// Fetch sectors when education changes
	useEffect(() => {
		if (!formData.education) return;

		const fetchSectors = async () => {
			try {
				const selectedEdu = educationOptions.find(
					(edu) => edu.description === formData.education,
				);
				if (!selectedEdu) return;

				const res = await axios.get(
					`http://localhost:8000/api/sectors/by-education/${selectedEdu.id}`,
				);

				setSectorOptions(
					Array.isArray(res.data.sectors) ? res.data.sectors : [],
				);
				setFormData((prev) => ({ ...prev, sector: "", skills: [] })); // reset sector & skills
			} catch (err) {
				console.error("Error fetching sectors:", err);
			}
		};

		fetchSectors();
	}, [formData.education]);

	// Fetch skills when sector changes
	useEffect(() => {
		if (!formData.sector) return;

		const fetchSkills = async () => {
			try {
				const selectedSector = sectorOptions.find(
					(sec) => sec.description === formData.sector,
				);
				if (!selectedSector) return;

				const res = await axios.get(
					`http://localhost:8000/api/skills/by-sector/${selectedSector.id}`,
				);

				const mergedSkills = Array.isArray(res.data.skills)
					? res.data.skills
					: [];

				// Clean comma separated descriptions
				const individualSkills = [];
				mergedSkills.forEach((skillObj) => {
					skillObj.description.split(",").forEach((skill) => {
						const trimmedSkill = skill.trim();
						if (
							trimmedSkill &&
							!individualSkills.some((s) => s.description === trimmedSkill)
						) {
							individualSkills.push({
								id: `${skillObj.id}-${trimmedSkill}`,
								description: trimmedSkill,
							});
						}
					});
				});

				setSkillsOptions(individualSkills);
				setFormData((prev) => ({ ...prev, skills: [], tempSkillId: "" }));
			} catch (err) {
				console.error("Error fetching skills:", err);
			}
		};

		fetchSkills();
	}, [formData.sector]);

	const t = translations[language?.value] || translations.en;

	const handleSubmit = async (e) => {
		e.preventDefault();
		setIsLoading(true);

		const payload = {
			education: formData.education,
			sector: formData.sector,
			skills: formData.skills.map((s) => s.description),
			preferred_location: formData.location,
		};

		try {
			const response = await axios.post(
				"http://localhost:8000/api/recommendations",
				payload,
			);
			navigate("/internships", { state: { internships: response.data } });
		} catch (err) {
			console.error("Error fetching recommendations:", err);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<>
			{isLoading && (
				<div className="loading-overlay">
					<div className="spinner" />
					<p className="loading-text">
						Fetching best internships according to your data...
					</p>
				</div>
			)}

			<div className="main-box">
				<div className="form-wrapper">
					{/* Language selector */}
					<div className="language-selector">
						<Select
							options={languageOptions}
							value={language}
							onChange={handleLanguageChange}
							placeholder="Select Language"
							isSearchable
						/>
					</div>

					<div className="form-card">
						<h2 className="form-title">{t.title}</h2>
						<form onSubmit={handleSubmit}>
							{/* Education */}
							<div className="form-field">
								<label className="form-label">{t.education}</label>
								<Select
									options={educationOptions.map((edu) => ({
										value: edu.id,
										label: edu.description,
									}))}
									value={
										educationOptions
											.map((edu) => ({
												value: edu.id,
												label: edu.description,
											}))
											.find((o) => o.label === formData.education) || null
									}
									onChange={(opt) =>
										setFormData((prev) => ({
											...prev,
											education: opt?.label || "",
										}))
									}
									placeholder={t.selectEducation}
									className="form-select"
									isClearable
								/>
							</div>

							{/* Sector */}
							<div className="form-field">
								<label className="form-label">{t.sector}</label>
								<Select
									options={sectorOptions.map((sec) => ({
										value: sec.id,
										label: sec.description,
									}))}
									value={
										sectorOptions
											.map((sec) => ({
												value: sec.id,
												label: sec.description,
											}))
											.find((o) => o.label === formData.sector) || null
									}
									onChange={(opt) =>
										setFormData((prev) => ({
											...prev,
											sector: opt?.label || "",
										}))
									}
									placeholder={t.selectSector}
									className="form-select"
									isClearable
								/>
							</div>

							{/* Skills */}
							<div className="form-field">
								<label className="form-label">{t.skills}</label>
								<div
									style={{ display: "flex", gap: "10px", alignItems: "center" }}
								>
									<Select
										options={skillsOptions.map((s) => ({
											value: s.id,
											label: s.description,
										}))}
										value={
											formData.tempSkillId
												? skillsOptions
														.map((s) => ({
															value: s.id,
															label: s.description,
														}))
														.find(
															(s) =>
																String(s.value) ===
																String(formData.tempSkillId),
														)
												: null
										}
										onChange={(opt) =>
											setFormData((prev) => ({
												...prev,
												tempSkillId: opt?.value || "",
											}))
										}
										placeholder={t.addYourSkills}
										className="form-select"
										isClearable
									/>

									<button
										type="button"
										className="form-button"
										onClick={() => {
											const selectedSkill = skillsOptions.find(
												(s) => s.id === formData.tempSkillId,
											);
											if (
												selectedSkill &&
												!formData.skills.some((s) => s.id === selectedSkill.id)
											) {
												setFormData((prev) => ({
													...prev,
													skills: [...prev.skills, selectedSkill],
													tempSkillId: "",
												}));
											}
										}}
									>
										Add
									</button>
								</div>

								{/* Selected skills */}
								<div className="selected-skills" style={{ marginTop: "10px" }}>
									{formData.skills.length > 0 ? (
										formData.skills.map((s) => (
											<span
												key={s.id}
												style={{
													display: "inline-block",
													padding: "5px 10px",
													margin: "5px",
													background: "#f0f0f0",
													borderRadius: "15px",
												}}
											>
												{s.description}
												<button
													type="button"
													style={{
														marginLeft: "5px",
														border: "none",
														background: "transparent",
														cursor: "pointer",
														color: "red",
														fontWeight: "bold",
													}}
													onClick={() =>
														setFormData((prev) => ({
															...prev,
															skills: prev.skills.filter(
																(sk) => sk.id !== s.id,
															),
														}))
													}
												>
													❌
												</button>
											</span>
										))
									) : (
										<p style={{ color: "#888" }}>{t.noSkillsAdded}</p>
									)}
								</div>
							</div>

							{/* Location */}
							<div className="form-field">
								<label className="form-label">{t.location}</label>
								<Select
									options={locationOptions.map((loc) => ({
										value: loc.id,
										label: loc.description,
									}))}
									value={
										locationOptions
											.map((loc) => ({
												value: loc.id,
												label: loc.description,
											}))
											.find((o) => o.label === formData.location) || null
									}
									onChange={(opt) =>
										setFormData((prev) => ({
											...prev,
											location: opt?.label || "",
										}))
									}
									placeholder={t.selectLocation}
									className="form-select"
									isClearable
								/>
							</div>

							{/* Description */}
							<div className="form-field">
								<label className="form-label">{t.descriptionLabel}</label>
								<textarea
									className="form-textarea"
									rows="4"
									value={formData.description || ""}
									onChange={(e) =>
										setFormData((prev) => ({
											...prev,
											description: e.target.value,
										}))
									}
									placeholder={t.descriptionPlaceholder}
								/>
							</div>

							<div>
								<button type="submit" className="form-button2">
									{t.submit}
								</button>
							</div>
						</form>
					</div>
				</div>
			</div>
		</>
	);
};

export default RegistrationForm;
