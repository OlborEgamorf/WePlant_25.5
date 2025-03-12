<script lang="ts">
    import * as Select from "$lib/components/ui/select/index.js";

    let { selected = $bindable(), params = $bindable(), placeholder } : {selected?:Selected, params:Selects[], placeholder:string} = $props();

</script>

<Select.Root portal={null} bind:selected={selected}>
    <Select.Trigger class="w-[180px] bg-lime-50 border-2 border-gray-950">
        <Select.Value placeholder={placeholder} />
    </Select.Trigger>
    <Select.Content>
        <Select.Group>
        {#each params as param}
            <Select.Item value={param.value} label={param.label}
            >{param.label}</Select.Item
            >
        {/each}
        </Select.Group>
    </Select.Content>
    <Select.Input name="favoriteFruit" />
</Select.Root>