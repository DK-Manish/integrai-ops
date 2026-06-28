gsap.registerPlugin(ScrollTrigger);

gsap.defaults({
    ease: "power3.out",
    duration: 0.9
});

gsap.from(".hero__eyebrow", {
    opacity: 0,
    y: 20,
    duration: 0.8
});

gsap.from(".hero__title", {
    opacity: 0,
    y: 50,
    duration: 1,
    delay: 0.1
});

gsap.from(".hero__subtitle", {
    opacity: 0,
    y: 35,
    duration: 0.9,
    delay: 0.25
});

gsap.from(".hero__actions", {
    opacity: 0,
    y: 30,
    duration: 0.8,
    delay: 0.4
});

gsap.from(".hero__metric", {
    opacity: 0,
    y: 30,
    stagger: 0.12,
    duration: 0.8,
    delay: 0.55
});

gsap.utils.toArray(".reveal").forEach((element) => {
    gsap.from(element, {
        opacity: 0,
        y: 60,
        scrollTrigger: {
            trigger: element,
            start: "top 78%"
        }
    });
});

gsap.from(".timeline-item", {
    opacity: 0,
    y: 45,
    stagger: 0.12,
    scrollTrigger: {
        trigger: ".investigation-timeline",
        start: "top 75%"
    }
});

gsap.from(".capability-card", {
    opacity: 0,
    y: 55,
    stagger: 0.12,
    scrollTrigger: {
        trigger: ".capabilities-grid",
        start: "top 75%"
    }
});

gsap.from(".architecture-node", {
    opacity: 0,
    y: 35,
    stagger: 0.12,
    scrollTrigger: {
        trigger: ".architecture-flow",
        start: "top 78%"
    }
});

gsap.from(".engine-card", {
    opacity: 0,
    y: 55,
    stagger: 0.12,
    scrollTrigger: {
        trigger: ".engine-grid",
        start: "top 75%"
    }
});

gsap.from(".mcp-node", {
    opacity: 0,
    scale: 0.92,
    stagger: 0.12,
    scrollTrigger: {
        trigger: ".mcp-diagram",
        start: "top 78%"
    }
});

gsap.from(".enterprise-grid article", {
    opacity: 0,
    y: 45,
    stagger: 0.08,
    scrollTrigger: {
        trigger: ".enterprise-grid",
        start: "top 78%"
    }
});
