<script lang="ts">

    import * as Select from "$lib/components/ui/select/index.js";
    import { Slider } from "$lib/components/ui/slider/index.js";

    let { light = $bindable(), moisture = $bindable(), temperture = $bindable(), soil = $bindable() } = $props();

    type Selects = {
        value:string,
        label:string
    }

    let soils:Selects[] = [
        {value:"clay", label:"Argile"},
        {value:"sand", label:"Sable"},
        {value:"loam", label:"Terre"}
    ]

    let roots:Selects[] = [
        {value:"short", label:"Racines courtes"},
        {value:"medium", label:"Racines moyennes"},
        {value:"long", label:"Racines longues"},
    ]

    let minLight:number = 0
    let minMoisture:number = 0
    let minTemperture:number = 0 

    let maxLight:number = 100
    let maxMoisture:number = 100
    let maxTemperture:number = 35

    let duration:number = 1000
    let incr:number = 0

    let lightTemp:number[] = $state([50])
    let moistureTemp:number[] = $state([50])
    let tempertureTemp:number[] = $state([20])

    $effect(() => {
        lightTemp; moistureTemp; tempertureTemp;
        let i = ++incr
        const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
        sleep(1000).then(() => {
            if (i == incr) {
                light = lightTemp
                moisture = moistureTemp
                temperture = tempertureTemp
            }
        })
    })


</script>

<div class="w-[300px]">
    <div class="mb-5">
        <div class="font-bold text-xl">Caractéristiques de la plante</div>
        <div>Ces caractéristiques concernent la vie de la plante et de kjq...</div>
    </div>

    <div class="mb-3">
        <div class="mb-1 font-semibold">Choix du sol</div>
        <Select.Root portal={null} bind:selected={soil}>
            <Select.Trigger class="w-[180px] bg-[#ACE1AF] border-2 border-gray-950">
              <Select.Value placeholder="Choisir un sol" />
            </Select.Trigger>
            <Select.Content>
              <Select.Group>
                <Select.Label>Sols</Select.Label>
                {#each soils as soil}
                  <Select.Item value={soil.value} label={soil.label}
                    >{soil.label}</Select.Item
                  >
                {/each}
              </Select.Group>
            </Select.Content>
            <Select.Input name="favoriteFruit" />
          </Select.Root>
    </div>

    <div>
        <div class="mb-1 font-semibold">Type de racines</div>
        <Select.Root portal={null}>
            <Select.Trigger class="w-[180px] bg-[#ACE1AF] border-2 border-gray-950">
              <Select.Value placeholder="Choisir une racine" />
            </Select.Trigger>
            <Select.Content>
              <Select.Group>
                <Select.Label>Racines</Select.Label>
                {#each roots as root}
                  <Select.Item value={root.value} label={root.label} 
                    >{root.label}</Select.Item
                  >
                {/each}
              </Select.Group>
            </Select.Content>
            <Select.Input name="favoriteFruit" />
          </Select.Root>
    </div>

    <div class="mb-5 mt-5">
        <div class="font-bold text-xl">Paramètres environnementaux</div>
        <div>L'environnement correspond aux conditions de vie de la plante...</div>
    </div>

    <div class="mb-3">
        <div class="mb-2 font-semibold">Luminosité - {lightTemp}</div>
        <Slider bind:value={lightTemp} min={minLight} max={maxLight} step={1} class="w-[180px]" />
    </div>

    <div class="mb-3">
        <div class="mb-2 font-semibold">Humidité - {moistureTemp}</div>
        <Slider bind:value={moistureTemp} min={minMoisture} max={maxMoisture} step={1} class="w-[180px]"/>
    </div>

    <div>
        <div class="mb-2 font-semibold">Température - {tempertureTemp}</div>
        <Slider bind:value={tempertureTemp} min={minTemperture} max={maxTemperture} step={1} class="w-[180px]" />
    </div>
</div>