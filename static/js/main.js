// ====== MAIN JAVASCRIPT FILE ====== //
// Core functionality and event handlers

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeSearch();
    initializeForms();
    initializeModals();
    initializeTooltips();
    initializeLazyLoading();
    initializeSmoothScrolling();
    initializeNewsletter();
});

// ====== NAVIGATION ====== //
function initializeNavigation() {
    // Sticky navbar effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Mobile menu toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navbar.contains(e.target)) {
                navbarCollapse.classList.remove('show');
            }
        });
    }
    
    // Active nav link highlighting
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// ====== SEARCH FUNCTIONALITY ====== //
function initializeSearch() {
    const searchModal = document.getElementById('searchModal');
    const searchBtns = document.querySelectorAll('[data-bs-toggle="modal"][data-bs-target="#searchModal"]');
    const searchInput = document.querySelector('#searchModal input[type="text"]');
    
    // Focus search input when modal opens
    if (searchModal && searchInput) {
        searchModal.addEventListener('shown.bs.modal', function() {
            searchInput.focus();
        });
        
        // Handle search submission
        searchModal.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInput.value.trim();
            if (query) {
                window.location.href = `/search/?q=${encodeURIComponent(query)}`;
            }
        });
    }
}

// ====== FORMS ====== //
function initializeForms() {
    // Add form validation styles
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Handle form submission
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';
                
                // Re-enable button after 5 seconds (fallback)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Submit';
                }, 5000);
            }
        });
        
        // Add real-time validation feedback
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    });
}

function validateField(field) {
    const isValid = field.checkValidity();
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
    
    return isValid;
}

// ====== MODALS ====== //
function initializeModals() {
    // Auto-hide messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
    
    // Newsletter modal trigger (show after 10 seconds on homepage)
    if (window.location.pathname === '/' || window.location.pathname === '/home/') {
        setTimeout(() => {
            if (!localStorage.getItem('newsletterModalShown')) {
                const newsletterModal = document.getElementById('newsletterModal');
                if (newsletterModal) {
                    const modal = new bootstrap.Modal(newsletterModal);
                    modal.show();
                    localStorage.setItem('newsletterModalShown', 'true');
                }
            }
        }, 10000);
    }
}

// ====== TOOLTIPS ====== //
function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// ====== LAZY LOADING ====== //
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// ====== SMOOTH SCROLLING ====== //
function initializeSmoothScrolling() {
    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            const target = document.querySelector(href);
            
            if (target) {
                e.preventDefault();
                const offsetTop = target.offsetTop - 80; // Account for sticky navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Update URL without jumping
                history.pushState(null, null, href);
            }
        });
    });
}

// ====== NEWSLETTER ====== //
function initializeNewsletter() {
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    
    newsletterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = form.querySelector('input[type="email"]').value;
            const submitBtn = form.querySelector('[type="submit"]');
            
            // Show loading state
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Subscribing...';
            }
            
            // Simulate API call (replace with actual form submission)
            setTimeout(() => {
                // Show success message
                showNotification('Thank you for subscribing!', 'success');
                
                // Reset form
                form.reset();
                
                // Reset button
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Subscribe';
                }
            }, 1500);
        });
    });
}

// ====== NOTIFICATIONS ====== //
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 80px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

// ====== UTILITY FUNCTIONS ====== //
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength).replace(/\s+\S*$/, '') + '...';
}

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

// ====== ERROR HANDLING ====== //
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
});

// ====== PERFORMANCE MONITORING ====== //
if (window.performance && window.performance.timing) {
    window.addEventListener('load', function() {
        const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
        console.log(`Page load time: ${loadTime}ms`);
    });
}

// ====== EXPORT UTILITIES ====== //
window.utils = {
    showNotification,
    formatNumber,
    truncateText,
    debounce,
    throttle,
    validateField
};
