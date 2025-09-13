import React from 'react'
import { Routes, Route } from 'react-router-dom'
import HomePage from './HomePage'
import FormPage from './RegistrationForm'
import InternshipPage from './InternshipPage'

function App() {
  return (
    <Routes>
      <Route path="/internships" element={<InternshipPage />}/>
      <Route path="/" element={<HomePage />} />
      <Route path="/form" element={<FormPage />} />
    </Routes>
  )
}

export default App
