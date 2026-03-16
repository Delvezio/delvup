<script lang="ts">
	import Section from '$lib/components/layout/Section.svelte';
	import Container from '$lib/components/layout/Container.svelte';
	import LineRevealTitle from '$lib/components/ui/LineRevealTitle.svelte';
	import RevealLines from '$lib/components/ui/RevealLines.svelte';
	import { introDone } from '$lib/stores/intro';
</script>

<Section id="hero" className="relative z-20 h-full min-h-0 overflow-hidden">
	<Container width="site" className="h-full min-h-0">
		<div class="grid h-full min-h-0 grid-rows-[auto_minmax(0,1fr)]">
			<!-- RIGA 1: titolo -->
			<div class="shrink-0 py-2 sm:py-3 lg:py-4">
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
						className="text-fluid-h1 font-bold md:text-fluid-display text-left text-zinc-900"
					/>
				</div>
			</div>

			<!-- RIGA 2: copy + video -->
			<div class="min-h-0 mt-6 overflow-hidden">
				<div class="flex h-full min-h-0 w-full flex-col justify-center gap-4 lg:flex-row lg:items-end lg:justify-between lg:gap-0 md:pb-8">
					<RevealLines
						as="div"
						trigger={$introDone}
						baseDelay={0}
						stepDelay={120}
						duration={1100}
						className="text-fluid-h3 font-bold text-zinc-700"
					>
						<span>
							<span class="inline-flex flex-wrap">Vuoi vedere i miei progetti?</span>
						</span>

						<span>
							<span class="inline-flex flex-wrap">
								<span><a href="#contact" class="underline transition">scrivimi</a> ✍️</span>
							</span>
						</span>
					</RevealLines>

					<div class="flex h-full min-h-0 w-full justify-center lg:w-auto lg:justify-end">
						<div
							class="flex h-full min-h-0 items-end origin-bottom transition-all duration-800 lg:origin-bottom-right"
							class:scale-0={!$introDone}
							class:opacity-0={!$introDone}
							class:scale-100={$introDone}
							class:opacity-100={$introDone}
							aria-hidden="true"
						>
							<video
								class="block h-full w-auto max-w-full rounded-[1.5rem] object-contain sm:rounded-[1.75rem] lg:rounded-[2rem]"
								autoplay
								muted
								loop
								playsinline
								preload="auto"
							>
								<source src="/media/blob_motivo.webm" type="video/webm" />
							</video>
						</div>
					</div>
				</div>
			</div>
		</div>
	</Container>
</Section>
