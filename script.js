const scoreInput = document.querySelector("#score-input");
const scoreValue = document.querySelector("#score-value");
const awardFields = {
  grand: {
    bar: document.querySelector("#bar-grand"),
    value: document.querySelector("#grand-value"),
  },
  first: {
    bar: document.querySelector("#bar-first"),
    value: document.querySelector("#first-value"),
  },
  second: {
    bar: document.querySelector("#bar-second"),
    value: document.querySelector("#second-value"),
  },
  third: {
    bar: document.querySelector("#bar-third"),
    value: document.querySelector("#third-value"),
  },
};

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function updateAward(score) {
  const grand = clamp((score - 88) * 3.5, 0, 42);
  const first = clamp((score - 72) * 2.1, 4, 58);
  const second = clamp(65 - Math.abs(score - 76) * 1.45, 12, 54);
  const third = clamp(100 - grand - first - second, 2, 72);
  const total = grand + first + second + third;
  const values = {
    grand: Math.round((grand / total) * 100),
    first: Math.round((first / total) * 100),
    second: Math.round((second / total) * 100),
    third: Math.round((third / total) * 100),
  };

  scoreValue.textContent = score;
  Object.entries(values).forEach(([key, value]) => {
    awardFields[key].bar.style.width = `${value}%`;
    awardFields[key].value.textContent = `${value}%`;
  });
}

if (scoreInput) {
  scoreInput.addEventListener("input", (event) => updateAward(Number(event.target.value)));
  updateAward(Number(scoreInput.value));
}

const fileInput = document.querySelector("#paper-file");
const fileName = document.querySelector("#file-name");

if (fileInput && fileName) {
  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    fileName.textContent = file ? file.name : "选择或拖放论文文件";
  });
}

const paperPreview = document.querySelector("#paper-preview");
const paperPageLabel = document.querySelector("#paper-page-label");
const paperDots = document.querySelectorAll(".paper-dots button");
const paperPrev = document.querySelector(".stage-prev");
const paperNext = document.querySelector(".stage-next");
const paperPages = Array.from({ length: 6 }, (_, index) => ({
  src: `assets/reference-paper-page-${index + 1}.png`,
  alt: `MathorCup 2026 B 参考例文第 ${index + 1} 页预览`,
}));
let activePaperPage = 0;
let pointerInsidePaperStage = false;

function updatePaperPreview(nextPage, direction = 1) {
  if (!paperPreview || !paperPageLabel || !paperPages.length) return;

  activePaperPage = (nextPage + paperPages.length) % paperPages.length;
  const page = paperPages[activePaperPage];

  paperPreview.classList.add("is-changing");
  paperPreview.style.transform = `translateX(${direction * 22}px) scale(0.985)`;

  window.setTimeout(() => {
    paperPreview.src = page.src;
    paperPreview.alt = page.alt;
    paperPreview.dataset.page = String(activePaperPage + 1);
    paperPageLabel.textContent = `${activePaperPage + 1} / ${paperPages.length}`;

    paperDots.forEach((dot, index) => {
      dot.classList.toggle("active", index === activePaperPage);
      dot.setAttribute("aria-current", index === activePaperPage ? "true" : "false");
    });

    paperPreview.style.transform = `translateX(${-direction * 18}px) scale(0.99)`;
    requestAnimationFrame(() => {
      paperPreview.classList.remove("is-changing");
      paperPreview.style.transform = "";
    });
  }, 180);
}

if (paperPreview) {
  paperPrev?.addEventListener("click", () => updatePaperPreview(activePaperPage - 1, -1));
  paperNext?.addEventListener("click", () => updatePaperPreview(activePaperPage + 1, 1));
  paperDots.forEach((dot) => {
    dot.addEventListener("click", () => {
      const nextPage = Number(dot.dataset.page);
      updatePaperPreview(nextPage, nextPage >= activePaperPage ? 1 : -1);
    });
  });

  document.querySelector(".paper-stage")?.addEventListener("pointerenter", () => {
    pointerInsidePaperStage = true;
  });
  document.querySelector(".paper-stage")?.addEventListener("pointerleave", () => {
    pointerInsidePaperStage = false;
  });

  window.addEventListener("keydown", (event) => {
    if (!pointerInsidePaperStage && !document.activeElement?.closest?.(".paper-stage")) return;
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      updatePaperPreview(activePaperPage - 1, -1);
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      updatePaperPreview(activePaperPage + 1, 1);
    }
  });
}

document.body.classList.add("motion-ready");

const header = document.querySelector(".site-header");
const glow = document.createElement("div");
glow.className = "cursor-glow";
document.body.appendChild(glow);

window.addEventListener("scroll", () => {
  header?.classList.toggle("is-scrolled", window.scrollY > 16);
}, { passive: true });

window.addEventListener("pointermove", (event) => {
  document.body.style.setProperty("--glow-x", `${event.clientX}px`);
  document.body.style.setProperty("--glow-y", `${event.clientY}px`);
  glow.style.left = `${event.clientX}px`;
  glow.style.top = `${event.clientY}px`;
  glow.style.opacity = "1";
}, { passive: true });

const revealTargets = document.querySelectorAll(
  ".section-heading, .intro-text, .intro-grid article, .competition-card, .pipeline-strip, .workflow-inner, .steps article, .evaluation-head, .evaluation-card, .ecosystem-chips, .ecosystem-map, .ecosystem-flow, .paper-intro, .paper-stage, .reference-rules article, .estimate-copy, .award-board, .report-score-panel, .report-radar, .report-actions, .platform-copy, .dashboard-preview, .trust-stats article, .testimonial-card, .download-cta > div, .upload-panel, .upload-workbench, .live-console, .download-card, .release-card"
);

revealTargets.forEach((element, index) => {
  element.classList.add("reveal-item");
  element.style.transitionDelay = `${Math.min(index % 8, 5) * 45}ms`;
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("is-visible");
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });

revealTargets.forEach((element) => revealObserver.observe(element));

document.querySelectorAll(".competition-card, .evaluation-card, .ecosystem-map, .intro-grid article, .steps article, .testimonial-card, .download-card, .release-card").forEach((card) => {
  card.classList.add("tilt-card");
  card.addEventListener("pointermove", (event) => {
    const rect = card.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;
    card.style.setProperty("--tilt-x", `${(-y * 4).toFixed(2)}deg`);
    card.style.setProperty("--tilt-y", `${(x * 5).toFixed(2)}deg`);
  });
  card.addEventListener("pointerleave", () => {
    card.style.setProperty("--tilt-x", "0deg");
    card.style.setProperty("--tilt-y", "0deg");
  });
});

const canvas = document.createElement("canvas");
canvas.className = "site-particles";
document.body.prepend(canvas);

const context = canvas.getContext("2d");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
let particles = [];
let width = 0;
let height = 0;
let frame = 0;

function resizeParticles() {
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = Math.floor(width * ratio);
  canvas.height = Math.floor(height * ratio);
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;
  context.setTransform(ratio, 0, 0, ratio, 0, 0);

  const count = Math.min(130, Math.max(54, Math.floor((width * height) / 15000)));
  particles = Array.from({ length: count }, (_, index) => {
    const seed = index + 1;
    return {
      x: (seed * 97) % width,
      y: (seed * 193) % height,
      r: 1.2 + ((seed * 17) % 42) / 18,
      vx: (((seed * 29) % 100) - 50) / 900,
      vy: (((seed * 37) % 100) - 50) / 900,
      hue: ["#5b8cff", "#8a5cf6", "#19d5bf", "#f4a51c"][seed % 4],
      alpha: 0.18 + ((seed * 13) % 70) / 220,
    };
  });
}

function drawParticles() {
  context.clearRect(0, 0, width, height);
  frame += 1;

  particles.forEach((particle, index) => {
    if (!reducedMotion) {
      particle.x += particle.vx * 16;
      particle.y += particle.vy * 16;
      if (particle.x < -20) particle.x = width + 20;
      if (particle.x > width + 20) particle.x = -20;
      if (particle.y < -20) particle.y = height + 20;
      if (particle.y > height + 20) particle.y = -20;
    }

    context.globalAlpha = particle.alpha * (0.74 + Math.sin((frame + index * 11) / 56) * 0.26);
    context.fillStyle = particle.hue;
    context.beginPath();
    context.arc(particle.x, particle.y, particle.r, 0, Math.PI * 2);
    context.fill();

    for (let next = index + 1; next < Math.min(index + 6, particles.length); next += 1) {
      const other = particles[next];
      const dx = particle.x - other.x;
      const dy = particle.y - other.y;
      const distance = Math.hypot(dx, dy);
      if (distance < 150) {
        context.globalAlpha = (1 - distance / 150) * 0.08;
        context.strokeStyle = particle.hue;
        context.lineWidth = 1;
        context.beginPath();
        context.moveTo(particle.x, particle.y);
        context.lineTo(other.x, other.y);
        context.stroke();
      }
    }
  });

  context.globalAlpha = 1;
  requestAnimationFrame(drawParticles);
}

resizeParticles();
drawParticles();
window.addEventListener("resize", resizeParticles, { passive: true });
