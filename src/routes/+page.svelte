<script lang="ts">
	import IntroBrand from '$lib/components/sections/IntroBrand.svelte';
	import BackgroundVideo from '$lib/components/sections/BackgroundVideo.svelte';
	import Header from '$lib/components/sections/Header.svelte';
	import Hero from '$lib/components/sections/Hero.svelte';
	import Footer from '$lib/components/sections/Footer.svelte';
</script>

<svelte:head>
	<title>Delvup — Design, develop & care websites</title>
	<meta
		name="description"
		content="Delvup – Design, sviluppo e supporto di siti web, brands e prodotti digitali."
	/>
</svelte:head>

<main
	class="relative grid h-dvh grid-rows-[auto_minmax(0,1fr)_auto] overflow-hidden bg-[var(--color-bg)] text-[var(--color-text)]"
>
	<IntroBrand />
	<BackgroundVideo />
	<Header />
	<Hero />
	<Footer />
</main>
