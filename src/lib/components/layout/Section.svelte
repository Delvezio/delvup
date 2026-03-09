<script lang="ts">
	type Tag = 'section' | 'div' | 'header' | 'footer' | 'main';

	export let as: Tag = 'section';
	export let id = '';
	export let className = '';
</script>

<svelte:element this={as} {id} class={`relative w-full ${className}`}>
	<slot />
</svelte:element>
