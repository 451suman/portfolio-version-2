// ====== THEME SYSTEM ====== //
// Dark/Light theme toggle with localStorage persistence

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    
    // Add theme toggle event listener
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Add theme transition class removal after transition completes
    setTimeout(() => {
        document.body.classList.remove('theme-transition');
    }, 300);
});

function initializeTheme() {
    // Get saved theme from localStorage or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    
    // Apply theme
    setTheme(savedTheme);
    
    // Add transition class for smooth theme switching
    document.body.classList.add('theme-transition');
}

function setTheme(theme) {
    const body = document.body;
    const themeIcon = document.getElementById('themeIcon');
    
    // Set data-theme attribute
    body.setAttribute('data-theme', theme);
    
    // Update theme icon
    if (themeIcon) {
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-moon';
        } else {
            themeIcon.className = 'fas fa-sun';
        }
    }
    
    // Save theme to localStorage
    localStorage.setItem('theme', theme);
    
    // Update theme CSS link
    updateThemeCSS(theme);
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    // Add transition class
    document.body.classList.add('theme-transition');
    
    // Set new theme
    setTheme(newTheme);
    
    // Remove transition class after animation completes
    setTimeout(() => {
        document.body.classList.remove('theme-transition');
    }, 300);
    
    // Dispatch theme change event
    const event = new CustomEvent('themeChanged', {
        detail: { theme: newTheme }
    });
    document.dispatchEvent(event);
}

function updateThemeCSS(theme) {
    const themeCSS = document.getElementById('theme-css');
    if (themeCSS) {
        // Update CSS file based on theme
        if (theme === 'dark') {
            themeCSS.href = '/static/css/dark-theme.css';
        } else {
            themeCSS.href = '/static/css/light-theme.css';
        }
    }
}

// ====== THEME TRANSITION STYLES ====== //
const style = document.createElement('style');
style.textContent = `
    .theme-transition,
    .theme-transition *,
    .theme-transition *::before,
    .theme-transition *::after {
        transition: 
            background-color 0.3s ease,
            color 0.3s ease,
            border-color 0.3s ease,
            box-shadow 0.3s ease !important;
    }
`;
document.head.appendChild(style);

// ====== SYSTEM THEME DETECTION ====== //
function detectSystemTheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    }
    return 'light';
}

// Listen for system theme changes
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        // Only apply system theme if user hasn't manually set a preference
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
}

// ====== THEME UTILITY FUNCTIONS ====== //
function getTheme() {
    return document.body.getAttribute('data-theme');
}

function isDarkTheme() {
    return getTheme() === 'dark';
}

function isLightTheme() {
    return getTheme() === 'light';
}

// Export functions for use in other scripts
window.themeUtils = {
    getTheme,
    setTheme,
    toggleTheme,
    isDarkTheme,
    isLightTheme,
    detectSystemTheme
};
