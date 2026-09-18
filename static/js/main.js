document.addEventListener('DOMContentLoaded', function () {
    // CSRF Token Helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Global Toast Notification Helper
    window.showToast = function (message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) return;

        const toastId = 'toast-' + Math.random().toString(36).substring(2, 9);
        const iconClass = type === 'success' ? 'bi-check-circle-fill text-success' : (type === 'error' ? 'bi-exclamation-triangle-fill text-danger' : 'bi-info-circle-fill text-primary');

        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center bg-white border-0 shadow-lg mb-2" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body d-flex align-items-center gap-2">
                        <i class="bi ${iconClass} fs-5"></i>
                        <span class="text-dark fw-medium">${message}</span>
                    </div>
                    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toastElem = document.getElementById(toastId);
        const bsToast = new bootstrap.Toast(toastElem, { delay: 3500 });
        bsToast.show();
        toastElem.addEventListener('hidden.bs.toast', () => toastElem.remove());
    };

    // Wishlist Toggle
    document.querySelectorAll('.save-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            const listingId = this.dataset.listingId;
            const icon = this.querySelector('i');

            fetch(`/hostels/save/${listingId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                }
            })
            .then(res => {
                if (res.status === 403 || res.status === 401) {
                    window.location.href = '/accounts/login/?next=' + encodeURIComponent(window.location.pathname);
                    return null;
                }
                return res.json();
            })
            .then(data => {
                if (!data) return;
                if (data.status === 'saved') {
                    this.classList.add('saved');
                    icon.classList.remove('bi-heart');
                    icon.classList.add('bi-heart-fill');
                    showToast('Saved to your wishlist!', 'success');
                } else if (data.status === 'removed') {
                    this.classList.remove('saved');
                    icon.classList.remove('bi-heart-fill');
                    icon.classList.add('bi-heart');
                    showToast('Removed from saved items', 'info');
                }
            })
            .catch(err => {
                console.error('Error toggling save:', err);
                showToast('Unable to update saved item', 'error');
            });
        });
    });

    // Zero-Brokerage Contact Reveal
    document.querySelectorAll('.reveal-contact-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const listingId = this.dataset.listingId;
            const targetContainer = document.getElementById(`contact-info-${listingId}`);

            fetch(`/hostels/reveal-contact/${listingId}/`)
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        this.style.display = 'none';
                        if (targetContainer) {
                            targetContainer.innerHTML = `
                                <div class="p-3 bg-light rounded-3 border">
                                    <div class="d-flex align-items-center gap-2 mb-2">
                                        <i class="bi bi-shield-check text-success fs-5"></i>
                                        <span class="fw-bold text-dark">Direct Owner Contact Revealed</span>
                                    </div>
                                    <div class="mb-2">
                                        <span class="text-muted small">Contact Person:</span>
                                        <div class="fw-bold fs-6">${data.contact_person || 'Owner'}</div>
                                    </div>
                                    <div class="d-flex flex-wrap gap-2 mt-3">
                                        <a href="tel:${data.contact_phone}" class="btn btn-sm btn-outline-primary px-3">
                                            <i class="bi bi-telephone-fill me-1"></i> Call ${data.contact_phone}
                                        </a>
                                        <a href="${data.whatsapp_url}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-whatsapp px-3">
                                            <i class="bi bi-whatsapp me-1"></i> Chat on WhatsApp
                                        </a>
                                    </div>
                                </div>
                            `;
                            targetContainer.style.display = 'block';
                        }
                    }
                })
                .catch(err => console.error(err));
        });
    });

    // Price Slider display sync
    const priceSlider = document.getElementById('priceRangeSlider');
    const priceDisplay = document.getElementById('priceRangeValue');
    if (priceSlider && priceDisplay) {
        priceSlider.addEventListener('input', function () {
            priceDisplay.textContent = '₹' + parseInt(this.value).toLocaleString('en-IN');
        });
    }
});
