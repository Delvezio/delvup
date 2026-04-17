<script lang="ts">
	import Section from '$lib/components/layout/Section.svelte';
	import Container from '$lib/components/layout/Container.svelte';
	import LineRevealTitle from '$lib/components/ui/LineRevealTitle.svelte';
	import RevealLines from '$lib/components/ui/RevealLines.svelte';
	import { introDone } from '$lib/stores/intro';
</script>

<Section id="hero" className="relative z-20 h-full min-h-0">
	<Container width="site" className="h-full min-h-0">
		<div class="relative grid h-full min-h-0 grid-rows-[auto_minmax(0,1fr)]">
			<!-- RIGA 1: titolo -->
			<div class="relative z-20 shrink-0 py-2 sm:py-3 lg:py-4">
				<div
					class="transition-all duration-700"
					class:pointer-events-none={!$introDone}
					class:translate-y-4={!$introDone}
					class:opacity-0={!$introDone}
					class:translate-y-0={$introDone}
					class:opacity-100={$introDone}
				>
					<LineRevealTitle
						as="h1"
						trigger={$introDone}
						lines={["Progetto", "il tuo online."]}
						baseDelay={0}
						stepDelay={140}
						duration={1200}
						className="text-fluid-h1 font-bold md:text-fluid-display text-left text-zinc-50"
					/>
				</div>
			</div>

			<!-- RIGA 2: copy + video -->
			<div class="relative mt-6 min-h-0">
				<div class="relative z-20 flex h-full min-h-0 w-full flex-col justify-end gap-4 md:pb-8 lg:pr-[min(42vw,38rem)]">
					<RevealLines
						as="div"
						trigger={$introDone}
						baseDelay={0}
						stepDelay={120}
						duration={1100}
						className="text-fluid-h3 font-bold text-zinc-300"
					>
						<span>
							<span class="inline-flex flex-wrap">Vuoi vedere i miei progetti?</span>
						</span>

						<span>
							<span class="inline-flex flex-wrap">
								<span><a href="mailto:ciao@delvup.com" target="_blank" class="underline transition">scrivimi</a> ✍️</span>
							</span>
						</span>
					</RevealLines>
				</div>
			</div>
		</div>
	</Container>
</Section>
