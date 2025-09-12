from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal, engine
from app import models
import random

def create_sample_data():
    # Create sample data for testing
    db = SessionLocal()
    
    try:
        # Education data - Concise and clear
        educations_data = [
            "Class 10",
            "Class 12", 
            "Diploma Engineering",
            "Diploma Computer Applications",
            "Diploma Business",
            "B.Tech",
            "B.E.",
            "BCA",
            "B.Sc",
            "B.A.",
            "B.Com",
            "BBA",
            "M.Tech",
            "M.E.",
            "MCA",
            "M.Sc",
            "M.A.",
            "M.Com",
            "MBA",
            "Ph.D",
            "B.Arch",
            "B.Des",
            "M.Des",
            "B.Pharm",
            "MBBS"
        ]
        
        education_objects = []
        for edu in educations_data:
            education_objects.append(models.Education(description=edu))
        db.add_all(education_objects)
        db.commit()
        print("✅ Education data created")

        # Skills data - More specific and industry-relevant
        skills_data = [
            "Python Programming", "JavaScript Development", "Java Programming", "C++ Programming",
            "React.js", "Angular", "Vue.js", "Node.js", "Django", "Flask", "FastAPI", "Spring Boot",
            "HTML5", "CSS3", "TypeScript", "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin",
            "SQL", "PostgreSQL", "MongoDB", "MySQL", "Redis", "Elasticsearch",
            "Machine Learning", "Deep Learning", "Data Science", "Artificial Intelligence",
            "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib",
            "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud Platform", "DevOps",
            "Git", "Jenkins", "CI/CD", "Linux", "Bash Scripting",
            "UI/UX Design", "Figma", "Adobe XD", "Sketch", "Photoshop", "Illustrator",
            "Digital Marketing", "SEO", "SEM", "Google Analytics", "Facebook Ads", "Content Marketing",
            "Social Media Marketing", "Email Marketing", "Affiliate Marketing",
            "Project Management", "Agile", "Scrum", "Kanban", "JIRA", "Confluence",
            "Business Analysis", "Market Research", "Data Analysis", "Excel", "Power BI", "Tableau",
            "Financial Analysis", "Accounting", "Budgeting", "Risk Management", "Investment Analysis",
            "Human Resources", "Recruitment", "Training", "Performance Management",
            "Sales", "CRM", "Lead Generation", "Customer Support", "Communication",
            "Content Writing", "Copywriting", "Technical Writing", "Blog Writing",
            "Video Editing", "Premiere Pro", "After Effects", "Final Cut Pro",
            "Cybersecurity", "Ethical Hacking", "Penetration Testing", "Network Security",
            "Mobile App Development", "React Native", "Flutter", "iOS Development", "Android Development",
            "Game Development", "Unity", "Unreal Engine", "3D Modeling", "Animation",
            "Blockchain", "Cryptocurrency", "Smart Contracts", "Solidity",
            "Quality Assurance", "Software Testing", "Automation Testing", "Selenium",
            "Research", "Statistical Analysis", "SPSS", "R Programming", "Data Visualization"
        ]
        
        skill_objects = []
        for skill in skills_data:
            skill_objects.append(models.Skill(description=skill))
        db.add_all(skill_objects)
        db.commit()
        print("✅ Skills data created")

        # Locations data - More comprehensive Indian cities
        locations_data = [
            ("Delhi", "Delhi"), ("Mumbai", "Maharashtra"), ("Bangalore", "Karnataka"),
            ("Chennai", "Tamil Nadu"), ("Hyderabad", "Telangana"), ("Pune", "Maharashtra"),
            ("Kolkata", "West Bengal"), ("Ahmedabad", "Gujarat"), ("Jaipur", "Rajasthan"),
            ("Lucknow", "Uttar Pradesh"), ("Kochi", "Kerala"), ("Indore", "Madhya Pradesh"),
            ("Coimbatore", "Tamil Nadu"), ("Gurgaon", "Haryana"), ("Noida", "Uttar Pradesh"),
            ("Vadodara", "Gujarat"), ("Nagpur", "Maharashtra"), ("Visakhapatnam", "Andhra Pradesh"),
            ("Bhopal", "Madhya Pradesh"), ("Patna", "Bihar"), ("Thiruvananthapuram", "Kerala"),
            ("Chandigarh", "Chandigarh"), ("Mysore", "Karnataka"), ("Surat", "Gujarat"),
            ("Rajkot", "Gujarat"), ("Faridabad", "Haryana"), ("Ghaziabad", "Uttar Pradesh"),
            ("Kanpur", "Uttar Pradesh"), ("Nashik", "Maharashtra"), ("Remote Work", "Pan India")
        ]
        
        location_objects = []
        for loc, state in locations_data:
            location_objects.append(models.Location(description=loc, state=state))
        db.add_all(location_objects)
        db.commit()
        print("✅ Locations data created")

        # Sectors data - Concise industry sectors
        sectors_data = [
            ("Technology", "IT and Software Development"),
            ("Artificial Intelligence", "AI and Machine Learning"),
            ("Web Development", "Frontend and Backend Development"),
            ("Mobile Development", "iOS and Android Apps"),
            ("Data Science", "Analytics and Big Data"),
            ("Cybersecurity", "Information Security"),
            ("Cloud Computing", "AWS, Azure, and DevOps"),
            ("Digital Marketing", "Online Marketing and SEO"),
            ("Graphic Design", "Visual Design and Branding"),
            ("UI/UX Design", "User Experience Design"),
            ("Finance", "Banking and Investment"),
            ("Healthcare", "Medical Technology"),
            ("Education", "EdTech and Learning"),
            ("E-commerce", "Online Retail"),
            ("Gaming", "Game Development"),
            ("Blockchain", "Cryptocurrency and Web3"),
            ("Consulting", "Strategy and Management"),
            ("Human Resources", "Talent Management"),
            ("Sales & Marketing", "Business Development"),
            ("Content Creation", "Writing and Media"),
            ("Research & Development", "Innovation and R&D"),
            ("Manufacturing", "Industrial Production"),
            ("Logistics", "Supply Chain"),
            ("Telecommunications", "Networking and Telecom"),
            ("Renewable Energy", "Clean Technology")
        ]
        
        sector_objects = []
        for name, desc in sectors_data:
            sector_objects.append(models.Sector(name=name, description=desc))
        db.add_all(sector_objects)
        db.commit()
        print("✅ Sectors data created")

        # Create many-to-many relationships between Education and Sectors
        education_sector_mappings = [
            # Technology sectors for tech education
            ([6, 7, 8], [1, 3, 4, 5, 6, 7]),  # B.Tech, B.E., BCA -> Technology, Web Dev, Mobile Dev, Data Science, Cybersecurity, Cloud
            ([13, 14, 15], [1, 2, 5, 7]),     # M.Tech, M.E., MCA -> Technology, AI, Data Science, Cloud
            ([3, 4], [1, 3, 8]),              # Engineering Diploma, DCA -> Technology, Web Dev, Digital Marketing
            
            # Business sectors for business education
            ([11, 12, 19], [8, 17, 18, 19]),  # B.Com, BBA, MBA -> Digital Marketing, Consulting, HR, Sales
            ([5], [8, 19, 20]),               # Diploma in Business -> Digital Marketing, Sales, Content
            
            # Design sectors for arts/design education
            ([10, 22, 23], [9, 10]),          # B.A., B.Des, M.Des -> Graphic Design, UI/UX
            ([21], [9, 10]),                  # B.Arch -> Graphic Design, UI/UX
            
            # Science sectors for science education
            ([9, 16], [2, 5, 12, 21, 22]),    # B.Sc, M.Sc -> AI, Data Science, Healthcare, R&D, Manufacturing
            ([20], [21, 22]),                 # Ph.D -> R&D, Manufacturing
            
            # Healthcare for medical education
            ([24, 25], [12]),                 # B.Pharm, MBBS -> Healthcare
            
            # Finance for commerce education
            ([11, 18], [11, 17]),             # B.Com, M.Com -> Finance, Consulting
            
            # General sectors for basic education
            ([1, 2], [8, 19, 20, 23]),        # 10th, 12th -> Digital Marketing, Sales, Content, Logistics
        ]
        
        # Fetch all education and sector objects
        all_educations = db.query(models.Education).all()
        all_sectors = db.query(models.Sector).all()
        
        for edu_ids, sector_ids in education_sector_mappings:
            for edu_id in edu_ids:
                if edu_id <= len(all_educations):
                    education = all_educations[edu_id - 1]
                    for sector_id in sector_ids:
                        if sector_id <= len(all_sectors):
                            sector = all_sectors[sector_id - 1]
                            if sector not in education.sectors:
                                education.sectors.append(sector)
        
        db.commit()
        print("✅ Education-Sector relationships created")

        # Create many-to-many relationships between Sectors and Skills
        sector_skill_mappings = [
            # Technology sector skills - using actual skill IDs from our 91 skills
            (1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 43, 44, 45, 46, 47]),  # Technology
            (2, [1, 27, 28, 29, 30, 31, 32, 33, 34, 35]),                       # AI
            (3, [1, 2, 5, 6, 7, 8, 13, 14, 15]),                                # Web Development
            (4, [20, 21, 75, 76]),                                              # Mobile Development (limited to existing skills)
            (5, [1, 27, 28, 29, 30, 31, 32, 33, 34, 35, 57, 58, 59, 60]),      # Data Science
            (6, [74, 75, 76, 77]),                                              # Cybersecurity (limited to existing skills)
            (7, [36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 47]),                 # Cloud Computing
            (8, [48, 49, 50, 51, 52, 53, 54, 55, 56]),                         # Digital Marketing
            (9, [47, 48, 49, 50, 51]),                                          # Graphic Design (limited to existing skills)
            (10, [47, 48, 49, 50]),                                             # UI/UX Design
            (11, [61, 62, 63, 64, 65]),                                         # Finance
            (12, [66, 67, 68, 69]),                                             # Healthcare
            (13, [70, 71, 72, 73]),                                             # Education
            (14, [2, 5, 6, 7, 8, 48, 66, 67]),                                 # E-commerce
            (15, [79, 80, 81, 82, 83]),                                         # Gaming (limited to existing skills)
            (16, [84, 85, 86, 87]),                                             # Blockchain (limited to existing skills)
            (17, [57, 58, 59, 60, 70]),                                         # Consulting
            (18, [66, 67, 68, 69]),                                             # HR
            (19, [66, 67, 70, 71]),                                             # Sales & Marketing
            (20, [72, 73, 74, 75]),                                             # Content Creation (limited to existing skills)
            (21, [88, 89, 90, 91]),                                             # R&D (limited to existing skills)
            (22, [1, 3, 4, 88, 89]),                                            # Manufacturing (limited to existing skills)
            (23, [57, 58, 70, 71]),                                             # Logistics
            (24, [1, 3, 4, 43, 46]),                                            # Telecommunications
            (25, [88, 89, 90, 91])                                              # Renewable Energy (limited to existing skills)
        ]
        
        all_skills = db.query(models.Skill).all()
        
        for sector_id, skill_ids in sector_skill_mappings:
            if sector_id <= len(all_sectors):
                sector = all_sectors[sector_id - 1]
                for skill_id in skill_ids:
                    if skill_id <= len(all_skills):
                        skill = all_skills[skill_id - 1]
                        if skill not in sector.skills:
                            sector.skills.append(skill)
        
        db.commit()
        print("✅ Sector-Skill relationships created")

        # Company names - More diverse and realistic
        companies = [
            # Tech Giants
            "Microsoft India", "Google India", "Amazon India", "IBM India", "Oracle India",
            "Accenture", "TCS", "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra",
            "Cognizant", "Capgemini", "Deloitte Digital", "EY Digital",
            
            # Indian Startups & Unicorns
            "Flipkart", "Paytm", "Zomato", "Swiggy", "Ola", "Uber India", "InMobi",
            "Freshworks", "Zoho Corporation", "Razorpay", "BYJU'S", "Unacademy",
            "UrbanClap", "PolicyBazaar", "Nykaa", "BigBasket", "Grofers",
            "Sharechat", "Dream11", "PhonePe", "Meesho", "CRED",
            
            # Fintech & Banking
            "HDFC Bank", "ICICI Bank", "Axis Bank", "Yes Bank", "Kotak Mahindra Bank",
            "Zerodha", "Groww", "Upstox", "AngelOne", "Paytm Money",
            
            # E-commerce & Retail
            "Amazon India", "Flipkart", "Myntra", "Jabong", "Snapdeal",
            "Reliance Digital", "Future Group", "Spencer's Retail",
            
            # Healthcare & Pharma
            "Apollo Hospitals", "Fortis Healthcare", "Max Healthcare", "Dr. Reddy's",
            "Cipla", "Sun Pharma", "Lupin", "Practo", "1mg", "PharmEasy",
            
            # Media & Entertainment
            "Times Internet", "Network18", "Zee Entertainment", "Star India",
            "Sony Pictures India", "Netflix India", "Hotstar", "ALTBalaji",
            
            # Automotive
            "Tata Motors", "Mahindra & Mahindra", "Maruti Suzuki", "Hyundai India",
            "Honda India", "Bajaj Auto", "Hero MotoCorp", "Ola Electric",
            
            # Real Estate & PropTech
            "Housing.com", "99acres", "MagicBricks", "PropTiger", "NoBroker",
            "Oyo Rooms", "Airbnb India", "RedDoorz",
            
            # EdTech
            "BYJU'S", "Unacademy", "Vedantu", "Toppr", "WhiteHat Jr", "Emeritus",
            "UpGrad", "Simplilearn", "Great Learning", "Coursera India",
            
            # Food & Beverage
            "Zomato", "Swiggy", "Dunzo", "FreshMenu", "Box8", "Faasos",
            "McDonald's India", "KFC India", "Domino's India", "Pizza Hut India",
            
            # Travel & Tourism
            "MakeMyTrip", "Goibibo", "Cleartrip", "Yatra", "EaseMyTrip",
            "OYO", "Treebo", "FabHotels", "Thomas Cook India"
        ]

        # ----------- INTERNSHIP TEMPLATES (Comprehensive and Diverse) -----------
        internship_templates = [
            {
                "titles": ["Software Developer Intern", "Backend Developer Intern", "Full Stack Developer Intern"],
                "descriptions": [
                    "Develop scalable web applications using modern frameworks and best practices.",
                    "Work on backend APIs, database design, and cloud infrastructure integration.",
                    "Collaborate with cross-functional teams to deliver high-quality software solutions.",
                    "Participate in code reviews, testing, and deployment processes.",
                    "Learn and implement industry-standard development methodologies."
                ],
                "sector_id": 1,  # Technology
                "skill_ids": [1, 2, 3, 4, 5, 6, 9, 10, 11],  # Python, JS, Java, C++, React, Angular, Django, Flask, FastAPI
                "education_ids": [6, 7, 8, 13, 14, 15],
                "durations": ["3 months", "4 months", "6 months"],
                "companies": ["TCS", "Infosys", "Microsoft India", "Amazon India", "Google India", "Flipkart", "Paytm"]
            },
            {
                "titles": ["Data Scientist Intern", "ML Engineer Intern", "AI Research Intern"],
                "descriptions": [
                    "Build machine learning models for predictive analytics and automation.",
                    "Analyze large datasets to extract meaningful business insights.",
                    "Work on natural language processing and computer vision projects.",
                    "Develop data pipelines and implement MLOps best practices.",
                    "Collaborate with data engineers and product teams on AI initiatives."
                ],
                "sector_id": 2,  # Artificial Intelligence
                "skill_ids": [1, 27, 28, 29, 30, 31, 32, 33, 34, 35],  # Python, ML, Deep Learning, Data Science, AI, TensorFlow, PyTorch, etc.
                "education_ids": [6, 7, 8, 9, 13, 14, 15, 16, 20],
                "durations": ["4 months", "6 months"],
                "companies": ["Microsoft India", "Google India", "IBM India", "Amazon India", "Flipkart", "Zomato", "BYJU'S"]
            },
            {
                "titles": ["Frontend Developer Intern", "React Developer Intern", "UI Developer Intern"],
                "descriptions": [
                    "Create responsive and interactive user interfaces using modern frameworks.",
                    "Implement pixel-perfect designs and ensure cross-browser compatibility.",
                    "Optimize web applications for performance and accessibility.",
                    "Work closely with UX designers and backend developers.",
                    "Learn about component architecture and state management."
                ],
                "sector_id": 3,  # Web Development
                "skill_ids": [2, 5, 6, 7, 13, 14, 15],  # JavaScript, React, Angular, Vue, HTML5, CSS3, TypeScript
                "education_ids": [6, 7, 8, 3, 4],
                "durations": ["3 months", "4 months"],
                "companies": ["Flipkart", "Zomato", "Swiggy", "Myntra", "Nykaa", "Razorpay", "PhonePe"]
            },
            {
                "titles": ["Mobile App Developer Intern", "iOS Developer Intern", "Android Developer Intern"],
                "descriptions": [
                    "Develop native mobile applications for iOS and Android platforms.",
                    "Work with cross-platform frameworks like React Native or Flutter.",
                    "Implement mobile-first user experiences and app store optimization.",
                    "Learn about mobile architecture patterns and performance optimization.",
                    "Collaborate with designers on mobile UI/UX implementation."
                ],
                "sector_id": 4,  # Mobile Development
                "skill_ids": [20, 21],  # Swift, Kotlin (limited to available skills)
                "education_ids": [6, 7, 8, 13, 14],
                "durations": ["4 months", "6 months"],
                "companies": ["Ola", "Uber India", "Swiggy", "Zomato", "Paytm", "PhonePe", "CRED"]
            },
            {
                "titles": ["DevOps Intern", "Cloud Engineer Intern", "Infrastructure Intern"],
                "descriptions": [
                    "Work with CI/CD pipelines and automated deployment processes.",
                    "Manage containerized applications using Docker and Kubernetes.",
                    "Support scalable cloud deployments on AWS, Azure, or GCP.",
                    "Monitor system performance and implement infrastructure as code.",
                    "Learn about microservices architecture and distributed systems."
                ],
                "sector_id": 7,  # Cloud Computing
                "skill_ids": [36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 47],  # Docker, Kubernetes, AWS, Azure, GCP, DevOps, Git, etc.
                "education_ids": [6, 7, 8, 13, 14],
                "durations": ["4 months", "6 months"],
                "companies": ["Amazon India", "Microsoft India", "Google India", "IBM India", "TCS", "Infosys"]
            },
            {
                "titles": ["Digital Marketing Intern", "SEO Specialist Intern", "Social Media Marketing Intern"],
                "descriptions": [
                    "Execute digital marketing campaigns across multiple channels.",
                    "Optimize websites for search engines and analyze traffic metrics.",
                    "Create engaging content for social media platforms and blogs.",
                    "Work with marketing automation tools and CRM systems.",
                    "Learn about conversion optimization and customer acquisition."
                ],
                "sector_id": 8,  # Digital Marketing
                "skill_ids": [48, 49, 50, 51, 52, 53, 54, 55, 56],  # Digital Marketing, SEO, SEM, Google Analytics, etc.
                "education_ids": [10, 11, 12, 19, 5],
                "durations": ["2 months", "3 months", "4 months"],
                "companies": ["Flipkart", "Amazon India", "Nykaa", "BigBasket", "UrbanClap", "PolicyBazaar"]
            },
            {
                "titles": ["UI/UX Design Intern", "Graphic Design Intern", "Product Design Intern"],
                "descriptions": [
                    "Design intuitive user interfaces for web and mobile applications.",
                    "Create visual designs, prototypes, and design systems.",
                    "Conduct user research and usability testing sessions.",
                    "Collaborate with developers to ensure design implementation.",
                    "Learn about design thinking and human-centered design principles."
                ],
                "sector_id": 10,  # UI/UX Design
                "skill_ids": [47, 48, 49, 50],  # UI/UX Design, Figma, Adobe XD, Sketch
                "education_ids": [22, 23, 10, 6, 7],
                "durations": ["3 months", "4 months"],
                "companies": ["Flipkart", "Swiggy", "Ola", "BYJU'S", "Razorpay", "Freshworks", "Zoho Corporation"]
            },
            {
                "titles": ["Finance Intern", "Investment Analyst Intern", "Financial Analyst Intern"],
                "descriptions": [
                    "Assist with financial planning, budgeting, and forecasting.",
                    "Support investment analysis and portfolio management activities.",
                    "Prepare financial reports and presentations for stakeholders.",
                    "Learn about risk management and regulatory compliance.",
                    "Work with financial modeling and valuation techniques."
                ],
                "sector_id": 11,  # Finance
                "skill_ids": [61, 62, 63, 64, 65],  # Financial Analysis, Accounting, Budgeting, Risk Management, Investment Analysis
                "education_ids": [11, 12, 18, 19, 6],
                "durations": ["3 months", "6 months"],
                "companies": ["HDFC Bank", "ICICI Bank", "Axis Bank", "Zerodha", "Groww", "Paytm Money"]
            },
            {
                "titles": ["Content Writer Intern", "Digital Content Creator Intern", "Marketing Content Intern"],
                "descriptions": [
                    "Create engaging content for websites, blogs, and social media.",
                    "Develop marketing materials and copywriting for campaigns.",
                    "Research industry trends and create thought leadership content.",
                    "Learn about SEO writing and content marketing strategies.",
                    "Collaborate with design and marketing teams on content creation."
                ],
                "sector_id": 20,  # Content Creation
                "skill_ids": [72, 73],  # Content Writing, Copywriting (limited to available skills)
                "education_ids": [10, 11, 16, 17, 1, 2],
                "durations": ["2 months", "3 months"],
                "companies": ["Times Internet", "Network18", "Zee Entertainment", "BYJU'S", "Unacademy"]
            },
            {
                "titles": ["HR Intern", "Talent Acquisition Intern", "HR Operations Intern"],
                "descriptions": [
                    "Support recruitment processes and candidate screening.",
                    "Assist with employee onboarding and training programs.",
                    "Help with HR policy development and employee relations.",
                    "Learn about performance management and organizational development.",
                    "Work on HR analytics and employee engagement initiatives."
                ],
                "sector_id": 18,  # Human Resources
                "skill_ids": [66, 67, 68, 69],  # Human Resources, Recruitment, Training, Performance Management
                "education_ids": [10, 11, 12, 19, 16, 17],
                "durations": ["3 months", "4 months"],
                "companies": ["TCS", "Infosys", "Wipro", "Accenture", "Capgemini", "HCL Technologies"]
            },
            {
                "titles": ["Sales Intern", "Business Development Intern", "Customer Success Intern"],
                "descriptions": [
                    "Support sales team with lead generation and customer outreach.",
                    "Assist with market research and competitive analysis.",
                    "Help with customer relationship management and follow-ups.",
                    "Learn about sales processes and business development strategies.",
                    "Work on customer success initiatives and retention programs."
                ],
                "sector_id": 19,  # Sales & Marketing
                "skill_ids": [66, 67, 70, 71],  # Sales, CRM, Lead Generation, Communication
                "education_ids": [11, 12, 19, 1, 2, 10],
                "durations": ["2 months", "3 months", "4 months"],
                "companies": ["Flipkart", "Amazon India", "Swiggy", "Ola", "PolicyBazaar", "Housing.com"]
            }
        ]

        # ----------- GENERATE INTERNSHIPS -----------
        print("🚀 Starting internship generation...")
        internships_to_create = []
        num_locations = len(all_locations := db.query(models.Location).all())
        num_educations = len(all_educations)
        num_sectors = len(all_sectors)
        num_skills = len(all_skills)

        for i in range(7500):  # Generate 7500 diverse internships
            template = random.choice(internship_templates)
            
            # Select random values from template arrays
            title = random.choice(template["titles"])
            description = random.choice(template["descriptions"])
            company = random.choice(template["companies"])
            skill_id = random.choice(template["skill_ids"])
            education_id = random.choice(template["education_ids"])
            duration = random.choice(template["durations"])
            
            # Ensure IDs are within valid ranges
            if (skill_id <= num_skills and 
                education_id <= num_educations and 
                template["sector_id"] <= num_sectors):
                
                internship = models.Internship(
                    title=title,
                    description=description,
                    company_name=company,
                    skills_id=skill_id,
                    edu_id=education_id,
                    sector_id=template["sector_id"],
                    location_id=random.randint(1, num_locations),
                    duration=duration,
                    no_of_post=random.randint(1, 15),  # Varying number of positions
                    details=f"Join {company} as a {title} and gain hands-on experience in {all_sectors[template['sector_id']-1].name}. This {duration} internship offers mentorship, real-world projects, and potential for full-time conversion."
                )
                internships_to_create.append(internship)

            # Batch insert for better performance
            if len(internships_to_create) >= 250:
                db.add_all(internships_to_create)
                db.commit()
                print(f"✅ Inserted {i+1} internships...")
                internships_to_create = []

        # Insert remaining internships
        if internships_to_create:
            db.add_all(internships_to_create)
            db.commit()
            print(f"✅ Inserted remaining {len(internships_to_create)} internships.")

        print("🎉 Internship generation completed successfully!")
        
        # Print summary statistics
        total_internships = db.query(models.Internship).count()
        total_educations = db.query(models.Education).count()
        total_skills = db.query(models.Skill).count()
        total_sectors = db.query(models.Sector).count()
        total_locations = db.query(models.Location).count()
        
        print(f"\n📊 DATABASE SUMMARY:")
        print(f"   📚 Education levels: {total_educations}")
        print(f"   🏢 Sectors: {total_sectors}")
        print(f"   🛠️  Skills: {total_skills}")
        print(f"   📍 Locations: {total_locations}")
        print(f"   💼 Internships: {total_internships}")
        print(f"\n🎯 Seed data creation completed successfully!")

    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    choice = input("⚠️ Do you want to DROP ALL tables and recreate them? (y/n): ").strip().lower()
    
    if choice == "y":
        try:
            # Get a session to manually drop foreign key constraints
            db = SessionLocal()
            
            # Disable foreign key checks for MySQL
            db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            db.commit()
            
            # Drop all tables
            models.Base.metadata.drop_all(bind=engine)
            print("🗑️ All existing tables dropped!")
            
            # Re-enable foreign key checks
            db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            db.commit()
            db.close()
            
            # Create tables fresh
            models.Base.metadata.create_all(bind=engine)
            print("📦 Tables created fresh!")
            
            create_sample_data()
            
        except Exception as e:
            print(f"❌ Error during table recreation: {e}")
            print("Trying alternative approach...")
            try:
                # Alternative: Just create tables (they might already exist)
                models.Base.metadata.create_all(bind=engine)
                print("📦 Tables ensured to exist!")
                create_sample_data()
            except Exception as e2:
                print(f"❌ Failed to create sample data: {e2}")
    else:
        print("❎ Skipped dropping tables. Using existing database.")
        try:
            create_sample_data()
        except Exception as e:
            print(f"❌ Error creating sample data: {e}")
            print("💡 Try running with 'y' to recreate tables first.")
