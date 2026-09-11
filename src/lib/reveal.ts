import { introDone } from '$lib/stores/intro';

type RevealDirection = 'top' | 'bottom' | 'title' | 'signal';

/** Recreates the original Delvup direction, timing and title rotation. */
export function revealOnView(root: HTMLElement) {
	const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
	const items = new Map<HTMLElement, RevealDirection>();

	function collect(selector: string, direction: RevealDirection) {
		root.querySelectorAll<HTMLElement>(selector).forEach((element) => {
			if (!items.has(element)) items.set(element, direction);
		});
	}

	collect('.brand, .site-header nav a, .theme-switch, .hero-topline > span', 'top');
	collect('.title-line', 'title');
	collect('.signal-column', 'signal');
	collect(
		'.hero-arrow, .hero-bottom > *, .hero-rule > span, .signals-heading .signal-arrow, .section-heading .eyebrow, .section-heading > p, .project, .approach-label > *, .about-copy p, .service > :not(.reveal-title), .contact > .eyebrow, .contact-bottom > *, .site-footer > *',
		'bottom'
	);

	const elements = [...items.keys()];
	elements.forEach((element) => {
		const direction = items.get(element)!;
		element.classList.add('reveal-item', `reveal-from-${direction}`, 'reveal-pending');
		if (direction === 'title') {
			const title = element.closest('.reveal-title, h1');
			const lines = title ? [...title.querySelectorAll<HTMLElement>('.title-line')] : [];
			element.style.setProperty('--reveal-delay', `${Math.max(0, lines.indexOf(element)) * 140}ms`);
		} else if (direction === 'signal') {
			const columns = [...root.querySelectorAll<HTMLElement>('.signal-column')];
			element.style.setProperty(
				'--reveal-delay',
				`${Math.max(0, columns.indexOf(element)) * 85}ms`
			);
		}
	});

	let observer: IntersectionObserver | undefined;
	let introFinished = false;

	function show(element: HTMLElement, delay = 0) {
		if (!['title', 'signal'].includes(items.get(element)!)) {
			element.style.setProperty('--reveal-delay', `${delay}ms`);
		}
		element.classList.remove('reveal-pending');
		observer?.unobserve(element);
	}

	function showAll() {
		observer?.disconnect();
		elements.forEach((element) => show(element));
	}

	if (!reducedMotion.matches && 'IntersectionObserver' in window) {
		observer = new IntersectionObserver(
			(entries) => {
				entries
					.filter((entry) => entry.isIntersecting)
					.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)
					.forEach((entry, index) => show(entry.target as HTMLElement, Math.min(index, 4) * 80));
			},
			{ threshold: 0.12, rootMargin: '0px 0px -8% 0px' }
		);
	}

	const unsubscribe = introDone.subscribe((done) => {
		if (!done || introFinished) return;
		introFinished = true;
		if (observer && !reducedMotion.matches) elements.forEach((element) => observer!.observe(element));
		else showAll();
	});

	const handleReducedMotion = () => {
		if (reducedMotion.matches) showAll();
	};
	const revealFocused = (event: FocusEvent) => {
		if (!(event.target instanceof HTMLElement)) return;
		const item = event.target.closest<HTMLElement>('.reveal-item');
		if (item) show(item);
	};

	reducedMotion.addEventListener('change', handleReducedMotion);
	root.addEventListener('focusin', revealFocused);

	return {
		destroy() {
			unsubscribe();
			root.removeEventListener('focusin', revealFocused);
			observer?.disconnect();
			reducedMotion.removeEventListener('change', handleReducedMotion);
			showAll();
		}
	};
}
