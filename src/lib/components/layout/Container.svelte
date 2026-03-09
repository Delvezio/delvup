<script lang="ts">
	type Tag = 'div' | 'section' | 'header' | 'footer' | 'main';
	type Width = 'narrow' | 'content' | 'site' | 'wide' | 'full';

	export let as: Tag = 'div';
	export let width: Width = 'site';
	export let className = '';

	$: widthClass =
		width === 'narrow'
			? 'max-w-3xl'
			: width === 'content'
				? 'max-w-5xl'
				: width === 'site'
					? 'max-w-[90rem]'
					: width === 'wide'
						? 'max-w-[110rem]'
						: 'max-w-none';
</script>

<svelte:element
	this={as}
	class={`mx-auto w-full px-4 sm:px-6 lg:px-8 ${widthClass} ${className}`}
>
	<slot />
</svelte:element>
