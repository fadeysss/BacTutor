const chapterFilter = document.getElementById('chapterFilter');
if (chapterFilter) {
  chapterFilter.addEventListener('input', (event) => {
    const needle = event.target.value.toLowerCase().trim();
    document.querySelectorAll('.chapter-card').forEach((card) => {
      const haystack = card.dataset.title || '';
      card.style.display = haystack.includes(needle) ? '' : 'none';
    });
  });
}

document.querySelectorAll('.quiz-question').forEach((question) => {
  const inputs = question.querySelectorAll('input[type="radio"]');
  const labels = question.querySelectorAll('.quiz-option');
  const sync = () => {
    labels.forEach((label) => {
      const input = label.querySelector('input[type="radio"]');
      label.classList.toggle('selected', Boolean(input && input.checked));
    });
  };
  inputs.forEach((input) => input.addEventListener('change', sync));
  sync();
});

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (prefersReducedMotion) {
  document.body.classList.add('reduced-motion');
} else {
  document.body.classList.add('motion-enabled');

  const revealNodes = document.querySelectorAll(
    '.hero, .card, .subject-card, .chapter-card, .timeline-item, .quiz-question, .knowledge-card'
  );
  revealNodes.forEach((node, index) => {
    node.classList.add('reveal');
    node.style.setProperty('--stagger-index', String(index % 10));
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  revealNodes.forEach((node) => observer.observe(node));

  const shell = document.querySelector('.shell');
  if (shell) {
    let rafId = 0;
    let lastX = 0;
    let lastY = 0;
    const updateGlow = () => {
      shell.style.setProperty('--pointer-x', `${lastX}px`);
      shell.style.setProperty('--pointer-y', `${lastY}px`);
      rafId = 0;
    };
    window.addEventListener('pointermove', (event) => {
      lastX = event.clientX;
      lastY = event.clientY;
      if (!rafId) {
        rafId = requestAnimationFrame(updateGlow);
      }
    });
  }
}
