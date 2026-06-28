const componentData = {
    frontend: {
        title: "React Dashboard",
        body: "The engineering UI for incident timelines, AI explanations, system health and operational insights.",
        points: ["Displays incident timeline", "Shows AI-generated summaries", "Supports engineer investigation workflow", "Connects to FastAPI backend"]
    },
    api: {
        title: "FastAPI Backend",
        body: "The application API layer that exposes incidents, integrations, AI insights, users and operational workflows.",
        points: ["REST API surface", "Authentication boundary", "Business orchestration", "Connects services and data layer"]
    },
    gateway: {
        title: "API Gateway",
        body: "The edge layer responsible for routing, policy enforcement, authentication and request protection.",
        points: ["Request routing", "JWT validation", "Rate limiting", "External API boundary"]
    },
    events: {
        title: "Event Bus",
        body: "The asynchronous backbone for incident events, retries, background processing and operational state changes.",
        points: ["Publishes operational events", "Decouples services", "Supports replayable workflows", "Improves reliability"]
    },
    ai: {
        title: "AI Reasoning Engine",
        body: "Correlates telemetry, events and operational context to explain failures and recommend next actions.",
        points: ["Builds investigation context", "Uses MCP tools", "Generates root-cause summaries", "Produces recommended actions"]
    },
    mcp: {
        title: "MCP Server",
        body: "Provides safe, controlled tools that AI agents can call during investigations.",
        points: ["Tool registry", "Controlled execution", "Audit trail", "System-specific context lookup"]
    },
    postgres: {
        title: "PostgreSQL",
        body: "Primary relational store for incidents, integrations, users, timelines and AI insights.",
        points: ["Structured data", "Relational integrity", "Audit records", "Query-ready operational model"]
    },
    redis: {
        title: "Redis Queue",
        body: "Supports async processing, background jobs, event buffering and fast operational state access.",
        points: ["Job queues", "Temporary state", "Retry support", "Low-latency processing"]
    },
    observability: {
        title: "Observability",
        body: "Captures logs, traces, metrics and AI reasoning evidence for transparent operations.",
        points: ["Structured logs", "Request tracing", "Health metrics", "AI evidence records"]
    }
};

const panel = document.querySelector("#componentPanel");
const nodes = document.querySelectorAll(".arch-node");

nodes.forEach((node) => {
    node.addEventListener("click", () => {
        const data = componentData[node.dataset.component];
        if (!data || !panel) return;

        panel.innerHTML = `
            <p class="panel-label">Selected Component</p>
            <h3>${data.title}</h3>
            <p>${data.body}</p>
            <ul>${data.points.map((point) => `<li>${point}</li>`).join("")}</ul>
        `;

        nodes.forEach((item) => item.classList.remove("node-featured"));
        node.classList.add("node-featured");
    });
});

if (window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);

    gsap.utils.toArray(".section, .portal-hero").forEach((section) => {
        gsap.from(section.children, {
            opacity: 0,
            y: 36,
            duration: 0.9,
            ease: "power3.out",
            stagger: 0.08,
            scrollTrigger: {
                trigger: section,
                start: "top 72%"
            }
        });
    });
}

const navLinks = document.querySelectorAll(".side-nav a");
const sections = [...navLinks].map((link) => document.querySelector(link.getAttribute("href"))).filter(Boolean);

window.addEventListener("scroll", () => {
    const current = sections.findLast((section) => section.getBoundingClientRect().top <= 160);
    if (!current) return;

    navLinks.forEach((link) => {
        link.classList.toggle("active", link.getAttribute("href") === `#${current.id}`);
    });
});
