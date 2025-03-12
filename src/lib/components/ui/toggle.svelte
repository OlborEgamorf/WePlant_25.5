<script lang="ts">
    import * as ToggleGroup from "$lib/components/ui/toggle-group/index.js";

    let { selected = $bindable(), params = $bindable(), image, styles } : {selected?:string, params:Selects[], image?:string[], styles?:string} = $props();
</script>

<ToggleGroup.Root type="single" bind:value={selected} class="justify-start">
    {#each params as param, i}
        <ToggleGroup.Item 
            class="border-2 bg-lime-50 border-gray-950 
                {param.value != selected ? 'cursor-pointer' : '!bg-green-600 !text-white'} 
                hover:bg-lime-100 " 
            value={param.value} 
            aria-label={param.label}>
            
            {#if image}
                <img src={image[i]} alt={param.label} class="mr-2 inline-block {styles}" />
            {/if}
            {param.label}
        </ToggleGroup.Item>
    {/each}
</ToggleGroup.Root>
