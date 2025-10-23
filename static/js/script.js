        // Menu toggle for mobile
        const menuToggle = document.querySelector('.menu-toggle');
        const mainNav = document.querySelector('.main-nav');

        menuToggle.addEventListener('click', () => {
            mainNav.classList.toggle('active');
            menuToggle.classList.toggle('active');
            const expanded = menuToggle.getAttribute('aria-expanded') === 'true' || false;
            menuToggle.setAttribute('aria-expanded', !expanded);
        });

        // Hide/show header on scroll
        let lastScroll = 0;
        const header = document.querySelector('header');

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            if (currentScroll <= 0) {
                header.classList.remove('header-hidden');
                return;
            }

            if (currentScroll > lastScroll && !header.classList.contains('header-hidden')) {
                // Scrolling down
                header.classList.add('header-hidden');
            } else if (currentScroll < lastScroll && header.classList.contains('header-hidden')) {
                // Scrolling up
                header.classList.remove('header-hidden');
            }
            lastScroll = currentScroll;
        });

        // --- New Script for Dynamic Popular Posts Grid ---
        function setPopularGridColumns() {
            const grid = document.getElementById('popular-posts-grid');
            if (!grid) return;

            // Only apply this logic on screens wider than 900px (desktop/large tablet)
            // Below this, CSS media queries will handle the layout (auto-fit/single column)
            if (window.innerWidth <= 900) {
                grid.className = 'popular-posts-grid'; // Clear JS classes on smaller screens
                return;
            }

            const postCount = grid.querySelectorAll('.popular-post-card').length;
            
            // Remove previous column classes
            grid.classList.remove('cols-1', 'cols-2', 'cols-3');

            if (postCount === 1) {
                // One post: occupies one-third width (by adding .cols-1 and aligning it to the start)
                grid.classList.add('cols-1'); 
                // To center a single post in a 1fr grid, you can use:
                // grid.style.justifyContent = 'center'; 
                // But since the requirement is "just one post width occupied", we'll just set the column count.
            } else if (postCount === 2) {
                // Two posts: occupies two-thirds width
                grid.classList.add('cols-2');
            } else if (postCount >= 3) {
                // Three or more posts: full three columns (default CSS)
                grid.classList.add('cols-3');
            }
            // If postCount is 0, nothing happens, which is fine.
        }

        // Run the script on load and resize
        window.addEventListener('load', setPopularGridColumns);
        window.addEventListener('resize', setPopularGridColumns);