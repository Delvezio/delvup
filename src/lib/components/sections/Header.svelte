<script lang="ts">
	import { resolve } from '$app/paths';
	import Section from '$lib/components/layout/Section.svelte';
	import Container from '$lib/components/layout/Container.svelte';
	import { introDone } from '$lib/stores/intro';
</script>

<Section as="header" className="relative z-30">
	<Container width="site">
		<div
			class="flex flex-row justify-between items-start gap-4 py-4 transition-all duration-700 sm:py-5 lg:py-6"
			class:pointer-events-none={!$introDone}
			class:translate-y-4={!$introDone}
			class:opacity-0={!$introDone}
			class:translate-y-0={$introDone}
			class:opacity-100={$introDone}
		>
			<p
				class="font-sm font-title col-span-8 m-0 max-w-[18ch] text-left leading-5 text-zinc-400 lg:col-span-4"
			>
				Design /<br />
				Dev & Care
			</p>

			<p
				class="hidden md:block font-sm font-title col-span-8 m-0 max-w-[18ch] text-left leading-5 text-zinc-400 lg:col-span-4"
			>
				Websites, brands<br />
				digital and other stuff.
			</p>

			<a
				class="col-span-4 justify-self-end lg:col-span-2 lg:col-start-11"
				href={resolve('/')}
				aria-label="Delvup home"
			>
				<img
					src="/brand/logo.svg"
					alt="Delvup"
					class="block h-auto w-[clamp(4rem,18vw,6.5rem)]"
				/>
			</a>
		</div>
	</Container>
</Section>
