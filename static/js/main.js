// Umut Vagonu - Main JavaScript
// Professional & Responsive

document.addEventListener('DOMContentLoaded', function () {

    // ===========================================
    // MOBILE NAVIGATION
    // ===========================================
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const body = document.body;

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
            body.classList.toggle('menu-open');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function (e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                body.classList.remove('menu-open');
            }
        });

        // Close menu when clicking a link
        navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                body.classList.remove('menu-open');
            });
        });

        // Close menu on window resize (if switching to desktop)
        window.addEventListener('resize', function () {
            if (window.innerWidth > 768) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                body.classList.remove('menu-open');
            }
        });
    }

    // ===========================================
    // HEADER SCROLL EFFECT
    // ===========================================
    const header = document.querySelector('.header');
    if (header) {
        let lastScroll = 0;

        window.addEventListener('scroll', function () {
            const currentScroll = window.scrollY;

            // Add scrolled class
            if (currentScroll > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }

            // Hide/show header on scroll (optional)
            // if (currentScroll > lastScroll && currentScroll > 200) {
            //     header.classList.add('hidden');
            // } else {
            //     header.classList.remove('hidden');
            // }

            lastScroll = currentScroll;
        });
    }

    // ===========================================
    // ALERT CLOSE
    // ===========================================
    document.querySelectorAll('.alert-close').forEach(btn => {
        btn.addEventListener('click', function () {
            const alert = this.closest('.alert');
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        });
    });

    // ===========================================
    // SMOOTH SCROLL
    // ===========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const headerHeight = header ? header.offsetHeight : 0;
                const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ===========================================
    // GALLERY LIGHTBOX
    // ===========================================
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxClose = document.querySelector('.lightbox-close');

    if (galleryItems.length > 0 && lightbox && lightboxImage) {
        let currentIndex = 0;
        const images = Array.from(galleryItems).map(item => ({
            src: item.querySelector('img').src,
            title: item.querySelector('h4')?.textContent || ''
        }));

        galleryItems.forEach((item, index) => {
            item.addEventListener('click', function () {
                currentIndex = index;
                openLightbox(images[currentIndex]);
            });
        });

        function openLightbox(image) {
            lightboxImage.src = image.src;
            lightboxImage.alt = image.title;
            lightbox.classList.add('active');
            body.classList.add('lightbox-open');
        }

        function closeLightbox() {
            lightbox.classList.remove('active');
            body.classList.remove('lightbox-open');
        }

        if (lightboxClose) {
            lightboxClose.addEventListener('click', closeLightbox);
        }

        lightbox.addEventListener('click', function (e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });

        // Keyboard navigation
        document.addEventListener('keydown', function (e) {
            if (!lightbox.classList.contains('active')) return;

            if (e.key === 'Escape') {
                closeLightbox();
            } else if (e.key === 'ArrowRight') {
                currentIndex = (currentIndex + 1) % images.length;
                openLightbox(images[currentIndex]);
            } else if (e.key === 'ArrowLeft') {
                currentIndex = (currentIndex - 1 + images.length) % images.length;
                openLightbox(images[currentIndex]);
            }
        });

        // Touch swipe for mobile
        let touchStartX = 0;
        let touchEndX = 0;

        lightbox.addEventListener('touchstart', function (e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        lightbox.addEventListener('touchend', function (e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });

        function handleSwipe() {
            const swipeThreshold = 50;
            const diff = touchStartX - touchEndX;

            if (Math.abs(diff) > swipeThreshold) {
                if (diff > 0) {
                    // Swipe left - next image
                    currentIndex = (currentIndex + 1) % images.length;
                } else {
                    // Swipe right - previous image
                    currentIndex = (currentIndex - 1 + images.length) % images.length;
                }
                openLightbox(images[currentIndex]);
            }
        }
    }

    // ===========================================
    // LAZY LOADING IMAGES
    // ===========================================
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        }, { rootMargin: '50px' });

        document.querySelectorAll('img[loading="lazy"], img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ===========================================
    // ANIMATE ON SCROLL
    // ===========================================
    const animateElements = document.querySelectorAll(
        '.service-card, .stat-card, .news-card, .writer-card, .link-card, .link-card-full, .mv-card, .activity-card'
    );

    if ('IntersectionObserver' in window && animateElements.length > 0) {
        const animateObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    // Stagger animation
                    setTimeout(() => {
                        entry.target.classList.add('animated');
                    }, index * 100);
                    animateObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        animateElements.forEach(el => {
            el.classList.add('animate-ready');
            animateObserver.observe(el);
        });
    }

    // ===========================================
    // GALLERY CATEGORY FILTER
    // ===========================================
    const filterButtons = document.querySelectorAll('.filter-btn');
    const galleryGrid = document.querySelector('.gallery-masonry, .gallery-grid');

    if (filterButtons.length > 0 && galleryGrid) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', function (e) {
                // Only handle if it's not a link
                if (!this.getAttribute('href') || this.getAttribute('href') === '#') {
                    e.preventDefault();

                    filterButtons.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');

                    const category = this.dataset.category;
                    const items = galleryGrid.querySelectorAll('.gallery-item');

                    items.forEach(item => {
                        if (category === 'all' || item.dataset.category === category) {
                            item.style.display = '';
                            setTimeout(() => item.style.opacity = '1', 10);
                        } else {
                            item.style.opacity = '0';
                            setTimeout(() => item.style.display = 'none', 300);
                        }
                    });
                }
            });
        });
    }

    // ===========================================
    // CONTACT FORM VALIDATION
    // ===========================================
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            let isValid = true;
            const requiredFields = this.querySelectorAll('[required]');

            requiredFields.forEach(field => {
                const formGroup = field.closest('.form-group');

                if (!field.value.trim()) {
                    isValid = false;
                    formGroup.classList.add('error');
                } else {
                    formGroup.classList.remove('error');
                }

                // Email validation
                if (field.type === 'email' && field.value) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(field.value)) {
                        isValid = false;
                        formGroup.classList.add('error');
                    }
                }
            });

            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const firstError = this.querySelector('.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });

        // Remove error on input
        contactForm.querySelectorAll('input, textarea').forEach(field => {
            field.addEventListener('input', function () {
                this.closest('.form-group').classList.remove('error');
            });
        });
    }

    // ===========================================
    // BACK TO TOP BUTTON
    // ===========================================
    const backToTop = document.createElement('button');
    backToTop.className = 'back-to-top';
    backToTop.innerHTML = '<i class="fas fa-chevron-up"></i>';
    backToTop.setAttribute('aria-label', 'Yukarı git');
    document.body.appendChild(backToTop);

    window.addEventListener('scroll', function () {
        if (window.scrollY > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });

    backToTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});

// Add CSS for back to top button dynamically
const style = document.createElement('style');
style.textContent = `
    .back-to-top {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: var(--primary, #3EB89A);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        font-size: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        visibility: hidden;
        transform: translateY(20px);
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(62, 184, 154, 0.3);
    }
    
    .back-to-top.visible {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }
    
    .back-to-top:hover {
        background: var(--primary-dark, #2D9A7E);
        transform: translateY(-3px);
    }
    
    .animate-ready {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.6s ease;
    }
    
    .animated {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    
    body.menu-open {
        overflow: hidden;
    }
    
    body.lightbox-open {
        overflow: hidden;
    }
    
    .form-group.error input,
    .form-group.error textarea {
        border-color: #EF4444 !important;
    }
    
    @media (max-width: 576px) {
        .back-to-top {
            bottom: 20px;
            right: 20px;
            width: 45px;
            height: 45px;
            font-size: 16px;
        }
    }
`;
document.head.appendChild(style);
