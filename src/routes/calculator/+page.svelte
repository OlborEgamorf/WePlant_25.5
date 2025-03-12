<script lang="ts">
    import * as Tabs from "$lib/components/ui/tabs/index.js";
    import Cycle from "$lib/components/ui/cycle.svelte";
    import Life from "$lib/components/ui/life.svelte";
    import Stress from "$lib/components/ui/stress.svelte";
    import Recommand from "$lib/components/ui/recommand.svelte";
</script>


<div class="bg-[#ACE1AF] min-h-screen">

    <Tabs.Root value="calc" class="pt-10">
        <Tabs.List class="grid mx-100 grid-cols-4">
          <Tabs.Trigger value="calc">Entretien</Tabs.Trigger>
          <Tabs.Trigger value="grow">Prédiction de vie</Tabs.Trigger>
          <Tabs.Trigger value="stress">Stress hydrique</Tabs.Trigger>
          <Tabs.Trigger value="recom">Recommandation</Tabs.Trigger>
        </Tabs.List>
        <Tabs.Content value="calc">

            <Cycle></Cycle>
          
        </Tabs.Content>
        <Tabs.Content value="grow">

            <Life></Life>
          
        </Tabs.Content>
        <Tabs.Content value="stress">

            <Stress></Stress>
          
        </Tabs.Content>
        <Tabs.Content value="recom">
          <Recommand></Recommand>
        </Tabs.Content>
      </Tabs.Root>   

</div>