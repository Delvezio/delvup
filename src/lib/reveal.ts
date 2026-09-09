import { introDone } from '$lib/stores/intro';

/** Reveal groups once, preserving the project cards' independent rotations. */
export function revealOnView(root: HTMLElement) {
	const media = matchMedia('(prefers-reduced-motion: reduce)');
	const elements = Array.from(
		root.querySelectorAll<HTMLElement>(
			'.brand, nav a, .theme-switch, .hero-topline, h1, .hero-arrow, .hero-bottom > *, .hero-rule, .section-heading, .project, .approach-label, .approach-copy h2, .about-copy p, .service, .contact > .eyebrow, .contact h2, .contact-bottom > *, .site-footer > *'
		)
	);
	let observer: IntersectionObserver | undefined;
	let finished = false;
	function showAll() {
		observer?.disconnect();
		elements.forEach((el) => el.classList.remove('reveal-pending'));
	}
	if (!media.matches && 'IntersectionObserver' in window) {
		elements.forEach((el) => el.classList.add('reveal-pending'));
		observer = new IntersectionObserver(
			(entries) => {
				entries
					.filter((entry) => entry.isIntersecting)
					.forEach((entry, index) => {
						const el = entry.target as HTMLElement;
						el.style.setProperty('--reveal-delay', `${Math.min(index, 4) * 75}ms`);
						el.classList.remove('reveal-pending');
						observer?.unobserve(el);
					});
			},
			{ threshold: 0.08, rootMargin: '0px 0px -24px 0px' }
		);
	}
	const unsubscribe = introDone.subscribe((done) => {
		if (!done || finished) return;
		finished = true;
		if (observer && !media.matches) elements.forEach((el) => observer!.observe(el));
		else showAll();
	});
	const reduceMotion = () => {
		if (media.matches) showAll();
	};
	media.addEventListener('change', reduceMotion);
	return {
		destroy() {
			unsubscribe();
			observer?.disconnect();
			media.removeEventListener('change', reduceMotion);
			showAll();
		}
	};
}
