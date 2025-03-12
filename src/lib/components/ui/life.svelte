<script lang="ts">
    import { Slider } from "$lib/components/ui/slider/index.js";
    import Results from "$lib/components/ui/results.svelte";
    import Toggle from "./toggle.svelte";

    let soils:Selects[] = [
        {value:"loam", label:"Terre"},
        {value:"clay", label:"Argile"},
        {value:"sand", label:"Sable"},
    ]

    let soil:string = "loam"

    let water:Selects[] = [
        {value:"1", label:"Rare"},
        {value:"2", label:"Moyen"},
        {value:"3", label:"Fréquent"}
    ]

    let minMoisture:number = 0
    let minTemperture:number = 0 
    let minSun:number = 0

    let maxMoisture:number = 100
    let maxTemperture:number = 35
    let maxSun:number = 100

    let incr:number = 0

    let moisture:number[] = $state([50])
    let temperature:number[] = $state([20])
    let sun:number[] = $state([50])

    let moistureTemp:number[] = $state([50])
    let temperatureTemp:number[] = $state([20])
    let sunTemp:number[] = $state([50])

    $effect(() => {
        moistureTemp; temperatureTemp; sunTemp;
        let i = ++incr
        const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
        sleep(1000).then(() => {
            if (i == incr) {
                moisture = moistureTemp
                temperature = temperatureTemp
                sun = sunTemp
                incr = 0
            }
        })
    })

    let dataAPI = $state({})

    $effect(() => {
        moisture;temperature;sun;soil;water
        fetch('http://127.0.0.1:8000/life?')
        .then(response => response.json())
        .then(data => dataAPI = data);
    })

</script>

<div class="grid mx-10 my-5 lg:mx-75 items-center grid-cols-2 gap-x-10">
    <div class="col-start-1">
        <div class="w-[300px]">
            <div class="mb-5">
                <div class="font-bold text-xl">Caractéristiques de la plante</div>
                <div>Ces caractéristiques concernent la vie de la plante et de kjq...</div>
            </div>
        
            <div class="mb-3">
                <div class="mb-1 font-semibold">Choix du sol</div>
                <Toggle selected={soil} params={soils}></Toggle>
                <!-- <Selection params={soils} placeholder={"Choisir un sol"}></Selection> -->
            </div> 
            
            <div class="mb-5 mt-5">
                <div class="font-bold text-xl">Paramètres environnementaux</div>
                <div>L'environnement correspond aux conditions de vie de la plante...</div>
            </div>
        
            <div class="mb-3">
                <div class="mb-2 font-semibold">Humidité - {moistureTemp}</div>
                <Slider bind:value={moistureTemp} min={minMoisture} max={maxMoisture} step={1} class="w-[180px]"/>
            </div>
        
            <div class="mb-3">
                <div class="mb-2 font-semibold">Température - {temperatureTemp}</div>
                <Slider bind:value={temperatureTemp} min={minTemperture} max={maxTemperture} step={1} class="w-[180px]" />
            </div>

            <div class="mb-3">
                <div class="mb-2 font-semibold">Exposition au soleil - {sunTemp}</div>
                <Slider bind:value={sunTemp} min={minSun} max={maxSun} step={1} class="w-[180px]" />
            </div>

            <div>
                <div class="mb-2 font-semibold">Fréquence d'arosage</div>
                <Toggle params={water}></Toggle>
            </div>

            
        </div>
    </div>

    <div class="col-start-2 row-start-1 row-span-2">
        <Results></Results>
    </div>

</div>