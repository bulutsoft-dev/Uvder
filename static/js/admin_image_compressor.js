/**
 * Django Admin Image Compressor
 * -----------------------------
 * This script intercepts form submissions in the Django Admin and compresses
 * images larger than 3MB before they are uploaded to Vercel/Cloudinary.
 * This is necessary to avoid Vercel's 4.5MB payload limit.
 */

(function () {
    'use strict';

    const MAX_SIZE_MB = 3;
    const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;
    const QUALITY = 0.7; // Compression quality (0.1 to 1.0)
    const MAX_WIDTH = 1920; // Max width for compressed images
    const MAX_HEIGHT = 1080; // Max height for compressed images

    /**
     * Compresses an image file using Canvas API
     * @param {File} file 
     * @returns {Promise<File>}
     */
    async function compressImage(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = event => {
                const img = new Image();
                img.src = event.target.result;
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    let width = img.width;
                    let height = img.height;

                    // Calculate new dimensions while maintaining aspect ratio
                    if (width > height) {
                        if (width > MAX_WIDTH) {
                            height *= MAX_WIDTH / width;
                            width = MAX_WIDTH;
                        }
                    } else {
                        if (height > MAX_HEIGHT) {
                            width *= MAX_HEIGHT / height;
                            height = MAX_HEIGHT;
                        }
                    }

                    canvas.width = width;
                    canvas.height = height;

                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, width, height);

                    canvas.toBlob((blob) => {
                        if (!blob) {
                            reject(new Error('Canvas toBlob failed'));
                            return;
                        }
                        const compressedFile = new File([blob], file.name, {
                            type: 'image/jpeg',
                            lastModified: Date.now()
                        });
                        resolve(compressedFile);
                    }, 'image/jpeg', QUALITY);
                };
                img.onerror = reject;
            };
            reader.onerror = reject;
        });
    }

    /**
     * Handles form submission
     * @param {Event} e 
     */
    async function handleSubmit(e) {
        const form = e.target;
        const fileInputs = form.querySelectorAll('input[type="file"]');
        let needsPrevention = false;

        // Check if any file needs compression
        for (const input of fileInputs) {
            for (const file of input.files) {
                if (file.type.startsWith('image/') && file.size > MAX_SIZE_BYTES) {
                    needsPrevention = true;
                    break;
                }
            }
            if (needsPrevention) break;
        }

        if (needsPrevention) {
            e.preventDefault();
            e.stopPropagation();

            // Show a loading indicator if possible (Django Unfold might have its own, but we'll use a simple one)
            const submitButtons = form.querySelectorAll('input[type="submit"], button[type="submit"]');
            submitButtons.forEach(btn => {
                btn.disabled = true;
                btn.dataset.originalText = btn.value || btn.innerText;
                if (btn.tagName === 'INPUT') btn.value = 'Sıkıştırılıyor...';
                else btn.innerText = 'Sıkıştırılıyor...';
            });

            try {
                for (const input of fileInputs) {
                    const dataTransfer = new DataTransfer();
                    let inputChanged = false;

                    for (const file of input.files) {
                        if (file.type.startsWith('image/') && file.size > MAX_SIZE_BYTES) {
                            console.log(`Compressing ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`);
                            const compressed = await compressImage(file);
                            console.log(`Compressed ${file.name} to ${(compressed.size / 1024 / 1024).toFixed(2)} MB`);
                            dataTransfer.items.add(compressed);
                            inputChanged = true;
                        } else {
                            dataTransfer.items.add(file);
                        }
                    }

                    if (inputChanged) {
                        input.files = dataTransfer.files;
                    }
                }

                // Re-submit the form
                form.submit();
            } catch (error) {
                console.error('Image compression failed:', error);
                alert('Görsel sıkıştırma sırasında bir hata oluştu. Lütfen daha küçük bir görsel deneyin.');

                // Reset buttons
                submitButtons.forEach(btn => {
                    btn.disabled = false;
                    if (btn.tagName === 'INPUT') btn.value = btn.dataset.originalText;
                    else btn.innerText = btn.dataset.originalText;
                });
            }
        }
    }

    // Initialize
    document.addEventListener('DOMContentLoaded', () => {
        const djangoForm = document.getElementById('news_form') ||
            document.getElementById('sitesettings_form') ||
            document.getElementById('writer_form') ||
            document.getElementById('article_form') ||
            document.getElementById('galleryimage_form') ||
            document.getElementById('aboutcard_form') ||
            document.getElementById('organizationmember_form');

        if (djangoForm) {
            djangoForm.addEventListener('submit', handleSubmit);
        } else {
            // Fallback for any other Django Admin form
            const anyAdminForm = document.querySelector('.change-form form');
            if (anyAdminForm) {
                anyAdminForm.addEventListener('submit', handleSubmit);
            }
        }
    });
})();
