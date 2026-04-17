<script lang="ts">
	import { introDone } from '$lib/stores/intro';
</script>

<div
	class="pointer-events-none absolute inset-0 z-0 overflow-hidden"
	aria-hidden="true"
>
	<div
		class="absolute inset-x-0 top-1/2 flex -translate-y-1/2 justify-center md:inset-x-auto md:right-6 md:justify-end lg:right-8"
	>
		<div
			class="flex items-center origin-right transition-all duration-800"
			class:scale-0={!$introDone}
			class:opacity-0={!$introDone}
			class:scale-100={$introDone}
			class:opacity-100={$introDone}
		>
			<video
				class="block h-auto w-full max-w-none object-contain md:h-[min(70svh,36rem)] md:w-auto md:max-w-full md:rounded-[1.75rem] lg:h-[min(70svh,calc(100dvh-10rem))] lg:max-w-[42vw] lg:rounded-[2rem]"
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
