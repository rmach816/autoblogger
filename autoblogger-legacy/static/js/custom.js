// AutoBlogger Custom JavaScript - Enhanced UI Interactions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all enhancements
    initializeAnimations();
    initializeLoadingStates();
    initializeTooltips();
    initializeFormValidation();
    initializeThemeToggle();
});

// Smooth animations and transitions
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Enhanced loading states
function initializeLoadingStates() {
    // Override the existing showLoading function with enhanced version
    window.showLoading = function(button) {
        if (!button) return;
        
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
        button.disabled = true;
        button.classList.add('loading');
        
        // Store original text for restoration
        button.dataset.originalText = originalText;
        
        // Add pulse effect
        button.style.animation = 'pulse 1.5s infinite';
    };
    
    window.hideLoading = function(button) {
        if (!button) return;
        
        if (button.dataset.originalText) {
            button.innerHTML = button.dataset.originalText;
            button.disabled = false;
            button.classList.remove('loading');
            button.style.animation = '';
        }
    };
    
    // Add pulse animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
    `;
    document.head.appendChild(style);
}

// Simple tooltips for better UX
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.textContent = this.dataset.tooltip;
            tooltip.style.cssText = `
                position: absolute;
                background: #1e293b;
                color: white;
                padding: 0.5rem 0.75rem;
                border-radius: 0.375rem;
                font-size: 0.875rem;
                z-index: 1000;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.2s;
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
            
            setTimeout(() => tooltip.style.opacity = '1', 10);
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Enhanced form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Add error message if not exists
                    if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'invalid-feedback';
                        errorDiv.textContent = 'This field is required.';
                        field.parentNode.insertBefore(errorDiv, field.nextSibling);
                    }
                } else {
                    field.classList.remove('is-invalid');
                    field.classList.add('is-valid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Show error message
                showNotification('Please fill in all required fields.', 'error');
            }
        });
    });
}

// Theme toggle functionality
function initializeThemeToggle() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('autoblogger-theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
    
    // Create theme toggle button
    const themeToggle = document.createElement('button');
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    themeToggle.className = 'btn btn-outline-secondary btn-sm';
    themeToggle.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 1000;';
    themeToggle.title = 'Toggle dark mode';
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('autoblogger-theme', newTheme);
        
        this.innerHTML = newTheme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    });
    
    document.body.appendChild(themeToggle);
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1050;
        min-width: 300px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Enhanced auto-hide for alerts
function initializeAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.5s ease-out';
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 500);
            }
        }, 5000);
    });
}

// Initialize auto-hide on page load
document.addEventListener('DOMContentLoaded', initializeAutoHideAlerts);

// Smooth scrolling for anchor links
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search (if search functionality exists)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals/alerts
    if (e.key === 'Escape') {
        const activeAlert = document.querySelector('.alert.show');
        if (activeAlert) {
            activeAlert.remove();
        }
    }
});

// Performance monitoring
function initializePerformanceMonitoring() {
    // Monitor page load time
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
        
        // Send to analytics if available
        if (typeof gtag !== 'undefined') {
            gtag('event', 'page_load_time', {
                'value': Math.round(loadTime)
            });
        }
    });
}

// Initialize performance monitoring
document.addEventListener('DOMContentLoaded', initializePerformanceMonitoring);

