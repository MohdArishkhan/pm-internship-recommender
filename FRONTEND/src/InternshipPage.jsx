// InternshipPage.jsx
import React from "react";
import { useLocation } from "react-router-dom";
import InternshipList from "./InternshipList"; // adjust path as needed

const InternshipPage = () => {
  const location = useLocation();
  const internships = location.state?.internships || [];

  return <InternshipList internships={internships} />;
};

export default InternshipPage;
