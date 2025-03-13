<script lang="ts">
    import * as Select from "$lib/components/ui/select/index.js";

    let { selected = $bindable(), params = $bindable(), placeholder, image } : {selected?: Selected, params: Selects[], placeholder: string, image?: string[]} = $props();
</script>

<Select.Root portal={null} bind:selected={selected}>
    <Select.Trigger class="w-[180px] border-[#DED08C] bg-[#DED08C] mx-1">
        <Select.Value placeholder={placeholder} />
    </Select.Trigger>
    <Select.Content>
        <Select.Group>
            {#each params as param, i}
                <Select.Item value={param.value} label={param.label}>
                    <div class="flex items-center">
                        {#if image && image[i]}
                            <img src={image[i]} alt={param.label} class="w-6 h-6 mr-2 rounded-full" />
                        {/if}
                        {param.label}
                    </div>
                </Select.Item>
            {/each}
        </Select.Group>
    </Select.Content>
    <Select.Input name="favoriteFruit" />
</Select.Root>
