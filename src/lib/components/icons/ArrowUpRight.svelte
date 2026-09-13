<script lang="ts">
	let {
		variant = 'fill',
		class: className = ''
	}: { variant?: 'fill' | 'outline'; class?: string } = $props();
</script>

<svg
	class={`arrow-icon arrow-${variant} ${className}`}
	viewBox="0 0 149 149"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
	aria-hidden="true"
	focusable="false"
	tabindex="-1"
>
	{#if variant === 'fill'}
		<path
			fill-rule="evenodd"
			clip-rule="evenodd"
			d="M104.358 82.6608L55.4778 149H0L76.8509 44.6999H0.191443V0H104.358H149V149H104.358V82.6608Z"
		/>
	{:else}
		<path
			class="outline-stroke"
			fill-rule="evenodd"
			clip-rule="evenodd"
			d="M104.358 82.6608L55.4778 149H0L76.8509 44.6999H0.191443V0H104.358H149V149H104.358V82.6608Z"
		/>
	{/if}
</svg>

<style>
	.arrow-icon {
		display: inline-block;
		width: var(--arrow-width, var(--arrow-size, 1em));
		height: var(--arrow-height, var(--arrow-size, 1em));
		flex: none;
		overflow: visible;
	}
	.arrow-fill path {
		fill: currentColor;
	}
	.outline-stroke {
		fill: none;
		stroke: currentColor;
		stroke-width: 3;
		stroke-linejoin: round;
		vector-effect: non-scaling-stroke;
	}
</style>
