document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('searchBtn');
    const searchBtnMobile = document.getElementById('searchBtnMobile');
    const searchPopup = document.getElementById('searchPopup');

    const toggleSearch = (e) => {
        e.preventDefault();
        searchPopup.classList.toggle('active');
        if (searchPopup.classList.contains('active')) {
            const input = searchPopup.querySelector('input');
            setTimeout(() => input.focus(), 300);
        }
    };

    if (searchBtn) {
        searchBtn.addEventListener('click', toggleSearch);
    }

    if (searchBtnMobile) {
        searchBtnMobile.addEventListener('click', toggleSearch);
    }

    // Close search on clicks outside
    document.addEventListener('click', (e) => {
        if (!searchPopup.contains(e.target) &&
            e.target !== searchBtn &&
            !searchBtn?.contains(e.target) &&
            e.target !== searchBtnMobile &&
            !searchBtnMobile?.contains(e.target)) {
            searchPopup.classList.remove('active');
        }
    });

    // Close search on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            searchPopup.classList.remove('active');
        }
    });

   



    
    const initSlider = () => {
        const heroSlider = $('.hero-slider');
        if (heroSlider.length) {
            heroSlider.owlCarousel({
                items: 1,
                loop: true,
                margin: 0,
                nav: false,
                dots: false,
                autoplay: true,
                autoplayTimeout: 5000,
                smartSpeed: 800,
                onInitialized: function () {
                    $('.hero-slider').css('opacity', 1);
                }
            });

            $('.slider-prev').off('click').click(function () {
                heroSlider.trigger('prev.owl.carousel');
            });
            $('.slider-next').off('click').click(function () {
                heroSlider.trigger('next.owl.carousel');
            });
        }
    };

    // Run carousel init
    initSlider();

    // Initialize Testimonial Slider




    // const addtocartbtn = document.getElementsByClassName('addtocartbtn');
    // addtocartbtn.addEventListener('click', () => {
    //     addtocartbtn.textContent = 'Added';
    //     addtocartbtn.style.backgroundColor = '#1d2d03ff';
    //     setTimeout(() => {
    //         addtocartbtn.textContent = 'Add to cart';
    //         addtocartbtn.style.backgroundColor = '#558903';
    //     }, 2000);
    // });

    
    
    
    // const addtocartbtn = Array.from(document.getElementsByClassName('addtocartbtn'));

    // addtocartbtn.map(el => {
    //     el.addEventListener('click', () => {
    //         el.textContent = 'Added';
    //         el.style.backgroundColor = '#1d2d03ff';
    //         setTimeout(() => {
    //             alert('Product added to cart');
    //             el.textContent = 'Add to cart';
    //             el.style.backgroundColor = '#558903';
    //         }, 2000);
    //     });
    // });






  
// const addtocartbtn = Array.from(document.getElementsByClassName('addtocartbtn'));

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// addtocartbtn.forEach(el => {
//     el.addEventListener('click', function () {

//         const productId = this.dataset.productId;
//         const csrfToken = getCookie('csrftoken');

//         fetch("{% url 'add_to_cart' %}", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/x-www-form-urlencoded",
//                 "X-CSRFToken": csrfToken
//             },
//             body: `product_id=${productId}`
//         })
//         .then(response => response.json())
//         .then(data => {

//             if (data.status === "success") {

//                 // Update cart badge
//                 document.getElementById('cart-count').textContent = data.cart_count;

//                 // Button animation
//                 this.textContent = "Added";
//                 this.style.backgroundColor = "#1d2d03ff";

//                 setTimeout(() => {
//                     this.textContent = "Add to cart";
//                     this.style.backgroundColor = "#558903";
//                 }, 1500);
//             }
//         })
//         .catch(error => console.error("Error:", error));
//     });
// });















    // Offer Popup Logic
    const offerPopup = document.getElementById('offerPopup');
    const popupOverlay = document.getElementById('offerPopupOverlay');
    const closePopupBtn = document.getElementById('closePopup');
    let popupShown = false;

    const showPopup = () => {
        if (!popupShown) {
            if (offerPopup) offerPopup.style.display = 'block';
            if (popupOverlay) popupOverlay.style.display = 'block';
            setTimeout(() => {
                if (offerPopup) offerPopup.classList.add('active');
            }, 10);
            popupShown = true;
            // Store in session to only show once per session
            sessionStorage.setItem('offerPopupShown', 'true');
        }
    };

    const closePopup = () => {
        if (offerPopup) offerPopup.classList.remove('active');
        setTimeout(() => {
            if (offerPopup) offerPopup.style.display = 'none';
            if (popupOverlay) popupOverlay.style.display = 'none';
        }, 400);
    };

    // Check if already shown in this session
    if (sessionStorage.getItem('offerPopupShown')) {
        popupShown = true;
    }

    window.addEventListener('scroll', () => {
        if (!popupShown) {
            const scrollDistance = window.scrollY;
            const documentHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPercentage = (scrollDistance / documentHeight) * 100;

            if (scrollPercentage >= 20) {
                showPopup();
            }
        }
    });

    if (closePopupBtn) {
        closePopupBtn.addEventListener('click', closePopup);
    }

    if (popupOverlay) {
        popupOverlay.addEventListener('click', closePopup);
    }













    // Product Details Interactivity
    if ($('.thumbnail-slider').length) {
        const thumbSlider = $('.thumbnail-slider').owlCarousel({
            items: 4,
            margin: 10,
            nav: false,
            dots: true, // Enable dots for identification on scroll
            responsive: {
                0: { items: 3, dots: true },
                576: { items: 4, dots: false } // Hide dots on larger screens where arrows are visible
            }
        });

        $('.thumb-prev').click(() => thumbSlider.trigger('prev.owl.carousel'));
        $('.thumb-next').click(() => thumbSlider.trigger('next.owl.carousel'));

        // Sync thumbnails with main image
        $('.thumb-img').click(function () {
            $('.thumb-img').removeClass('active');
            $(this).addClass('active');
            const newSrc = $(this).data('large');
            $('#mainProductImage').fadeOut(200, function () {
                $(this).attr('src', newSrc).fadeIn(200);
            });
        });
    }

    // Read More Toggle
    const readMoreBtn = document.getElementById('readMoreBtn');
    const shortDesc = document.getElementById('shortDesc');
    if (readMoreBtn && shortDesc) {
        readMoreBtn.addEventListener('click', () => {
            const isExpanded = shortDesc.classList.toggle('expanded');
            readMoreBtn.textContent = isExpanded ? 'Read less...' : 'Read more...';
        });
    }

    // Tabs logic
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabPanes = document.querySelectorAll('.tab-pane');
    if (tabLinks.length) {
        tabLinks.forEach(link => {
            link.addEventListener('click', () => {
                const target = link.dataset.tab;
                tabLinks.forEach(l => l.classList.remove('active'));
                tabPanes.forEach(p => p.classList.remove('active'));
                link.classList.add('active');
                document.getElementById(target).classList.add('active');
            });
        });
    }

    // Quantity Control
    const qtyInput = document.querySelector('.qty-input');
    const plusBtn = document.querySelector('.qty-btn.plus');
    const minusBtn = document.querySelector('.qty-btn.minus');
    if (qtyInput && plusBtn && minusBtn) {
        plusBtn.addEventListener('click', () => qtyInput.value = parseInt(qtyInput.value) + 1);
        minusBtn.addEventListener('click', () => {
            if (parseInt(qtyInput.value) > 1) qtyInput.value = parseInt(qtyInput.value) - 1;
        });
    }
});





document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('click', function (e) {

        // If Add to Cart button (or inside it) is clicked → don't redirect
        if (e.target.closest('.addtocartbtn')) {
            return;
        }

        // Get URL from data attribute
        const url = this.dataset.url;

        if (url) {
            window.location.href = url;
        }
    });
});














// ── Mobile Nav Drawer ──
const mobOverlay = document.getElementById('mobNavOverlay');
const mobDrawer = document.getElementById('mobNavDrawer');
const mobOpen = document.getElementById('mobNavOpen');
const mobClose = document.getElementById('mobNavClose');

function openMobNav() {
    mobOverlay.classList.add('open');
    mobDrawer.classList.add('open');
    document.body.classList.add('mob-nav-open');
}

function closeMobNav() {
    mobOverlay.classList.remove('open');
    mobDrawer.classList.remove('open');
    document.body.classList.remove('mob-nav-open');
}

if (mobOpen) mobOpen.addEventListener('click', openMobNav);
if (mobClose) mobClose.addEventListener('click', closeMobNav);
if (mobOverlay) mobOverlay.addEventListener('click', closeMobNav);

// Close on ESC key
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMobNav(); });

// ── Category accordion in mobile drawer ──
const mobCatBtn = document.getElementById('mobCatBtn');
const mobCatSubmenu = document.getElementById('mobCatSubmenu');
if (mobCatBtn && mobCatSubmenu) {
    mobCatBtn.addEventListener('click', () => {
        const isOpen = mobCatSubmenu.classList.toggle('open');
        mobCatBtn.classList.toggle('open', isOpen);
        mobCatBtn.setAttribute('aria-expanded', isOpen);
    });
}






















    $('.testimonial-slider').owlCarousel({
        items: 1,
        loop: true,
        autoplay: true,
        autoplayTimeout: 5000,
        dots: true,
        smartSpeed: 800,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            }
        }
    });






    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 4000);
















