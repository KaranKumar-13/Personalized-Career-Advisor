"""
Career Compass Platform - Advanced Backend
Intelligent role matching with compatibility scores
"""


from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

DATABASE = 'career_compass.db'

def get_mdn_link(topic_name):
    """
    Map topic names to MDN (Mozilla Developer Network) documentation URLs.
    Returns appropriate learning resource link based on topic name.
    """
    topic_lower = topic_name.lower()
    
    # Comprehensive MDN mapping
    mdn_mappings = {
        # Web Fundamentals
        'html': 'https://developer.mozilla.org/en-US/docs/Learn/HTML',
        'html basics': 'https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML',
        'html5': 'https://developer.mozilla.org/en-US/docs/Web/HTML',
        'css': 'https://developer.mozilla.org/en-US/docs/Learn/CSS',
        'css basics': 'https://developer.mozilla.org/en-US/docs/Learn/CSS/First_steps',
        'css3': 'https://developer.mozilla.org/en-US/docs/Web/CSS',
        'javascript': 'https://developer.mozilla.org/en-US/docs/Learn/JavaScript',
        'javascript basics': 'https://developer.mozilla.org/en-US/docs/Learn/JavaScript/First_steps',
        'js': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
        
        # Programming Fundamentals
        'python': 'https://docs.python.org/3/tutorial/',
        'python basics': 'https://docs.python.org/3/tutorial/introduction.html',
        'java': 'https://docs.oracle.com/javase/tutorial/',
        'c++': 'https://cplusplus.com/doc/tutorial/',
        'c': 'https://www.learn-c.org/',
        
        # Data Structures & Algorithms
        'data structures': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures',
        'algorithms': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
        'arrays': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array',
        'linked lists': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Indexed_collections',
        'trees': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
        'graphs': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
        
        # Web Development
        'dom': 'https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model',
        'dom manipulation': 'https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Manipulating_documents',
        'ajax': 'https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX',
        'fetch api': 'https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API',
        'promises': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise',
        'async/await': 'https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises',
        
        # Frameworks & Libraries
        'react': 'https://react.dev/learn',
        'vue': 'https://vuejs.org/guide/introduction.html',
        'angular': 'https://angular.io/docs',
        'node.js': 'https://nodejs.org/en/docs/guides/getting-started-guide',
        'express': 'https://expressjs.com/en/starter/installing.html',
        'django': 'https://docs.djangoproject.com/en/stable/intro/tutorial01/',
        'flask': 'https://flask.palletsprojects.com/en/latest/quickstart/',
        
        # Databases
        'sql': 'https://www.w3schools.com/sql/',
        'mysql': 'https://dev.mysql.com/doc/',
        'postgresql': 'https://www.postgresql.org/docs/current/tutorial.html',
        'mongodb': 'https://www.mongodb.com/docs/manual/tutorial/',
        'database design': 'https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Introduction',
        
        # Version Control
        'git': 'https://git-scm.com/doc',
        'github': 'https://docs.github.com/en/get-started',
        'version control': 'https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control',
        
        # APIs & Web Services
        'rest api': 'https://developer.mozilla.org/en-US/docs/Glossary/REST',
        'restful': 'https://developer.mozilla.org/en-US/docs/Glossary/REST',
        'graphql': 'https://graphql.org/learn/',
        'api': 'https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Introduction',
        
        # Testing
        'unit testing': 'https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Cross_browser_testing',
        'testing': 'https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing',
        'jest': 'https://jestjs.io/docs/getting-started',
        
        # DevOps & Tools
        'docker': 'https://docs.docker.com/get-started/',
        'kubernetes': 'https://kubernetes.io/docs/tutorials/',
        'ci/cd': 'https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools',
        
        # Security
        'web security': 'https://developer.mozilla.org/en-US/docs/Web/Security',
        'https': 'https://developer.mozilla.org/en-US/docs/Glossary/HTTPS',
        'authentication': 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication',
        'oauth': 'https://oauth.net/2/',
        
        # Performance
        'performance': 'https://developer.mozilla.org/en-US/docs/Web/Performance',
        'optimization': 'https://developer.mozilla.org/en-US/docs/Learn/Performance',
        
        # Mobile
        'responsive design': 'https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design',
        'mobile development': 'https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps',
        
        # Cloud & Infrastructure
        'aws': 'https://aws.amazon.com/getting-started/',
        'azure': 'https://learn.microsoft.com/en-us/azure/',
        'cloud computing': 'https://aws.amazon.com/what-is-cloud-computing/',
        
        # AI & ML
        'machine learning': 'https://developers.google.com/machine-learning/crash-course',
        'deep learning': 'https://www.deeplearning.ai/',
        'neural networks': 'https://www.tensorflow.org/tutorials',
        'tensorflow': 'https://www.tensorflow.org/learn',
        'pytorch': 'https://pytorch.org/tutorials/',
        
        # Data Science
        'data analysis': 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/',
        'pandas': 'https://pandas.pydata.org/docs/getting_started/index.html',
        'numpy': 'https://numpy.org/doc/stable/user/absolute_beginners.html',
        'data visualization': 'https://matplotlib.org/stable/tutorials/index.html',
    }
    
    # Check for exact matches first
    for key, url in mdn_mappings.items():
        if key in topic_lower:
            return url
    
    # Default to MDN web docs if no match
    return 'https://developer.mozilla.org/en-US/docs/Learn'

# Database helper
def get_db():
    conn = sqlite3.connect('database/career_compass.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def require_login():
    allowed_routes = ['login', 'static', 'index'] # Index redirects to login anyway
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

# ==========================================
# ADVANCED COMPATIBILITY SCORING ENGINE
# ==========================================

def calculate_compatibility(user_profile, role):
    """
    Advanced multi-factor compatibility scoring
    Returns score out of 100 with detailed breakdown
    """
    
    breakdown = {}
    total_score = 0
    
    # FACTOR 1: Specialization Match (30 points)
    spec_score = 0
    user_spec = user_profile.get('specialization', '')
    
    if user_spec == role['primary_specialization']:
        spec_score = 30
        breakdown['spec_reason'] = f"Perfect match for {user_spec}"
    elif user_spec in role['related_specializations'].split(','):
        spec_score = 15
        breakdown['spec_reason'] = f"Good match for {user_spec}"
    else:
        spec_score = 5
        breakdown['spec_reason'] = "Can transition to this role"
    
    breakdown['specialization'] = spec_score
    total_score += spec_score
    
    # FACTOR 2: Skills Match (45 points)
    user_skills = user_profile.get('skills', {})
    required_skills = role['tech_stack'].split(',') if role['tech_stack'] else []
    
    matched_skills = []
    missing_skills = []
    skills_score = 0
    
    if required_skills:
        skill_value = 45.0 / len(required_skills)
        
        for req_skill in required_skills:
            req_skill = req_skill.strip()
            found = False
            
            for user_skill, level in user_skills.items():
                if req_skill.lower() in user_skill.lower() or user_skill.lower() in req_skill.lower():
                    found = True
                    # Weighted by proficiency
                    if level == 'Advanced':
                        skills_score += skill_value
                        matched_skills.append(f"{user_skill} (Advanced ✓)")
                    elif level == 'Intermediate':
                        skills_score += skill_value * 0.8
                        matched_skills.append(f"{user_skill} (Good ✓)")
                    else:  # Beginner
                        skills_score += skill_value * 0.5
                        matched_skills.append(f"{user_skill} (Basic)")
                    break
            
            if not found:
                missing_skills.append(req_skill)
    
    # Cap at 45
    skills_score = min(45, round(skills_score))
    breakdown['skills'] = skills_score
    breakdown['matched_skills'] = matched_skills
    breakdown['missing_skills'] = missing_skills
    total_score += skills_score
    
    # FACTOR 3: Interest Alignment (20 points)
    interest_score = 0
    interests = user_profile.get('interest_areas', [])
    
    if role['category'] in interests:
        interest_score = 20
        breakdown['interest_reason'] = f"Perfect match with your {role['category']} interest"
    elif any(interest in role['category'] for interest in interests):
        interest_score = 10
        breakdown['interest_reason'] = "Related to your interests"
    else:
        interest_score = 5
        breakdown['interest_reason'] = "Good career exploration opportunity"
    
    breakdown['interest'] = interest_score
    total_score += interest_score
    
    # FACTOR 4: Career Goals (5 points)
    goal_score = 0
    career_goal = user_profile.get('career_goal', 'First Job')
    timeline = user_profile.get('timeline', '6 months')
    
    if career_goal == 'First Job' and role['entry_friendly']:
        goal_score += 3
    
    if timeline == '3 months' and role['difficulty'] == 'Beginner':
        goal_score += 2
    elif timeline == '6 months' and role['difficulty'] in ['Beginner', 'Intermediate']:
        goal_score += 2
    else:
        goal_score += 1
    
    breakdown['goals'] = min(5, goal_score)
    total_score += breakdown['goals']
    
    # BONUSES (up to 10 points)
    bonus_score = 0
    bonuses = []
    
    if role['demand_level'] == 'Very High':
        bonus_score += 3
        bonuses.append("🔥 Very high market demand (+3)")
    
    if role['growth_rate'] in ['Fast', 'Very Fast']:
        bonus_score += 2
        bonuses.append("🚀 Fast growing field (+2)")
    
    if role['remote_friendly']:
        bonus_score += 2
        bonuses.append("🏢 Remote work friendly (+2)")
    
    if role['entry_friendly'] and user_profile.get('current_year', 3) <= 2:
        bonus_score += 3
        bonuses.append("🎓 Perfect for early career (+3)")
    
    breakdown['bonuses'] = bonus_score
    breakdown['bonus_list'] = bonuses
    total_score += bonus_score
    
    # PENALTIES
    penalty = 0
    penalties = []
    
    if len(missing_skills) >= 3:
        penalty += 5
        penalties.append(f"⚠️ Missing {len(missing_skills)} critical skills (-5)")
    
    if not role['entry_friendly'] and role['experience_required'] == 'Required':
        penalty += 3
        penalties.append("⚠️ Experience preferred (-3)")
    
    breakdown['penalties'] = penalty
    breakdown['penalty_list'] = penalties
    total_score -= penalty
    
    # Final score (0-100)
    final_score = max(0, min(100, total_score))
    
    # Generate grade
    if final_score >= 90:
        grade = 'A+'
        match_level = '🌟 Excellent Match'
    elif final_score >= 85:
        grade = 'A'
        match_level = '✅ Strong Match'
    elif final_score >= 75:
        grade = 'B+'
        match_level = '👍 Good Match'
    elif final_score >= 65:
        grade = 'B'
        match_level = '✓ Decent Match'
    elif final_score >= 55:
        grade = 'C+'
        match_level = '○ Fair Match'
    else:
        grade = 'C'
        match_level = '⚠️ Moderate Match'
    
    return {
        'score': final_score,
        'grade': grade,
        'match_level': match_level,
        'breakdown': breakdown
    }

# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/home')
def home():
    """Home page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    is_parent = session.get('user_type') == 'parent'
    return render_template('index.html', is_parent=is_parent)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect
    if 'user_id' in session:
        if session.get('user_type') == 'parent':
            return redirect(url_for('dashboard'))
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('login.html')
    
    action = request.form.get('action')
    email = request.form.get('email')
    password = request.form.get('password')
    user_type = request.form.get('user_type', 'student')
    child_email = request.form.get('child_email')
    
    db = get_db()
    
    if action == 'register':
        name = request.form.get('name')
        try:
            db.execute('INSERT INTO users (name, email, password, user_type, specialization) VALUES (?, ?, ?, ?, ?)',
                       (name, email, password, user_type, 'Not Set'))
            db.commit()
            
            # Auto login
            user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            session['user_id'] = user['id']
            session['user_type'] = user['user_type']
            session['name'] = user['name']
            
            if user_type == 'parent':
                if child_email:
                    session['child_email'] = child_email
                return redirect(url_for('dashboard'))
            return redirect(url_for('home'))
            
        except sqlite3.IntegrityError:
            return "Email already exists", 400
        finally:
            db.close()
            
    else: # Login
        user = db.execute('SELECT * FROM users WHERE email = ? AND password = ? AND user_type = ?', 
                          (email, password, user_type)).fetchone()
        db.close()
        
        if user:
            session['user_id'] = user['id']
            session['user_type'] = user['user_type']
            session['name'] = user['name']
            
            if user_type == 'parent':
                if child_email:
                    session['child_email'] = child_email
                return redirect(url_for('dashboard'))
            return redirect(url_for('home'))
        else:
            return "Invalid credentials", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if session.get('user_type') != 'parent':
        return redirect(url_for('login'))
        
    db = get_db()
    
    # Filter by linked child email if available
    child_email = session.get('child_email')
    
    query = '''
        SELECT u.id, u.name, u.email, u.specialization, u.current_year, up.* 
        FROM users u 
        LEFT JOIN user_preferences up ON u.id = up.user_id 
        WHERE u.user_type = 'student'
    '''
    
    params = ()
    
    if child_email:
        query += ' AND u.email = ?'
        params = (child_email,)
        
    students_data = db.execute(query, params).fetchall()
    
    students_list = []
    
    # We need to recalculate roles for each student to show in dashboard
    roles = db.execute('SELECT * FROM career_roles').fetchall()
    
    for student in students_data:
        if not student['skills']: # Skip users without preferences set
            continue
            
        # Reconstruct profile
        profile = {
            'name': student['name'],
            'specialization': student['specialization'],
            'skills': json.loads(student['skills']) if student['skills'] else {},
            'interest_areas': json.loads(student['interest_areas']) if student['interest_areas'] else [],
            'career_goal': student['career_goal'],
            'timeline': student['timeline'],
            'current_year': student['current_year']
        }
        
        # Calculate top roles
        student_roles = []
        for role in roles:
            role_dict = dict(role)
            compatibility = calculate_compatibility(profile, role_dict)
            student_roles.append({
                'name': role_dict['role_name'],
                'score': compatibility['score']
            })
        
        student_roles.sort(key=lambda x: x['score'], reverse=True)
        
        students_list.append({
            'name': student['name'],
            'email': student['email'],
            'career_goal': student['career_goal'],
            'current_year': student['current_year'],
            'specialization': student['specialization'],
            'roles': student_roles[:3], # Top 3
            'skills': list(profile['skills'].keys()),
            'interests': profile['interest_areas']
        })
    
    db.close()
    return render_template('dashboard.html', students=students_list)

@app.route('/student-dashboard')
def student_dashboard():
    """Student's personal dashboard"""
    if session.get('user_type') != 'student':
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    db = get_db()
    
    # Get user basic info
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    # Get user preferences
    preferences = db.execute('SELECT * FROM user_preferences WHERE user_id = ?', (user_id,)).fetchone()
    
    # Check if user has completed their profile
    if not preferences or not preferences['skills']:
        # User hasn't completed profile yet
        db.close()
        return render_template('student_dashboard.html', 
                             user_name=user['name'],
                             has_profile=False)
    
    # Reconstruct profile
    profile = {
        'name': user['name'],
        'specialization': user['specialization'],
        'skills': json.loads(preferences['skills']) if preferences['skills'] else {},
        'interest_areas': json.loads(preferences['interest_areas']) if preferences['interest_areas'] else [],
        'career_goal': preferences['career_goal'],
        'timeline': preferences['timeline'],
        'current_year': user['current_year']
    }
    
    # Get all roles and calculate compatibility
    roles = db.execute('SELECT * FROM career_roles').fetchall()
    
    role_recommendations = []
    for role in roles:
        role_dict = dict(role)
        compatibility = calculate_compatibility(profile, role_dict)
        
        role_recommendations.append({
            'id': role_dict['id'],
            'name': role_dict['role_name'],
            'category': role_dict['category'],
            'description': role_dict['description'],
            'salary': role_dict['avg_salary_range'],
            'demand': role_dict['demand_level'],
            'score': compatibility['score'],
            'grade': compatibility['grade'],
            'match_level': compatibility['match_level']
        })
    
    # Sort by score
    role_recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    db.close()
    
    return render_template('student_dashboard.html',
                         user_name=user['name'],
                         has_profile=True,
                         profile=profile,
                         top_roles=role_recommendations[:5])

@app.route('/api/suggest-roles', methods=['POST'])
def suggest_roles():
    """
    Advanced role suggestion with compatibility scoring
    """
    data = request.json
    
    # Extract user profile
    user_profile = {
        'name': data.get('name'),
        'specialization': data.get('specialization'),
        'skills': data.get('skills', {}),  # {skill: level}
        'interest_areas': data.get('interest_areas', []),
        'career_goal': data.get('career_goal', 'First Job'),
        'timeline': data.get('timeline', '6 months'),
        'current_year': data.get('current_year', 2)
    }
    
    # Save to database if logged in (or if we can match by email/name - simplistic for now)
    # We'll rely on session if available, otherwise just calculate
    if 'user_id' in session and session.get('user_type') == 'student':
        db = get_db()
        user_id = session['user_id']
        
        # Update user basic info
        db.execute('UPDATE users SET specialization = ?, current_year = ? WHERE id = ?',
                   (user_profile['specialization'], user_profile['current_year'], user_id))
        
        # Update preferences
        # Check if preferences exist
        existing = db.execute('SELECT id FROM user_preferences WHERE user_id = ?', (user_id,)).fetchone()
        
        if existing:
            db.execute('''
                UPDATE user_preferences SET 
                skills = ?, interest_areas = ?, career_goal = ?, timeline = ?
                WHERE user_id = ?
            ''', (json.dumps(user_profile['skills']), json.dumps(user_profile['interest_areas']),
                  user_profile['career_goal'], user_profile['timeline'], user_id))
        else:
            db.execute('''
                INSERT INTO user_preferences (user_id, skills, interest_areas, career_goal, timeline)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, json.dumps(user_profile['skills']), json.dumps(user_profile['interest_areas']),
                  user_profile['career_goal'], user_profile['timeline']))
            
        db.commit()
        db.close()
    
    # Get all roles
    db = get_db()
    roles = db.execute('SELECT * FROM career_roles').fetchall()
    
    # Calculate compatibility for each role
    role_scores = []
    
    for role in roles:
        role_dict = dict(role)
        compatibility = calculate_compatibility(user_profile, role_dict)
        
        role_scores.append({
            'role_id': role_dict['id'],
            'role_name': role_dict['role_name'],
            'category': role_dict['category'],
            'description': role_dict['description'],
            'salary': role_dict['avg_salary_range'],
            'demand': role_dict['demand_level'],
            'difficulty': role_dict['difficulty'],
            'remote_friendly': bool(role_dict['remote_friendly']),
            'compatibility': compatibility
        })
    
    # Sort by score
    role_scores.sort(key=lambda x: x['compatibility']['score'], reverse=True)
    
    # Return top 5
    top_roles = role_scores[:5]
    
    db.close()
    
    return jsonify({
        'success': True,
        'user_name': user_profile['name'],
        'roles': top_roles
    })

@app.route('/api/role/<int:role_id>')
def get_role_details(role_id):
    """Get detailed role information"""
    db = get_db()
    role = db.execute('SELECT * FROM career_roles WHERE id = ?', (role_id,)).fetchone()
    
    if not role:
        return jsonify({'success': False, 'message': 'Role not found'}), 404
    
    role_dict = dict(role)
    db.close()
    
    return jsonify({
        'success': True,
        'role': role_dict
    })

@app.route('/api/roadmap/<int:role_id>')
def get_roadmap(role_id):
    """Get roadmap for a role"""
    db = get_db()
    
    # Get role
    role = db.execute('SELECT * FROM career_roles WHERE id = ?', (role_id,)).fetchone()
    
    if not role:
        return jsonify({'success': False, 'message': 'Role not found'}), 404
    
    # Get phases
    phases = db.execute('''
        SELECT * FROM roadmap_phases 
        WHERE role_id = ? 
        ORDER BY phase_number
    ''', (role_id,)).fetchall()
    
    roadmap = []
    for phase in phases:
        topics = db.execute('''
            SELECT * FROM roadmap_topics 
            WHERE phase_id = ? 
            ORDER BY topic_order
        ''', (phase['id'],)).fetchall()
        
        # Convert topics to dict and add MDN links
        topics_list = []
        for topic in topics:
            topic_dict = dict(topic)
            # If resource_link is null or empty, generate MDN link
            if not topic_dict.get('resource_link'):
                topic_dict['resource_link'] = get_mdn_link(topic_dict['topic_name'])
            topics_list.append(topic_dict)
        
        roadmap.append({
            'phase_number': phase['phase_number'],
            'phase_name': phase['phase_name'],
            'description': phase['phase_description'],
            'duration': phase['estimated_duration'],
            'topics': topics_list
        })
    
    db.close()
    
    return jsonify({
        'success': True,
        'role': dict(role),
        'roadmap': roadmap
    })

@app.route('/roles')
def roles_page():
    """Role suggestions page"""
    return render_template('roles.html')

# ==========================================
# ENROLLMENT & PROGRESS TRACKING APIs
# ==========================================

@app.route('/api/enroll', methods=['POST'])
def enroll_in_role():
    """Enroll student in a career role"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    data = request.get_json()
    role_id = data.get('role_id')
    user_id = session['user_id']
    
    if not role_id:
        return jsonify({'success': False, 'message': 'Role ID required'}), 400
    
    db = get_db()
    
    # Check if already enrolled
    existing = db.execute(
        'SELECT * FROM student_enrollments WHERE user_id = ? AND role_id = ?',
        (user_id, role_id)
    ).fetchone()
    
    if existing:
        return jsonify({'success': False, 'message': 'Already enrolled in this role'}), 400
    
    # Get role name
    role = db.execute('SELECT role_name FROM career_roles WHERE id = ?', (role_id,)).fetchone()
    
    if not role:
        return jsonify({'success': False, 'message': 'Role not found'}), 404
    
    # Create enrollment
    cursor = db.execute(
        'INSERT INTO student_enrollments (user_id, role_id) VALUES (?, ?)',
        (user_id, role_id)
    )
    db.commit()
    enrollment_id = cursor.lastrowid
    db.close()
    
    return jsonify({
        'success': True,
        'message': f'Successfully enrolled in {role["role_name"]}!',
        'enrollment_id': enrollment_id
    })

@app.route('/api/my-enrollments')
def get_my_enrollments():
    """Get current user's enrollments with progress"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    user_id = session['user_id']
    db = get_db()
    
    enrollments = db.execute('''
        SELECT e.id, e.role_id, e.enrolled_at, e.status, r.role_name, r.description
        FROM student_enrollments e
        JOIN career_roles r ON e.role_id = r.id
        WHERE e.user_id = ?
        ORDER BY e.enrolled_at DESC
    ''', (user_id,)).fetchall()
    
    result = []
    for enrollment in enrollments:
        # Get total topics for this role
        total_topics = db.execute('''
            SELECT COUNT(*) as count
            FROM roadmap_topics rt
            JOIN roadmap_phases rp ON rt.phase_id = rp.id
            WHERE rp.role_id = ?
        ''', (enrollment['role_id'],)).fetchone()
        
        # Get completed topics
        completed_topics = db.execute('''
            SELECT COUNT(*) as count
            FROM topic_progress
            WHERE user_id = ? AND role_id = ? AND completed = 1
        ''', (user_id, enrollment['role_id'])).fetchone()
        
        total = total_topics['count'] if total_topics else 0
        completed = completed_topics['count'] if completed_topics else 0
        progress = round((completed / total * 100) if total > 0 else 0, 1)
        
        result.append({
            'id': enrollment['id'],
            'role_id': enrollment['role_id'],
            'role_name': enrollment['role_name'],
            'description': enrollment['description'],
            'enrolled_at': enrollment['enrolled_at'],
            'status': enrollment['status'],
            'progress_percentage': progress,
            'completed_topics': completed,
            'total_topics': total
        })
    
    db.close()
    
    return jsonify({
        'success': True,
        'enrollments': result
    })

@app.route('/api/progress/toggle', methods=['POST'])
def toggle_topic_progress():
    """Mark topic as complete/incomplete"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    data = request.get_json()
    role_id = data.get('role_id')
    topic_id = data.get('topic_id')
    completed = data.get('completed', True)
    user_id = session['user_id']
    
    if not role_id or not topic_id:
        return jsonify({'success': False, 'message': 'Missing parameters'}), 400
    
    db = get_db()
    
    # Check if progress record exists
    existing = db.execute('''
        SELECT * FROM topic_progress 
        WHERE user_id = ? AND role_id = ? AND topic_id = ?
    ''', (user_id, role_id, topic_id)).fetchone()
    
    if existing:
        # Update existing record
        db.execute('''
            UPDATE topic_progress 
            SET completed = ?, completed_at = CASE WHEN ? = 1 THEN CURRENT_TIMESTAMP ELSE NULL END
            WHERE user_id = ? AND role_id = ? AND topic_id = ?
        ''', (1 if completed else 0, 1 if completed else 0, user_id, role_id, topic_id))
    else:
        # Create new record
        db.execute('''
            INSERT INTO topic_progress (user_id, role_id, topic_id, completed, completed_at)
            VALUES (?, ?, ?, ?, CASE WHEN ? = 1 THEN CURRENT_TIMESTAMP ELSE NULL END)
        ''', (user_id, role_id, topic_id, 1 if completed else 0, 1 if completed else 0))
    
    db.commit()
    
    # Calculate new progress percentage
    total_topics = db.execute('''
        SELECT COUNT(*) as count
        FROM roadmap_topics rt
        JOIN roadmap_phases rp ON rt.phase_id = rp.id
        WHERE rp.role_id = ?
    ''', (role_id,)).fetchone()
    
    completed_topics = db.execute('''
        SELECT COUNT(*) as count
        FROM topic_progress
        WHERE user_id = ? AND role_id = ? AND completed = 1
    ''', (user_id, role_id)).fetchone()
    
    total = total_topics['count'] if total_topics else 0
    completed_count = completed_topics['count'] if completed_topics else 0
    progress = round((completed_count / total * 100) if total > 0 else 0, 1)
    
    db.close()
    
    return jsonify({
        'success': True,
        'completed': completed,
        'progress_percentage': progress,
        'completed_topics': completed_count,
        'total_topics': total
    })

@app.route('/api/progress/<int:role_id>')
def get_role_progress(role_id):
    """Get progress for a specific role"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    user_id = session['user_id']
    db = get_db()
    
    # Get completed topic IDs
    completed = db.execute('''
        SELECT topic_id FROM topic_progress
        WHERE user_id = ? AND role_id = ? AND completed = 1
    ''', (user_id, role_id)).fetchall()
    
    completed_ids = [row['topic_id'] for row in completed]
    
    # Calculate progress
    total_topics = db.execute('''
        SELECT COUNT(*) as count
        FROM roadmap_topics rt
        JOIN roadmap_phases rp ON rt.phase_id = rp.id
        WHERE rp.role_id = ?
    ''', (role_id,)).fetchone()
    
    total = total_topics['count'] if total_topics else 0
    progress = round((len(completed_ids) / total * 100) if total > 0 else 0, 1)
    
    db.close()
    
    return jsonify({
        'success': True,
        'role_id': role_id,
        'completed_topics': completed_ids,
        'progress_percentage': progress,
        'total_topics': total
    })

@app.route('/roadmap/<int:role_id>')
def roadmap_page(role_id):
    """Roadmap display page"""
    return render_template('roadmap.html', role_id=role_id)

@app.route('/api/specializations')
def get_specializations():
    """Get all specializations"""
    specializations = [
        'Software Engineering',
        'AI & ML',
        'Cloud Computing',
        'Data Science',
        'Cyber Security',
        'Computer Networks',
        'Mobile Computing'
    ]
    return jsonify({'specializations': specializations})

if __name__ == '__main__':
    print("\n" + "="*60)
    print(" Career Compass Platform Starting...")
    print("="*60)
    print("\n Server: http://localhost:5000")
    print(" Advanced compatibility scoring enabled")
    print(" Press CTRL+C to stop\n")
    
    # app.run(debug=True, host='0.0.0.0', port=5000)
if __name__ == "__main__":
    app.run()
    