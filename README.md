
# PM Internship Recommender

A web application to help students find and apply for product management internships. This project is divided into two main parts: a React-based frontend and a Node.js backend.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

## Features
- Internship recommendations based on user profile
- User-friendly interface
- Fast and modern web experience

## Tech Stack
- **Frontend:** React, Vite
- **Backend:** Node.js, Express

## Project Structure
```
pm-internship-recommender/
├── BACKEND/         # Node.js backend
│   ├── Index.js
│   └── package.json
├── FRONTEND/        # React frontend (Vite)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
└── README.md        # Project documentation
```

## Getting Started

### Prerequisites
- Node.js (v16 or above recommended)
- npm (comes with Node.js)

### 1. Fork & Clone
1. Click the "Fork" button on GitHub to create your own copy.
2. Clone your fork:
	```sh
	git clone https://github.com/<your-username>/pm-internship-recommender.git
	cd pm-internship-recommender
	```

### 2. Install Dependencies
#### Backend
```sh
cd BACKEND
npm install
```
#### Frontend
```sh
cd ../FRONTEND
npm install
```

### 3. Run the Project
#### Start Backend
```sh
cd BACKEND
node Index.js
```
#### Start Frontend
```sh
cd ../FRONTEND
npm run dev
```

### 4. Open in Browser
Visit `http://localhost:5173` to view the frontend.

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Make your changes
4. Commit and push (`git commit -m "Add feature"`)
5. Open a Pull Request

## License
This project is licensed under the MIT License.

---
Feel free to open issues or pull requests for improvements!
