"use strict"

// Sticky Header JS 
const nav = document.querySelector('.sticky-header');
const header = document.querySelector('.header');
const navHight = nav.getBoundingClientRect().height;

const stickyNav = function (entries) {
  const [entry] = entries;
  if (!entry.isIntersecting) nav.classList.add('is-sticky');
  else nav.classList.remove('is-sticky');
};

const headerObServer = new IntersectionObserver(stickyNav, {
  root: null,
  threshold: 0,
  rootMargin: `${navHight}px`,
});
headerObServer.observe(header);


// Header Top bar Toggle 
const topbarCloseBtn = document.querySelector(".topbar-close-btn")
const topbarActive = document.querySelector(".notification-bar-area")

if(topbarCloseBtn) {
    topbarCloseBtn.addEventListener("click", () => {
        slideToggle(topbarActive, 300)
    })
}

// arrow("name", 30)
// function arrow (set, value){
//     console.log(set, value)
// }


// Mobile Menu JS 
/*--
    Mobile Menu 

    Global Functions
    - Get Sibling
    - Slide Up
    - Slide Down
    - Slide Toggle
-----------------------------------*/

/* Get Sibling */
const getSiblings = (elem) => {
    const siblings = []
    let sibling = elem.parentNode.firstChild

    while (sibling) {
        if (sibling.nodeType === 1 && sibling !== elem) {
            siblings.push(sibling)
        }
        sibling = sibling.nextSibling
    }
    return siblings
}

/* Slide Up */
const slideUp = (target, time) => {
    const duration = time ? time : 500
    target.style.transitionProperty = "height, margin, padding"
    target.style.transitionDuration = duration + "ms"
    target.style.boxSizing = "border-box"
    target.style.height = target.offsetHeight + "px"
    target.offsetHeight
    target.style.overflow = "hidden"
    target.style.height = 0
    window.setTimeout(() => {
        target.style.display = "none"
        target.style.removeProperty("height")
        target.style.removeProperty("overflow")
        target.style.removeProperty("transition-duration")
        target.style.removeProperty("transition-property")
    }, duration)
}

/* Slide Down */
const slideDown = (target, time) => {
    const duration = time ? time : 500
    target.style.removeProperty("display")
    let display = window.getComputedStyle(target).display
    if (display === "none") display = "block"
    target.style.display = display
    const height = target.offsetHeight
    target.style.overflow = "hidden"
    target.style.height = 0
    target.offsetHeight
    target.style.boxSizing = "border-box"
    target.style.transitionProperty = "height, margin, padding"
    target.style.transitionDuration = duration + "ms"
    target.style.height = height + "px"
    window.setTimeout(() => {
        target.style.removeProperty("height")
        target.style.removeProperty("overflow")
        target.style.removeProperty("transition-duration")
        target.style.removeProperty("transition-property")
    }, duration)
}

/* Slide Toggle */
const slideToggle = (target, time) => {
    const duration = time ? time : 500
    if (window.getComputedStyle(target).display === "none") {
        return slideDown(target, duration)
    } else {
        return slideUp(target, duration)
    }
}

/* Offcanvas/Collapseable Menu */
const offCanvasMenu = (selector) => {
    const offCanvasNav = document.querySelector(selector)

    offCanvasNav.querySelectorAll(".menu-expand").forEach((item) => {
        item.addEventListener("click", (e) => {
            e.preventDefault()
            const parent = item.parentElement.parentElement

            if (parent.classList.contains("active")) {
                parent.classList.remove("active")

                parent
                    .querySelectorAll(".sub-menu, .mega-menu, .children")
                    .forEach((subMenu) => {
                        subMenu.parentElement.classList.remove("active")
                        slideUp(subMenu)
                    })
            } else {
                parent.classList.add("active")
                slideDown(item.parentElement.nextElementSibling)

                getSiblings(parent).forEach((item) => {
                    item.classList.remove("active")

                    item.querySelectorAll(
                        ".sub-menu, .mega-menu, .children"
                    ).forEach((subMenu) => {
                        subMenu.parentElement.classList.remove("active")
                        slideUp(subMenu)
                    })
                })
            }
        })
    })
}

offCanvasMenu(".navbar-mobile-menu")



// Hero Slider Js
var swiperHeroSlider = new Swiper(".hero-slider-active", {
    navigation: {
        nextEl: ".hero-swiper-button-next",
        prevEl: ".hero-swiper-button-prev",
    },
    pagination: {
        el: ".hero-swiper-pagination",
        clickable: true,
    },
});


// Product Row Slider Js
var swiperProductSlider = new Swiper(".product-row-2-slider-active", {
    spaceBetween: 30,
    slidesPerView: 1,
    navigation: {
        nextEl: ".product-row-2-swiper-button-next",
        prevEl: ".product-row-2-swiper-button-prev",
    },
    pagination: {
        el: ".product-swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        1200: {
            slidesPerView: 4,
            spaceBetween: 30,
        },
        1024: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 30,
        },
        576: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        400: {
            slidesPerView: 2,
            spaceBetween: 15,
        },
        320: {
            slidesPerView: 1,
            spaceBetween: 15,
        },
    },
});
var swiperProductSlider = new Swiper(".product-row-2-slider-two-active", {
    spaceBetween: 30,
    slidesPerView: 1,
    navigation: {
        nextEl: ".product-row-2-swiper-button-next",
        prevEl: ".product-row-2-swiper-button-prev",
    },
    pagination: {
        el: ".product-swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        1200: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        1024: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 30,
        },
        576: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        400: {
            slidesPerView: 2,
            spaceBetween: 15,
        },
        320: {
            slidesPerView: 1,
            spaceBetween: 15,
        },
    },
});
// Product Row Slider Js
var swiperProductSlider = new Swiper(".product-slider-active", {
    spaceBetween: 30,
    slidesPerView: 1,
    navigation: {
        nextEl: ".product-swiper-button-next",
        prevEl: ".product-swiper-button-prev",
    },
    pagination: {
        el: ".product-swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        1200: {
            slidesPerView: 4,
            spaceBetween: 30,
        },
        1024: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 30,
        },
        576: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        400: {
            slidesPerView: 2,
            spaceBetween: 15,
        },
        320: {
            slidesPerView: 1,
            spaceBetween: 15,
        },
    },
});
// Product Row Slider Js
var swiperProductSlider = new Swiper(".product-slider-two-active", {
    spaceBetween: 30,
    slidesPerView: 1,
    navigation: {
        nextEl: ".product-swiper-button-next",
        prevEl: ".product-swiper-button-prev",
    },
    pagination: {
        el: ".product-swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        1200: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        1024: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 30,
        },
        576: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        400: {
            slidesPerView: 2,
            spaceBetween: 15,
        },
        320: {
            slidesPerView: 1,
            spaceBetween: 15,
        },
    },
});


// Quick View Poduct Slider JS
var swiperProductThumbItem = new Swiper(".product-quickview-sm-thum-active", {
    slidesPerView: 'auto',
    spaceBetween: 10,
    centeredSlides: false,
    loop: true,
    slideToClickedSlide: true,
    slidesPerView: 4,
    center: true,
});

var swiperProductLargeItem = new Swiper(".product-quickview-lg-active", {
    slidesPerView: 1,
    centeredSlides: true,
    loop: true,
    loopedSlides: 6,
    navigation: {
        nextEl: ".product-details-button-next",
        prevEl: ".product-details-button-prev",
    },
    thumbs: {
        swiper: swiperProductThumbItem,
    },
});


// Poduct Details Slider JS
var swiperProductThumbItem = new Swiper(".product-details-sm-thum-active", {
    loop: true,
    spaceBetween: 10,
    slidesPerView: 4,
    freeMode: true,
    watchSlidesProgress: true,
});
var swiperProductLargeItem = new Swiper(".product-details-lg-active", {
    loop: true,
    spaceBetween: 10,
    center: true,
    navigation: {
        nextEl: ".product-details-button-next",
        prevEl: ".product-details-button-prev",
    },
    thumbs: {
        swiper: swiperProductThumbItem,
    },
});


// Testimonials Slider Js
var swiperTestimonialSlider = new Swiper(".testimonials-slider-active", {
    spaceBetween: 30,
    slidesPerView: 1,
    navigation: {
        nextEl: ".testimonial-swiper-button-next",
        prevEl: ".testimonial-swiper-button-prev",
    },
    pagination: {
        el: ".testimonial-swiper-pagination",
        clickable: true,
    },
});


var swiperBrandSlider = new Swiper(".patner-brand-slider-active", {
    spaceBetween: 60,
    slidesPerView: 6,
    breakpoints: {
        1024: {
            slidesPerView: 6,
            spaceBetween: 50,
        },
        768: {
            slidesPerView: 4,
            spaceBetween: 40,
        },
        640: {
            slidesPerView: 3,
            spaceBetween: 20,
        },
        320: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
    },
});


// Testimonials Slider Js
var swiperSubCategorisSlider = new Swiper(".shop-subcategories-slider-active", {
    spaceBetween: 30,
    slidesPerView: 1,
    navigation: {
        nextEl: ".shop-subcategories-swiper-button-next",
        prevEl: ".shop-subcategories-swiper-button-prev",
    },
    pagination: {
        el: ".shop-subcategory-swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        1024: {
            slidesPerView: 5,
            spaceBetween: 30,
        },
        768: {
            slidesPerView: 4,
            spaceBetween: 30,
        },
        640: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        420: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
    },
});



// Product Row Slider Js
var swiperProductSlider = new Swiper(".product-slider-03-active", {
    spaceBetween: 30,
    slidesPerView: 1,
    navigation: {
        nextEl: ".product-swiper-button-next",
        prevEl: ".product-swiper-button-prev",
    },
    pagination: {
        el: ".product-swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        1200: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        1024: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 30,
        },
        576: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        400: {
            slidesPerView: 2,
            spaceBetween: 15,
        },
        320: {
            slidesPerView: 1,
            spaceBetween: 15,
        },
    },
});


// Product Row Slider Js
var swiperProductSlider = new Swiper(".related-posts-slider-active", {
    spaceBetween: 30,
    slidesPerView: 1,
    navigation: {
        nextEl: ".related-posts-swiper-button-next",
        prevEl: ".related-posts-swiper-button-prev",
    },
    pagination: {
        el: ".related-posts-swiper-pagination",
        clickable: true,
    },
    breakpoints: {
        1200: {
            slidesPerView: 3,
            spaceBetween: 30,
        },
        1024: {
            slidesPerView: 2,
            spaceBetween: 30,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 30,
        },
        576: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        400: {
            slidesPerView: 2,
            spaceBetween: 15,
        },
        320: {
            slidesPerView: 1,
            spaceBetween: 15,
        },
    },
});

// Blog Slider Js
var swiperHeroSlider = new Swiper(".blog-post-slider-active", {
    navigation: {
        nextEl: ".blog-post-swiper-button-next",
        prevEl: ".blog-post-swiper-button-prev",
    },
    pagination: {
        el: ".blog-post-swiper-pagination",
        clickable: true,
    },
});

/*-------------------------
// Product Quantity Increment & Decrement 
---------------------------*/
const quantityItems = document.querySelectorAll(".product-item-quantity");
const productQuantity = (selector) => {
    selector && selector.forEach((item) => {
        const quantityInput = item.querySelector(".product-item-quantity-input");
        const quantityDecrement = item.querySelector(".product-item-quantity-decrement");
        const quantityIncrement = item.querySelector(".product-item-quantity-increment");
        let quantityValue = 1;

        quantityIncrement.addEventListener("click", () => {
            quantityValue++;
            quantityInput.value = quantityValue;
        });

        quantityDecrement.addEventListener("click", () => {
            if (quantityValue > 1) {
            quantityValue--;
            quantityInput.value = quantityValue;
            }
        });
    });
} 
productQuantity(quantityItems) 

/*-------------------------
    Shop Page Product Grid or List View Action JS
--------------------------*/
const viewDisplayButtons = document.querySelectorAll(".shop-display")
const viewsOptionsWrap = document.querySelector('.shop-views-wrap');
const parentsDiv = document.querySelector(".products-wrapper")

const productViewItem = (selector) => {
    selector && selector.addEventListener("click", (e)=> {
        const clicked = e.target.closest('.shop-display');
        if(!clicked) return;
        // Remove active class
        viewDisplayButtons.forEach(t => t.classList.remove('active'));
        // Class added
        clicked.classList.add('active');

        // Parent div class active
        if(clicked.dataset.display === "grid") {
            parentsDiv.classList.remove("shop-view-item-list")
            parentsDiv.classList.add("shop-view-item-grid")
            const childElementToModify = parentsDiv.children[0];
            if (childElementToModify) {
                childElementToModify.classList.add("row-cols-sm-2", "row-cols-md-3" ,"row-cols-lg-3" );
            }
        } 
        if(clicked.dataset.display === "list") {
            parentsDiv.classList.remove("shop-view-item-grid")
            parentsDiv.classList.add("shop-view-item-list")
            const childElementToModify = parentsDiv.children[0];
            if (childElementToModify) {
                childElementToModify.classList.remove("row-cols-sm-2", "row-cols-md-3" ,"row-cols-lg-3");
            }
        }
    })
}
productViewItem(viewsOptionsWrap)


/*---------------------------------
    Price Range Slider
-----------------------------------*/
const priceRange = (selector) => {
    const priceRange = document.querySelector(selector)

    if (priceRange) {
        const rangeInput = document.querySelectorAll(
            ".filter-range-input input"
        )
        const priceInput = document.querySelectorAll(
            ".filter-price-value input"
        )
        const range = document.querySelector(".filter-slider .filter-progress")
        let priceGap = 10

        window.addEventListener("load", () => {
            let minVal = parseInt(rangeInput[0].value)
            let maxVal = parseInt(rangeInput[1].value)

            range.style.left = (minVal / rangeInput[0].max) * 100 + "%"
            range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%"
        })

        priceInput.forEach((input) => {
            input.addEventListener("input", (e) => {
                let minPrice = parseInt(priceInput[0].value)
                let maxPrice = parseInt(priceInput[1].value)

                if (
                    maxPrice - minPrice >= priceGap &&
                    maxPrice <= rangeInput[1].max
                ) {
                    if (e.target.className === "input-min") {
                        rangeInput[0].value = minPrice
                        range.style.left =
                            (minPrice / rangeInput[0].max) * 100 + "%"
                    } else {
                        rangeInput[1].value = maxPrice
                        range.style.right =
                            100 - (maxPrice / rangeInput[1].max) * 100 + "%"
                    }
                }
            })
        })

        rangeInput.forEach((input) => {
            input.addEventListener("input", (e) => {
                let minVal = parseInt(rangeInput[0].value)
                let maxVal = parseInt(rangeInput[1].value)

                if (maxVal - minVal < priceGap) {
                    if (e.target.className === "range-min") {
                        rangeInput[0].value = maxVal - priceGap
                    } else {
                        rangeInput[1].value = minVal + priceGap
                    }
                } else {
                    priceInput[0].value = "$" + minVal
                    priceInput[1].value = "$" + maxVal
                    range.style.left = (minVal / rangeInput[0].max) * 100 + "%"
                    range.style.right =
                        100 - (maxVal / rangeInput[1].max) * 100 + "%"
                }
            })
        })
    }
}

priceRange(".price-range-filter")

/*------------------------
    Expand Content
--------------------------*/
const blockExpand = document.querySelector('.block-expand')
const expandContent = document.querySelector('.expand-content')
if(blockExpand) {
    blockExpand.addEventListener('click', function(e){
        e.preventDefault();
        const text = this.textContent.trim()
        if(text === "Show more") {
            this.innerHTML = "Show less"
            this.classList.add('remove')
        } else {
            this.innerHTML = "Show more"
            this.classList.remove('remove')
        }
        expandContent.classList.toggle('expanded-content')
    })
}

/*------------------------
    Product Zoom Element 
--------------------------*/
// Get all the zoom image items
const zoomImageItems = document.querySelectorAll(".zoom-item");

// Loop through each zoom image item and apply the event listener
if(zoomImageItems) {
    zoomImageItems.forEach((zoomImageItem) => {
        const zoomImage = zoomImageItem.querySelector(".zoom-img");

        zoomImageItem.addEventListener("mousemove", (e) => {
            const x = (e.pageX - zoomImageItem.offsetLeft) / zoomImageItem.offsetWidth;
            const y = (e.pageY - zoomImageItem.offsetTop) / zoomImageItem.offsetHeight;

            zoomImage.style.transformOrigin = `${x * 50}% ${y * 50}%`;
        });
    });
}

//  Vertical Swiper Gallery
var galleryThumbs = new Swiper(".gallery-vertical-thumbs", {
    loop: true,
    slidesPerView: 4,
    watchOverflow: true,
    watchSlidesVisibility: true,
    watchSlidesProgress: true,
    direction: 'vertical',
    spaceBetween: 15,
    breakpoints: {
        1420: {
            slidesPerView: 4,
            spaceBetween: 30,
        },
        1200: {
            slidesPerView: 4,
            spaceBetween: 30,
        },
        992: {
            slidesPerView: 4,
            spaceBetween: 10,
        },
        768: {
            slidesPerView: 4,
            spaceBetween: 10,
        },
        575: {
            slidesPerView: 3,
            spaceBetween: 10,
        },
        320: {
            slidesPerView: 3,
            spaceBetween: 10,
        },
    },
});

var galleryMain = new Swiper(".gallery-main", {
    watchOverflow: true,
    watchSlidesVisibility: true,
    watchSlidesProgress: true,
    preventInteractionOnTransition: true,
    navigation: {
      nextEl: '.product-details-button-next',
      prevEl: '.product-details-button-prev',
    },
    effect: 'fade',
      fadeEffect: {
      crossFade: true
    },
    thumbs: {
      swiper: galleryThumbs
    }
});
  
galleryMain.on('slideChangeTransitionStart', function() {
    galleryThumbs.slideTo(galleryMain.activeIndex);
});
  
galleryThumbs.on('transitionStart', function(){
    galleryMain.slideTo(galleryThumbs.activeIndex);
});

/*------------------------
    Counter Up
------------------------*/
// Function to handle the Counter Up animation
function startCounterUp(item) {
    let count = 0;
    function counterUp() {
        count++;
        item.innerHTML = count;
        if (count == item.dataset.number) {
            clearInterval(stop);
        }
    }
    let stop = setInterval(() => {
        counterUp();
    }, 100 / item.dataset.speed);
}

// Intersection Observer callback
function handleIntersection(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            startCounterUp(entry.target);
            observer.unobserve(entry.target);
        }
    });
}

// Select all counters and convert NodeList to array
let counterUpAll = document.querySelectorAll(".counterup-item-number");
let counterUpArray = Array.from(counterUpAll);

// Create Intersection Observer instance
let counterUpObserverHendler = new IntersectionObserver(handleIntersection, {
    threshold: 0.1, // Adjust this threshold as needed
});

// Observe each counter Up element
counterUpArray.forEach(counterUpItem => {
    counterUpObserverHendler.observe(counterUpItem);
});


/*------------------------
    Coupon Form toggle JS
--------------------------*/
const couponViewClickTarget = document.querySelector(".coupon-toggle-text");
const couponContent = document.querySelector(".coupon-form-content");
if(couponViewClickTarget) {
    couponViewClickTarget.addEventListener("click", (e) => {
        e.preventDefault();
        slideToggle(couponContent, 300);
    })
}
const couponForm = document.querySelector("#chekout-box-2");
const shipBoxInfo = document.querySelector(".ship-box-info");
const createAccountchekoutBox = document.querySelector("#create-account-box");
const checkoutAccountCreateContainer = document.querySelector(".checkout-account-create");
if(couponForm) {
    couponForm.addEventListener("change", (e) => {
        slideToggle(shipBoxInfo, 300);
    })
}
if(createAccountchekoutBox) {
    createAccountchekoutBox.addEventListener("change", (e) => {
        slideToggle(checkoutAccountCreateContainer, 300);
    })
}



/*------------------------
    Accordion/Collapse
--------------------------*/

const accordionCollapseElements = document.querySelectorAll('.collapse');

accordionCollapseElements.forEach((collapse) => {
    collapse.addEventListener('show.bs.collapse', function(e) {
        let card = this.closest('.payment-method-accordion-card');
        card.classList.add('active');
        // Remove active class
        getSiblings(card).forEach((sibling) => {
            sibling.classList.remove('active');
        });
    });
    
    collapse.addEventListener('hide.bs.collapse', function(e) {
        let card = this.closest('.payment-method-accordion-card');
        card.classList.remove('active');
    });
});

