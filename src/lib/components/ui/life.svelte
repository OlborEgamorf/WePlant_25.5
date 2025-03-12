<script lang="ts">
    import { Slider } from "$lib/components/ui/slider/index.js";
    import Toggle from "./toggle.svelte";

    import ClayIcon from "$lib/assets/argile.svg";
    import SandIcon from "$lib/assets/sable.svg";
    import LoamIcon from "$lib/assets/terre.svg";
    import Grow1 from "$lib/assets/grow_1.svg"
    import Grow2 from "$lib/assets/grow_2.svg"
    import Grow3 from "$lib/assets/grow_3.svg"
    import Grow4 from "$lib/assets/grow_4.svg"

    let animation = true

    let soils:Selects[] = [
        {value:"loam", label:"Terre"},
        {value:"clay", label:"Argile"},
        {value:"sand", label:"Sable"},
    ]

    let soil:string = $state("loam")
    let waterNeed:string = $state("0")

    let water:Selects[] = [
        {value:"0", label:"Quotidien"},
        {value:"1", label:"Semi-hebdomadaire"},
        {value:"2", label:"Hebdomadaire"}
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
        sleep(700).then(() => {
            if (i == incr) {
                moisture = moistureTemp
                temperature = temperatureTemp
                sun = sunTemp
                incr = 0
            }
        })
    })

    let dataAPI:APIPredict = $state({prediction:0})
    let predi:number = -1

    // 0 : neutral à bon
    // 1 : neutral à mauvais
    // 2 : bon à mauvais
    // 3 : mauvais à bon
    let stateAnim = $state(-1)

    $effect(() => {
        moisture;temperature;sun;soil;waterNeed
        fetch(`http://127.0.0.1:8000/predict_croissance?sunlight_hours=${sun}&temperature=${temperature}&moisture=${moisture}&soil=${soil}&water_freq=${waterNeed}`)
        .then(response => response.json())
        .then(data => dataAPI = data);
    })

    $effect(() => {
        if (predi == 0 && dataAPI.prediction == 1) stateAnim = 3
        else if (predi == 1 && dataAPI.prediction == 0) stateAnim = 2
        else if (predi == -1 && dataAPI.prediction == 1) stateAnim = 0
        else if (predi == -1 && dataAPI.prediction == 0) stateAnim = 1

        predi = dataAPI.prediction
    })

    function setAnimBad(stateAnim:number) {
        if (stateAnim == 0) return "hidden"
        if (stateAnim == 1 || stateAnim == 2) return 'animate-fade animate-once animate-duration-1000 animate-delay-1500 animate-normal'
        if (stateAnim == 3) return 'animate-fade animate-once animate-duration-1000 animate-delay-1000 animate-reverse'
    }

    function setAnimNeutral(stateAnim:number ) {
        if (stateAnim == 0 || stateAnim == 1) return 'animate-fade animate-once animate-duration-1000 animate-delay-1000 animate-reverse'
        else return  "hidden"
    }

    function setAnimGood(stateAnim:number) {
        if (stateAnim == 1) return "hidden"
        if (stateAnim == 0 || stateAnim == 3) return 'animate-fade animate-once animate-duration-1000 animate-delay-1500 animate-normal'
        if (stateAnim == 2) return 'animate-fade animate-once animate-duration-1000 animate-delay-1000 animate-reverse'
    }

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
                <Toggle bind:selected={soil} params={soils} image={[LoamIcon,ClayIcon,SandIcon]}></Toggle>
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
                <Toggle bind:selected={waterNeed} params={water}></Toggle>
            </div>

            
        </div>
    </div>

    <div class="col-start-2 row-start-1 row-span-2">
        <div class="col-start-2 row-start-1 row-span-2 relative transition-all">
            {#if stateAnim == -1}
                <img src={Grow3} class="transition-all w-[300px] absolute -top-20 left-15 z-5" alt="">
            {:else if stateAnim == 0}
                <img src={Grow3} class="transition-all w-[300px] absolute -top-20 left-15 z-5 animate-fade animate-once animate-duration-1000 animate-delay-1000 animate-reverse" alt="">
                <img src={Grow4} class="transition-all w-[300px] absolute -top-61 left-15.5 z-5 animate-fade animate-once animate-duration-1000 animate-delay-1500 animate-normal" alt="">
            {:else if stateAnim == 1}
                <img src={Grow3} class="transition-all w-[300px] absolute -top-20 left-15 z-5 animate-fade animate-once animate-duration-1000 animate-delay-1000 animate-reverse" alt="">
                <img src={Grow1} class="transition-all w-[300px] absolute -top-20 left-15 z-5 animate-fade animate-once animate-duration-1000 animate-delay-1500 animate-normal" alt="">
            {:else if stateAnim == 2}
                <img src={Grow4} class="transition-all w-[300px] absolute -top-61 left-15.5 z-5 animate-fade animate-once animate-duration-1000 animate-delay-1000 animate-reverse" alt="">
                <img src={Grow1} class="transition-all w-[300px] absolute -top-20 left-15 z-5 animate-fade animate-once animate-duration-1000 animate-delay-1500 animate-normal" alt="">
            {:else if stateAnim == 3}
                <img src={Grow1} class="transition-all w-[300px] absolute -top-20 left-15 z-5 animate-fade animate-once animate-duration-1000 animate-delay-1000 animate-reverse" alt="">
                <img src={Grow4} class="transition-all w-[300px] absolute -top-61 left-15.5 z-5 animate-fade animate-once animate-duration-1000 animate-delay-1500 animate-normal" alt="">
            {/if}           

        </div>
    </div>

</div>