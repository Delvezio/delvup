<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { introDone } from '$lib/stores/intro';
	import Container from '$lib/components/layout/Container.svelte';

	/**
	 * mounted:
	 * serve per non renderizzare subito l'intro lato SSR / primissimo paint.
	 * In questo modo la pagina parte bianca e il pannello scuro entra dopo il mount.
	 */
	let mounted = false;

	/**
	 * introGone:
	 * quando diventa true rimuoviamo completamente l'overlay intro dal DOM.
	 */
	let introGone = false;

	/**
	 * panelCovered:
	 * false  -> pannello fuori schermo a sinistra
	 * true   -> pannello visibile e a copertura completa
	 */
	let panelCovered = false;

	/**
	 * panelLeaving:
	 * quando diventa true, il pannello continua il suo movimento ed esce a destra.
	 */
	let panelLeaving = false;
	let baseLeaving = false;

	/**
	 * Stati del brand / logo.
	 * Li usiamo per orchestrare entrata, reveal e uscita delle lettere.
	 */
	let brandVisible = false;
	let brandShifted = false;
	let brandCentered = false;

	let logoRevealed = false;
	let upRevealed = false;

	let dOut = false;
	let eOut = false;
	let lOut = false;
	let vOut = false;
	let arrowOut = false;

	/**
	 * Utility: aspetta un frame di rendering.
	 * Serve per essere sicuri che il browser abbia dipinto lo stato iniziale
	 * prima di far partire la sequenza.
	 */
	function waitFrame() {
		return new Promise<void>((resolve) => {
			requestAnimationFrame(() => resolve());
		});
	}

	onMount(() => {
		let destroyed = false;
		const timers: ReturnType<typeof setTimeout>[] = [];

		async function startIntro() {
			/**
			 * All'inizio l'intro non è ancora conclusa,
			 * quindi header / hero restano nascosti.
			 */
			introDone.set(false);

			/**
			 * Renderizziamo il componente solo dopo il mount,
			 * così il primo paint della pagina resta bianco.
			 */
			mounted = true;

			/**
			 * Aspettiamo:
			 * - tick Svelte
			 * - 2 frame browser
			 *
			 * Questo aiuta a evitare il "salto" in cui il pannello
			 * appare già scuro al refresh senza mostrare bene l'ingresso.
			 */
			await tick();
			await waitFrame();
			await waitFrame();

			if (destroyed) return;

			/**
			 * 1) INGRESSO DEL PANNELLO SCURO
			 *
			 * Aumenta / diminuisci questo valore se vuoi:
			 * - vedere più a lungo il bianco iniziale
			 * - oppure far partire subito l'intro
			 *
			 * Valori utili da testare:
			 * 80 / 120 / 180 / 250
			 */
			timers.push(
				setTimeout(() => {
					panelCovered = true;
				}, 50)
			);

			/**
			 * 2) APPARIZIONE DEL BRAND
			 *
			 * Qui compare il gruppo logo con opacità bassa.
			 * Se vuoi che il logo arrivi più tardi, aumenta questo valore.
			 */
			timers.push(
				setTimeout(() => {
					brandVisible = true;
				}, 760)
			);

			/**
			 * 3) REVEAL DEL BLOCCO LOGO PRINCIPALE
			 *
			 * Qui parte il reveal sinistra->destra del logo testo.
			 * Insieme facciamo anche un primo spostamento orizzontale del brand.
			 */
			timers.push(
				setTimeout(() => {
					brandShifted = true;
					logoRevealed = true;
				}, 1260)
			);

			/**
			 * 4) REVEAL DEL BLOCCO UP + centratura finale del brand
			 *
			 * Se vuoi rendere più "solenne" la comparsa della freccia,
			 * alza questo valore.
			 */
			timers.push(
				setTimeout(() => {
					upRevealed = true;
					brandCentered = true;
				}, 2260)
			);

			/**
			 * 5) USCITA SEQUENZIALE DELLE LETTERE
			 *
			 * Qui puoi regolare il ritmo della scomparsa:
			 * - più ravvicinato = più veloce / nervoso
			 * - più distante = più elegante / leggibile
			 */
			setTimeout(() => (dOut = true), 3000);
			setTimeout(() => (eOut = true), 3150);
			setTimeout(() => (lOut = true), 3250);
			setTimeout(() => (vOut = true), 3300);
			setTimeout(() => (arrowOut = true), 3330);

			/**
			 * 6) USCITA DEL PANNELLO SCURO VERSO DESTRA
			 *
			 * Questo è il momento in cui il pannello "continua"
			 * il suo movimento naturale e libera la schermata bianca.
			 *
			 * Se vuoi che il logo resti visibile più a lungo prima dell'uscita,
			 * aumenta questo valore.
			 */
			timers.push(
				setTimeout(() => {
					panelLeaving = true;
				}, 3600)
			);

			/**
			 * 7) USCITA DEL PANNELLO CHIARO
			 *
			 * Parte solo quando il pannello scuro ha già terminato la sua uscita,
			 * così i due layer risultano ben distinti.
			 */
			timers.push(
				setTimeout(() => {
					baseLeaving = true;
				}, 4140)
			);

			/**
			 * 7) ATTIVAZIONE CONTENUTO PAGINA
			 *
			 * Qui diciamo a Header / Hero che l'intro è finita,
			 * così possono entrare.
			 *
			 * Se vuoi che compaiano leggermente prima o dopo rispetto
			 * all'uscita del pannello, modifica questo valore.
			 */
			timers.push(
				setTimeout(() => {
					introDone.set(true);
				}, 4320)
			);

			/**
			 * 8) RIMOZIONE COMPLETA OVERLAY INTRO
			 *
			 * Quando il pannello è ormai fuori schermo,
			 * eliminiamo il componente intro dal DOM.
			 */
			timers.push(
				setTimeout(() => {
					introGone = true;
				}, 6200)
			);
		}

		void startIntro();

		return () => {
			destroyed = true;
			timers.forEach((timer) => clearTimeout(timer));
		};
	});
</script>

{#if mounted && !introGone}
	<div class="intro-root pointer-events-none absolute inset-0 z-50 overflow-hidden">
		<div class="intro-base absolute inset-0" class:base-leaving={baseLeaving}></div>

		<!--
			PANNELLO SCURO
			- parte da sinistra fuori viewport
			- entra a coprire tutto
			- poi esce a destra
		-->
		<div
			class="intro-panel absolute inset-y-0 left-0 h-full w-full"
			class:panel-covered={panelCovered}
			class:panel-leaving={panelLeaving}
		></div>

		<!--
			CENTRATURA DEL BRAND
			Il logo resta sempre centrato nell'overlay.
		-->
		<div class="absolute inset-0">
			<Container width="site" className="flex min-h-screen items-center justify-center">
				<div
					class="brand grid w-full grid-cols-[minmax(0,1101fr)_minmax(0,301fr)] items-end gap-[clamp(0.5rem,1.2vw,1rem)]"
					class:brand-visible={brandVisible}
					class:brand-shifted={brandShifted}
					class:brand-centered={brandCentered}
					class:brand-hidden={panelLeaving}
					aria-hidden="true"
				>
				<!-- BLOCCO LOGO TESTUALE -->
				<div class="relative w-full overflow-hidden" class:logo-open={logoRevealed}>
					<div class="overlay-logo absolute inset-y-0 left-0 h-full w-full"></div>

					<svg
						class="block h-auto w-full"
						viewBox="0 0 1101 300"
						preserveAspectRatio="xMidYMid meet"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							class:letter-out={dOut}
							d="M0 300V0H126.429C230.571 0 280.714 51 280.714 150C280.714 249 230.571 300 126.429 300H0ZM81.4286 227.143H126.429C174.429 227.143 197.143 201 197.143 149.571C197.143 99 174.429 72.8571 126.429 72.8571H81.4286V227.143Z"
							fill="#FEFEFE"
						/>
						<path
							class:letter-out={eOut}
							d="M315.151 300V0H563.722V72.8571H396.579V113.571H546.579V186.429H396.579V227.143H568.008V300H315.151Z"
							fill="#FEFEFE"
						/>
						<path
							class:letter-out={lOut}
							d="M602.26 300V0H683.689V227.143H846.546V300H602.26Z"
							fill="#FEFEFE"
						/>
						<path
							class:letter-out={vOut}
							d="M1100.83 0L994.978 300H907.978L802.12 0H889.12L951.692 176.571L1013.83 0H1100.83Z"
							fill="#FEFEFE"
						/>
					</svg>
				</div>

				<!-- BLOCCO FRECCIA / UP -->
				<div class="relative w-full overflow-hidden" class:up-open={upRevealed}>
					<div class="overlay-up absolute inset-y-0 right-0 h-full w-full"></div>

					<svg
						class="block h-auto w-full"
						viewBox="0 0 301 300"
						fill="none"
						preserveAspectRatio="xMidYMid meet"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							class:letter-out={arrowOut}
							fill-rule="evenodd"
							clip-rule="evenodd"
							d="M301 300H211V166.431L112.457 300H0.613861L155.546 90H1V-6.10352e-05L301 0V90V300Z"
							fill="#6455A5"
						/>
					</svg>
				</div>
				</div>
			</Container>
		</div>
	</div>
{/if}

<style>
	/*
		ROOT INTRO
		Non ha background proprio: il bianco che vedi sotto
		è il background reale della pagina.
	*/
	.intro-root {
		background: transparent;
	}

	.intro-base {
		background: var(--color-surface);
		transform: translateX(0);
		will-change: transform;
		transition: transform 0.32s cubic-bezier(0.58, 0, 0.3, 1);
	}

	.base-leaving {
		transform: translateX(100%);
	}

	/*
		PANNELLO PRINCIPALE
		Stato iniziale: completamente fuori schermo a sinistra.
	*/
	.intro-panel {
		background: var(--color-intro-panel);
		transform: translateX(-100%);
		will-change: transform;

		/*
			QUI REGOLI L'ENTRATA DEL PANNELLO

			- primo valore: durata
			- cubic-bezier: curva di accelerazione

			Se vuoi un ingresso:
			- più rapido: abbassa 0.72s
			- più cinematografico: prova 0.9s / 1s
		*/
		transition: transform 0.72s cubic-bezier(0.5, 0, 0.24, 1);
	}

	/*
		PANNELLO COMPLETAMENTE IN SCHERMO
	*/
	.panel-covered {
		transform: translateX(0);
	}

	/*
		PANNELLO IN USCITA A DESTRA

		Questa fase parte dopo l'animazione del logo.
		Puoi rendere l'uscita più lenta o più veloce cambiando transition-duration.
	*/
	.panel-leaving {
		transform: translateX(100%);
		transition-duration: 0.54s;
	}

	/*
		BRAND
		Parte leggermente spostato a sinistra e invisibile.
	*/
	.brand {
		opacity: 0;
		transform: translateX(-8vw);
		transition:
			transform 1.2s ease,
			opacity 1.2s ease;
		will-change: transform, opacity;
	}

	/*
		Prima apparizione leggera del brand.
	*/
	.brand-visible {
		opacity: 0.21;
	}

	/*
		Primo step di spostamento orizzontale del brand.
	*/
	.brand-shifted {
		transform: translateX(-4vw);
	}

	/*
		Stato finale del brand: centrato e completamente visibile.
	*/
	.brand-centered {
		transform: translateX(0);
		opacity: 1;
	}

	/*
		Quando il pannello parte in uscita, facciamo sparire anche il brand.
	*/
	.brand-hidden {
		opacity: 0;
	}

	/*
		REVEAL DEL LOGO PRINCIPALE
		L'overlay si restringe fino a 0 e lascia vedere il logo.
	*/
	.overlay-logo {
		background: var(--color-intro-panel);
		transition: width 0.9s ease;
	}

	.logo-open .overlay-logo {
		width: 0;
	}

	/*
		REVEAL DEL BLOCCO UP
		Stesso principio, con durata leggermente diversa.
	*/
	.overlay-up {
		background: var(--color-intro-panel);
		transition: width 0.7s ease;
	}

	.up-open .overlay-up {
		width: 0;
	}

	/*
		ANIMAZIONE DELLE LETTERE
		Serve alla fase finale in cui ogni lettera esce verso l'alto.
	*/
	svg path {
		transform-origin: center;
		transition:
			transform 0.3s ease-out,
			opacity 0.3s ease-out;
	}

	.letter-out {
		transform: translateY(-100%);
		opacity: 0;
	}
</style>
