// ModernShop - Main JavaScript

$(document).ready(function() {
    // Initialize all components
    initCart();
    initForms();
    initAnimations();
    initSearch();
    initModals();
    
    // === Cart Management ===
    function initCart() {
        // Update cart count on page load
        updateCartCount();
        
        // Add to cart functionality
        $(document).on('click', '.add-to-cart', function(e) {
            e.preventDefault();
            const button = $(this);
            const productId = button.data('product-id');
            const productName = button.data('product-name');
            const productPrice = button.data('product-price');
            const productImage = button.data('product-image');
            
            addToCart(productId, productName, productPrice, productImage, button);
        });
        
        // Remove from cart
        $(document).on('click', '.remove-from-cart', function(e) {
            e.preventDefault();
            const button = $(this);
            const itemId = button.data('item-id');
            
            removeFromCart(itemId, button);
        });
        
        // Update quantity
        $(document).on('change', '.quantity-input', function() {
            const input = $(this);
            const itemId = input.data('item-id');
            const quantity = parseInt(input.val());
            
            updateCartItemQuantity(itemId, quantity);
        });
    }
    
    function addToCart(productId, productName, productPrice, productImage, button) {
        $.ajax({
            url: '/add-to-cart/',
            method: 'POST',
            data: JSON.stringify({
                product_id: productId,
                quantity: 1
            }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function(response) {
                if (response.success) {
                    // Update cart count
                    updateCartCount(response.cart_count);
                    
                    // Show success message
                    showNotification('Product added to cart!', 'success');
                    
                    // Button animation
                    animateButton(button, 'Added');
                    
                    // Update cart total if on cart page
                    if (response.cart_total) {
                        updateCartTotal(response.cart_total);
                    }
                }
            },
            error: function() {
                showNotification('Error adding product to cart', 'error');
            }
        });
    }
    
    function removeFromCart(itemId, button) {
        if (confirm('Are you sure you want to remove this item?')) {
            $.ajax({
                url: '/remove-from-cart/',
                method: 'POST',
                data: JSON.stringify({
                    item_id: itemId
                }),
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                success: function(response) {
                    if (response.success) {
                        // Remove item from DOM
                        button.closest('.cart-item-row').fadeOut(300, function() {
                            $(this).remove();
                        });
                        
                        // Update cart count
                        updateCartCount(response.cart_count);
                        
                        // Update cart total
                        if (response.cart_total) {
                            updateCartTotal(response.cart_total);
                        }
                        
                        showNotification('Item removed from cart', 'success');
                    }
                },
                error: function() {
                    showNotification('Error removing item from cart', 'error');
                }
            });
        }
    }
    
    function updateCartItemQuantity(itemId, quantity) {
        $.ajax({
            url: '/update-cart-item/',
            method: 'POST',
            data: JSON.stringify({
                item_id: itemId,
                quantity: quantity
            }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function(response) {
                if (response.success) {
                    // Update item total
                    $(`.cart-item-row[data-item-id="${itemId}"] .item-total`).text('₹' + response.item_total);
                    
                    // Update cart total
                    if (response.cart_total) {
                        updateCartTotal(response.cart_total);
                    }
                    
                    // Update cart count
                    updateCartCount(response.cart_count);
                }
            },
            error: function() {
                showNotification('Error updating cart', 'error');
            }
        });
    }
    
    function updateCartCount(count) {
        $('.cart-count').text(count || '0');
    }
    
    function updateCartTotal(total) {
        $('.cart-total').text('₹' + total);
    }
    
    // === Form Management ===
    function initForms() {
        // Form validation
        $('form').on('submit', function(e) {
            const form = $(this);
            if (!validateForm(form)) {
                e.preventDefault();
                return false;
            }
        });
        
        // Real-time validation
        $('input, select, textarea').on('blur', function() {
            validateField($(this));
        });
        
        // Password strength indicator
        $('#id_password1').on('input', function() {
            const password = $(this).val();
            const strength = checkPasswordStrength(password);
            updatePasswordStrengthIndicator(strength);
        });
        
        // Password confirmation check
        $('#id_password2').on('input', function() {
            const password1 = $('#id_password1').val();
            const password2 = $(this).val();
            
            if (password2 && password1 !== password2) {
                $(this).addClass('is-invalid');
                showFieldError($(this), 'Passwords do not match');
            } else {
                $(this).removeClass('is-invalid');
                clearFieldError($(this));
            }
        });
    }
    
    function validateForm(form) {
        let isValid = true;
        
        // Check required fields
        form.find('[required]').each(function() {
            if (!validateField($(this))) {
                isValid = false;
            }
        });
        
        // Check email format
        form.find('input[type="email"]').each(function() {
            if (!validateEmail($(this).val())) {
                $(this).addClass('is-invalid');
                showFieldError($(this), 'Please enter a valid email address');
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    function validateField(field) {
        const value = field.val().trim();
        const isRequired = field.prop('required');
        
        if (isRequired && !value) {
            field.addClass('is-invalid');
            showFieldError(field, 'This field is required');
            return false;
        }
        
        field.removeClass('is-invalid');
        clearFieldError(field);
        return true;
    }
    
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    function showFieldError(field, message) {
        let errorDiv = field.siblings('.field-error');
        if (errorDiv.length === 0) {
            errorDiv = $('<div class="field-error text-danger small mt-1"></div>');
            field.after(errorDiv);
        }
        errorDiv.text(message);
    }
    
    function clearFieldError(field) {
        field.siblings('.field-error').remove();
    }
    
    function checkPasswordStrength(password) {
        let strength = 0;
        
        if (password.length >= 8) strength++;
        if (password.match(/[a-z]/)) strength++;
        if (password.match(/[A-Z]/)) strength++;
        if (password.match(/[0-9]/)) strength++;
        if (password.match(/[^a-zA-Z0-9]/)) strength++;
        
        return strength;
    }
    
    function updatePasswordStrengthIndicator(strength) {
        const strengthText = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
        const strengthClass = ['danger', 'warning', 'info', 'success', 'success'];
        
        // Remove existing indicator
        $('.password-strength').remove();
        
        if (strength > 0) {
            const indicator = $(`
                <div class="password-strength mt-1">
                    <div class="progress" style="height: 4px;">
                        <div class="progress-bar bg-${strengthClass[strength - 1]}" 
                             style="width: ${strength * 20}%"></div>
                    </div>
                    <small class="text-${strengthClass[strength - 1]}">${strengthText[strength - 1]}</small>
                </div>
            `);
            $('#id_password1').after(indicator);
        }
    }
    
    // === Search and Filter ===
    function initSearch() {
        // Search suggestions
        let searchTimeout;
        $('#search-input').on('input', function() {
            clearTimeout(searchTimeout);
            const query = $(this).val();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(function() {
                    getSearchSuggestions(query);
                }, 300);
            } else {
                hideSearchSuggestions();
            }
        });
        
        // Filter form submission
        $('#filter-form').on('submit', function(e) {
            const form = $(this);
            const data = form.serialize();
            
            // Update URL without page reload
            const url = window.location.pathname + '?' + data;
            window.history.pushState({}, '', url);
            
            // Submit form normally
        });
    }
    
    function getSearchSuggestions(query) {
        $.ajax({
            url: '/api/search-suggestions/',
            method: 'GET',
            data: { q: query },
            success: function(response) {
                showSearchSuggestions(response.suggestions);
            }
        });
    }
    
    function showSearchSuggestions(suggestions) {
        const container = $('#search-suggestions');
        container.empty();
        
        suggestions.forEach(function(suggestion) {
            container.append(`
                <div class="suggestion-item p-2 border-bottom">
                    <a href="${suggestion.url}" class="text-decoration-none">
                        <i class="bi bi-search me-2"></i>${suggestion.title}
                    </a>
                </div>
            `);
        });
        
        container.show();
    }
    
    function hideSearchSuggestions() {
        $('#search-suggestions').hide();
    }
    
    // === Modal Management ===
    function initModals() {
        // Quick view modal
        $(document).on('click', '.quick-view', function(e) {
            e.preventDefault();
            const productId = $(this).data('product-id');
            loadQuickViewModal(productId);
        });
        
        // Review modal
        $(document).on('click', '.add-review', function(e) {
            e.preventDefault();
            const productId = $(this).data('product-id');
            $('#reviewModal').modal('show');
        });
    }
    
    function loadQuickViewModal(productId) {
        $.ajax({
            url: `/api/product/${productId}/quick-view/`,
            method: 'GET',
            success: function(response) {
                $('#quickViewModal .modal-body').html(response.html);
                $('#quickViewModal').modal('show');
            },
            error: function() {
                showNotification('Error loading product details', 'error');
            }
        });
    }
    
    // === Animations ===
    function initAnimations() {
        // Animate elements on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-up');
                }
            });
        }, observerOptions);
        
        // Observe elements for animation
        $('.product-card, .category-card, .card').each(function() {
            observer.observe(this);
        });
        
        // Smooth scrolling for anchor links
        $('a[href^="#"]').on('click', function(e) {
            e.preventDefault();
            const target = $($(this).attr('href'));
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top - 80
                }, 600);
            }
        });
    }
    
    function animateButton(button, text) {
        const originalText = button.html();
        button.addClass('btn-success').removeClass('btn-primary');
        button.html(`<i class="bi bi-check"></i> ${text}`);
        
        setTimeout(function() {
            button.addClass('btn-primary').removeClass('btn-success');
            button.html(originalText);
        }, 2000);
    }
    
    // === Utility Functions ===
    function getCSRFToken() {
        return $('[name=csrfmiddlewaretoken]').val();
    }
    
    function showNotification(message, type) {
        const alertClass = type === 'error' ? 'danger' : type;
        const icon = type === 'success' ? 'check-circle' : 'exclamation-triangle';
        
        const notification = $(`
            <div class="alert alert-${alertClass} alert-dismissible fade show position-fixed" 
                 style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
                <i class="bi bi-${icon} me-2"></i>${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $('body').append(notification);
        
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            notification.alert('close');
        }, 5000);
    }
    
    // === Image Lazy Loading ===
    function initLazyLoading() {
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        $('img[data-src]').each(function() {
            imageObserver.observe(this);
        });
    }
    
    // === Responsive Navigation ===
    function initResponsiveNav() {
        // Close mobile menu when clicking on a link
        $('.navbar-nav .nav-link').on('click', function() {
            $('.navbar-collapse').collapse('hide');
        });
        
        // Add shadow to navbar on scroll
        $(window).on('scroll', function() {
            if ($(window).scrollTop() > 50) {
                $('.navbar').addClass('navbar-scrolled');
            } else {
                $('.navbar').removeClass('navbar-scrolled');
            }
        });
    }
    
    // === Initialize Lazy Loading and Responsive Nav ===
    initLazyLoading();
    initResponsiveNav();
    
    // === Global Event Handlers ===
    
    // Handle back button for modals
    $(window).on('popstate', function() {
        $('.modal').modal('hide');
    });
    
    // Handle form submission with loading state
    $('form').on('submit', function() {
        const submitBtn = $(this).find('button[type="submit"]');
        if (submitBtn.length) {
            submitBtn.prop('disabled', true);
            submitBtn.html('<span class="spinner-border spinner-border-sm me-2"></span>Processing...');
        }
    });
    
    // Handle AJAX errors globally
    $(document).ajaxError(function(event, xhr, settings, error) {
        if (xhr.status === 403) {
            showNotification('Session expired. Please refresh the page.', 'error');
        } else if (xhr.status >= 500) {
            showNotification('Server error. Please try again later.', 'error');
        }
    });
    
    // Handle AJAX success globally
    $(document).ajaxSuccess(function(event, xhr, settings) {
        // Re-enable submit buttons after AJAX success
        $('button[type="submit"]:disabled').each(function() {
            const btn = $(this);
            btn.prop('disabled', false);
            btn.html(btn.data('original-text') || 'Submit');
        });
    });
    
    // Store original button text
    $('button[type="submit"]').each(function() {
        $(this).data('original-text', $(this).html());
    });
});

// === Global Functions ===

// Debounce function for performance
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Throttle function for scroll events
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

// Format currency
function formatCurrency(amount, currency = '₹') {
    return currency + parseFloat(amount).toFixed(2);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Validate phone number
function validatePhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Copied to clipboard!', 'success');
    }).catch(function() {
        showNotification('Failed to copy to clipboard', 'error');
    });
}
