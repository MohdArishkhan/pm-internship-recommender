// import React, { useState } from "react";
// import axios from "axios";
// import "./InternshipList.css";

// const InternshipCard = ({ internship, onView }) => {
//   return (
//     <div className="card">
//       <h3>{internship.title}</h3>
//       <p><strong>Sector:</strong> {internship.sector}</p>
//       <p><strong>Location:</strong> {internship.location}</p>
//       <p><strong>Skills:</strong> {internship.skills?.join(", ")}</p>
//       <p><strong>Duration:</strong> {internship.duration}</p>
//       <p><strong>Match Score:</strong> {internship.match_score?.toFixed(2)}%</p>
//       <button onClick={() => onView(internship)}>View & Apply</button>
//     </div>
//   );
// };

// const InternshipModal = ({ internship, onClose }) => {
//   if (!internship) return null;

//   return (
//     <div className="modal-overlay">
//       <div className="modal">
//         <h2>{internship.title}</h2>
//         <p><strong>Sector:</strong> {internship.sector}</p>
//         <p><strong>Location:</strong> {internship.location}</p>
//         <p><strong>Skills:</strong> {internship.skills?.join(", ")}</p>
//         <p><strong>Duration:</strong> {internship.duration}</p>
//         <p><strong>Description:</strong> {internship.description}</p>
//         <p><strong>Match Score:</strong> {internship.match_score?.toFixed(2)}%</p>

//         <div className="modal-buttons">
//           <button onClick={onClose}>Close</button>
//           <button className="apply-btn">Apply Now</button>
//         </div>
//       </div>
//     </div>
//   );
// };

// const InternshipList = ({ formData }) => {
//   const [internships, setInternships] = useState([]);
//   const [selectedInternship, setSelectedInternship] = useState(null);
//   const [loading, setLoading] = useState(false);

//   const fetchRecommendations = async () => {
//     setLoading(true);
//     try {
//       const res = await axios.post("http://localhost:8000/api/recommendations", {
//         education: formData.education,
//         skills: formData.skills,
//         sector: formData.sector, 
//         preferred_location: formData.location,
//         description: "Candidate applying through platform" // 👈 extra bio/desc tum baad me add kr sakte ho
//       });

//       setInternships(res.data || []);
//     } catch (err) {
//       console.error("Error fetching recommendations:", err);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleView = (internship) => setSelectedInternship(internship);
//   const handleClose = () => setSelectedInternship(null);

//   return (
//     <div className="list-container">
//       <h2>Recommended Internships</h2>
//       <button onClick={fetchRecommendations}>Get Recommendations</button>

//       {loading ? (
//         <p>Loading...</p>
//       ) : internships.length === 0 ? (
//         <p>No recommendations yet. Fill form and click button above.</p>
//       ) : (
//         <div className="card-list">
//           {internships.map((internship) => (
//             <InternshipCard
//               key={internship.id}
//               internship={internship}
//               onView={handleView}
//             />
//           ))}
//         </div>
//       )}

//       <InternshipModal internship={selectedInternship} onClose={handleClose} />
//     </div>
//   );
// };

// export default InternshipList;






import React, { useState } from "react";
import "./InternshipList.css";

const InternshipCard = ({ internship, onView }) => (
  <div className="card">
    <h3>{internship.title}</h3>
    <p><strong>Sector:</strong> {internship.sector}</p>
    <p><strong>Location:</strong> {internship.location}</p>
    <p><strong>Skills:</strong> {internship.skills}</p>
    <p><strong>Duration:</strong> {internship.duration}</p>
    {/* <p><strong>Match Score:</strong> {internship.match_score?.toFixed(2)}%</p> */}
    <button onClick={() => onView(internship)}>View & Apply</button>
  </div>
);

const InternshipModal = ({ internship, onClose }) => {
  if (!internship) return null;

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>{internship.title}</h2>
        <p><strong>Sector:</strong> {internship.sector}</p>
        <p><strong>Location:</strong> {internship.location}</p>
        <p><strong>Skills:</strong> {internship.skills}</p>
        <p><strong>Duration:</strong> {internship.duration}</p>
        <p><strong>Description:</strong> {internship.description}</p>
        {/* <p><strong>Match Score:</strong> {internship.match_score?.toFixed(2)}%</p> */}

        <div className="modal-buttons">
          <button onClick={onClose}>Close</button>
          <button className="apply-btn">Apply Now</button>
        </div>
      </div>
    </div>
  );
};

const InternshipList = ({ internships = [] }) => {  // default to empty array here
  const [selectedInternship, setSelectedInternship] = useState(null);

  const handleView = (internship) => setSelectedInternship(internship);
  const handleClose = () => setSelectedInternship(null);

  // Defensive fallback: If internships is undefined or not array, set to []
  const safeInternships = Array.isArray(internships) ? internships : [];

  return (
    <div className="list-container">
      <h2>Recommended Internships</h2>

      {safeInternships.length === 0 ? (
        <p>No internships found. Try different inputs.</p>
      ) : (
        <div className="card-list">
          {safeInternships.map((internship) => (
            <InternshipCard
              key={internship.id}
              internship={internship}
              onView={handleView}
            />
          ))}
        </div>
      )}

      <InternshipModal internship={selectedInternship} onClose={handleClose} />
    </div>
  );
};

export default InternshipList;
