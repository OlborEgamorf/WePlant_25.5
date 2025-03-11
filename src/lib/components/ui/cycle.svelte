<script lang="ts">
    import Separator from "./separator/separator.svelte";
    import Slider from "./slider/slider.svelte";
    import Toggle from "./toggle.svelte";
    import Pot from "$lib/assets/pot.svg"
    import Tree from "$lib/assets/tree.svg"

    let soils:Selects[] = [
        {value:"loam", label:"Terre"},
        {value:"clay", label:"Argile"},
        {value:"sand", label:"Sable"},
    ]

    let pots:Selects[] = [
        {value:"5l", label:"5 Litres"},
        {value:"50l", label:"50 Litres"},
        {value:"100l", label:"100 Litres"}
    ]

    let roots:Selects[] = [
        {value:"short", label:"Courtes"},
        {value:"medium", label:"Moyennes"},
        {value:"long", label:"Longues"},
    ]

    let soil:string = "loam"
    let root:string = "medium"

    let minMoisture:number = 0
    let maxMoisture:number = 100

    let moisture:number[] = $state([50])
    let moistureTemp:number[] = $state([50])
    let incr:number = 0

    $effect(() => {
        moistureTemp;
        let i = ++incr
        const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
        sleep(1000).then(() => {
            if (i == incr) {
                moisture = moistureTemp
                incr = 0
            }
        })
    })

</script>

<div class="grid mx-10 my-10 lg:mx-75 items-center grid-cols-2 gap-x-10">
    <div class="col-start-1">
        <div class="w-[300px]">
            <div class="mb-5">
                <div class="font-bold text-xl">Caractéristiques de la plante</div>
                <div>Ces caractéristiques concernent la vie de la plante et de kjq...</div>
            </div>
        
            <div class="mb-3">
                <div class="mb-1 font-semibold">Choix du sol</div>
                <Toggle selected={soil} params={soils}></Toggle>
            </div>
        
            <div>
                <div class="mb-1 font-semibold">Type de racines</div>
                <Toggle selected={root} params={roots}></Toggle>
            </div>

            <Separator class="my-4 bg-gray-950" />

            <div class="mb-5">
                <div class="font-bold text-xl">Caractéristiques du pot</div>
                <div>Ces caractéristiques concernent la vie de la plante et de kjq...</div>
            </div>

            <div class="mb-3">
                <div class="mb-2 font-semibold">Type de pot</div>
                <Toggle params={pots}></Toggle>
            </div>
            
            <div>
                <div class="mb-2 font-semibold">Taux d'humidité - {moistureTemp} %</div>
                <Slider bind:value={moistureTemp} min={minMoisture} max={maxMoisture} step={1} class="w-[180px]" />
            </div>
            
        </div>
    </div>

    <div class="col-start-2 row-start-1 row-span-2 relative">
        <img src={Pot} class="w-[200px] absolute top-0 left-0 z-5" alt="pot">
        <img src={Tree} class="w-[200px] absolute -top-46 left-0" alt="">
    </div>
</div>