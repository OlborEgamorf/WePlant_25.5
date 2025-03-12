<script lang="ts">
    import Results from "$lib/components/ui/results.svelte";
    import Separator from "./separator/separator.svelte";
    import Slider from "./slider/slider.svelte";

    import Banzai from "$lib/assets/banzai.svg"

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

    $effect(() => {
        moistureTemp;temperatureTemp;phosphoreTemp;nitroTemp;potassisumTemp;
        let i = ++incr
        const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
        sleep(700).then(() => {
            if (i == incr) {
                moisture = moistureTemp
                temperature = temperatureTemp
                phosphore = phosphoreTemp
                nitro = nitroTemp
                potassisum = potassisumTemp
                incr = 0
            }
        })
    })

    let dataAPI = $state({})

    $effect(() => {
        moisture;temperature;phosphore;nitro;potassisum;
        fetch(`http://127.0.0.1:8000/stress_hydrique?soil_moisture=${moisture}&soil_temperature=${temperature}&nitrogen_level=${nitro}&phosphorus_level=${phosphore}&potassium_level=${potassisum}`)
        .then(response => response.json())
        .then(data => dataAPI = data);
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


    
            <img src={Banzai} class="w-[300px] absolute top-0 left-0 z-5" alt="">

    
        </div>
    </div>

    <div class="col-start-1 col-span-2 row-start-2 mt-10">
        <Separator class="mb-4"></Separator>
    </div>
</div>