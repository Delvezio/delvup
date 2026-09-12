<script lang="ts">
	import { onMount } from 'svelte';
	import { introDone } from '$lib/stores/intro';

	let host: HTMLDivElement;
	let liquid: HTMLDivElement;
	let ready = $state(false);
	let reduced = $state(false);
	let dark = $state(false);
	let hydrated = $state(false);
	const asset = $derived(
		dark
			? reduced
				? '/media/water-bubble-poster.webp'
				: '/media/water-bubble.webp'
			: reduced
				? '/media/water-bubble-light-poster.webp'
				: '/media/water-bubble-light.webp'
	);

	type Stop = { scroll: number; x: number; y: number; scale: number };

	onMount(() => {
		let frame = 0;
		let last = performance.now();
		let size = 480;
		let mobile = false;
		let baseX = innerWidth * 0.82;
		let baseY = 245;
		let baseScale = 1;
		let pushX = 0;
		let pushY = 0;
		let pushVelocityX = 0;
		let pushVelocityY = 0;
		let rotation = 0;
		let rotationVelocity = 0;
		let stretch = 0;
		let stretchVelocity = 0;
		let pointerX = innerWidth * 0.5;
		let pointerY = innerHeight * 0.5;
		let previousPointerX = pointerX;
		let previousPointerY = pointerY;
		let pointerSpeed = 0;
		let pointerActive = false;
		let stops: Stop[] = [];
		const preference = matchMedia('(prefers-reduced-motion: reduce)');

		function top(element: HTMLElement) {
			return element.getBoundingClientRect().top + scrollY;
		}

		function updateHost() {
			host.style.transform = `translate3d(${baseX - size / 2 + pushX}px, ${baseY - size / 2 + pushY}px, 0) scale(${baseScale})`;
		}

		function updateLiquid() {
			liquid.style.transform = `rotate(${rotation}deg) scale3d(${1 + stretch}, ${1 - stretch * 0.62}, 1)`;
			host.style.setProperty('--reaction', `${Math.min(1, Math.abs(stretch) * 12)}`);
		}

		function handleScroll() {
			if (!stops.length) return;
			if (mobile || reduced) {
				baseX = stops[0].x;
				baseY = stops[0].y - scrollY;
				baseScale = 1;
				host.style.opacity = baseY < -size ? '0' : '1';
			} else {
				let a = stops[0];
				let b = stops[1];
				for (let index = 1; index < stops.length; index++) {
					a = stops[index - 1];
					b = stops[index];
					if (scrollY <= b.scroll) break;
				}
				let progress = Math.max(
					0,
					Math.min(1, (scrollY - a.scroll) / Math.max(1, b.scroll - a.scroll))
				);
				progress = progress * progress * (3 - 2 * progress);
				baseX = a.x + (b.x - a.x) * progress;
				baseY = a.y + (b.y - a.y) * progress;
				baseScale = a.scale + (b.scale - a.scale) * progress;
				host.style.opacity = '1';
			}
			updateHost();
		}

		function measure() {
			mobile = innerWidth <= 680;
			reduced = preference.matches;
			size = mobile ? Math.min(340, innerWidth * 0.8) : Math.min(660, innerWidth * 0.48);
			host.style.width = host.style.height = `${size}px`;

			const hero = document.querySelector('.hero') as HTMLElement | null;
			const signals = document.getElementById('per-te');
			const works = document.getElementById('lavori');
			const about = document.getElementById('approccio');
			const contact = document.getElementById('contatti');
			if (!hero || !signals || !works || !about || !contact) return;

			const heroY = top(hero) + (mobile ? 310 : 250);
			stops = [
				{ scroll: 0, x: innerWidth * (mobile ? 0.7 : 0.82), y: heroY, scale: 1 },
				{
					scroll: Math.max(120, top(signals) - innerHeight * 0.28),
					x: innerWidth * 0.46,
					y: innerHeight * 0.34,
					scale: 0.42
				},
				{
					scroll: Math.max(240, top(works) - innerHeight * 0.28),
					x: innerWidth * 0.63,
					y: innerHeight * 0.16,
					scale: 0.4
				},
				{
					scroll: Math.max(360, top(about) - innerHeight * 0.22),
					x: innerWidth * 0.14,
					y: innerHeight * 0.34,
					scale: 0.62
				},
				{
					scroll: Math.max(480, top(contact) - innerHeight * 0.15),
					x: innerWidth * 0.83,
					y: innerHeight * 0.5,
					scale: 1
				}
			];
			handleScroll();
		}

		function handlePointer(event: PointerEvent) {
			if (event.pointerType === 'touch' || reduced) return;
			previousPointerX = pointerX;
			previousPointerY = pointerY;
			pointerX = event.clientX;
			pointerY = event.clientY;
			pointerSpeed = Math.min(
				1,
				pointerSpeed * 0.35 +
					Math.hypot(pointerX - previousPointerX, pointerY - previousPointerY) / 52
			);
			pointerActive = true;
		}

		function clearPointer() {
			pointerActive = false;
		}

		function updateTheme() {
			const nextDark = document.documentElement.dataset.theme === 'dark';
			if (nextDark !== dark) ready = false;
			dark = nextDark;
		}

		function simulate(now: number) {
			frame = requestAnimationFrame(simulate);
			if (document.hidden) return;
			const delta = Math.min(0.034, Math.max(0.001, (now - last) / 1000));
			last = now;
			if (reduced) return;

			const renderedRadius = Math.max(1, size * baseScale * 0.39);
			const dx = pointerX - (baseX + pushX);
			const dy = pointerY - (baseY + pushY);
			const distance = Math.hypot(dx, dy);
			const influence = pointerActive ? Math.max(0, 1 - distance / (renderedRadius * 1.8)) : 0;
			const normalizedX = Math.max(-1, Math.min(1, dx / renderedRadius));
			const normalizedY = Math.max(-1, Math.min(1, dy / renderedRadius));

			const targetPushX = -normalizedX * 24 * influence;
			const targetPushY = -normalizedY * 19 * influence;
			const targetRotation = (normalizedX * 5.5 - normalizedY * 2.2) * influence;
			const targetStretch = Math.min(0.075, (0.018 + pointerSpeed * 0.058) * influence);

			const spring = 43;
			const damping = 10.5;
			pushVelocityX += (targetPushX - pushX) * spring * delta;
			pushVelocityY += (targetPushY - pushY) * spring * delta;
			rotationVelocity += (targetRotation - rotation) * 31 * delta;
			stretchVelocity += (targetStretch - stretch) * 38 * delta;
			const decay = Math.exp(-damping * delta);
			pushVelocityX *= decay;
			pushVelocityY *= decay;
			rotationVelocity *= Math.exp(-8.2 * delta);
			stretchVelocity *= Math.exp(-9.2 * delta);
			pushX += pushVelocityX * delta;
			pushY += pushVelocityY * delta;
			rotation += rotationVelocity * delta;
			stretch += stretchVelocity * delta;
			pointerSpeed *= Math.exp(-5.5 * delta);

			updateHost();
			updateLiquid();
		}

		const resize = new ResizeObserver(measure);
		resize.observe(document.body);
		const themeObserver = new MutationObserver(updateTheme);
		themeObserver.observe(document.documentElement, {
			attributes: true,
			attributeFilter: ['data-theme']
		});
		window.addEventListener('scroll', handleScroll, { passive: true });
		window.addEventListener('resize', measure);
		window.addEventListener('pointermove', handlePointer, { passive: true });
		window.addEventListener('blur', clearPointer);
		document.documentElement.addEventListener('pointerleave', clearPointer);
		preference.addEventListener('change', measure);

		updateTheme();
		measure();
		hydrated = true;
		updateLiquid();
		frame = requestAnimationFrame(simulate);

		return () => {
			cancelAnimationFrame(frame);
			resize.disconnect();
			themeObserver.disconnect();
			window.removeEventListener('scroll', handleScroll);
			window.removeEventListener('resize', measure);
			window.removeEventListener('pointermove', handlePointer);
			window.removeEventListener('blur', clearPointer);
			document.documentElement.removeEventListener('pointerleave', clearPointer);
			preference.removeEventListener('change', measure);
		};
	});
</script>

<div class="scroll-blob" class:active={ready} bind:this={host} aria-hidden="true">
	<div class="liquid-entry" class:entered={$introDone}>
		<div class="liquid" bind:this={liquid}>
			{#if hydrated}
				<img
					src={asset}
					alt=""
					width="480"
					height="480"
					fetchpriority="high"
					onload={() => (ready = true)}
				/>
			{/if}
		</div>
	</div>
</div>

<style>
	.scroll-blob {
		position: fixed;
		top: 0;
		left: 0;
		width: 480px;
		height: 480px;
		visibility: hidden;
		pointer-events: none;
		z-index: 1;
		will-change: transform;
		contain: layout style;
		filter: drop-shadow(0 26px 34px rgb(45 24 102 / calc(0.1 + var(--reaction, 0) * 0.05)));
		transition:
			opacity 0.35s ease,
			visibility 0s linear 0.35s;
	}
	.scroll-blob.active {
		visibility: visible;
		transition-delay: 0s;
	}
	.liquid-entry {
		width: 100%;
		height: 100%;
		opacity: 0;
		transform: scale(0.94);
		transform-origin: center;
		will-change: transform;
		transition:
			opacity 1s ease,
			transform 1.35s cubic-bezier(0.16, 1, 0.3, 1);
	}
	.liquid-entry.entered {
		opacity: 1;
		transform: scale(1);
	}
	.liquid {
		position: relative;
		width: 100%;
		height: 100%;
		transform-origin: center;
		will-change: transform;
	}
	.liquid img {
		position: absolute;
		inset: 0;
		display: block;
		width: 100%;
		height: 100%;
		object-fit: contain;
		-webkit-user-drag: none;
		user-select: none;
	}
	:global(html[data-theme='light']) .liquid {
		filter: saturate(1.08) contrast(0.98) brightness(1.02);
	}
	:global(html[data-theme='dark']) .liquid {
		filter: saturate(1.18) contrast(1.08) brightness(1.03);
	}
	@media (max-width: 680px) {
		.scroll-blob {
			width: 300px;
			height: 300px;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.liquid-entry {
			transition: opacity 0.2s ease;
		}
	}
</style>
