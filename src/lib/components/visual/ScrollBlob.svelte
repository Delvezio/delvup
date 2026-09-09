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
			const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 30);
			camera.position.z = 5.9;
			renderer.setClearColor(0, 0);
			renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
			renderer.toneMapping = THREE.ACESFilmicToneMapping;
			renderer.toneMappingExposure = 1.15;
			const environment = new RoomEnvironment();
			const pmrem = new THREE.PMREMGenerator(renderer);
			const env = pmrem.fromScene(environment, 0.04);
			scene.environment = env.texture;
			environment.dispose();
			pmrem.dispose();
			const geometry = new THREE.SphereGeometry(1, 72, 48);
			const positions = geometry.attributes.position;
			const original = new Float32Array(positions.array);
			const material = new THREE.MeshStandardMaterial({
				color: 0xc4a3f2,
				metalness: 1,
				roughness: 0.105,
				envMapIntensity: 1.7
			});
			const mesh = new THREE.Mesh(geometry, material);
			scene.add(mesh);
			const fill = new THREE.DirectionalLight(0x9560ed, 4);
			fill.position.set(-3, 1, 2);
			scene.add(fill);
			let frame = 0,
				last = 0,
				phase = 0,
				size = 380,
				mobile = false,
				reduced = false;
			let x = 0,
				y = 0,
				scale = 1,
				progress = 0;
			let stops: { scroll: number; x: number; y: number; scale: number }[] = [];
			const preference = matchMedia('(prefers-reduced-motion: reduce)');
			function measure() {
				mobile = innerWidth <= 680;
				reduced = preference.matches;
				size = mobile ? 270 : Math.min(540, innerWidth * 0.41);
				renderer.setSize(size, size);
				host.style.width = host.style.height = `${size}px`;
				const hero = document.querySelector('.hero') as HTMLElement;
				const works = document.getElementById('lavori')!;
				const about = document.getElementById('approccio')!;
				const contact = document.getElementById('contatti')!;
				const top = (el: HTMLElement) => el.getBoundingClientRect().top + scrollY;
				const heroY = top(hero) + (mobile ? 265 : 215);
				stops = [
					{ scroll: 0, x: innerWidth * (mobile ? 0.67 : 0.83), y: heroY, scale: 1 },
					{
						scroll: Math.max(100, top(works) - innerHeight * 0.3),
						x: innerWidth * 0.91,
						y: innerHeight * 0.31,
						scale: 0.55
					},
					{
						scroll: Math.max(200, top(about) - innerHeight * 0.22),
						x: innerWidth * 0.15,
						y: innerHeight * 0.52,
						scale: 0.78
					},
					{
						scroll: Math.max(300, top(contact) - innerHeight * 0.15),
						x: innerWidth * 0.83,
						y: innerHeight * 0.5,
						scale: 1.03
					}
				];
				scroll();
			}
			function scroll() {
				progress = scrollY / Math.max(1, document.documentElement.scrollHeight - innerHeight);
				if (mobile || reduced) {
					x = stops[0].x;
					y = stops[0].y - scrollY;
					scale = 1;
					host.style.opacity = y < -size ? '0' : '1';
				} else {
					let a = stops[0],
						b = stops[1];
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
					x = THREE.MathUtils.lerp(a.x, b.x, t);
					y = THREE.MathUtils.lerp(a.y, b.y, t);
					scale = THREE.MathUtils.lerp(a.scale, b.scale, t);
					host.style.opacity = '1';
				}
				host.style.transform = `translate3d(${x - size / 2}px,${y - size / 2}px,0) scale(${scale})`;
				if (reduced) draw(0);
			}
			function draw(t: number) {
				for (let i = 0; i < positions.count; i++) {
					const nx = original[i * 3],
						ny = original[i * 3 + 1],
						nz = original[i * 3 + 2];
					const azimuth = Math.atan2(nz, nx);
					const r =
						1 +
						0.24 * Math.sin(3 * azimuth + t * 0.35) * Math.pow(1 - ny * ny, 1.5) +
						0.14 * Math.cos(4 * ny + t * 0.45) +
						0.09 * Math.sin(ny * 6 + nx * 3 + t * 0.3);
					positions.setXYZ(i, nx * r * 1.08, ny * r * 0.9, nz * r);
				}
				positions.needsUpdate = true;
				geometry.computeVertexNormals();
				mesh.rotation.set(
					0.25 + (reduced ? 0 : progress * 1.5),
					0.4 + (reduced ? 0 : progress * Math.PI * 3 + t * 0.1),
					-0.3 + (reduced ? 0 : progress * 0.8)
				);
				renderer.render(scene, camera);
			}
			function loop(now: number) {
				frame = requestAnimationFrame(loop);
				if (document.hidden || reduced || (mobile && y < -size) || now - last < 33) return;
				phase += Math.min((now - last) / 1000, 0.05);
				last = now;
				draw(phase);
			}
			const resize = new ResizeObserver(measure);
			resize.observe(document.body);
			const contextLost = (event: Event) => {
				event.preventDefault();
				ready = false;
				cancelAnimationFrame(frame);
			};
			canvas.addEventListener('webglcontextlost', contextLost);
			window.addEventListener('scroll', scroll, { passive: true });
			window.addEventListener('resize', measure);
			preference.addEventListener('change', measure);
			measure();
			draw(0);
			ready = true;
			frame = requestAnimationFrame(loop);
			cleanup = () => {
				cancelAnimationFrame(frame);
				resize.disconnect();
				window.removeEventListener('scroll', scroll);
				window.removeEventListener('resize', measure);
				preference.removeEventListener('change', measure);
				canvas.removeEventListener('webglcontextlost', contextLost);
				geometry.dispose();
				material.dispose();
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
		position: absolute;
		top: 0;
		left: 0;
		width: 380px;
		height: 380px;
		transform: translate3d(calc(83vw - 190px), 180px, 0);
		pointer-events: none;
		z-index: 1;
		will-change: transform;
		contain: layout style;
		filter: drop-shadow(0 18px 20px #0000000c);
	}
	.scroll-blob.active {
		position: fixed;
	}
	.scroll-blob canvas {
		width: 100%;
		height: 100%;
		display: block;
	}
	.scroll-blob canvas {
		opacity: 0;
		transition: opacity 1s ease;
	}
	.scroll-blob canvas.entered {
		opacity: 1;
	}
	.scroll-blob canvas.hidden {
		display: none;
	}
	@media (max-width: 680px) {
		.scroll-blob {
			width: 220px;
			height: 220px;
			transform: translate3d(calc(67vw - 110px), 290px, 0);
		}
	}
</style>
