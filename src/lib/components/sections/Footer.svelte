<script lang="ts">
	import { onMount } from 'svelte';
	import Section from '$lib/components/layout/Section.svelte';
	import Container from '$lib/components/layout/Container.svelte';
	import { introDone } from '$lib/stores/intro';

	let footerVisible = false;
	let footerTimer: ReturnType<typeof setTimeout> | null = null;

	onMount(() => {
		const unsubscribe = introDone.subscribe((done) => {
			if (footerTimer) {
				clearTimeout(footerTimer);
				footerTimer = null;
			}

			if (done) {
				footerVisible = false;

				footerTimer = setTimeout(() => {
					footerVisible = true;
				}, 700);
			} else {
				footerVisible = false;
			}
		});

		return () => {
			unsubscribe();

			if (footerTimer) {
				clearTimeout(footerTimer);
			}
		};
	});
</script>

<Section as="footer" className="relative z-20 pb-4 sm:pb-6 lg:pb-8">
	<Container width="site">
		<div
			class="flex flex-col items-start justify-between gap-3 pt-4 text-xs text-zinc-500 transition-all duration-700 sm:flex-row sm:items-center"
			class:pointer-events-none={!footerVisible}
			class:translate-y-3={!footerVisible}
			class:opacity-0={!footerVisible}
			class:translate-y-0={footerVisible}
			class:opacity-100={footerVisible}
		>
			<p class="m-0">Delvup © 2026 by Alessandro Delvezio</p>
			<p class="m-0">Made in Torino • Italy</p>
		</div>
	</Container>
</Section>
