<script lang="ts">
    import * as ToggleGroup from "$lib/components/ui/toggle-group/index.js";

    let { selected = $bindable(), params = $bindable() } : {selected?:string, params:Selects[]} = $props();


</script>

<ToggleGroup.Root type="single" value={selected} class="justify-start">
    {#each params as param}
        <ToggleGroup.Item class="border-2 border-gray-950 {param.value != selected ? "cursor-pointer" : ""}" value={param.value} aria-label={param.label}>
            {param.label}
        </ToggleGroup.Item>
    {/each}
</ToggleGroup.Root>