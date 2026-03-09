<script lang="ts">
	import { onMount } from 'svelte';
	import Section from '$lib/components/layout/Section.svelte';
	import Container from '$lib/components/layout/Container.svelte';
	import LineRevealTitle from '$lib/components/ui/LineRevealTitle.svelte';
	import RevealLines from '$lib/components/ui/RevealLines.svelte';
	import { introDone } from '$lib/stores/intro';

	let titleReady = false;
	let titleTimer: ReturnType<typeof setTimeout> | null = null;

	const VIDEO_DELAY = 250;
	const VIDEO_DURATION = 300;
	const TITLE_AFTER_VIDEO = 50;
	const COPY_DELAY = 180;

	onMount(() => {
		const unsubscribe = introDone.subscribe((done) => {
			if (titleTimer) {
				clearTimeout(titleTimer);
				titleTimer = null;
			}

			if (done) {
				titleReady = false;

				titleTimer = setTimeout(() => {
					titleReady = true;
				}, VIDEO_DELAY + VIDEO_DURATION + TITLE_AFTER_VIDEO);
			} else {
				titleReady = false;
			}
		});

		return () => {
			unsubscribe();

			if (titleTimer) {
				clearTimeout(titleTimer);
			}
		};
	});
</script>

<Section id="hero" className="relative z-20 h-full min-h-0 overflow-hidden">
	<Container width="site" className="h-full min-h-0">
		<div class="grid h-full min-h-0 grid-rows-[auto_minmax(0,1fr)]">
			<!-- RIGA 1: titolo -->
			<div class="shrink-0 py-2 sm:py-3 lg:py-4">
				<div
					class="transition-all duration-700 [transition-delay:250ms]"
					class:pointer-events-none={!titleReady}
					class:translate-y-4={!titleReady}
					class:opacity-0={!titleReady}
					class:translate-y-0={titleReady}
					class:opacity-100={titleReady}
				>
					<LineRevealTitle
						as="h1"
						trigger={titleReady}
						lines={["Progetto", "il tuo online."]}
						baseDelay={80}
						stepDelay={140}
						duration={1200}
						className="text-fluid-h1 font-bold md:text-fluid-display text-left text-zinc-900"
					/>
				</div>
			</div>

			<!-- RIGA 2: copy + video -->
			<div class="min-h-0 mt-6 overflow-hidden">
				<div class="flex h-full min-h-0 w-full flex-col justify-center gap-4 lg:flex-row lg:items-end lg:justify-between lg:gap-0">
					<RevealLines
						as="div"
						trigger={titleReady}
						baseDelay={COPY_DELAY}
						stepDelay={120}
						duration={1100}
						className="text-fluid-h3 font-bold text-zinc-700"
					>
						<span>
							<span class="inline-flex flex-wrap">Vuoi vedere i miei progetti?</span>
						</span>

						<span>
							<span class="inline-flex flex-wrap">
								<span>Allora&nbsp;</span>
								<a href="mailto:ciao@delvup.com" class="underline transition">scrivimi</a>
							</span>
						</span>
					</RevealLines>

					<div class="flex h-full min-h-0 w-full justify-center lg:w-auto lg:justify-end">
						<div
							class="flex h-full min-h-0 items-end origin-bottom transition-all duration-800 [transition-delay:300ms] lg:origin-bottom-right"
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
