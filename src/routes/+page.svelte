<script lang="ts">
	import { onMount } from 'svelte';
	import IntroBrand from '$lib/components/sections/IntroBrand.svelte';
	import ScrollBlob from '$lib/components/visual/ScrollBlob.svelte';
	import { introDone } from '$lib/stores/intro';
	import { revealOnView } from '$lib/reveal';
	let mounted = $state(false);
	let mode = $state('auto');
	let activeSignal = $state<string | null>(null);
	const modes = [
		{ value: 'light', label: 'Chiaro', icon: '☼' },
		{ value: 'dark', label: 'Scuro', icon: '☾' },
		{ value: 'auto', label: 'Auto', icon: '◐' }
	];
	const signals = [
		{
			letter: 'A',
			text: 'Pensavi: bastano i social, il sito non serve.',
			gif: '/gifs/boris-proda.gif',
			axis: -15
		},
		{
			letter: 'B',
			text: 'Brand confuso, ma sito già online.',
			gif: '/gifs/cosi-de-botto.gif',
			axis: -6
		},
		{
			letter: 'C',
			text: 'Homepage romanzo, zero comunicazione.',
			gif: '/gifs/boris-monnezza.gif',
			axis: 5
		},
		{
			letter: 'D',
			text: 'Quando hai aggiornato l’ultima volta?',
			gif: '/gifs/boris-like.gif',
			axis: 15
		}
	];
	const siteDescription =
		'Sono Alessandro Delvezio: progetto siti web chiari, veloci e curati nel tempo per professionisti e PMI. Scopri i lavori di Delvup.';
	function moveSignalGif(event: PointerEvent) {
		if (event.pointerType === 'touch') return;
		const column = event.currentTarget as HTMLElement;
		const rect = column.getBoundingClientRect();
		const progress = Math.max(-1, Math.min(1, ((event.clientX - rect.left) / rect.width) * 2 - 1));
		const angle = Number(column.dataset.axis || 0) * (Math.PI / 180);
		const distance = progress * Math.min(68, rect.width * 0.22);
		column.style.setProperty('--gif-shift-x', `${Math.cos(angle) * distance}px`);
		column.style.setProperty('--gif-shift-y', `${Math.sin(angle) * distance}px`);
	}
	function resetSignalGif(event: PointerEvent) {
		const column = event.currentTarget as HTMLElement;
		column.style.setProperty('--gif-shift-x', '0px');
		column.style.setProperty('--gif-shift-y', '0px');
	}
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
	<title>Delvup | Siti web per professionisti e PMI</title>
	<meta name="description" content={siteDescription} />
	<meta name="robots" content="index, follow, max-image-preview:large" />
	<meta name="author" content="Alessandro Delvezio" />
	<meta name="theme-color" content="#733fe0" />
	<link rel="canonical" href="https://www.delvup.com/" />

	<meta property="og:type" content="website" />
	<meta property="og:locale" content="it_IT" />
	<meta property="og:site_name" content="Delvup" />
	<meta property="og:title" content="Delvup | Siti web per professionisti e PMI" />
	<meta property="og:description" content={siteDescription} />
	<meta property="og:url" content="https://www.delvup.com/" />
	<meta property="og:image" content="https://www.delvup.com/og-image.png" />
	<meta property="og:image:width" content="1200" />
	<meta property="og:image:height" content="630" />
	<meta property="og:image:alt" content="Delvup — Progetto il tuo online" />

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="Delvup | Siti web per professionisti e PMI" />
	<meta name="twitter:description" content={siteDescription} />
	<meta name="twitter:image" content="https://www.delvup.com/og-image.png" />

	<script type="application/ld+json">
		{
			"@context": "https://schema.org",
			"@type": "ProfessionalService",
			"name": "Delvup",
			"url": "https://www.delvup.com/",
			"logo": "https://www.delvup.com/favicon-192.png",
			"image": "https://www.delvup.com/og-image.png",
			"email": "ciao@delvup.com",
			"description": "Sono Alessandro Delvezio: progetto siti web chiari, veloci e curati nel tempo per professionisti e PMI. Scopri i lavori di Delvup.",
			"founder": {
				"@type": "Person",
				"name": "Alessandro Delvezio"
			},
			"areaServed": {
				"@type": "Country",
				"name": "Italia"
			},
			"serviceType": [
				"Web design",
				"Sviluppo siti web",
				"Manutenzione e supporto web"
			]
		}
	</script>
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
				<h1 id="hero-title">
					<span class="title-line-mask"><span class="title-line">Progetto</span></span>
					<span class="title-line-mask"><span class="title-line">il tuo <span class="purple">online.</span></span></span>
				</h1>
				<span class="hero-arrow" aria-hidden="true">↗</span>
			</div>
			<div class="hero-bottom">
				<p>Siti essenziali per professionisti e PMI.<br />Chiari, veloci, mantenuti nel tempo.</p>
				<a class="round-link" href="#per-te"
					><span>Ti posso aiutare se</span><span class="round-icon" aria-hidden="true">
						<svg class="round-timer" viewBox="0 0 64 64">
							<circle cx="32" cy="32" r="29" pathLength="100"></circle>
						</svg>
						<svg class="round-arrow" viewBox="0 0 24 24">
							<path d="M12 4v15M6.5 13.5 12 19l5.5-5.5"></path>
						</svg></span
					></a
				>
			</div>
			<div class="hero-rule">
				<span>DAL PRIMO PIXEL. AL GIORNO DOPO.</span><span>SCROLL PER SCOPRIRE ↓</span>
			</div>
		</section>
		<section id="per-te" class="signals-section wrap" aria-labelledby="signals-title">
			<div class="signals-heading">
				<h2 id="signals-title" class="reveal-title">
					<span class="title-line-mask"><span class="title-line">Sono qui per te se</span></span>
				</h2>
				<span class="signal-arrow" aria-hidden="true">↓</span>
			</div>
			<div class="signals-grid">
				{#each signals as signal (signal.letter)}
					<button
						type="button"
						class:signal-active={activeSignal === signal.letter}
						class="signal-column"
						data-axis={signal.axis}
						style={`--axis-angle: ${signal.axis}deg`}
						aria-pressed={activeSignal === signal.letter}
						aria-label={`${signal.text} Mostra l’animazione.`}
						onpointermove={moveSignalGif}
						onpointerleave={resetSignalGif}
						onclick={() =>
							(activeSignal = activeSignal === signal.letter ? null : signal.letter)}
					>
						<span class="signal-gif" aria-hidden="true">
							<img src={signal.gif} alt="" width="498" height="295" loading="lazy" />
						</span>
						<span class="signal-copy">
							<span class="signal-marker">
								<svg class="signal-timer" viewBox="0 0 36 36" aria-hidden="true">
									<circle cx="18" cy="18" r="16" pathLength="100"></circle>
								</svg>
								<span>{signal.letter}</span>
							</span>
							<span class="signal-text">{signal.text}</span>
						</span>
					</button>
				{/each}
			</div>
		</section>
		<section id="lavori" class="work-section wrap" aria-labelledby="work-title">
			<div class="section-heading">
				<div>
					<span class="eyebrow">01 / SELEZIONE</span>
					<h2 id="work-title" class="reveal-title">
						<span class="title-line-mask"><span class="title-line">Fatti, poi online<span class="purple">.</span></span></span>
					</h2>
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
							<h3 class="reveal-title">
								<span class="title-line-mask"><span class="title-line">Farmacia</span></span>
								<span class="title-line-mask"><span class="title-line">San Michele</span></span>
							</h3>
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
							<h3 class="reveal-title">
								<span class="title-line-mask"><span class="title-line">Giulia</span></span>
								<span class="title-line-mask"><span class="title-line">Forcignano</span></span>
							</h3>
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
							<h3 class="reveal-title">
								<span class="title-line-mask"><span class="title-line">De Martiis</span></span>
								<span class="title-line-mask"><span class="title-line">Catalano</span></span>
							</h3>
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
				<h2 id="approach-title" class="reveal-title">
					<span class="title-line-mask"><span class="title-line">Non sono il tuo fornitore.</span></span>
					<span class="title-line-mask"><span class="title-line">Sono un <span class="purple">partner,</span></span></span>
					<span class="title-line-mask"><span class="title-line">un riferimento stabile.</span></span>
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
					<h3 class="reveal-title"><span class="title-line-mask"><span class="title-line">{service.title}</span></span></h3>
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
			<h2 id="contact-title" class="reveal-title">
				<span class="title-line-mask"><span class="title-line">Hai un progetto</span></span>
				<span class="title-line-mask"><span class="title-line">in mente?</span></span>
				<span class="title-line-mask"><span class="title-line"><a href="mailto:ciao@delvup.com">Parliamone<span aria-hidden="true">↗</span></a></span></span>
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
