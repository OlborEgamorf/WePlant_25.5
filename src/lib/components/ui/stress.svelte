<script lang="ts">
    import Results from "$lib/components/ui/results.svelte";
    import Separator from "./separator/separator.svelte";
    import Slider from "./slider/slider.svelte";

    let soils:Selects[] = [
        {value:"clay", label:"Argile"},
        {value:"sand", label:"Sable"},
        {value:"loam", label:"Terre"}
    ]

    let pots:Selects[] = [
        {value:"5l", label:"5 Litres"},
        {value:"50l", label:"50 Litres"},
        {value:"100l", label:"100 Litres"}
    ]

    let roots:Selects[] = [
        {value:"short", label:"Racines courtes"},
        {value:"medium", label:"Racines moyennes"},
        {value:"long", label:"Racines longues"},
    ]

    let soil:Selected = $state({value:"loam", label:"Terre", disabled:false})

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
                <div class="font-bold text-xl">Paramètres obligatoires</div>
                <div>Ces caractéristiques concernent la vie de la plante et de kjq...</div>
            </div>
            
            <div class="mb-3">
                <div class="mb-2 font-semibold">Taux d'humidité - {moistureTemp} %</div>
                <Slider bind:value={moistureTemp} min={minMoisture} max={maxMoisture} step={1} class="w-[180px]" />
            </div>

            <div>
                <div class="mb-2 font-semibold">Température - {moistureTemp}°C</div>
                <Slider bind:value={moistureTemp} min={minMoisture} max={maxMoisture} step={1} class="w-[180px]" />
            </div>
            
            <Separator class="my-4 bg-gray-950" />

            <div class="mb-5">
                <div class="font-bold text-xl">Paramètres optionnels</div>
                <div>Ces caractéristiques concernent la vie de la plante et de kjq...</div>
            </div>

            <div class="mb-3">
                <div class="mb-2 font-semibold">Taux de phosphore - {moistureTemp} %</div>
                <Slider min={minMoisture} max={maxMoisture} step={1} class="w-[180px]" />
            </div>

            <div class="mb-3">
                <div class="mb-2 font-semibold">Taux de nitrogène - {moistureTemp} %</div>
                <Slider min={minMoisture} max={maxMoisture} step={1} class="w-[180px]" />
            </div>

            <div>
                <div class="mb-2 font-semibold">Taux de potassium - {moistureTemp} %</div>
                <Slider min={minMoisture} max={maxMoisture} step={1} class="w-[180px]" />
            </div>
        </div>
    </div>

    <div class="col-start-2 row-start-1 row-span-2">
        <Results></Results>
    </div>
</div>