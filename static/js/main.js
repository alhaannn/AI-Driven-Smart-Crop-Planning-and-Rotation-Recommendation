/**
 * Smart Crop Planner - Main JavaScript
 * Handles interactive functionality and UI enhancements
 */

// Document Ready
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeForms();
    initializeTooltips();
    initializeCharts();
});

/**
 * Sidebar Navigation
 */
function initializeSidebar() {
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Active link highlighting
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

/**
 * Form Enhancements
 */
function initializeForms() {
    // Form validation
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-save draft functionality
    const draftForms = document.querySelectorAll('.auto-save-form');
    draftForms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                saveDraft(form);
            });
        });
        
        // Load saved draft
        loadDraft(form);
    });
}

/**
 * Form Validation
 */
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    return isValid;
}

/**
 * Show Field Error
 */
function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    const error = document.createElement('div');
    error.className = 'error-message';
    error.style.color = '#e74c3c';
    error.style.fontSize = '0.85rem';
    error.style.marginTop = '0.25rem';
    error.textContent = message;
    
    field.parentElement.appendChild(error);
}

/**
 * Clear Field Error
 */
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const error = field.parentElement.querySelector('.error-message');
    if (error) {
        error.remove();
    }
}

/**
 * Save Form Draft to LocalStorage
 */
function saveDraft(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    const formId = form.id || 'default-form';
    localStorage.setItem(`draft_${formId}`, JSON.stringify(data));
    
    showNotification('Draft saved automatically', 'success');
}

/**
 * Load Form Draft from LocalStorage
 */
function loadDraft(form) {
    const formId = form.id || 'default-form';
    const savedData = localStorage.getItem(`draft_${formId}`);
    
    if (savedData) {
        const data = JSON.parse(savedData);
        
        for (let [key, value] of Object.entries(data)) {
            const field = form.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = value;
            }
        }
    }
}

/**
 * Clear Form Draft
 */
function clearDraft(formId) {
    localStorage.removeItem(`draft_${formId}`);
}

/**
 * Initialize Tooltips
 */
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            showTooltip(this);
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
}

/**
 * Show Tooltip
 */
function showTooltip(element) {
    const tooltipText = element.getAttribute('data-tooltip');
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = tooltipText;
    tooltip.style.position = 'absolute';
    tooltip.style.background = '#333';
    tooltip.style.color = '#fff';
    tooltip.style.padding = '0.5rem';
    tooltip.style.borderRadius = '4px';
    tooltip.style.fontSize = '0.85rem';
    tooltip.style.zIndex = '10000';
    tooltip.style.pointerEvents = 'none';
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.top = `${rect.top - tooltip.offsetHeight - 8}px`;
    tooltip.style.left = `${rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)}px`;
}

/**
 * Hide Tooltip
 */
function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

/**
 * Show Notification
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '10000';
    notification.style.minWidth = '250px';
    notification.style.animation = 'slideIn 0.3s ease';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

/**
 * Initialize Charts (placeholder for Chart.js integration)
 */
function initializeCharts() {
    // This will be expanded when we add Chart.js visualizations
    console.log('Charts initialized');
}

/**
 * Confirm Delete Action
 */
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

/**
 * Format Date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Debounce Function
 */
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

/**
 * AJAX Helper
 */
function ajaxRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred', 'danger');
    });
}

/**
 * Get CSRF Token
 */
function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

/**
 * Toggle Element Visibility
 */
function toggleElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'block' : 'none';
    }
}

/**
 * Smooth Scroll to Element
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .is-invalid {
        border-color: #e74c3c !important;
    }
`;
document.head.appendChild(style);
