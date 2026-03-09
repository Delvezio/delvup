<script lang="ts">
	import { resolve } from '$app/paths';
	import Section from '$lib/components/layout/Section.svelte';
	import Container from '$lib/components/layout/Container.svelte';
	import { introDone } from '$lib/stores/intro';
</script>

<Section as="header" className="relative z-30">
	<Container width="site">
		<div
			class="flex flex-row justify-between items-center gap-4 py-4 transition-all duration-700 delay-250 sm:py-5 lg:py-6"
			class:pointer-events-none={!$introDone}
			class:translate-y-4={!$introDone}
			class:opacity-0={!$introDone}
			class:translate-y-0={$introDone}
			class:opacity-100={$introDone}
		>
			<!-- <nav
				class="col-span-8 flex items-center gap-4 sm:gap-6 lg:col-span-3 lg:gap-8"
				aria-label="Primary"
			>
				<a
					href="#work"
					class="font-title text-fluid-h3 leading-none text-zinc-900 no-underline"
				>
					Lavori
				</a>

				<a
					href="#contact"
					class="font-title text-fluid-h3 leading-none text-zinc-900 no-underline"
				>
					Contatti
				</a>
			</nav> -->


			<p
				class="font-title text-sm lg:text-base col-span-12 m-0 text-left leading-[1.25] text-zinc-900/40 lg:col-span-6"
			>
				Design / develop <br />
				& care
			</p>

			<p
				class="font-title text-sm lg:text-base col-span-12 m-0 text-left leading-[1.25] text-zinc-900/40 lg:col-span-6"
			>
				Websites, brands <br />
				and digital products.
			</p>


			<a
				class="col-span-4 justify-self-end lg:col-span-3"
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
