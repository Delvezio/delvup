<script lang="ts">
	import { onMount } from 'svelte';
	import IntroBrand from '$lib/components/sections/IntroBrand.svelte';
	import { introDone } from '$lib/stores/intro';
	import { revealOnView } from '$lib/reveal';
	let mounted = $state(false);
	import ScrollBlob from '$lib/components/visual/ScrollBlob.svelte';
	let mode = $state('auto');
	const modes = [
		{ value: 'light', label: 'Chiaro', icon: '☼' },
		{ value: 'dark', label: 'Scuro', icon: '☾' },
		{ value: 'auto', label: 'Auto', icon: '◐' }
	];
	function applyTheme(value: string) {
		mode = value;
		const hour = new Date().getHours();
		document.documentElement.dataset.theme =
			value === 'auto' ? (hour >= 7 && hour < 19 ? 'light' : 'dark') : value;
	}
	function chooseTheme(value: string) {
		applyTheme(value);
		try {
			localStorage.setItem('delvup-theme', value);
		} catch {
			/* Theme remains usable without storage. */
		}
	}
	onMount(() => {
		mounted = true;
		let saved = 'auto';
		try {
			saved = localStorage.getItem('delvup-theme') || 'auto';
		} catch {
			/* Use local time. */
		}
		applyTheme(['auto', 'light', 'dark'].includes(saved) ? saved : 'auto');
		const refresh = () => {
			if (mode === 'auto') applyTheme('auto');
		};
		const timer = setInterval(refresh, 30_000);
		document.addEventListener('visibilitychange', refresh);
		return () => {
			clearInterval(timer);
			document.removeEventListener('visibilitychange', refresh);
		};
	});
</script>

<svelte:head>
	<title>Delvup — Design, sviluppo e cura del tuo sito web</title>
	<meta
		name="description"
		content="Sono Alessandro Delvezio. Progetto siti web per professionisti e PMI: design, sviluppo e supporto nel tempo. Scopri i lavori di Delvup."
	/>
</svelte:head>
<IntroBrand />
<div use:revealOnView inert={mounted && !$introDone}>
	<a class="skip-link" href="#contenuto">Vai al contenuto</a>
	<header id="inizio" class="site-header wrap">
		<a href="#inizio" class="brand" aria-label="Delvup, inizio pagina"
			><img class="logo-light" src="/brand/logo.svg" alt="Delvup" width="102" height="61" /><img
				class="logo-dark"
				src="/brand/logo-on-dark.svg"
				alt=""
				width="102"
				height="61"
			/></a
		>
		<nav aria-label="Navigazione principale">
			<a href="#lavori">Lavori <span>↗</span></a><a href="#approccio">Approccio</a><a
				href="#contatti">Parliamone <span>↗</span></a
			>
		</nav>
		<div class="theme-switch" role="group" aria-label="Tema del sito">
			{#each modes as option (option.value)}<button
					aria-label={option.label === 'Auto'
						? 'Tema automatico: chiaro dalle 7 alle 19, scuro di notte'
						: `Tema ${option.label.toLowerCase()}`}
					aria-pressed={mode === option.value}
					onclick={() => chooseTheme(option.value)}
					title={option.label}
					><span aria-hidden="true">{option.icon}</span><span class="theme-label"
						>{option.label}</span
					></button
				>{/each}
		</div>
	</header>
	<ScrollBlob />
	<main id="contenuto">
		<section class="hero wrap" aria-labelledby="hero-title">
			<div class="hero-topline">
				<span>DESIGN / DEV & CARE</span><span>INDIPENDENTE, PER SCELTA.</span>
			</div>
			<div class="hero-title-wrap">
				<h1 id="hero-title">Progetto<br />il tuo <span>online.</span></h1>
				<span class="hero-arrow" aria-hidden="true">↗</span>
			</div>
			<div class="hero-bottom">
				<p>Siti essenziali per professionisti e PMI.<br />Chiari, veloci, mantenuti nel tempo.</p>
				<a class="round-link" href="#lavori"
					><span>Esplora i lavori</span><span class="round-icon" aria-hidden="true">↓</span></a
				>
			</div>
			<div class="hero-rule">
				<span>DAL PRIMO PIXEL. AL GIORNO DOPO.</span><span>SCROLL PER SCOPRIRE ↓</span>
			</div>
		</section>
		<section id="lavori" class="work-section wrap" aria-labelledby="work-title">
			<div class="section-heading">
				<div>
					<span class="eyebrow">01 / SELEZIONE</span>
					<h2 id="work-title">Fatti, poi online<span class="purple">.</span></h2>
				</div>
				<p>Tre realtà diverse.<br />Un progetto su misura, ogni volta.</p>
			</div>
			<div class="projects">
				<a
					class="project project-pharmacy"
					href="https://www.sanmichelefarmacia.com/"
					target="_blank"
					rel="noopener noreferrer"
					><div class="folder-tab">01 / FARMACIA</div>
					<div class="project-art">
						<img
							src="/projects/farmacia.webp"
							alt="Anteprima del design di Farmacia San Michele"
							width="1321"
							height="917"
							loading="lazy"
						/>
					</div>
					<div class="project-info">
						<div>
							<h3>Farmacia<br />San Michele</h3>
							<p>Salute e servizi, a portata di click.</p>
						</div>
						<span class="project-arrow" aria-label="Visita il sito, si apre in una nuova scheda"
							>↗</span
						>
					</div>
					<span class="project-domain">sanmichelefarmacia.com</span></a
				>
				<a
					class="project project-psychology"
					href="https://giuliaforcignano.it/"
					target="_blank"
					rel="noopener noreferrer"
					><div class="folder-tab">02 / PROFESSIONISTI</div>
					<div class="project-art">
						<img
							src="/projects/giulia.webp"
							alt="Anteprima del sito della psicologa Giulia Forcignano"
							width="1261"
							height="907"
							loading="lazy"
						/>
					</div>
					<div class="project-info">
						<div>
							<h3>Giulia<br />Forcignano</h3>
							<p>Uno spazio per iniziare un percorso.</p>
						</div>
						<span class="project-arrow" aria-label="Visita il sito, si apre in una nuova scheda"
							>↗</span
						>
					</div>
					<span class="project-domain">giuliaforcignano.it</span></a
				>
				<a
					class="project project-law"
					href="https://dmcavvocati.it/"
					target="_blank"
					rel="noopener noreferrer"
					><div class="folder-tab">03 / STUDIO LEGALE</div>
					<div class="project-art law-art">
						<span class="law-wordmark">De Martiis<br />Catalano<span>AVVOCATI</span></span><img
							src="/projects/apollo.webp"
							alt="Busto classico, riferimento visivo del progetto De Martiis Catalano"
							width="400"
							height="400"
							loading="lazy"
						/>
					</div>
					<div class="project-info">
						<div>
							<h3>De Martiis<br />Catalano</h3>
							<p>Identità e presenza, anche sul web.</p>
						</div>
						<span class="project-arrow" aria-label="Visita il sito, si apre in una nuova scheda"
							>↗</span
						>
					</div>
					<span class="project-domain">dmcavvocati.it</span></a
				>
			</div>
		</section>
		<section id="approccio" class="approach wrap" aria-labelledby="approach-title">
			<div class="approach-label">
				<span class="eyebrow">02 / IL MIO APPROCCIO</span><span
					class="outline-arrow"
					aria-hidden="true">↗</span
				>
			</div>
			<div class="approach-copy">
				<h2 id="approach-title">
					Non sono il tuo fornitore.<br />Sono un <span class="purple">partner,</span><br />un
					riferimento stabile.
				</h2>
				<div class="about-copy">
					<p>
						Sono Alessandro, la persona dietro Delvup. Metto insieme design e sviluppo per dare
						forma alla tua presenza online.
					</p>
					<p>
						Ti accompagno nelle scelte, costruisco il tuo sito e continuo a prendermene cura. Perché
						andare online è solo l’inizio.
					</p>
				</div>
			</div>
		</section>
		<section class="services wrap" aria-label="Come posso aiutarti">
			{#each [{ n: '01', title: 'Design.', subtitle: 'Dare forma alle idee.', text: 'Identità visiva e interfacce che parlano di te. Ogni scelta parte dalle persone che vuoi raggiungere.' }, { n: '02', title: 'Develop.', subtitle: 'Farle funzionare.', text: 'Siti chiari, veloci e adatti a ogni schermo. Un’esperienza semplice, dal primo accesso al contatto.' }, { n: '03', title: 'Care.', subtitle: 'Esserci, anche dopo.', text: 'Supporto, aggiornamenti e attenzione nel tempo. Il tuo sito cresce insieme alla tua attività.' }] as service (service.n)}
				<div class="service">
					<span class="service-number">{service.n}</span>
					<h3>{service.title}</h3>
					<div>
						<h4>{service.subtitle}</h4>
						<p>{service.text}</p>
					</div>
					<span class="service-plus" aria-hidden="true">↗</span>
				</div>
			{/each}
		</section>
		<section id="contatti" class="contact wrap" aria-labelledby="contact-title">
			<span class="eyebrow">03 / IL PROSSIMO PROGETTO</span>
			<h2 id="contact-title">
				Hai un progetto<br />in mente?<br /><a href="mailto:ciao@delvup.com"
					>Parliamone<span aria-hidden="true">↗</span></a
				>
			</h2>
			<div class="contact-bottom">
				<a href="mailto:ciao@delvup.com">ciao@delvup.com ↗</a>
				<p>Una buona conversazione<br />è un ottimo punto di partenza.</p>
			</div>
		</section>
	</main>
	<footer class="site-footer wrap">
		<span>DELVUP © {new Date().getFullYear()}</span><span>Design, develop & care.</span><span
			>By Alessandro Delvezio · Made in Italy</span
		><a href="#inizio">Torna su ↑</a>
	</footer>
</div>
