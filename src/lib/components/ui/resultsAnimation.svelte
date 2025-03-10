<script lang="ts">

    import Separator from "./separator/separator.svelte";
    import Tree from "$lib/assets/tree.svg"
    import Sun from "$lib/assets/sun.svg"
    import Cloud from "$lib/assets/cloud.svg"
    import Cactus from "$lib/assets/cactus.svg"

    let { light, moisture, temperture, soil }: { light:number[], moisture:number[], temperture:number[], soil:string } = $props()

    let numberLight:number = $derived(light[0])
    let numberMoisture:number = $derived(moisture[0])
    let numberTemperture:number = $derived(temperture[0])

</script>

<!-- svelte-ignore a11y_missing_attribute -->
 
<div>
    <div class="grid grid-cols-2">
        <div class="row-start-2 flex">
            <img class="w-[100px]" src={soil == "sand" ? Cactus : Tree}>
            <img class="w-[100px]" src={soil == "sand" ? Cactus : Tree}>
        </div>
        
        <img class="w-[80px] row-start-1 col-start-1 col-span-2 animate-spin animate-infinite animate-duration-[{25000-500*numberTemperture}ms] justify-self-center" src={Sun}>

        {#if numberLight < 50}
            <img class="w-[80px] row-start-1 col-start-1 justify-self-end animate-shake animate-infinite animate-duration-[10000ms]" src={Cloud}>
        {/if}

        {#if numberLight < 30}
            <img class="w-[80px] row-start-1 col-start-2 justify-self-start animate-shake animate-infinite animate-duration-[10000ms]" src={Cloud}>
        {/if}

        {#if numberLight < 15}
            <img class="w-[80px] row-start-1 col-start-1 col-span-2 justify-self-center animate-shake animate-infinite animate-duration-[10000ms]" src={Cloud}>
        {/if}
    </div>

    {#if soil == "sand"}
        <Separator orientation="vertical" class="w-full h-[5px] bg-amber-300"></Separator>
    {:else if soil == "loam"}
        <Separator orientation="vertical" class="w-full h-[5px] bg-yellow-950"></Separator>
    {:else}
        <Separator orientation="vertical" class="w-full h-[5px]"></Separator>
    {/if}
</div>