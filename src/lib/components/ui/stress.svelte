<script lang="ts">
    import Results from "$lib/components/ui/results.svelte";
    import Separator from "./separator/separator.svelte";
    import Slider from "./slider/slider.svelte";

    import LoaderCircle from "lucide-svelte/icons/loader-circle";

    import Banzai from "$lib/assets/banzai.svg"
    import Eclair from "$lib/assets/eclair.svg"
    import Eclair2 from "$lib/assets/thunder.svg"
    import Fleur from "$lib/assets/flower.svg"

    let minMoisture:number = 10
    let minTemperture:number = 15
    let minPhosphore:number = 0
    let minNitro:number = 0
    let minPotassium:number = 0

    let maxMoisture:number = 40
    let maxTemperture:number = 25
    let maxPhosphore:number = 100
    let maxNitro:number = 100
    let maxPotassium:number = 100

    let moisture:number[] = $state([20])
    let temperature:number[] = $state([15])
    let phosphore:number[] = $state([50])
    let nitro:number[] = $state([50])
    let potassisum:number[] = $state([50]) 

    let moistureTemp:number[] = $state([20])
    let temperatureTemp:number[] = $state([15])
    let phosphoreTemp:number[] = $state([30])
    let nitroTemp:number[] = $state([30])
    let potassisumTemp:number[] = $state([30]) 

    let incr:number = 0
    let change:boolean= $state(false)

    $effect(() => {
        moistureTemp;temperatureTemp;phosphoreTemp;nitroTemp;potassisumTemp;
        let i = ++incr
        change = true
        const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
        sleep(700).then(() => {
            if (i == incr) {
                moisture = moistureTemp
                temperature = temperatureTemp
                phosphore = phosphoreTemp
                nitro = nitroTemp
                potassisum = potassisumTemp
                incr = 0
                change = false
            }
        })
    })

    let dataAPI:APIStress = $state({prediction:0, prob0:0, prob1:0, prob2:0})
    let health:number = $derived(dataAPI.prediction)

    // let health = 2

    $effect(() => {
        moisture;temperature;phosphore;nitro;potassisum;
        fetch(`http://127.0.0.1:8000/stress_hydrique?soil_moisture=${moisture}&soil_temperature=${temperature}&nitrogen_level=${nitro}&phosphorus_level=${phosphore}&potassium_level=${potassisum}`)
        .then(response => response.json())
        .then(data => dataAPI = data);
    })

    $effect(() => {
        console.log(health)
    })

</script>

<div class="grid mx-10 my-10 lg:mx-75 items-center grid-cols-2 gap-x-10">
    <div class="col-start-1">
        <div class="w-[300px]">
            <div class="mb-5">
                <div class="font-bold text-xl">Paramètres obligatoires</div>
                <div>Ces caractéristiques concernent la vie de la plante et de kjq...</div>
            </div>
            
            <div class="mb-3">
                <div class="mb-2 font-semibold">Taux d'humidité - {moistureTemp} %</div>
                <Slider bind:value={moistureTemp} min={minMoisture} max={maxMoisture} step={1} class="w-[180px]" />
            </div>

            <div>
                <div class="mb-2 font-semibold">Température - {temperatureTemp}°C</div>
                <Slider bind:value={temperatureTemp} min={minTemperture} max={maxTemperture} step={1} class="w-[180px]" />
            </div>
            
            <Separator class="my-4 bg-gray-950" />

            <div class="mb-5">
                <div class="font-bold text-xl">Paramètres optionnels</div>
                <div>Ces caractéristiques concernent la vie de la plante et de kjq...</div>
            </div>

            <div class="mb-3">
                <div class="mb-2 font-semibold">Taux de phosphore - {phosphoreTemp} %</div>
                <Slider bind:value={phosphoreTemp} min={minPhosphore} max={maxPhosphore} step={1} class="w-[180px]" />
            </div>

            <div class="mb-3">
                <div class="mb-2 font-semibold">Taux de nitrogène - {nitroTemp} %</div>
                <Slider bind:value={nitroTemp} min={minNitro} max={maxNitro} step={1} class="w-[180px]" />
            </div>

            <div>
                <div class="mb-2 font-semibold">Taux de potassium - {potassisumTemp} %</div>
                <Slider bind:value={potassisumTemp} min={minPotassium} max={maxPotassium} step={1} class="w-[180px]" />
            </div>
        </div>
    </div>

    <div class="col-start-2 row-start-1 row-span-2">
        
        <div class="col-start-2 row-start-1 row-span-2 relative transition-all">

            {#if change}
                <div class="col-start-2 row-start-1 row-span-2 absolute flex -top-60 left-60 items-center">
                    <LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
                    Chut chut ça pousse !</div>
            {/if}
            
            <img src={Banzai} class="w-[300px] absolute -top-40 left-15 z-5" alt="">

            <img src={Eclair2} class="w-[40px] absolute -top-25 left-20 z-5 transition-all {health >= 1 ? 'animate-bounce animate-infinite animate-duration-[2000ms] animate-ease-out' : 'opacity-0'}" alt="">
            <img src={Eclair2} class="w-[40px] absolute -top-40 left-70 z-5 transition-all {health >= 1 ? 'animate-bounce animate-infinite animate-duration-[2000ms] animate-ease-out ' : 'opacity-0'}" alt="">

            <img src={Eclair2} class="w-[40px] absolute -top-0 left-72 z-5 transition-all {health == 2 ? 'animate-bounce animate-infinite animate-duration-[2000ms] animate-ease-out ' : 'opacity-0'}" alt="">
            <img src={Eclair2} class="w-[40px] absolute -top-50 left-42 z-5 transition-all {health == 2 ? 'animate-bounce animate-infinite animate-duration-[2000ms] animate-ease-out ' : 'opacity-0'}" alt="">

            <img src={Fleur} class="w-[25px] absolute -top-38 left-45 z-5 transition-all {health <= 1 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
            <img src={Fleur} class="w-[25px] absolute -top-33 left-33 z-5 transition-all {health <= 1 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
            <img src={Fleur} class="w-[25px] absolute -top-29 left-55 z-5 transition-all {health == 0 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">

            <img src={Fleur} class="w-[25px] absolute -top-28 left-72 z-5 transition-all {health <= 1 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
            <img src={Fleur} class="w-[25px] absolute -top-22 left-55 z-5 transition-all {health == 0 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">

            <img src={Fleur} class="w-[25px] absolute -top-5 left-22 z-5 transition-all {health <= 1 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
            <img src={Fleur} class="w-[25px] absolute -top-10 left-43 z-5 transition-all  {health == 0 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
            <img src={Fleur} class="w-[25px] absolute -top-14 left-35 z-5 transition-all  {health == 0 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">

    
        </div>
    </div>

    <div class="col-start-1 col-span-2 row-start-2 mt-10">
        <Separator class="mb-4"></Separator>
    </div>
</div>