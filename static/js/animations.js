// ====== ANIMATIONS SYSTEM ====== //
// Particle effects, scroll animations, and interactive elements

// Initialize animations on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeParticles();
    initializeScrollAnimations();
    initializeCounters();
    initializeTypingEffect();
    initializeScrollProgress();
    initializeBackToTop();
    initializeParallax();
});

// ====== PARTICLE SYSTEM ====== //
function initializeParticles() {
    const particlesContainer = document.querySelector('.particles-container');
    if (!particlesContainer) return;
    
    // Create particles
    const particleCount = 50;
    const colors = ['#00d4ff', '#9d50ff', '#ff006e', '#00ff88'];
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(particlesContainer, colors);
    }
}

function createParticle(container, colors) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // Random properties
    const size = Math.random() * 4 + 1;
    const color = colors[Math.floor(Math.random() * colors.length)];
    const duration = Math.random() * 20 + 10;
    const delay = Math.random() * 5;
    
    // Set styles
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.backgroundColor = color;
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.animationDuration = `${duration}s`;
    particle.style.animationDelay = `${delay}s`;
    
    container.appendChild(particle);
}

// ====== SCROLL ANIMATIONS ====== //
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                
                // Trigger specific animations based on element class
                if (entry.target.classList.contains('skill-progress-bar')) {
                    animateSkillProgress(entry.target);
                }
            }
        });
    }, observerOptions);
    
    // Observe all scroll-reveal elements
    document.querySelectorAll('.scroll-reveal, .scroll-reveal-left, .scroll-reveal-right, .stagger-item').forEach(el => {
        observer.observe(el);
    });
    
    // Observe skill progress bars
    document.querySelectorAll('.skill-progress-bar').forEach(el => {
        observer.observe(el);
    });
}

function animateSkillProgress(element) {
    const targetWidth = element.getAttribute('data-width') || element.style.width;
    setTimeout(() => {
        element.style.width = targetWidth;
    }, 200);
}

// ====== COUNTER ANIMATIONS ====== //
function initializeCounters() {
    const counters = document.querySelectorAll('.counter');
    const observerOptions = {
        threshold: 0.5
    };
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                animateCounter(entry.target);
                entry.target.classList.add('counted');
            }
        });
    }, observerOptions);
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target') || element.textContent);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

// ====== TYPING EFFECT ====== //
function initializeTypingEffect() {
    const typingElements = document.querySelectorAll('.typing-text');
    
    typingElements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        typeText(element, text, 0);
    });
}

function typeText(element, text, index) {
    if (index < text.length) {
        element.textContent += text.charAt(index);
        setTimeout(() => typeText(element, text, index + 1), 100);
    }
}

// ====== SCROLL PROGRESS ====== //
function initializeScrollProgress() {
    const progressBar = document.getElementById('scrollProgress');
    if (!progressBar) return;
    
    window.addEventListener('scroll', () => {
        const windowHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrolled = (window.scrollY / windowHeight) * 100;
        progressBar.style.width = `${scrolled}%`;
    });
}

// ====== BACK TO TOP BUTTON ====== //
function initializeBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    if (!backToTopBtn) return;
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });
    
    // Scroll to top on click
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ====== PARALLAX EFFECTS ====== //
function initializeParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    if (parallaxElements.length === 0) return;
    
    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;
        
        parallaxElements.forEach(element => {
            const speed = element.getAttribute('data-speed') || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// ====== HOVER EFFECTS ====== //
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to project cards
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover-lift');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover-lift');
        });
    });
    
    // Add hover effects to social icons
    const socialIcons = document.querySelectorAll('.social-icon');
    socialIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.classList.add('hover-scale');
        });
        
        icon.addEventListener('mouseleave', function() {
            this.classList.remove('hover-scale');
        });
    });
});

// ====== CODE EDITOR ANIMATION ====== //
function initializeCodeEditor() {
    const codeEditor = document.querySelector('.code-editor');
    if (!codeEditor) return;
    
    const codeLines = codeEditor.querySelectorAll('.code-line');
    codeLines.forEach((line, index) => {
        setTimeout(() => {
            line.style.opacity = '1';
            line.style.transform = 'translateX(0)';
        }, index * 100);
    });
}

// ====== NEON GLOW EFFECTS ====== //
function initializeNeonEffects() {
    const neonElements = document.querySelectorAll('.neon-border-animation, .neon-text');
    
    neonElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.classList.add('neon-glow');
        });
        
        element.addEventListener('mouseleave', function() {
            this.classList.remove('neon-glow');
        });
    });
}

// ====== PROFESSION TITLE ROTATION ====== //
function initializeProfessionRotation() {
    const rotationElements = document.querySelectorAll('.profession-rotation');
    
    rotationElements.forEach(element => {
        const titles = element.querySelectorAll('span');
        let currentIndex = 0;
        
        setInterval(() => {
            titles[currentIndex].style.opacity = '0';
            currentIndex = (currentIndex + 1) % titles.length;
            setTimeout(() => {
                titles[currentIndex].style.opacity = '1';
            }, 500);
        }, 3000);
    });
}

// ====== UTILITY FUNCTIONS ====== //
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ====== PERFORMANCE OPTIMIZATION ====== //
// Debounce scroll events for better performance
const optimizedScrollHandler = debounce(() => {
    // Scroll-related animations
}, 10);

window.addEventListener('scroll', optimizedScrollHandler);

// Throttle resize events
const optimizedResizeHandler = throttle(() => {
    // Resize-related adjustments
    initializeParticles();
}, 100);

window.addEventListener('resize', optimizedResizeHandler);

// ====== ANIMATION TRIGGERS ====== //
// Export functions for manual triggering
window.animationUtils = {
    animateCounter,
    typeText,
    createParticle,
    initializeCodeEditor,
    initializeNeonEffects,
    initializeProfessionRotation
};
