<script lang="ts">
    import LoaderCircle from "lucide-svelte/icons/loader-circle";

    let { change, load } : { change:boolean, load:boolean } = $props()
</script>

{#if change}
    <div class="flex items-center">
        <LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
        Changement des paramètres...
    </div>
{:else if load}
    <div class="flex items-center">
        <LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
        Chargement des données...
    </div>
{/if}