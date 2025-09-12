import React from 'react'
import { Routes, Route } from 'react-router-dom'
import LandingPage from './LandingPage'
import FormPage from './RegistrationForm'
import InternshipPage from './InternshipPage'

function App() {
  return (
    <Routes>
      <Route path="/internships" element={<InternshipPage />}/>
      <Route path="/" element={<LandingPage />} />
      <Route path="/form" element={<FormPage />} />
    </Routes>
  )
}

export default App
