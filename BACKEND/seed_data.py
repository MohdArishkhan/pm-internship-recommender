from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
import random


def create_sample_data():
    """Create sample data for testing"""
    db = SessionLocal()
    
    try:
        # Create comprehensive educations
        educations = [
            models.Education(description="10th Pass"),
            models.Education(description="12th Pass"),
            models.Education(description="Diploma"),
            models.Education(description="Bachelor's"),
            models.Education(description="Master's"),
            models.Education(description="PhD"),
            models.Education(description="Computer Science Engineering"),
            models.Education(description="Information Technology"),
            models.Education(description="Electronics and Communication"),
            models.Education(description="Mechanical Engineering"),
            models.Education(description="Civil Engineering"),
            models.Education(description="Electrical Engineering"),
            models.Education(description="Business Administration"),
            models.Education(description="Commerce"),
            models.Education(description="Arts"),
            models.Education(description="Science")
        ]
        
        for edu in educations:
            db.add(edu)
        db.commit()
        
        
        # Create comprehensive skills
        skills = [
            models.Skill(description="Python Programming, Django, Flask"),
            models.Skill(description="JavaScript, React, Node.js"),
            models.Skill(description="Java, Spring Boot, Hibernate"),
            models.Skill(description="Data Analysis, SQL, Excel"),
            models.Skill(description="Machine Learning, TensorFlow, PyTorch"),
            models.Skill(description="Digital Marketing, SEO, SEM"),
            models.Skill(description="Project Management, Agile, Scrum"),
            models.Skill(description="UI/UX Design, Figma, Adobe XD"),
            models.Skill(description="Content Writing, Copywriting"),
            models.Skill(description="Sales, CRM, Lead Generation"),
            models.Skill(description="Finance, Accounting, Excel"),
            models.Skill(description="HR, Recruitment, Employee Relations"),
            models.Skill(description="Mobile Development, React Native, Flutter"),
            models.Skill(description="DevOps, AWS, Docker, Kubernetes"),
            models.Skill(description="Cybersecurity, Ethical Hacking"),
            models.Skill(description="Graphic Design, Photoshop, Illustrator"),
            models.Skill(description="Video Editing, Premiere Pro, After Effects"),
            models.Skill(description="Research, Data Collection, Analysis"),
            models.Skill(description="Social Media Management, Instagram, LinkedIn"),
            models.Skill(description="Customer Service, Communication")
        ]
        
        for skill in skills:
            db.add(skill)
        db.commit()
        
        
        # Create comprehensive locations
        locations = [
            models.Location(description="Delhi", state="Delhi"),
            models.Location(description="Mumbai", state="Maharashtra"),
            models.Location(description="Bangalore", state="Karnataka"),
            models.Location(description="Chennai", state="Tamil Nadu"),
            models.Location(description="Hyderabad", state="Telangana"),
            models.Location(description="Pune", state="Maharashtra"),
            models.Location(description="Kolkata", state="West Bengal"),
            models.Location(description="Ahmedabad", state="Gujarat"),
            models.Location(description="Jaipur", state="Rajasthan"),
            models.Location(description="Lucknow", state="Uttar Pradesh"),
            models.Location(description="Kanpur", state="Uttar Pradesh"),
            models.Location(description="Nagpur", state="Maharashtra"),
            models.Location(description="Indore", state="Madhya Pradesh"),
            models.Location(description="Bhopal", state="Madhya Pradesh"),
            models.Location(description="Visakhapatnam", state="Andhra Pradesh"),
            models.Location(description="Patna", state="Bihar"),
            models.Location(description="Vadodara", state="Gujarat"),
            models.Location(description="Ghaziabad", state="Uttar Pradesh"),
            models.Location(description="Ludhiana", state="Punjab"),
            models.Location(description="Agra", state="Uttar Pradesh"),
            models.Location(description="Nashik", state="Maharashtra"),
            models.Location(description="Faridabad", state="Haryana"),
            models.Location(description="Meerut", state="Uttar Pradesh"),
            models.Location(description="Rajkot", state="Gujarat"),
            models.Location(description="Kalyan-Dombivali", state="Maharashtra"),
            models.Location(description="Vasai-Virar", state="Maharashtra"),
            models.Location(description="Varanasi", state="Uttar Pradesh"),
            models.Location(description="Srinagar", state="Jammu and Kashmir"),
            models.Location(description="Aurangabad", state="Maharashtra"),
            models.Location(description="Dhanbad", state="Jharkhand"),
            models.Location(description="Remote", state="Remote")
        ]
        
        for loc in locations:
            db.add(loc)
        db.commit()
        

        # Define comprehensive internship templates
        internship_templates = [
            {
                "titles": ["Software Developer Intern", "Backend Developer Intern", "Python Developer Intern", "Full Stack Developer Intern"],
                "descriptions": [
                    "Work on backend development using Python, Django, and FastAPI. Build scalable web applications and APIs.",
                    "Develop robust backend systems and microservices. Work with databases, caching, and cloud technologies.",
                    "Create modern web applications with Python frameworks. Learn about software architecture and best practices.",
                    "Build end-to-end web solutions using Python, JavaScript, and modern frameworks."
                ],
                "sector": "Technology",
                "skill_ids": [1, 13],  # Python Programming, Mobile Development
                "education_ids": [7, 8, 4, 5],  # CS, IT, Bachelor's, Master's
                "durations": ["3 months", "4 months", "6 months"]
            },
            {
                "titles": ["Frontend Developer Intern", "React Developer Intern", "UI Developer Intern", "Web Developer Intern"],
                "descriptions": [
                    "Develop user-friendly web interfaces using React, JavaScript, and modern CSS frameworks.",
                    "Build responsive and interactive web applications. Work with state management and component libraries.",
                    "Create engaging user experiences with modern frontend technologies and design systems.",
                    "Develop cross-browser compatible web applications with performance optimization."
                ],
                "sector": "Technology",
                "skill_ids": [2, 8],  # JavaScript/React, UI/UX Design
                "education_ids": [7, 8, 4, 5],
                "durations": ["3 months", "4 months", "6 months"]
            },
            {
                "titles": ["Data Analyst Intern", "Business Analyst Intern", "Research Analyst Intern", "Data Science Intern"],
                "descriptions": [
                    "Analyze large datasets to extract meaningful insights. Work with SQL, Python, and visualization tools.",
                    "Support business decisions through data analysis and reporting. Create dashboards and KPI tracking.",
                    "Conduct market research and competitive analysis. Present findings to stakeholder teams.",
                    "Apply statistical methods and machine learning to solve business problems with data."
                ],
                "sector": "Analytics",
                "skill_ids": [4, 5, 18],  # Data Analysis, ML, Research
                "education_ids": [7, 8, 4, 5, 16],
                "durations": ["3 months", "6 months"]
            },
            {
                "titles": ["Digital Marketing Intern", "Social Media Intern", "Content Marketing Intern", "SEO Intern"],
                "descriptions": [
                    "Learn digital marketing strategies including SEO, SEM, and social media marketing campaigns.",
                    "Manage social media accounts and create engaging content for various digital platforms.",
                    "Develop content marketing strategies and create compelling copy for websites and campaigns.",
                    "Optimize websites for search engines and analyze digital marketing performance metrics."
                ],
                "sector": "Marketing",
                "skill_ids": [6, 9, 19],  # Digital Marketing, Content Writing, Social Media
                "education_ids": [13, 14, 15, 4, 2],  # Business, Commerce, Arts, Bachelor's, 12th
                "durations": ["2 months", "3 months", "4 months"]
            },
            {
                "titles": ["HR Intern", "Recruitment Intern", "People Operations Intern", "Talent Acquisition Intern"],
                "descriptions": [
                    "Support HR operations including recruitment, employee onboarding, and policy implementation.",
                    "Assist in talent acquisition processes and candidate screening for various positions.",
                    "Help with employee engagement initiatives and HR analytics projects.",
                    "Learn recruitment strategies and participate in campus hiring and interview processes."
                ],
                "sector": "Human Resources",
                "skill_ids": [12, 20],  # HR, Customer Service
                "education_ids": [13, 14, 4, 5],
                "durations": ["2 months", "3 months", "6 months"]
            },
            {
                "titles": ["Finance Intern", "Investment Banking Intern", "Financial Analyst Intern", "Accounting Intern"],
                "descriptions": [
                    "Learn financial modeling, analysis, and reporting. Work with Excel and financial databases.",
                    "Support investment research and due diligence activities for financial products.",
                    "Assist in budgeting, forecasting, and financial planning processes.",
                    "Handle accounting tasks including bookkeeping, reconciliation, and audit support."
                ],
                "sector": "Finance",
                "skill_ids": [11, 4],  # Finance, Data Analysis
                "education_ids": [13, 14, 4, 5],
                "durations": ["3 months", "6 months"]
            },
            {
                "titles": ["Graphic Design Intern", "UI/UX Design Intern", "Creative Design Intern", "Brand Design Intern"],
                "descriptions": [
                    "Create visual designs for digital and print media using Adobe Creative Suite.",
                    "Design user interfaces and user experiences for web and mobile applications.",
                    "Develop brand identity elements and marketing collateral for various campaigns.",
                    "Work on creative projects including logos, brochures, and digital graphics."
                ],
                "sector": "Design",
                "skill_ids": [8, 16, 17],  # UI/UX, Graphic Design, Video Editing
                "education_ids": [15, 4, 3],  # Arts, Bachelor's, Diploma
                "durations": ["2 months", "3 months", "4 months"]
            },
            {
                "titles": ["Sales Intern", "Business Development Intern", "Market Research Intern", "Customer Success Intern"],
                "descriptions": [
                    "Learn sales processes and customer relationship management. Support lead generation activities.",
                    "Identify new business opportunities and support partnership development initiatives.",
                    "Conduct market research and competitive analysis to support business strategy.",
                    "Help customers achieve success with products and services through onboarding and support."
                ],
                "sector": "Sales",
                "skill_ids": [10, 18, 20],  # Sales, Research, Customer Service
                "education_ids": [13, 14, 4, 2],
                "durations": ["2 months", "3 months", "4 months"]
            },
            {
                "titles": ["Mobile App Developer Intern", "Android Developer Intern", "iOS Developer Intern", "Flutter Developer Intern"],
                "descriptions": [
                    "Develop mobile applications for Android and iOS platforms using modern frameworks.",
                    "Build native Android applications with Java/Kotlin and Android SDK.",
                    "Create iOS applications using Swift and Xcode development environment.",
                    "Develop cross-platform mobile apps using Flutter and React Native frameworks."
                ],
                "sector": "Technology",
                "skill_ids": [13, 2, 1],  # Mobile Development, JavaScript, Python
                "education_ids": [7, 8, 4, 5],
                "durations": ["4 months", "6 months"]
            },
            {
                "titles": ["DevOps Intern", "Cloud Engineering Intern", "Infrastructure Intern", "Site Reliability Intern"],
                "descriptions": [
                    "Learn DevOps practices including CI/CD, containerization, and cloud deployment.",
                    "Work with cloud platforms like AWS, Azure, and GCP for application deployment.",
                    "Support infrastructure automation and monitoring using modern DevOps tools.",
                    "Ensure system reliability and performance through monitoring and optimization."
                ],
                "sector": "Technology",
                "skill_ids": [14, 1],  # DevOps, Python Programming
                "education_ids": [7, 8, 4, 5],
                "durations": ["4 months", "6 months"]
            }
        ]
        
        # Generate 5000 internships
        internships_to_create = []
        num_locations = len(locations)
        
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
                details=f"Opportunity {i+1}: Gain hands-on experience in {template['sector'].lower()}. Perfect for students looking to build practical skills.",
                sector=template["sector"]
            )
            
            internships_to_create.append(internship)
            
            # Batch insert every 100 records for performance
            if len(internships_to_create) >= 100:
                db.add_all(internships_to_create)
                db.commit()
                print(f"Inserted {i+1} internships...")
                internships_to_create = []
        
        # Insert any remaining internships
        if internships_to_create:
            db.add_all(internships_to_create)
            db.commit()
            print(f"Inserted remaining {len(internships_to_create)} internships...")
        
        print("5000 internships created successfully!")

        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Drop all existing tables
    models.Base.metadata.drop_all(bind=engine)
    print("All existing tables dropped!")
    
    # Create tables fresh
    models.Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    # Then create sample data
    create_sample_data()
