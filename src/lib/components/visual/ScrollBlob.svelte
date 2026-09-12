<script lang="ts">
	import { onMount } from 'svelte';
	import { introDone } from '$lib/stores/intro';

	let host: HTMLDivElement;
	let canvas: HTMLCanvasElement;
	let ready = $state(false);

	onMount(() => {
		let disposed = false;
		let cleanup = () => {};

		async function start() {
			const THREE = await import('three');
			const { RoomEnvironment } = await import('three/addons/environments/RoomEnvironment.js');
			if (disposed) return;

			let renderer: InstanceType<typeof THREE.WebGLRenderer>;
			try {
				renderer = new THREE.WebGLRenderer({
					canvas,
					alpha: true,
					antialias: true,
					powerPreference: 'low-power'
				});
			} catch {
				return;
			}

			const scene = new THREE.Scene();
			const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 30);
			camera.position.z = 5.8;
			renderer.setClearColor(0, 0);
			renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
			renderer.outputColorSpace = THREE.SRGBColorSpace;
			renderer.toneMapping = THREE.ACESFilmicToneMapping;

			const environment = new RoomEnvironment();
			const pmrem = new THREE.PMREMGenerator(renderer);
			const env = pmrem.fromScene(environment, 0.03);
			scene.environment = env.texture;
			environment.dispose();
			pmrem.dispose();

			const geometry = new THREE.SphereGeometry(1, 72, 52);
			const positions = geometry.attributes.position;
			const original = new Float32Array(positions.array);
			const material = new THREE.MeshPhysicalMaterial({
				color: 0xccecff,
				metalness: 0,
				roughness: 0.045,
				transmission: 0.96,
				thickness: 1.65,
				ior: 1.333,
				clearcoat: 1,
				clearcoatRoughness: 0.035,
				specularIntensity: 1.35,
				specularColor: 0xffffff,
				attenuationColor: 0x8e72ee,
				attenuationDistance: 1.8,
				envMapIntensity: 1.9
			});
			const rimMaterial = new THREE.MeshPhysicalMaterial({
				color: 0x8565ed,
				metalness: 0,
				roughness: 0.08,
				transmission: 0.25,
				transparent: true,
				opacity: 0.13,
				side: THREE.BackSide,
				depthWrite: false,
				blending: THREE.AdditiveBlending
			});
			const bubble = new THREE.Group();
			const mesh = new THREE.Mesh(geometry, material);
			const rim = new THREE.Mesh(geometry, rimMaterial);
			rim.scale.setScalar(1.035);
			bubble.add(mesh, rim);
			scene.add(bubble);

			const violetLight = new THREE.DirectionalLight(0x8968ee, 3.2);
			violetLight.position.set(-3, 2.2, 3.5);
			scene.add(violetLight);
			const waterLight = new THREE.DirectionalLight(0xc9f4ff, 3.8);
			waterLight.position.set(3.4, -1.6, 2.6);
			scene.add(waterLight);
			const topLight = new THREE.PointLight(0xffffff, 5.5, 8);
			topLight.position.set(-0.7, 2.5, 3.2);
			scene.add(topLight);

			let frame = 0;
			let last = performance.now();
			let phase = 0;
			let size = 480;
			let mobile = false;
			let reduced = false;
			let baseX = 0;
			let baseY = 0;
			let scale = 1;
			let progress = 0;
			let pointerX = innerWidth * 0.5;
			let pointerY = innerHeight * 0.5;
			let pointerActive = false;
			let pointerSpeed = 0;
			let pointerInfluence = 0;
			let pushX = 0;
			let pushY = 0;
			let tiltX = 0;
			let tiltY = 0;
			let localPointerX = 0;
			let localPointerY = 0;
			let lastPointerTime = performance.now();
			let stops: { scroll: number; x: number; y: number; scale: number }[] = [];
			const preference = matchMedia('(prefers-reduced-motion: reduce)');

			function updateTheme() {
				const dark = document.documentElement.dataset.theme === 'dark';
				material.color.setHex(dark ? 0xa8d7ff : 0xccecff);
				material.attenuationColor.setHex(dark ? 0x7655e7 : 0x9a82ed);
				rimMaterial.color.setHex(dark ? 0xa889ff : 0x7651d7);
				rimMaterial.opacity = dark ? 0.19 : 0.13;
				renderer.toneMappingExposure = dark ? 1.35 : 1.12;
			}

			function top(el: HTMLElement) {
				return el.getBoundingClientRect().top + scrollY;
			}

			function measure() {
				mobile = innerWidth <= 680;
				reduced = preference.matches;
				size = mobile ? Math.min(330, innerWidth * 0.76) : Math.min(620, innerWidth * 0.45);
				renderer.setSize(size, size, false);
				host.style.width = host.style.height = `${size}px`;

				const hero = document.querySelector('.hero') as HTMLElement | null;
				const signals = document.getElementById('per-te');
				const works = document.getElementById('lavori');
				const about = document.getElementById('approccio');
				const contact = document.getElementById('contatti');
				if (!hero || !signals || !works || !about || !contact) return;

				const heroY = top(hero) + (mobile ? 300 : 245);
				stops = [
					{ scroll: 0, x: innerWidth * (mobile ? 0.7 : 0.82), y: heroY, scale: 1 },
					{
						scroll: Math.max(120, top(signals) - innerHeight * 0.28),
						x: innerWidth * 0.12,
						y: innerHeight * 0.36,
						scale: 0.62
					},
					{
						scroll: Math.max(240, top(works) - innerHeight * 0.28),
						x: innerWidth * 0.9,
						y: innerHeight * 0.31,
						scale: 0.55
					},
					{
						scroll: Math.max(360, top(about) - innerHeight * 0.22),
						x: innerWidth * 0.14,
						y: innerHeight * 0.52,
						scale: 0.76
					},
					{
						scroll: Math.max(480, top(contact) - innerHeight * 0.15),
						x: innerWidth * 0.83,
						y: innerHeight * 0.5,
						scale: 1
					}
				];
				handleScroll();
			}

			function setHostTransform() {
				host.style.transform = `translate3d(${baseX - size / 2 + pushX}px,${baseY - size / 2 + pushY}px,0) scale(${scale})`;
			}

			function handleScroll() {
				if (!stops.length) return;
				progress = scrollY / Math.max(1, document.documentElement.scrollHeight - innerHeight);
				if (mobile || reduced) {
					baseX = stops[0].x;
					baseY = stops[0].y - scrollY;
					scale = 1;
					host.style.opacity = baseY < -size ? '0' : '1';
				} else {
					let a = stops[0];
					let b = stops[1];
					for (let i = 1; i < stops.length; i++) {
						a = stops[i - 1];
						b = stops[i];
						if (scrollY <= b.scroll) break;
					}
					let t = THREE.MathUtils.clamp(
						(scrollY - a.scroll) / Math.max(1, b.scroll - a.scroll),
						0,
						1
					);
					t = t * t * (3 - 2 * t);
					baseX = THREE.MathUtils.lerp(a.x, b.x, t);
					baseY = THREE.MathUtils.lerp(a.y, b.y, t);
					scale = THREE.MathUtils.lerp(a.scale, b.scale, t);
					host.style.opacity = '1';
				}
				setHostTransform();
				if (reduced) draw(0, 1);
			}

			function handlePointer(event: PointerEvent) {
				if (event.pointerType === 'touch' || reduced) return;
				const elapsed = Math.max(12, event.timeStamp - lastPointerTime);
				const travelled = Math.hypot(event.clientX - pointerX, event.clientY - pointerY);
				pointerSpeed = Math.min(1, pointerSpeed * 0.45 + (travelled / elapsed) * 0.72);
				pointerX = event.clientX;
				pointerY = event.clientY;
				lastPointerTime = event.timeStamp;
				pointerActive = true;
			}

			function clearPointer() {
				pointerActive = false;
			}

			function updatePointer(delta: number) {
				const radius = Math.max(1, size * scale * 0.52);
				const dx = (pointerX - baseX) / radius;
				const dy = (pointerY - baseY) / radius;
				const distance = Math.hypot(dx, dy);
				const targetInfluence = pointerActive
					? THREE.MathUtils.smoothstep(1.55 - distance, 0, 1.35)
					: 0;
				const ease = 1 - Math.exp(-delta * 6.5);
				const spring = 1 - Math.exp(-delta * 4.8);
				pointerInfluence = THREE.MathUtils.lerp(pointerInfluence, targetInfluence, ease);
				localPointerX = THREE.MathUtils.lerp(
					localPointerX,
					THREE.MathUtils.clamp(dx, -1, 1),
					ease
				);
				localPointerY = THREE.MathUtils.lerp(
					localPointerY,
					THREE.MathUtils.clamp(dy, -1, 1),
					ease
				);
				pushX = THREE.MathUtils.lerp(pushX, -dx * 20 * targetInfluence, spring);
				pushY = THREE.MathUtils.lerp(pushY, -dy * 16 * targetInfluence, spring);
				tiltX = THREE.MathUtils.lerp(tiltX, dy * 0.2 * targetInfluence, ease);
				tiltY = THREE.MathUtils.lerp(tiltY, dx * 0.26 * targetInfluence, ease);
				pointerSpeed *= Math.exp(-delta * 5.5);
				setHostTransform();
			}

			function draw(t: number, delta: number) {
				updatePointer(delta);
				const pointerZ = Math.sqrt(
					Math.max(0.08, 1 - localPointerX * localPointerX - localPointerY * localPointerY)
				);
				for (let i = 0; i < positions.count; i++) {
					const nx = original[i * 3];
					const ny = original[i * 3 + 1];
					const nz = original[i * 3 + 2];
					const azimuth = Math.atan2(nz, nx);
					const baseWave =
						0.055 * Math.sin(3 * azimuth + t * 0.62) * Math.pow(1 - ny * ny, 1.7) +
						0.035 * Math.cos(4.5 * ny - t * 0.48) +
						0.02 * Math.sin(ny * 7 + nx * 3.5 + t * 0.75);
					const facing = Math.max(
						0,
						nx * localPointerX + ny * -localPointerY + nz * pointerZ
					);
					const contact = Math.pow(facing, 10) * pointerInfluence;
					const ripple =
						contact * Math.sin(t * 5.2 - facing * 13) * (0.018 + pointerSpeed * 0.018);
					const radius = 1 + baseWave + ripple - contact * 0.022;
					positions.setXYZ(i, nx * radius * 1.035, ny * radius * 0.985, nz * radius);
				}
				positions.needsUpdate = true;
				geometry.computeVertexNormals();

				const buoyancy = reduced ? 0 : Math.sin(t * 0.78) * 0.075;
				bubble.position.y = buoyancy;
				bubble.rotation.x = 0.12 + Math.sin(t * 0.34) * 0.08 + tiltX + progress * 0.38;
				bubble.rotation.y =
					0.28 + Math.cos(t * 0.29) * 0.11 + tiltY + progress * Math.PI * 2.4;
				bubble.rotation.z = -0.12 + Math.sin(t * 0.24) * 0.07 + progress * 0.35;
				const stretch = pointerInfluence * (0.025 + pointerSpeed * 0.025);
				bubble.scale.set(1 + stretch, 1 - stretch * 0.65, 1 + stretch * 0.25);
				renderer.render(scene, camera);
			}

			function loop(now: number) {
				frame = requestAnimationFrame(loop);
				const delta = Math.min((now - last) / 1000, 0.05);
				if (document.hidden || reduced || (mobile && baseY < -size) || now - last < 24) return;
				last = now;
				phase += delta;
				draw(phase, delta);
			}

			const resize = new ResizeObserver(measure);
			resize.observe(document.body);
			const themeObserver = new MutationObserver(updateTheme);
			themeObserver.observe(document.documentElement, {
				attributes: true,
				attributeFilter: ['data-theme']
			});
			const contextLost = (event: Event) => {
				event.preventDefault();
				ready = false;
				cancelAnimationFrame(frame);
			};

			canvas.addEventListener('webglcontextlost', contextLost);
			window.addEventListener('scroll', handleScroll, { passive: true });
			window.addEventListener('resize', measure);
			window.addEventListener('pointermove', handlePointer, { passive: true });
			window.addEventListener('blur', clearPointer);
			document.documentElement.addEventListener('pointerleave', clearPointer);
			preference.addEventListener('change', measure);

			updateTheme();
			measure();
			draw(0, 1);
			ready = true;
			frame = requestAnimationFrame(loop);

			cleanup = () => {
				cancelAnimationFrame(frame);
				resize.disconnect();
				themeObserver.disconnect();
				window.removeEventListener('scroll', handleScroll);
				window.removeEventListener('resize', measure);
				window.removeEventListener('pointermove', handlePointer);
				window.removeEventListener('blur', clearPointer);
				document.documentElement.removeEventListener('pointerleave', clearPointer);
				preference.removeEventListener('change', measure);
				canvas.removeEventListener('webglcontextlost', contextLost);
				geometry.dispose();
				material.dispose();
				rimMaterial.dispose();
				env.dispose();
				renderer.dispose();
			};
		}

		start().catch(() => {
			ready = false;
		});

		return () => {
			disposed = true;
			cleanup();
		};
	});
</script>

<div class="scroll-blob" class:active={ready} bind:this={host} aria-hidden="true">
	<canvas bind:this={canvas} class:hidden={!ready} class:entered={$introDone}></canvas>
</div>

<style>
	.scroll-blob {
		position: fixed;
		top: 0;
		left: 0;
		width: 480px;
		height: 480px;
		visibility: hidden;
		pointer-events: none;
		z-index: 1;
		will-change: transform;
		contain: layout style;
		filter: drop-shadow(0 24px 30px #34236d1a);
		transition:
			opacity 0.35s ease,
			visibility 0s linear 0.35s;
	}
	.scroll-blob.active {
		visibility: visible;
		transition-delay: 0s;
	}
	.scroll-blob canvas {
		width: 100%;
		height: 100%;
		display: block;
		opacity: 0;
		transform: scale(0.94);
		transition:
			opacity 1s ease,
			transform 1.35s cubic-bezier(0.16, 1, 0.3, 1);
	}
	.scroll-blob canvas.entered {
		opacity: 1;
		transform: scale(1);
	}
	.scroll-blob canvas.hidden {
		display: none;
	}
	@media (max-width: 680px) {
		.scroll-blob {
			width: 300px;
			height: 300px;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.scroll-blob canvas {
			transition: opacity 0.2s ease;
		}
	}
</style>
