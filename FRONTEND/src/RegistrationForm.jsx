import React, { useState, useEffect } from "react";
import "./Registration.css";
import { useNavigate } from "react-router-dom";
import translations from "../utility/Languages";
import sectorData from "../utility/sectors.json";
import Select from "react-select";
import axios from "axios";

// Language options must come BEFORE useState
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
    skills: [],
    location: "",
    sector: "",
  });

  const [language, setLanguage] = useState(languageOptions[0]); // ✅ declared after options

  const handleLanguageChange = (selectedOption) => {
    setLanguage(selectedOption);
    console.log("Selected language:", selectedOption.value);
  };

  const [locationOptions, setLocationOptions] = useState([]);
  const [educationOptions, setEducationOptions] = useState([]);
  const [skillsOptions, setSkillsOptions] = useState([]);
  const [sectorOptions, setSectorOptions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch Education + Location on load
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [eduRes, locRes] = await Promise.all([
          axios.get("http://localhost:8000/api/education"),
          axios.get("http://localhost:8000/api/location"),
        ]);
        setSectorOptions(sectorData.sectors || []);
        setEducationOptions(
          Array.isArray(eduRes.data) ? eduRes.data : [eduRes.data]
        );
        setLocationOptions(
          Array.isArray(locRes.data) ? locRes.data : [locRes.data]
        );
      } catch (err) {
        console.error("Error fetching initial data:", err);
      }
    };

    fetchInitialData();
  }, []);

  // Fetch skills whenever education changes
  useEffect(() => {
    if (!formData.education) return;

    const fetchSkills = async () => {
      try {
        const selectedEdu = educationOptions.find(
          (edu) => edu.description === formData.education
        );
        if (!selectedEdu) return;

        const res = await axios.get(
          `http://localhost:8000/api/skills/by-education/${selectedEdu.id}`
        );

        const mergedSkills = Array.isArray(res.data.skills)
          ? res.data.skills
          : [];
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
  }, [formData.education]);

  const t = translations[language?.value] || translations.en;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const payload = {
      education: formData.education,
      skills: formData.skills.map((skill) => skill.description),
      sector: formData.sector,
      preferred_location: formData.location,
    };

    try {
      const response = await axios.post(
        "http://localhost:8000/api/recommendations",
        payload
      );
      navigate("/internships", { state: { internships: response.data } });
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    } finally {
      setIsLoading(false);
    }
  };
		return (
			<>
				{/* Loading Spinner */}
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
								isSearchable={true}
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
												.find(
													(option) => option.label === formData.education,
												) || null
										}
										onChange={(selectedOption) => {
											setFormData((prev) => ({
												...prev,
												education: selectedOption?.label || "",
											}));
										}}
										placeholder={t.selectEducation}
										className="form-select"
										isClearable
									/>
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
												.find((option) => option.label === formData.location) ||
											null
										}
										onChange={(selectedOption) =>
											setFormData((prev) => ({
												...prev,
												location: selectedOption?.label || "",
											}))
										}
										placeholder={t.selectLocation}
										className="form-select"
										isClearable
									/>
								</div>

								{/* Sector Dropdown */}
								<div className="form-field">
									<label className="form-label">{t.sector}</label>
									<Select
										options={sectorOptions.map((sector) => ({
											value: sector,
											label: sector,
										}))}
										value={
											sectorOptions
												.map((s) => ({ value: s, label: s }))
												.find((option) => option.value === formData.sector) ||
											null
										}
										onChange={(selectedOption) =>
											setFormData((prev) => ({
												...prev,
												sector: selectedOption?.value || "",
											}))
										}
										placeholder={t.sector}
										className="form-select"
										isClearable
									/>
								</div>

								{/* Skills */}
								<div className="form-field">
									<label className="form-label">{t.skills}</label>
									<div
										style={{
											display: "flex",
											gap: "10px",
											alignItems: "center",
										}}
									>
										<Select
											options={skillsOptions.map((skill) => ({
												value: skill.id,
												label: skill.description,
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
											onChange={(selectedOption) =>
												setFormData((prev) => ({
													...prev,
													tempSkillId: selectedOption?.value || "",
												}))
											}
											placeholder={t.addYourSkills}
											className="form-select"
											isClearable
										/>

										<button
											type="button"
											onClick={() => {
												const selectedSkill = skillsOptions.find(
													(s) => s.id === formData.tempSkillId,
												);
												if (
													selectedSkill &&
													!formData.skills.some(
														(s) => s.id === selectedSkill.id,
													)
												) {
													setFormData((prev) => ({
														...prev,
														skills: [...prev.skills, selectedSkill],
														tempSkillId: "",
													}));
												}
											}}
											className="form-button"
										>
											Add
										</button>
									</div>

									{/* Selected Skills List */}
									<div
										className="selected-skills"
										style={{ marginTop: "10px" }}
									>
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
														onClick={() =>
															setFormData((prev) => ({
																...prev,
																skills: prev.skills.filter(
																	(skill) => skill.id !== s.id,
																),
															}))
														}
														style={{
															marginLeft: "5px",
															border: "none",
															background: "transparent",
															cursor: "pointer",
															color: "red",
															fontWeight: "bold",
														}}
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

								{/* Description Box */}
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
								{/* Submit Button */}
								<div onSubmit={handleSubmit}>
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
