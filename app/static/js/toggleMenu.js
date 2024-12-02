/*
This file controls the toggle functionality for the header menu on mobile screen sizes.
*/

let hamburger = document.querySelector('.hamburger');
let navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
    let isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
    hamburger.setAttribute('aria-expanded', !isExpanded);
    navLinks.classList.toggle('active');
});
