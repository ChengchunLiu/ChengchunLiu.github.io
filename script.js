const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: "0px 0px -40px" },
);

document.documentElement.classList.add("motion-ready");

document.querySelectorAll(".reveal").forEach((element, index) => {
  element.style.transitionDelay = `${Math.min(index % 3, 2) * 80}ms`;
  revealObserver.observe(element);
});

const sideGuideLinks = Array.from(document.querySelectorAll(".side-guide [data-guide-target]"));
const sideGuideSections = sideGuideLinks
  .map((link) => ({ link, section: document.getElementById(link.dataset.guideTarget) }))
  .filter(({ section }) => section);

function updateSideGuide() {
  if (!sideGuideSections.length) return;

  const probe = window.scrollY + window.innerHeight * 0.34;
  let activeId = sideGuideSections[0].section.id;

  sideGuideSections.forEach(({ section }) => {
    if (section.offsetTop <= probe) activeId = section.id;
  });

  if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 8) {
    activeId = sideGuideSections[sideGuideSections.length - 1].section.id;
  }

  sideGuideSections.forEach(({ link, section }) => {
    const isActive = section.id === activeId;
    link.classList.toggle("is-active", isActive);
    if (isActive) {
      link.setAttribute("aria-current", "location");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

let sideGuideFrame = null;

function requestSideGuideUpdate() {
  if (sideGuideFrame !== null) return;
  sideGuideFrame = window.requestAnimationFrame(() => {
    updateSideGuide();
    sideGuideFrame = null;
  });
}

window.addEventListener("scroll", requestSideGuideUpdate, { passive: true });
window.addEventListener("resize", requestSideGuideUpdate);
updateSideGuide();

document.querySelectorAll('a[href="#top"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    window.history.replaceState(null, "", `${window.location.pathname}${window.location.search}#top`);
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});

document.querySelectorAll(".mobile-menu a").forEach((link) => {
  link.addEventListener("click", () => {
    link.closest("details")?.removeAttribute("open");
  });
});
