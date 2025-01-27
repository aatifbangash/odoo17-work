/** @odoo-module **/
(function () {

//document.querySelector('.left_section').addEventListener('wheel', function(e) {
//            document.querySelector('.right_section').scrollTop += e.deltaY;
//        });
function toggleClass() {
        const designStudioDiv = document.getElementById('why_us');
        const seeMoreButton = document.getElementById('seeMoreButton');

        // This block will now work only if designStudioDiv and seeMoreButton exist.
        if (designStudioDiv && seeMoreButton) {
            designStudioDiv.classList.toggle('website_content_wrapper');
            designStudioDiv.classList.toggle('why_us_html');

            // Toggle button text
            if (seeMoreButton.textContent === "Show More") {
                seeMoreButton.textContent = "Show Less";
            } else {
                seeMoreButton.textContent = "Show More";
            }
        }
    }


    const seeMoreB = document.getElementById('seeMoreButton');
    const why_us_text = document.getElementById("why_us");

    if (seeMoreB && why_us_text) {
        seeMoreB.addEventListener('click', toggleClass);

        // Check if the container's scroll height is greater than its visible height
        if (why_us_text.scrollHeight > (why_us_text.clientHeight + 100)) {
            seeMoreB.style.display = "block"; // Show the button if content overflows
        } else {
            seeMoreB.style.display = "none"; // Hide the button if no overflow
        }
    }


 // Function to stop the video in the iframe
    function stopVideo(videoIframeId) {
        console.log('Stopping video...');
        const videoIframe = document.getElementById(videoIframeId);
        if (videoIframe) {
            // Save the original src in a data attribute to restore it later
            const originalSrc = videoIframe.getAttribute('data-original-src');
            if (!originalSrc) {
                videoIframe.setAttribute('data-original-src', videoIframe.src); // Save original URL
            }
            videoIframe.src = ""; // Resetting the src stops the video
        }
    }

    // Function to reset the video src when the modal opens
    function resetVideo(videoIframeId) {
        const videoIframe = document.getElementById(videoIframeId);
        if (videoIframe) {
            const originalSrc = videoIframe.getAttribute('data-original-src');
            if (originalSrc) {
                videoIframe.src = originalSrc; // Restore the original URL
            }
        }
    }

    // Function to add modal events
    function addModalEvents(modalId, videoIframeId) {
        const modalElement = document.getElementById(modalId);
        if (modalElement) {
            // Stop video when modal is hidden
            modalElement.addEventListener('hidden.bs.modal', function () {
                stopVideo(videoIframeId);
            });

            // Reset video src when modal is shown again
            modalElement.addEventListener('shown.bs.modal', function () {
                resetVideo(videoIframeId);
            });
        }
    }

    // Dynamically add modal events for each modal with dynamic IDs
    document.querySelectorAll('.modal').forEach(function (modalElement) {
        const modalId = modalElement.getAttribute('id');
        const videoIframeId = modalElement.querySelector('iframe')?.getAttribute('id');
        if (modalId && videoIframeId) {
            addModalEvents(modalId, videoIframeId);
        }
    });
let items = document.querySelectorAll('.carousel .carousel-item')

		items.forEach((el) => {
			const minPerSlide = 4
			let next = el.nextElementSibling
			for (var i=1; i<minPerSlide; i++) {
				if (!next) {
            // wrap carousel by using first child
            next = items[0]
        }
        let cloneChild = next.cloneNode(true)
        el.appendChild(cloneChild.children[0])
        next = next.nextElementSibling
    }
})

    const buttonElement= document.getElementById('button-home');
    const amenitiesElement= document.getElementById('button-amenities');
    const planVisitElement = document.getElementById('button-planVisit');
    const exploreElement = document.getElementById('button-explore');
    const learnElement = document.getElementById('button-learn');
    const sitePlanElement = document.getElementById('button-sitePlan');


    if(buttonElement){
        const dataAttribute = buttonElement.getAttribute('data-id');
        buttonElement.addEventListener("click", function scrollToSection() {
            const section = document.getElementById(dataAttribute);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    if(amenitiesElement){
        const amenitiesAttribute = amenitiesElement.getAttribute('data-id');
        amenitiesElement.addEventListener("click", function scrollToSection() {
                const section = document.getElementById(amenitiesAttribute);
                if (section) {
                    section.scrollIntoView({ behavior: 'smooth' });
                }
        });
    }

    if(planVisitElement){
        const planVisitAttribute = planVisitElement.getAttribute('data-id');
        planVisitElement.addEventListener("click", function scrollToSection() {
                const section = document.getElementById(planVisitAttribute);
                if (section) {
                    section.scrollIntoView({ behavior: 'smooth' });
                }
        });
    }

    if(exploreElement){
        const exploreAttribute = exploreElement.getAttribute('data-id');
        exploreElement.addEventListener("click", function scrollToSection() {
                const section = document.getElementById(exploreAttribute);
                if (section) {
                    section.scrollIntoView({ behavior: 'smooth' });
                }
        });
    }

    if(learnElement){
        const learnAttribute = learnElement.getAttribute('data-id');
        learnElement.addEventListener("click", function scrollToSection() {
                const section = document.getElementById(learnAttribute);
                if (section) {
                    section.scrollIntoView({ behavior: 'smooth' });
                }
        });
    }

    if(sitePlanElement){
        const sitePlanAttribute = sitePlanElement.getAttribute('data-id');
        sitePlanElement.addEventListener("click", function scrollToSection() {
                const section = document.getElementById(sitePlanAttribute);
                if (section) {
                    section.scrollIntoView({ behavior: 'smooth' });
                }
        });
    }

    $('.im_interested').on('click', function() {
          $("html, body").animate({ scrollTop: 0 }, "slow");
    })
})();