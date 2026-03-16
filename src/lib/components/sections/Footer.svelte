<script lang="ts">
	import Section from '$lib/components/layout/Section.svelte';
	import Container from '$lib/components/layout/Container.svelte';
	import { introDone } from '$lib/stores/intro';
</script>

<Section as="footer" className="relative z-20 pb-4 sm:pb-6 lg:pb-8">
	<Container width="site">
		<div
			class="flex flex-col items-start justify-between gap-3 pt-4 text-xs text-zinc-500 transition-all duration-700 sm:flex-row sm:items-center"
			class:pointer-events-none={!$introDone}
			class:translate-y-3={!$introDone}
			class:opacity-0={!$introDone}
			class:translate-y-0={$introDone}
			class:opacity-100={$introDone}
		>
			<p class="m-0">Delvup © 2026 · Made in Italy </p>
			<p class="m-0">by Alessandro Delvezio</p>
		</div>
	</Container>
</Section>
