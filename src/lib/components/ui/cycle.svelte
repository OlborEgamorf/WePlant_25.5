<script lang="ts">
    import Pot from "$lib/assets/pot.svg";
    import PotClay from "$lib/assets/potClay.svg";
    import PotClayTop from "$lib/assets/potClayTop.svg";
    import PotLoam from "$lib/assets/potLoam.svg";
    import PotLoamTop from "$lib/assets/potLoamTop.svg";
    import PotSand from "$lib/assets/potSand.svg";
    import PotSandTop from "$lib/assets/potSandTop.svg";
    import Roots from "$lib/assets/roots.svg";
    import Tree from "$lib/assets/tree.svg";
    import ClayIcon from "$lib/assets/argile.svg";
    import SandIcon from "$lib/assets/sable.svg";
    import LoamIcon from "$lib/assets/terre.svg";
    
    import Separator from "./separator/separator.svelte";
    import Slider from "./slider/slider.svelte";
    import Toggle from "./toggle.svelte";
    import Loading from "./loading.svelte";

    let soils:Selects[] = [
        {value:"loam", label:"Limon"},
        {value:"clay", label:"Argile"},
        {value:"sand", label:"Sable"},
    ]

    let pots:Selects[] = [
        {value:"M", label:"M"},
        {value:"L", label:"L"},
        {value:"XL", label:"XL"}
    ]

    let roots:Selects[] = [
        {value:"superficielles", label:"Superficielles"},
        {value:"moyennes", label:"Moyennes"},
        {value:"profondes", label:"Profondes"},
    ]

    let soil:string = $state("loam")
    let root:string = $state("profondes")
    let pot:string = $state("M")

    let minMoisture:number = 0
    let maxMoisture:number = 100

    let moisture:number[] = $state([50])
    let moistureTemp:number[] = $state([50])

    let incr:number = 0
    let change:boolean= $state(false)
    let load:boolean = $state(false)

    $effect(() => {
        moistureTemp;
        let i = ++incr
        change = true
        const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
        sleep(700).then(() => {
            if (i == incr) {
                moisture = moistureTemp
                incr = 0
                change = false
            }
        })
    })

    let dataAPI = $state({})

    $effect(() => {
        soil;root;pot;moisture
        load = true
        fetch(`http://127.0.0.1:8000/parametres_sol?sol=${soil}&racine=${root}&taille_pot=${pot}&humidity=${moisture}`)
        .then(response => response.json())
        .then(data => dataAPI = data);
    })

    $effect(() => {
        dataAPI;
        load = false;
    })

    function setPotClass(pot:string, z:number) {
        if (pot == "5l") return `transition-all w-[150px] absolute top-0 left-6 z-${z}`
        else if (pot == "50l") return `transition-all w-[175px] absolute top-0 left-3 z-${z}`
        else return `transition-all w-[200px] absolute top-0 left-0 z-${z}`
    }

    function setRootsClass(root:string) {
        if (root == "short") return "transition-all w-[67px] absolute -top-9 left-16.5 z-3"
        else if (root == "medium") return "transition-all w-[67px] absolute -top-6 left-16.5 z-3"
        else return "transition-all w-[67px] absolute -top-0 left-16.5 z-3"
    }

    function setSoilSrc(soil:string) {
        if (soil == "loam") return PotLoam
        else if (soil == "sand") return PotSand
        else return PotClay
    }

    function setSoilTopSrc(soil:string) {
        if (soil == "loam") return PotLoamTop
        else if (soil == "sand") return PotSandTop
        else return PotClayTop
    }

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
                <Toggle bind:selected={soil} params={soils} image={[LoamIcon,ClayIcon,SandIcon]}></Toggle>
            </div>
        
            <div>
                <div class="mb-1 font-semibold">Type de racines</div>
                <Toggle bind:selected={root} params={roots}></Toggle>
            </div>

            <Separator class="my-4 bg-gray-950" />

            <div class="mb-5">
                <div class="font-bold text-xl">Caractéristiques du pot</div>
                <div>Ces caractéristiques concernent la vie de la plante et de kjq...</div>
            </div>

            <div class="mb-3">
                <div class="mb-2 font-semibold">Taille de pot</div>
                <Toggle bind:selected={pot} params={pots}></Toggle>
            </div>
            
            <div class="mb-5">
                <div class="mb-2 font-semibold">Taux d'humidité - {moistureTemp} %</div>
                <Slider bind:value={moistureTemp} min={minMoisture} max={maxMoisture} step={1} class="w-[180px]" />
            </div>

            <Loading {change} {load}></Loading>
            
        </div>
    </div>

    <div class="col-start-2 row-start-1 row-span-2 relative transition-all">

        <img src={setSoilTopSrc(soil)} class={setPotClass(pot, 6)}  alt="">

        <img src={Pot} class={setPotClass(pot, 6)} alt="">

        <img src={setSoilSrc(soil)} class={setPotClass(pot, 6)} alt="">
        
        <svg class="absolute -top-37 z-4">
            <rect stroke="#ACE1AF" fill="#ACE1AF" height="200" width="200"></rect>
        </svg>

        <img src={Tree} class="w-[200px] absolute -top-46 left-0 z-5" alt="">
        <img src={Roots} class={setRootsClass(root)} alt="">

    </div>

    <div class="col-start-1 col-span-2 row-start-2 mt-5">
        <Separator class="mb-4 bg-gray-950 px-100"></Separator>
    </div>
</div>