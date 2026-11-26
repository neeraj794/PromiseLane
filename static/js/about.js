document.documentElement.classList.add("js");

var revealTargets = document.querySelectorAll("[data-about-reveal]");
var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    revealTargets.forEach(function (target) {
        target.classList.add("is-visible");
    });
} else {
    var revealObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            }
        });
    }, {
        rootMargin: "0px 0px -40px 0px",
        threshold: 0.12
    });

    revealTargets.forEach(function (target) {
        revealObserver.observe(target);
    });
}
