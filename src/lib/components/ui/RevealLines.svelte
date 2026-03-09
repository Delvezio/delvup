<script lang="ts">
	import { onMount } from 'svelte';

	type Tag = 'div' | 'p' | 'section';

	export let as: Tag = 'div';
	export let trigger = false;
	export let observe = false;
	export let once = true;

	export let baseDelay = 0;
	export let stepDelay = 120;
	export let duration = 1100;

	export let className = '';

	let root: HTMLElement;
	let visible = false;
	let hasAnimated = false;
	let observer: IntersectionObserver | null = null;

	function play() {
		if (once && hasAnimated) return;

		visible = false;

		requestAnimationFrame(() => {
			requestAnimationFrame(() => {
				visible = true;
				hasAnimated = true;
			});
		});
	}

	onMount(() => {
		if (observe) {
			observer = new IntersectionObserver(
				([entry]) => {
					if (entry.isIntersecting) {
						play();
						if (once) observer?.disconnect();
					} else if (!once) {
						visible = false;
					}
				},
				{
					threshold: 0.15,
					rootMargin: '0px 0px -10% 0px'
				}
			);

			if (root) observer.observe(root);

			return () => observer?.disconnect();
		}

		if (trigger) {
			play();
		}

		return () => observer?.disconnect();
	});

	$: if (!observe && trigger) {
		play();
	}

	$: if (!observe && !trigger && !once) {
		visible = false;
	}
</script>

<svelte:element
	this={as}
	bind:this={root}
	class={`reveal-lines ${className}`}
	class:reveal-lines-visible={visible}
	style={`--reveal-base-delay:${baseDelay}ms; --reveal-step-delay:${stepDelay}ms; --reveal-duration:${duration}ms;`}
>
	<slot />
</svelte:element>

<style>
	/*
		Ogni figlio diretto del componente è una "riga".
		Gli diamo una safe area verticale per non tagliare discendenti
		come g, p, y o la punteggiatura bassa.
	*/
	.reveal-lines :global(> *) {
		display: block;
		overflow: hidden;
		perspective: 1200px;

		padding-top: 0.08em;
		padding-bottom: 0.22em;
		margin-top: -0.08em;
		margin-bottom: -0.22em;
	}

	.reveal-lines :global(> * > *) {
		display: inline-block;
		opacity: 0;
		transform: translate3d(0, 95%, 0) rotateX(-80deg);
		transform-origin: top;
		backface-visibility: hidden;
		will-change: transform, opacity;
	}

	.reveal-lines-visible :global(> :nth-child(1) > *) {
		animation: reveal-line var(--reveal-duration) cubic-bezier(0.25, 0, 0, 1) forwards;
		animation-delay: calc(var(--reveal-base-delay) + 0 * var(--reveal-step-delay));
	}

	.reveal-lines-visible :global(> :nth-child(2) > *) {
		animation: reveal-line var(--reveal-duration) cubic-bezier(0.25, 0, 0, 1) forwards;
		animation-delay: calc(var(--reveal-base-delay) + 1 * var(--reveal-step-delay));
	}

	.reveal-lines-visible :global(> :nth-child(3) > *) {
		animation: reveal-line var(--reveal-duration) cubic-bezier(0.25, 0, 0, 1) forwards;
		animation-delay: calc(var(--reveal-base-delay) + 2 * var(--reveal-step-delay));
	}

	.reveal-lines-visible :global(> :nth-child(4) > *) {
		animation: reveal-line var(--reveal-duration) cubic-bezier(0.25, 0, 0, 1) forwards;
		animation-delay: calc(var(--reveal-base-delay) + 3 * var(--reveal-step-delay));
	}

	.reveal-lines-visible :global(> :nth-child(5) > *) {
		animation: reveal-line var(--reveal-duration) cubic-bezier(0.25, 0, 0, 1) forwards;
		animation-delay: calc(var(--reveal-base-delay) + 4 * var(--reveal-step-delay));
	}

	.reveal-lines-visible :global(> :nth-child(6) > *) {
		animation: reveal-line var(--reveal-duration) cubic-bezier(0.25, 0, 0, 1) forwards;
		animation-delay: calc(var(--reveal-base-delay) + 5 * var(--reveal-step-delay));
	}

	@keyframes reveal-line {
		0% {
			opacity: 0;
			transform: translate3d(0, 95%, 0) rotateX(-80deg);
		}

		100% {
			opacity: 1;
			transform: translate3d(0, 0, 0) rotateX(0deg);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.reveal-lines :global(> * > *) {
			opacity: 1;
			transform: none;
			animation: none !important;
		}
	}
</style>
