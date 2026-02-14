// Career Compass - Main JavaScript
// Handles form submission, dark mode, and user interactions

// ==========================================
// SKILLS DATA
// ==========================================

const skillsData = [
    // Programming Languages
    { name: 'Python', category: 'Programming' },
    { name: 'JavaScript', category: 'Programming' },
    { name: 'Java', category: 'Programming' },
    { name: 'C++', category: 'Programming' },
    { name: 'C#', category: 'Programming' },
    { name: 'Go', category: 'Programming' },
    { name: 'Rust', category: 'Programming' },
    { name: 'PHP', category: 'Programming' },
    { name: 'Ruby', category: 'Programming' },
    { name: 'Swift', category: 'Programming' },
    { name: 'Kotlin', category: 'Programming' },
    { name: 'Dart', category: 'Programming' },

    // Web Development
    { name: 'HTML', category: 'Web' },
    { name: 'CSS', category: 'Web' },
    { name: 'React', category: 'Web' },
    { name: 'Angular', category: 'Web' },
    { name: 'Vue.js', category: 'Web' },
    { name: 'Node.js', category: 'Web' },
    { name: 'Next.js', category: 'Web' },
    { name: 'TypeScript', category: 'Web' },
    { name: 'Tailwind CSS', category: 'Web' },

    // Mobile
    { name: 'React Native', category: 'Mobile' },
    { name: 'Flutter', category: 'Mobile' },
    { name: 'Android Development', category: 'Mobile' },
    { name: 'iOS Development', category: 'Mobile' },

    // Database
    { name: 'SQL', category: 'Database' },
    { name: 'PostgreSQL', category: 'Database' },
    { name: 'MySQL', category: 'Database' },
    { name: 'MongoDB', category: 'Database' },
    { name: 'Redis', category: 'Database' },

    // AI/ML
    { name: 'Machine Learning', category: 'AI/ML' },
    { name: 'Deep Learning', category: 'AI/ML' },
    { name: 'TensorFlow', category: 'AI/ML' },
    { name: 'PyTorch', category: 'AI/ML' },
    { name: 'NLP', category: 'AI/ML' },
    { name: 'Computer Vision', category: 'AI/ML' },

    // Data Science
    { name: 'Data Analysis', category: 'Data' },
    { name: 'Data Visualization', category: 'Data' },
    { name: 'Statistics', category: 'Data' },
    { name: 'Excel', category: 'Data' },
    { name: 'Power BI', category: 'Data' },
    { name: 'Tableau', category: 'Data' },

    // Cloud & DevOps
    { name: 'AWS', category: 'Cloud' },
    { name: 'Azure', category: 'Cloud' },
    { name: 'GCP', category: 'Cloud' },
    { name: 'Docker', category: 'DevOps' },
    { name: 'Kubernetes', category: 'DevOps' },
    { name: 'CI/CD', category: 'DevOps' },
    { name: 'Linux', category: 'DevOps' },

    // Security
    { name: 'Cybersecurity', category: 'Security' },
    { name: 'Penetration Testing', category: 'Security' },
    { name: 'Network Security', category: 'Security' },

    // Networking
    { name: 'Networking', category: 'Networks' },
    { name: 'TCP/IP', category: 'Networks' },
    { name: 'DNS', category: 'Networks' },

    // Others
    { name: 'Git', category: 'Tools' },
    { name: 'APIs', category: 'Tools' },
    { name: 'Testing', category: 'Tools' },
    { name: 'Agile', category: 'Tools' }
];

// ==========================================
// INITIALIZE PAGE
// ==========================================

document.addEventListener('DOMContentLoaded', function () {
    // Populate skills grid
    populateSkills();

    // Setup form handlers
    setupFormHandlers();

    // Setup theme toggle
    setupThemeToggle();
});

// ==========================================
// POPULATE SKILLS GRID
// ==========================================

const visibleSkills = new Set();
const allSkills = skillsData;

function populateSkills() {
    const skillsGrid = document.getElementById('skillsGrid');
    if (!skillsGrid) return;

    // Clear grid
    skillsGrid.innerHTML = '';

    // Add first 10 skills
    const initialSkills = allSkills.slice(0, 10);
    initialSkills.forEach(skill => {
        addSkillToGrid(skill, skillsGrid);
        visibleSkills.add(skill.name);
    });

    // Create search/add container
    const addSkillContainer = document.createElement('div');
    addSkillContainer.className = 'add-skill-container';
    addSkillContainer.style.marginTop = '1rem';
    addSkillContainer.style.position = 'relative';

    addSkillContainer.innerHTML = `
        <input type="text" id="skillSearch" class="form-input" placeholder="Search and add more skills..." autocomplete="off">
        <div id="skillSearchResults" class="skill-search-results" style="display: none; position: absolute; top: 100%; left: 0; right: 0; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--border-radius-sm); max-height: 200px; overflow-y: auto; z-index: 100; box-shadow: var(--shadow-md);"></div>
    `;

    skillsGrid.parentElement.appendChild(addSkillContainer);

    const searchInput = document.getElementById('skillSearch');
    const searchResults = document.getElementById('skillSearchResults');

    searchInput.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        if (query.length < 1) {
            searchResults.style.display = 'none';
            return;
        }

        const matches = allSkills.filter(skill =>
            !visibleSkills.has(skill.name) &&
            skill.name.toLowerCase().includes(query)
        );

        if (matches.length > 0) {
            searchResults.innerHTML = matches.map(skill => `
                <div class="skill-search-item" style="padding: 0.5rem; cursor: pointer; border-bottom: 1px solid var(--border-color); color: var(--text-primary);" data-skill-name="${skill.name}">
                    ${skill.name} <span style="font-size: 0.8em; color: var(--text-secondary);">(${skill.category})</span>
                </div>
            `).join('');
            searchResults.style.display = 'block';

            // Add click handlers
            searchResults.querySelectorAll('.skill-search-item').forEach(item => {
                item.addEventListener('click', function () {
                    const skillName = this.dataset.skillName;
                    const skillObj = allSkills.find(s => s.name === skillName);

                    addSkillToGrid(skillObj, skillsGrid);
                    visibleSkills.add(skillName);

                    searchInput.value = '';
                    searchResults.style.display = 'none';

                    // Auto-check the newly added skill
                    const checkbox = document.getElementById(`skill-${skillName.replace(/\s+/g, '-').toLowerCase()}`);
                    if (checkbox) {
                        checkbox.checked = true;
                        checkbox.dispatchEvent(new Event('change'));
                    }
                });
            });
        } else {
            searchResults.style.display = 'none';
        }
    });

    // Close search results when clicking outside
    document.addEventListener('click', function (e) {
        if (!addSkillContainer.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
}

function addSkillToGrid(skill, container) {
    const skillItem = document.createElement('div');
    skillItem.className = 'skill-item';

    skillItem.innerHTML = `
        <input type="checkbox" 
               id="skill-${skill.name.replace(/\s+/g, '-').toLowerCase()}" 
               class="skill-checkbox"
               value="${skill.name}">
        <label for="skill-${skill.name.replace(/\s+/g, '-').toLowerCase()}" 
               class="skill-label">
            <span class="skill-name">${skill.name}</span>
            <select class="skill-level-select" style="display: none;">
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
            </select>
        </label>
    `;

    container.appendChild(skillItem);

    // Show level selector when skill is checked
    const checkbox = skillItem.querySelector('.skill-checkbox');
    const levelSelect = skillItem.querySelector('.skill-level-select');

    checkbox.addEventListener('change', function () {
        if (this.checked) {
            levelSelect.style.display = 'block';
        } else {
            levelSelect.style.display = 'none';
        }
    });
}

// ==========================================
// FORM HANDLERS
// ==========================================

function setupFormHandlers() {


    // Form submission
    const careerForm = document.getElementById('careerForm');
    if (careerForm) {
        careerForm.addEventListener('submit', handleFormSubmit);
    }

    // Interest checkboxes (limit to 3)
    const interestCheckboxes = document.querySelectorAll('.interest-checkbox');
    interestCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const checked = document.querySelectorAll('.interest-checkbox:checked');
            if (checked.length > 3) {
                this.checked = false;
                alert('Please select maximum 3 areas of interest');
            }
        });
    });
}

// ==========================================
// HANDLE FORM SUBMISSION
// ==========================================

async function handleFormSubmit(e) {
    e.preventDefault();

    // Get form data
    const name = document.getElementById('name').value;
    const specialization = document.querySelector('input[name="specialization"]:checked')?.value;
    const currentYear = parseInt(document.querySelector('input[name="currentYear"]:checked')?.value || '0');
    const careerGoal = document.querySelector('input[name="careerGoal"]:checked')?.value;
    const timeline = document.querySelector('input[name="timeline"]:checked')?.value;

    if (!name || !specialization || !currentYear || !careerGoal || !timeline) {
        alert('Please fill in all fields!');
        return;
    }

    // Get selected skills with levels
    const skills = {};
    document.querySelectorAll('.skill-checkbox:checked').forEach(checkbox => {
        const skillName = checkbox.value;
        const levelSelect = checkbox.parentElement.querySelector('.skill-level-select');
        const level = levelSelect ? levelSelect.value : 'Beginner';
        skills[skillName] = level;
    });

    // Validate skills
    if (Object.keys(skills).length === 0) {
        alert('Please select at least one skill!');
        return;
    }

    // Get interest areas
    const interestAreas = [];
    document.querySelectorAll('.interest-checkbox:checked').forEach(checkbox => {
        interestAreas.push(checkbox.value);
    });

    // Prepare data
    const userData = {
        name,
        specialization,
        current_year: currentYear,
        skills,
        interest_areas: interestAreas,
        career_goal: careerGoal,
        timeline
    };

    // Show loading
    document.getElementById('careerForm').style.display = 'none';
    document.getElementById('loading').style.display = 'block';

    try {
        // Call API
        const response = await fetch('/api/suggest-roles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();

        if (data.success) {
            // Store in localStorage
            localStorage.setItem('rolesData', JSON.stringify(data));

            // Redirect to roles page
            window.location.href = '/roles';
        } else {
            alert('Error getting recommendations. Please try again.');
            document.getElementById('loading').style.display = 'none';
            document.getElementById('careerForm').style.display = 'block';
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to connect to server. Please try again.');
        document.getElementById('loading').style.display = 'none';
        document.getElementById('careerForm').style.display = 'block';
    }
}

// ==========================================
// THEME TOGGLE
// ==========================================

function setupThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;

    // Get saved theme or default to light
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Update checkbox state based on current theme
    themeToggle.checked = (currentTheme === 'dark');

    // Toggle theme on checkbox change
    themeToggle.addEventListener('change', function () {
        const newTheme = this.checked ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}



// ==========================================
// UTILITY FUNCTIONS
// ==========================================

// Console welcome message
console.log(`
╔═══════════════════════════════════════╗
║   Career Compass Platform v1.0        ║
║   Find Your Perfect Tech Career 🚀    ║
╚═══════════════════════════════════════╝
`);
