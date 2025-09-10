from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
import random

def create_sample_data():
    # Create sample data for testing
    db = SessionLocal()
    
    try:
        # Education data
        educations = [
            "10th Pass", "12th Pass", "Diploma", "Bachelor's", "Master's", "PhD",
            "Computer Science Engineering", "Information Technology", "Electronics and Communication",
            "Mechanical Engineering", "Civil Engineering", "Electrical Engineering",
            "Business Administration", "Commerce", "Arts", "Science"
        ]
        for e in educations:
            db.add(models.Education(description=e))
        db.commit()

        # Skills data
        skills = [
            "Python, Django, FastAPI", "JavaScript, React, Node.js", "Java, Spring Boot, Hibernate",
            "SQL, PostgreSQL, MongoDB", "Machine Learning, TensorFlow, PyTorch", "Data Science, Pandas, NumPy",
            "Digital Marketing, SEO, SEM", "Agile, Scrum, Project Management", "UI/UX Design, Figma, Adobe XD",
            "Content Writing, Copywriting", "Sales, CRM, Lead Generation", "Finance, Accounting, Excel",
            "HR, Recruitment, Employee Relations", "Mobile Development, React Native, Flutter",
            "DevOps, AWS, Docker, Kubernetes", "Cybersecurity, Ethical Hacking", "Cloud Computing, Azure, GCP",
            "Graphic Design, Photoshop, Illustrator", "Video Editing, Premiere Pro, After Effects",
            "Research, Data Collection, Analysis", "Social Media Marketing", "Customer Service, Communication",
            "C++, System Programming", "Go, Microservices", "Ruby, Rails", "PHP, Laravel",
            "Angular, TypeScript", "Vue.js, Frontend Development", "Swift, iOS Development",
            "Kotlin, Android Development", "Unity, Game Development", "Blockchain, Solidity",
            "AI/ML, Computer Vision", "NLP, Text Processing", "Big Data, Spark, Hadoop",
            "Quality Assurance, Testing", "Product Management", "Business Intelligence, Tableau",
            "Network Security, Penetration Testing", "Database Administration", "Technical Writing"
        ]
        for s in skills:
            db.add(models.Skill(description=s))
        db.commit()

        # Locations data
        locations = [
            ("Delhi", "Delhi"), ("Mumbai", "Maharashtra"), ("Bangalore", "Karnataka"),
            ("Chennai", "Tamil Nadu"), ("Hyderabad", "Telangana"), ("Pune", "Maharashtra"),
            ("Kolkata", "West Bengal"), ("Ahmedabad", "Gujarat"), ("Jaipur", "Rajasthan"),
            ("Lucknow", "Uttar Pradesh"), ("Remote", "Remote")
        ]
        for l in locations:
            db.add(models.Location(description=l[0], state=l[1]))
        db.commit()

        # ----------- INTERNSHIP TEMPLATES (More Diverse) -----------
        internship_templates = [
            {
                "titles": ["Software Developer Intern", "Backend Developer Intern", "Full Stack Developer Intern"],
                "descriptions": [
                    "Work on backend APIs and scalable applications.",
                    "Build end-to-end features with modern frameworks.",
                    "Contribute to microservices and database design."
                ],
                "sector": "Technology",
                "skill_ids": [1, 2, 3, 23, 25, 27],  # Python, JS, Java, C++, Go, Angular
                "education_ids": [7, 8, 4],  # CS, IT, Bachelors
                "durations": ["3 months", "6 months"]
            },
            {
                "titles": ["Data Scientist Intern", "ML Engineer Intern", "Data Analyst Intern"],
                "descriptions": [
                    "Build machine learning models for real-world problems.",
                    "Analyze large datasets to extract business insights.",
                    "Work with AI/ML pipelines and data visualization."
                ],
                "sector": "Data Science",
                "skill_ids": [5, 6, 4, 32, 33, 36],  # ML, Data Science, SQL, AI/ML, NLP, BI
                "education_ids": [4, 5, 16, 7, 8],  # Bachelor, Master, Science, CS, IT
                "durations": ["4 months", "6 months"]
            },
            {
                "titles": ["Frontend Developer Intern", "React Developer Intern", "UI Developer Intern"],
                "descriptions": [
                    "Create responsive and interactive user interfaces.",
                    "Work with modern frontend frameworks and libraries.",
                    "Collaborate with designers to implement pixel-perfect UIs."
                ],
                "sector": "Frontend Development",
                "skill_ids": [2, 27, 28],  # JavaScript, Angular, Vue.js
                "education_ids": [7, 8, 4, 3],
                "durations": ["3 months", "4 months"]
            },
            {
                "titles": ["Mobile App Developer Intern", "iOS Developer Intern", "Android Developer Intern"],
                "descriptions": [
                    "Develop native mobile applications for iOS and Android.",
                    "Work with cross-platform frameworks like React Native.",
                    "Implement mobile-first user experiences."
                ],
                "sector": "Mobile Development",
                "skill_ids": [14, 29, 30],  # Mobile Dev, Swift, Kotlin
                "education_ids": [7, 8, 4],
                "durations": ["4 months", "6 months"]
            },
            {
                "titles": ["DevOps Intern", "Cloud Engineer Intern", "Infrastructure Intern"],
                "descriptions": [
                    "Work with CI/CD pipelines and cloud infrastructure.",
                    "Manage containerized applications with Docker and Kubernetes.",
                    "Support scalable cloud deployments on AWS/Azure."
                ],
                "sector": "DevOps",
                "skill_ids": [15, 17, 37],  # DevOps, Cloud, Network Security
                "education_ids": [7, 8, 4],
                "durations": ["4 months", "6 months"]
            },
            {
                "titles": ["Digital Marketing Intern", "SEO Specialist Intern", "Social Media Intern"],
                "descriptions": [
                    "Run digital campaigns across Google and social platforms.",
                    "Optimize websites for SEO and analyze marketing metrics.",
                    "Create engaging content for social media platforms."
                ],
                "sector": "Marketing",
                "skill_ids": [7, 21, 22],  # Digital Marketing, Social Media, Customer Service
                "education_ids": [13, 14, 15, 4],
                "durations": ["2 months", "3 months"]
            },
            {
                "titles": ["UI/UX Design Intern", "Graphic Design Intern", "Product Design Intern"],
                "descriptions": [
                    "Design user interfaces for web and mobile applications.",
                    "Create branding, illustrations, and creative visuals.",
                    "Conduct user research and usability testing."
                ],
                "sector": "Design",
                "skill_ids": [9, 18],  # UI/UX, Graphic Design
                "education_ids": [15, 4, 3],
                "durations": ["3 months", "4 months"]
            },
            {
                "titles": ["Cybersecurity Intern", "Security Analyst Intern", "Penetration Tester Intern"],
                "descriptions": [
                    "Analyze security vulnerabilities and implement fixes.",
                    "Conduct penetration testing and security assessments.",
                    "Work with security tools and incident response."
                ],
                "sector": "Cybersecurity",
                "skill_ids": [16, 37],  # Cybersecurity, Network Security
                "education_ids": [7, 8, 4],
                "durations": ["4 months", "6 months"]
            },
            {
                "titles": ["Game Developer Intern", "Unity Developer Intern"],
                "descriptions": [
                    "Develop 2D and 3D games using Unity engine.",
                    "Work on game mechanics, graphics, and user experience.",
                    "Collaborate with artists and designers on game projects."
                ],
                "sector": "Gaming",
                "skill_ids": [31, 23],  # Unity, C++
                "education_ids": [7, 8, 4],
                "durations": ["4 months", "6 months"]
            },
            {
                "titles": ["Finance Intern", "Investment Analyst Intern", "Financial Analyst Intern"],
                "descriptions": [
                    "Work on budgeting, forecasting, and financial reports.",
                    "Support investment analysis and portfolio management.",
                    "Assist with audit preparation and compliance."
                ],
                "sector": "Finance",
                "skill_ids": [12, 36],  # Finance, Business Intelligence
                "education_ids": [13, 14, 4],
                "durations": ["3 months", "6 months"]
            }
        ]

        # ----------- GENERATE INTERNSHIPS -----------
        internships_to_create = []
        num_locations = db.query(models.Location).count()

        for i in range(5000):
            template = random.choice(internship_templates)
            internship = models.Internship(
                title=random.choice(template["titles"]),
                description=random.choice(template["descriptions"]),
                skills_id=random.choice(template["skill_ids"]),
                edu_id=random.choice(template["education_ids"]),
                location_id=random.randint(1, num_locations),
                duration=random.choice(template["durations"]),
                no_of_post=random.randint(1, 10),
                details=f"Opportunity {i+1}: Hands-on experience in {template['sector']}.",
                sector=template["sector"]
            )
            internships_to_create.append(internship)

            if len(internships_to_create) >= 200:
                db.add_all(internships_to_create)
                db.commit()
                print(f"Inserted {i+1} internships...")
                internships_to_create = []

        if internships_to_create:
            db.add_all(internships_to_create)
            db.commit()
            print(f"Inserted remaining {len(internships_to_create)} internships.")

        print("🎉 5000 internships created successfully!")

    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    choice = input("⚠️ Do you want to DROP ALL tables and recreate them? (y/n): ").strip().lower()
    
    if choice == "y":
        models.Base.metadata.drop_all(bind=engine)
        print("🗑️ All existing tables dropped!")
        
        models.Base.metadata.create_all(bind=engine)
        print("📦 Tables created fresh!")
        
        create_sample_data()
    else:
        print("❎ Skipped dropping tables. Using existing database.")
        create_sample_data()
