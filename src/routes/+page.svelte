<script lang="ts">
	import IntroBrand from '$lib/components/sections/IntroBrand.svelte';
	import Header from '$lib/components/sections/Header.svelte';
	import Hero from '$lib/components/sections/Hero.svelte';
	import Footer from '$lib/components/sections/Footer.svelte';
</script>

<svelte:head>
	<title>delvup — Work in progress</title>
	<meta
		name="description"
		content="Delvup, portfolio online di Alessandro. Work in progress."
	/>
</svelte:head>

<main class="relative grid h-dvh grid-rows-[auto_minmax(0,1fr)_auto] overflow-hidden bg-white">
	<IntroBrand />
	<Header />
	<Hero />
	<Footer />
</main>
