"""
Career Compass Platform - Enhanced Database with 5 Roles
Advanced matching algorithm with compatibility scoring
"""

import sqlite3
import os

# Create database directory
os.makedirs('database', exist_ok=True)

# Connect to database
conn = sqlite3.connect('database/career_compass.db')
cursor = conn.cursor()

print("Creating advanced database schema...")

# Drop existing tables
cursor.execute('DROP TABLE IF EXISTS user_progress')
cursor.execute('DROP TABLE IF EXISTS roadmap_topics')
cursor.execute('DROP TABLE IF EXISTS roadmap_phases')
cursor.execute('DROP TABLE IF EXISTS role_requirements')
cursor.execute('DROP TABLE IF EXISTS career_roles')
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('DROP TABLE IF EXISTS user_preferences')

# Create Users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    password TEXT,
    user_type TEXT DEFAULT 'student', -- 'student' or 'parent'
    specialization TEXT,
    current_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create User Preferences table
cursor.execute('''
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    skills TEXT,  -- JSON array of {skill: level}
    internship_done BOOLEAN DEFAULT 0,
    internship_role TEXT,
    internship_duration INTEGER,
    projects TEXT,  -- JSON array of projects
    interest_areas TEXT,  -- JSON array
    preferred_work_type TEXT,
    salary_priority INTEGER,
    career_goal TEXT,
    timeline TEXT,
    learning_pace TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
''')

# Create Career Roles table (Enhanced)
cursor.execute('''
CREATE TABLE career_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL,
    category TEXT,
    primary_specialization TEXT,
    related_specializations TEXT,
    description TEXT,
    avg_salary_range TEXT,
    avg_salary_numeric INTEGER,
    demand_level TEXT,
    growth_rate TEXT,
    difficulty TEXT,
    entry_friendly BOOLEAN,
    remote_friendly BOOLEAN,
    experience_required TEXT,
    tech_stack TEXT,
    related_internships TEXT,
    transferable_skills BOOLEAN DEFAULT 1,
    specialization_heavy BOOLEAN DEFAULT 0
)
''')

# Create Role Requirements table (Enhanced for scoring)
cursor.execute('''
CREATE TABLE role_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER,
    skill_name TEXT,
    skill_level TEXT,  -- Beginner, Intermediate, Advanced
    is_required BOOLEAN DEFAULT 1,  -- required vs nice-to-have
    weight INTEGER DEFAULT 1,  -- importance weight
    FOREIGN KEY (role_id) REFERENCES career_roles(id) ON DELETE CASCADE
)
''')

# Create Roadmap Phases table
cursor.execute('''
CREATE TABLE roadmap_phases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER,
    phase_number INTEGER,
    phase_name TEXT,
    phase_description TEXT,
    estimated_duration TEXT,
    FOREIGN KEY (role_id) REFERENCES career_roles(id) ON DELETE CASCADE
)
''')

# Create Roadmap Topics table (Enhanced with coordinates for flowchart)
cursor.execute('''
CREATE TABLE roadmap_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phase_id INTEGER,
    topic_name TEXT,
    topic_order INTEGER,
    description TEXT,
    resource_link TEXT,
    resource_type TEXT,
    is_essential BOOLEAN DEFAULT 1,
    is_checkpoint BOOLEAN DEFAULT 0,
    prerequisite_topic_id INTEGER,
    position_x INTEGER,
    position_y INTEGER,
    FOREIGN KEY (phase_id) REFERENCES roadmap_phases(id) ON DELETE CASCADE
)
''')

# Create User Progress table
cursor.execute('''
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    topic_id INTEGER,
    status TEXT DEFAULT 'not_started',  -- not_started, learning, completed
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES roadmap_topics(id) ON DELETE CASCADE
)
''')

print("Database schema created!")

# ============================================
# INSERT ALL 5 CAREER ROLES
# ============================================

roles_data = [
    # 1. Software Engineering
    ('Software Engineer', 'Software Engineering', 'Software Engineering', 'CSE,IT', 
     'Design, develop, and maintain software applications', '60-110', 85000, 'Very High', 'Steady', 'Intermediate', 1, 1, 'Some preferred', 
     'Java,Python,Git,SQL,Algorithms', 'Software Developer Intern,Engineering Intern', 1, 0),
    
    # 2. Data Science
    ('Data Scientist', 'AI/ML', 'Data Science', 'AI-ML,Data Science,CSE',
     'Analyze data and build ML models to extract insights', '75-135', 105000, 'Very High', 'Fast', 'Intermediate', 1, 1, 'Preferred',
     'Python,Statistics,Machine Learning,SQL,Data Visualization', 'Data Science Intern,Analytics Intern', 1, 1),

    # 3. Cloud Computing
    ('Cloud Solutions Architect', 'Cloud Computing', 'Cloud Computing', 'Cloud Computing,CSE,IT',
     'Design cloud infrastructure and solutions', '90-150', 120000, 'Very High', 'Fast', 'Advanced', 0, 1, 'Required',
     'AWS,Azure,GCP,Architecture,Networking', 'Cloud Intern,Solutions Architect Intern', 1, 1),

    # 4. Cybersecurity
    ('Cybersecurity Analyst', 'Cybersecurity', 'Cyber Security', 'Cyber Security,CSE,IT',
     'Monitor and protect systems from cyber threats', '65-110', 87500, 'Very High', 'Very Fast', 'Intermediate', 1, 0, 'Some preferred',
     'Security,Networking,SIEM,Incident Response', 'Security Analyst Intern,SOC Intern', 1, 0),

    # 5. Computer Networks
    ('Network Engineer', 'Computer Networks', 'Computer Networks', 'Computer Networks,CSE,IT',
     'Design, implement, and maintain networks', '65-110', 87500, 'High', 'Steady', 'Intermediate', 1, 0, 'Some preferred',
     'Networking,Cisco,Routing,Switching,TCP/IP', 'Network Engineer Intern,IT Intern', 1, 0)
]

print(f"Inserting {len(roles_data)} career roles...")

# Insert all roles
cursor.executemany('''
INSERT INTO career_roles (
    role_name, category, primary_specialization, related_specializations,
    description, avg_salary_range, avg_salary_numeric, demand_level, growth_rate,
    difficulty, entry_friendly, remote_friendly, experience_required, tech_stack,
    related_internships, transferable_skills, specialization_heavy
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', roles_data)

print(f"Inserted {len(roles_data)} career roles!")

# ============================================
# INSERT ROADMAPS
# ============================================

print("Generating roadmaps...")

roadmaps = {
    1: [ # Software Engineer
        ('Foundation', 'Master the basics of programming and computer science', '2-3 months', [
            ('CS Fundamentals', 'Data Structures, Algorithms, OS, DBMS'),
            ('Programming Basics', 'Python/Java syntax, OOP concepts'),
            ('Version Control', 'Git, GitHub basics')
        ]),
        ('Development Skills', 'Build real-world applications', '3-4 months', [
            ('Web Basics', 'HTML, CSS, JavaScript'),
            ('Backend Dev', 'APIs, Databases, Frameworks (Flask/Django/Spring)'),
            ('System Design', 'Basic architecture, Scalability')
        ]),
        ('Advanced & Deployment', 'Go to production', '2-3 months', [
            ('Testing', 'Unit tests, Integration tests'),
            ('Deployment', 'Docker, CI/CD, Cloud basics'),
            ('Advanced Topics', 'Microservices, Security')
        ])
    ],
    2: [ # Data Scientist
        ('Data Foundation', 'Math and Programming basics', '3 months', [
            ('Mathematics', 'Linear Algebra, Calculus, Statistics'),
            ('Python for Data', 'NumPy, Pandas, Matplotlib'),
            ('SQL', 'Database querying and management')
        ]),
        ('Machine Learning', 'Core ML algorithms and techniques', '4 months', [
            ('Supervised Learning', 'Regression, Classification'),
            ('Unsupervised Learning', 'Clustering, PCA'),
            ('Model Evaluation', 'Metrics, Validation strategies')
        ]),
        ('Specialization', 'Advanced AI/ML topics', '3-4 months', [
            ('Deep Learning', 'Neural Networks, TensorFlow/PyTorch'),
            ('NLP/CV', 'Text or Image processing specific skills'),
            ('Deployment', 'Serving models, MLOps basics')
        ])
    ],
    3: [ # Cloud Solutions Architect
        ('Cloud Basics', 'Understanding cloud concepts', '2 months', [
            ('Networking', 'DNS, TCP/IP, HTTP, VPN'),
            ('Virtualization', 'VMs, Containers, Hypervisors'),
            ('Linux Basics', 'Shell scripting, File systems')
        ]),
        ('Cloud Provider Skills', 'Mastering AWS/Azure/GCP', '4 months', [
            ('Core Services', 'Compute (EC2), Storage (S3), Database (RDS)'),
            ('IAM & Security', 'Permissions, Roles, Best practices'),
            ('Serverless', 'Lambda, Cloud Functions')
        ]),
        ('Architecture', 'Designing scalable systems', '3 months', [
            ('High Availability', 'Load balancing, Auto-scaling'),
            ('Disaster Recovery', 'Backup strategies, Multi-region'),
            ('Cost Optimization', 'Budgeting, monitoring')
        ])
    ],
    4: [ # Cybersecurity Analyst
        ('Security Fundamentals', 'Core security concepts', '2 months', [
            ('Networking', 'OSI Model, Ports, Protocols'),
            ('OS Security', 'Windows/Linux hardening'),
            ('Threats & Attacks', 'Malware, Phishing, Social Engineering')
        ]),
        ('Defensive Security', 'Protecting systems', '3 months', [
            ('SIEM Tools', 'Splunk, ELK Stack'),
            ('Incident Response', 'Detection, Analysis, Containment'),
            ('Vulnerability Mgmt', 'Scanning, Patching')
        ]),
        ('Advanced Analysis', 'Deep dive into security', '3 months', [
            ('Forensics', 'Digital evidence handling'),
            ('Threat Hunting', 'Proactive search for threats'),
            ('Compliance', 'GDPR, HIPAA, NIST standards')
        ])
    ],
    5: [ # Network Engineer
        ('Network Basics', 'Understanding how networks work', '2 months', [
            ('Protocols', 'TCP/IP, UDP, ICMP, DNS, DHCP'),
            ('Hardware', 'Routers, Switches, Cables'),
            ('Subnetting', 'IP addressing, CIDR')
        ]),
        ('Routing & Switching', 'Configuring network devices', '3 months', [
            ('Routing Protocols', 'OSPF, EIGRP, BGP'),
            ('VLANs', 'Segmentation, Trunking'),
            ('Network Security', 'ACLs, Firewalls, VPNs')
        ]),
        ('Advanced Networking', 'Enterprise scale networking', '3 months', [
            ('SD-WAN', 'Software Defined Networking'),
            ('Automation', 'Python for Network Engineers, Ansible'),
            ('Cloud Networking', 'VPCs, Direct Connect')
        ])
    ]
}

for role_id, phases in roadmaps.items():
    for i, (p_name, p_desc, p_dur, topics) in enumerate(phases):
        # Insert Phase
        cursor.execute('''
            INSERT INTO roadmap_phases (role_id, phase_number, phase_name, phase_description, estimated_duration)
            VALUES (?, ?, ?, ?, ?)
        ''', (role_id, i+1, p_name, p_desc, p_dur))
        
        phase_id = cursor.lastrowid
        
        # Insert Topics
        for j, (t_name, t_desc) in enumerate(topics):
            cursor.execute('''
                INSERT INTO roadmap_topics (phase_id, topic_name, topic_order, description)
                VALUES (?, ?, ?, ?)
            ''', (phase_id, t_name, j+1, t_desc))

print("Roadmaps generated!")

# Commit changes
conn.commit()
conn.close()

print("\n" + "="*60)
print("Database creation complete!")
print("="*60)
print(f"\nSummary:")
print(f"   - {len(roles_data)} career roles")
print(f"   - {len(roadmaps)} roadmaps generated")
print(f"   - Advanced compatibility scoring system")
print(f"\nDatabase: database/career_compass.db")
print("\nReady for enhanced role matching!")
