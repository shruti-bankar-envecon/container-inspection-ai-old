/**
 * Container Inspection AI - Micro-interactions
 * Enhanced UI animations and interactions
 */

(function() {
    'use strict';

    // ============================================
    // Number Counter Animation
    // ============================================
    function animateValue(element, start, end, duration) {
        if (!element) return;
        
        const range = end - start;
        const increment = end > start ? 1 : -1;
        const stepTime = Math.abs(Math.floor(duration / range));
        let current = start;
        
        const timer = setInterval(function() {
            current += increment;
            element.textContent = current;
            if (current === end) {
                clearInterval(timer);
            }
        }, stepTime);
    }

    // ============================================
    // Smooth Number Counter with Easing
    // ============================================
    function animateNumber(element, start, end, duration) {
        if (!element) return;
        
        const startTime = performance.now();
        const range = end - start;
        
        function easeOutExpo(t) {
            return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
        }
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = easeOutExpo(progress);
            const current = start + (range * easedProgress);
            
            element.textContent = Math.floor(current);
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        requestAnimationFrame(update);
    }

    // ============================================
    // Scan Line Animation on Images
    // ============================================
    function addScanAnimation() {
        const images = document.querySelectorAll('[data-testid="stImage"]');
        images.forEach(img => {
            if (!img.classList.contains('scanning-indicator')) {
                img.classList.add('scanning-indicator');
            }
        });
    }

    // ============================================
    // Progress Bar Animation
    // ============================================
    function animateProgressBar(element, targetWidth, duration) {
        if (!element) return;
        
        const startTime = performance.now();
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const currentWidth = targetWidth * progress;
            
            element.style.width = currentWidth + '%';
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        requestAnimationFrame(update);
    }

    // ============================================
    // Confidence Meter Animation
    // ============================================
    function animateConfidenceMeter() {
        const meters = document.querySelectorAll('.confidence-meter');
        meters.forEach(meter => {
            const targetWidth = parseFloat(meter.dataset.confidence) || 0;
            const fill = meter.querySelector('.confidence-fill');
            if (fill) {
                animateProgressBar(fill, targetWidth, 1000);
            }
        });
    }

    // ============================================
    // Card Hover Effects
    // ============================================
    function enhanceCardHovers() {
        const cards = document.querySelectorAll('[data-testid="stMetric"], .metric-card');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-4px)';
                this.style.transition = 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }

    // ============================================
    // Button Ripple Effect
    // ============================================
    function addRippleEffect() {
        const buttons = document.querySelectorAll('button');
        
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });
    }

    // ============================================
    // Fade In on Scroll
    // ============================================
    function fadeInOnScroll() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-visible');
                }
            });
        }, {
            threshold: 0.1
        });
        
        const elements = document.querySelectorAll('.fade-in-scroll');
        elements.forEach(el => observer.observe(el));
    }

    // ============================================
    // Typing Animation
    // ============================================
    function typeWriter(element, text, speed = 50) {
        if (!element) return;
        
        let i = 0;
        element.textContent = '';
        
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }

    // ============================================
    // Pulse Animation for Status Indicators
    // ============================================
    function pulseStatusIndicators() {
        const indicators = document.querySelectorAll('.status-indicator');
        indicators.forEach(indicator => {
            indicator.style.animation = 'pulse 2s ease-in-out infinite';
        });
    }

    // ============================================
    // Smooth Scroll to Element
    // ============================================
    function smoothScrollTo(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    // ============================================
    // Toast Notification
    // ============================================
    function showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        const colors = {
            success: '#10B981',
            error: '#EF4444',
            warning: '#F59E0B',
            info: '#3B82F6'
        };
        
        toast.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            padding: 1rem 1.5rem;
            background: ${colors[type] || colors.info};
            color: white;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            z-index: 9999;
            animation: slideInRight 0.3s ease-out;
            font-weight: 500;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    // ============================================
    // Loading Spinner Overlay
    // ============================================
    function showLoadingOverlay(message = 'Processing...') {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.innerHTML = `
            <div style="text-align: center;">
                <div class="spinner"></div>
                <p style="color: #CBD5E1; margin-top: 1rem; font-size: 1.1rem;">${message}</p>
            </div>
        `;
        
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.95);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            backdrop-filter: blur(4px);
        `;
        
        document.body.appendChild(overlay);
    }

    function hideLoadingOverlay() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => overlay.remove(), 300);
        }
    }

    // ============================================
    // Parallax Effect
    // ============================================
    function addParallaxEffect() {
        const parallaxElements = document.querySelectorAll('.parallax');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            
            parallaxElements.forEach(el => {
                const speed = el.dataset.speed || 0.5;
                const yPos = -(scrolled * speed);
                el.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // ============================================
    // Confetti Animation (for success states)
    // ============================================
    function triggerConfetti() {
        const duration = 3000;
        const animationEnd = Date.now() + duration;
        const colors = ['#00C7B7', '#10B981', '#3B82F6', '#F59E0B'];

        (function frame() {
            const timeLeft = animationEnd - Date.now();

            if (timeLeft <= 0) return;

            const particleCount = 2;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.style.cssText = `
                    position: fixed;
                    width: 10px;
                    height: 10px;
                    background: ${colors[Math.floor(Math.random() * colors.length)]};
                    top: ${Math.random() * 100}%;
                    left: ${Math.random() * 100}%;
                    border-radius: 50%;
                    pointer-events: none;
                    z-index: 9999;
                    animation: confettiFall 2s ease-out forwards;
                `;
                
                document.body.appendChild(particle);
                setTimeout(() => particle.remove(), 2000);
            }

            requestAnimationFrame(frame);
        })();
    }

    // ============================================
    // Initialize All Interactions
    // ============================================
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        // Add scan animations
        addScanAnimation();
        
        // Enhance card hovers
        enhanceCardHovers();
        
        // Add ripple effects
        addRippleEffect();
        
        // Fade in on scroll
        fadeInOnScroll();
        
        // Pulse status indicators
        pulseStatusIndicators();
        
        // Parallax effect
        addParallaxEffect();
        
        // Animate confidence meters
        animateConfidenceMeter();

        // Re-run on Streamlit updates
        const observer = new MutationObserver(() => {
            addScanAnimation();
            enhanceCardHovers();
            addRippleEffect();
            animateConfidenceMeter();
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // ============================================
    // CSS Animations (injected)
    // ============================================
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }

        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }

        @keyframes confettiFall {
            to {
                transform: translateY(100vh) rotate(360deg);
                opacity: 0;
            }
        }

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
                transform: scale(1);
            }
            50% {
                opacity: 0.8;
                transform: scale(1.05);
            }
        }

        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }

        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }

        .fade-in-scroll {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease-out, transform 0.6s ease-out;
        }

        .fade-in-visible {
            opacity: 1;
            transform: translateY(0);
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(0, 199, 183, 0.2);
            border-top-color: #00C7B7;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);

    // Export functions to global scope
    window.ContainerAI = {
        animateNumber,
        animateProgressBar,
        showToast,
        showLoadingOverlay,
        hideLoadingOverlay,
        triggerConfetti,
        smoothScrollTo,
        typeWriter
    };

    // Initialize
    init();
})();
