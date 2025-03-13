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

    import GraphCalc from "$lib/assets/graphs.png"
    
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
    let maxMoisture:number = 50

    let moisture:number[] = $state([10])
    let moistureTemp:number[] = $state([10])

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

    let dataAPI:APIEntretien = $state({})

    $effect(() => {
        soil;root;pot;moisture
        load = true
        fetch(`http://127.0.0.1:8000/parametres_sol?sol=${soil}&racine=${root}&taille_pot=${pot}&humidity=${moisture}`)
        .then(response => response.json())
        .then(data => dataAPI = data);
    })

    $effect(() => {
        console.log(dataAPI)
        dataAPI;
        load = false;
    })

    function setPotClass(pot:string, z:number) {
        if (pot == "M") return `transition-all w-[150px] absolute top-0 left-6 z-${z}`
        else if (pot == "L") return `transition-all w-[175px] absolute top-0 left-3 z-${z}`
        else return `transition-all w-[200px] absolute top-0 left-0 z-${z}`
    }

    function setRootsClass(root:string) {
        if (root == "superficielles") return "transition-all w-[67px] absolute -top-9 left-16.5 z-3"
        else if (root == "moyennes") return "transition-all w-[67px] absolute -top-6 left-16.5 z-3"
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
    <div class="col-start-1 row-start-1 row-span-2">
        <div class="w-[300px]">
            <div class="mb-5">
                <div class="font-bold text-xl">Caractéristiques de la plante</div>
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
            <rect stroke="#EBDC94" fill="#EBDC94" height="200" width="200"></rect>
        </svg>

        <img src={Tree} class="w-[200px] absolute -top-46 left-0 z-5" alt="">
        <img src={Roots} class={setRootsClass(root)} alt="">

    </div>

    <div class="col-start-2 row-start-2 text-start mb-[44px]">
        {#if dataAPI.volume_a_arroser != 0}
            <div class="text-xl font-semibold">Arrosez !</div>
            {dataAPI.volume_a_arroser} litres est le volume optimal pour arroser votre plante. 
        {:else}
            <div class="text-xl font-semibold">Pas besoin d'aroser !</div>
            Votre plante a un niveau d'eau déjà suffisant.
        {/if}
    </div>

    <div class="col-start-1 col-span-2 row-start-3 my-5">
        <Separator class="mb-4 bg-gray-950 px-100"></Separator>
    </div>

    <div class="col-start-1 col-span-2 row-start-4 text-justify">
        <div class="text-2xl font-bold mb-3">Notre outil vous accompagne pour votre entretien de plantes</div>

        <div>
            Vous ne savez jamais quelle quantité d’eau donner à vos plantes ? Vous avez peur de les noyer ou alors peur de leur donner pas assez d’eau ? <span class="font-bold">Notre outil de prédiction est la pour vous aider !</span> Il permet d’arroser avec précision pour ne plus jamais avoir de mauvaises surprises ! 

            <br><br>

            Pour des plantes d’intérieur comme d’extérieur, <span class="font-bold">allant de la petite Monstera au Bougainvillier</span> nous vous indiquons la quantité d’eau que la plante a besoin afin de lui offrir la meilleure croissance possible. 
        </div>

        <div class="text-2xl font-bold mb-3 mt-5">Les paramètres pris en compte pour nos calculs </div>

        <div>
            Sur notre outil vous pouvez renseigner : 
            
            <br><br>

            • <span class="font-bold">Le type de sol :</span> Argileux, limoneux ou sableux, du moins poreux au plus poreux, c’est à dire d’une forte capacité à retenir l’eau à une faible capacité à retenir l’eau et à forte capacité à laisser passer l’air.<br>
            • <span class="font-bold">Le type de racine :</span> Superficielles, moyennes ou profondes, elles dépendent de l’espèce et de l’âge de la plante. Des racines superficielles auront besoin d’être arrosées plus souvent tandis que des profondes auront une meilleure capacité à résister aux sécheresses et donc aux périodes longues sans arrosage.<br>
            • <span class="font-bold">La taille du pot :</span> Prend en compte le volume du pot <br> 
            • <span class="font-bold">Le taux d’humidité du sol :</span> A l'aide d’une sonde vous pouvez simplement obtenir le taux d’humidité et ainsi l’intégrer à notre calcul.

            <br><br>

            Prenons l’exemple du <span class="font-bold">Bougainvillier </span> :

            <br><br>

            Cette plante majoritairement en extérieur peut venir aussi fleurir vos intérieurs, pour cela nous sélectionnons comme sol, le limon, pour les racines, des racines superficielles car il possède des racines peu profonds et étendues. Concernant l’environnement les bougainvillier sont vendus dans des pots XL. Vous pouvez à présent mesurer dans votre pot le taux d’humidité et obtenir le volume d’arrosage conseillé ! 

        </div>

        <div class="text-2xl font-bold mb-3 mt-5">Pour aller plus loin</div>

        <div>
            Pour comprendre la différence d’arrosage entre les types de sol et les types de racine, vous retrouvez ci dessous les optimums hydrométriques. En X on retrouve le type de sol et en Y le % d’eau présent dans le pot en fonction de la masse volumique.

            <img src={GraphCalc} alt="" class="mt-3 rounded-md">
        </div>


    </div>
</div>