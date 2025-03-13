<script lang="ts">
    import * as ToggleGroup from "$lib/components/ui/toggle-group/index.js";

    let { selected = $bindable(), params = $bindable(), image, styles } : {selected?:string, params:Selects[], image?:string[], styles?:string} = $props();
</script>

<ToggleGroup.Root type="single" bind:value={selected} class="justify-start">
    {#each params as param, i}
        <ToggleGroup.Item 
            class="border-0 bg-[#DED08C]
                {param.value != selected ? 'cursor-pointer' : '!bg-[#ABAA6C] !text-white'} 
                hover:bg-[#D1C484] hover:text-white " 
            value={param.value} 
            aria-label={param.label}>
            
            {#if image}
                <img src={image[i]} alt={param.label} class="mr-2 inline-block {styles}" />
            {/if}
            {param.label}
        </ToggleGroup.Item>
    {/each}
</ToggleGroup.Root>
