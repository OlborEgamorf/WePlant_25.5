<script lang="ts">
    import Cycle from "$lib/components/ui/cycle.svelte";
    import Life from "$lib/components/ui/life.svelte";
    import Recommand from "$lib/components/ui/recommand.svelte";
    import Stress from "$lib/components/ui/stress.svelte";
    import * as Tabs from "$lib/components/ui/tabs/index.js";
    import fleur from "$lib/fleur.png";
    import bambou from "$lib/bambou.png";
    import home from "$lib/assets/home.svg";
    import logo from "$lib/weplante.png";
    import pv from "$lib/pv.png";
</script>

<img src={fleur} class="w-auto h-70 fixed top-0 right-0" alt="fleur" />
<img src={bambou} class="w-auto h-70 fixed bottom-0 left-0" alt="fleur" />


<div class="bg-[#EBDC94] min-h-screen text-zinc-700 font-[FuturaRener]">
    <a href="/" class="fixed top-1 left-1">
        <img src={home} class="w-10 h-10 cursor-pointer" alt="home" />
    </a>
    <Tabs.Root value="calc" class="pt-10 z-7">
        
        <Tabs.List class="grid mx-100 grid-cols-4">
          <Tabs.Trigger value="calc">Entretien</Tabs.Trigger>
          <Tabs.Trigger value="grow">Prédiction de croissance</Tabs.Trigger>
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

    <img src={logo} class=" hidden fixed w-auto h-15 absolute bottom-2 right-2" alt="logo" />
    <img src={pv} class="hidden fixed w-auto h-15 absolute bottom-2 right-17" alt="logo" />
</div>