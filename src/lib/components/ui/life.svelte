<script lang="ts">
    import { Slider } from "$lib/components/ui/slider/index.js";
    import Toggle from "./toggle.svelte";

    import ClayIcon from "$lib/assets/argile.svg";
    import SandIcon from "$lib/assets/sable.svg";
    import LoamIcon from "$lib/assets/terre.svg";

    import Watch from "$lib/assets/watch.svg";
    import Clock from "$lib/assets/clock.svg";
    import Calendar from "$lib/assets/calendar.svg";

    import Grow1 from "$lib/assets/grow_1.svg"
    import Grow2 from "$lib/assets/grow_2.svg"
    import Grow3 from "$lib/assets/grow_3.svg"
    import Grow4 from "$lib/assets/grow_4.svg"
    import Loading from "./loading.svelte";
    import Separator from "./separator/separator.svelte";

    let animation = true

    let soils:Selects[] = [
        {value:"loam", label:"Limon"},
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
    let change:boolean= $state(false)
    let load:boolean = $state(false)

    let moisture:number[] = $state([50])
    let temperature:number[] = $state([20])
    let sun:number[] = $state([50])

    let moistureTemp:number[] = $state([50])
    let temperatureTemp:number[] = $state([20])
    let sunTemp:number[] = $state([50])

    $effect(() => {
        moistureTemp; temperatureTemp; sunTemp;
        let i = ++incr
        change = true
        const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
        sleep(700).then(() => {
            if (i == incr) {
                moisture = moistureTemp
                temperature = temperatureTemp
                sun = sunTemp
                incr = 0
                change = false
            }
        })
    })

    let dataAPI:APIPredict = $state({prediction:0})
    let predi:number = $state(-1)

    // 0 : neutral à bon
    // 1 : neutral à mauvais
    // 2 : bon à mauvais
    // 3 : mauvais à bon
    let stateAnim = $state(-1)

    $effect(() => {
        load = true
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
        load = false
    })

</script>

<div class="grid mx-10 my-10 lg:mx-75 items-center grid-cols-2 gap-x-10">
    <div class="col-start-1 row-start-1 row-span-2">
        <div class="w-[420px]">
            <div class="mb-5">
                <div class="font-bold text-xl">Paramètres de l'environnement</div>
                <div>L'environnement donné va pouvoir déterminer si la plante poussera ou non.</div>
            </div>
        
            <div class="mb-3">
                <div class="mb-1 font-semibold">Choix du sol</div>
                <Toggle bind:selected={soil} params={soils} image={[LoamIcon,ClayIcon,SandIcon]}></Toggle>
                <!-- <Selection params={soils} placeholder={"Choisir un sol"}></Selection> -->
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

            <div class="mb-5">
                <div class="mb-2 font-semibold">Fréquence d'arosage</div>
                <Toggle bind:selected={waterNeed} params={water} image={[Watch,Clock,Calendar]} styles={"w-6 h-6"}></Toggle>
            </div>

            <Loading {change} {load}></Loading>

            
        </div>
    </div>

    <div class="col-start-2 row-start-1 row-span-2 relative transition-all">
            

        {#if stateAnim == -1}
            <img src={Grow3} class="transition-all w-[200px] absolute -top-31 left-27 z-5" alt="">
        {:else if stateAnim == 0}
            <img src={Grow3} class="transition-all w-[200px] absolute -top-31 left-27 z-5 animate-fade animate-once animate-duration-1000 animate-delay-250 animate-reverse" alt="">
            <img src={Grow4} class="transition-all w-[200px] absolute -top-58.5 left-27 z-5 animate-fade animate-once animate-duration-1000 animate-delay-750 animate-normal" alt="">
        {:else if stateAnim == 1}
            <img src={Grow3} class="transition-all w-[200px] absolute -top-31 left-27 z-5 animate-fade animate-once animate-duration-1000 animate-delay-250 animate-reverse" alt="">
            <img src={Grow1} class="transition-all w-[200px] absolute -top-31 left-27 z-5 animate-fade animate-once animate-duration-1000 animate-delay-750 animate-normal" alt="">
        {:else if stateAnim == 2}
            <img src={Grow4} class="transition-all w-[200px] absolute -top-58.5 left-27 z-5 animate-fade animate-once animate-duration-1000 animate-delay-250 animate-reverse" alt="">
            <img src={Grow1} class="transition-all w-[200px] absolute -top-31 left-27 z-5 animate-fade animate-once animate-duration-1000 animate-delay-750 animate-normal" alt="">
        {:else if stateAnim == 3}
            <img src={Grow1} class="transition-all w-[200px] absolute -top-31 left-27 z-5 animate-fade animate-once animate-duration-1000 animate-delay-250 animate-reverse" alt="">
            <img src={Grow4} class="transition-all w-[200px] absolute -top-58.5 left-27 z-5 animate-fade animate-once animate-duration-1000 animate-delay-750 animate-normal" alt="">
        {/if}           

    </div>

    <div class="col-start-2 row-start-2 text-start mb-[44px]">
        {#if predi == 0}
            <div class="text-xl font-semibold">🥵 La croissance de la plante est insuffisante.</div>
            Les conditions actuelles pourraient être optimisées en ajustant l’arrosage, l’exposition à la lumière, la température du sol ou le niveau d'humidité.
        {:else if predi == 1}
            <div class="text-xl font-semibold">🌱✨ La plante se développe sainement !</div>
            Les conditions environnementales et les soins apportés sont favorables à une croissance optimale.
        {/if}
    </div>

    <div class="col-start-1 col-span-2 row-start-3 my-5">
        <Separator class="mb-4 bg-gray-950 px-100"></Separator>
    </div>

    <div class="col-start-1 col-span-2 row-start-4 text-justify">
        <div class="text-2xl font-bold mb-3">Introduction</div>
        <div>
            Revenons dans le sud de la France avec nos deux amis les bougainvilliers.  L’un est splendide, couvert de fleurs colorées, tandis que l’autre semble fragile, ses feuilles sont fanées et ses branches éparpillées. <span class="font-bold">Pourquoi une telle différence ?</span> La réponse se trouve dans le cycle de vie des plantes et les conditions dont elles ont besoin pour s’épanouir.
            
            <br><br>

            Comme tous les êtres vivants, les plantes passent par plusieurs étapes avant d’atteindre leur plein développement. Tout commence avec la germination : sous l’effet de l’humidité et de la chaleur, la graine se réveille et commence à germer. Les premières racines et feuilles apparaissent permettant à la jeune plante d’absorber l’eau, les nutriments et la lumière du soleil pour produire son énergie. Peu à peu, elle renforce ses tiges et développe son feuillage. Puis vient la floraison, le moment où elle s’épanouit pleinement et embellit son environnement.
        </div>

        <div class="text-2xl font-bold mb-3 mt-5">Comment favoriser une croissance équilibrée et durable ?</div>

        <div>
            Pour bien grandir, une plante a besoin de plusieurs éléments essentiels : <span class="font-bold">l’eau</span>, <span class="font-bold">la lumière</span>, un <span class="font-bold">sol adapté</span> et un <span class="font-bold">climat favorable</span>. Si elle manque d’eau, elle se dessèche et peine à se nourrir. Si elle ne reçoit pas assez de lumière, elle n’a pas assez d’énergie pour se développer. La nature du sol est aussi importante : il doit retenir l’humidité sans être trop compact pour un bon développement des racines. Enfin, la température et l’humidité de l’air doivent être adaptées à ses besoins, car des changements brusques peuvent perturber sa croissance.
        </div>

        <div class="text-2xl font-bold mb-3 mt-5">Les secrets d’un bougainvillier épanoui : adapter son environnement pour réussir</div>

        <div>
            Dans notre jardin, le <span class="font-bold">bougainvillier</span> en difficulté n’a pas toutes ces bonnes conditions. Son sol ne garde pas assez d’humidité, le soleil brûle la plante, et il y a un manque de ressources pour la croissance de la plante. 
            <br><br>
            Comprendre ces étapes permet d’expliquer pourquoi certaines plantes s’épanouissent mieux que d’autres. En ajustant les conditions de croissance, comme <span class="font-bold">l’arrosage</span>, <span class="font-bold">l’exposition au soleil</span>, <span class="font-bold">le type de sol</span> ou en ajustant la <span class="font-bold">température</span> et <span class="font-bold">l’humidité</span>. Il est possible de créer un environnement optimal pour les plantes. 
        </div>

        <div class="text-2xl font-bold mb-3 mt-5">Utilisation de l’outil : Prédiction de croissance</div>

        <div>
            Cet outil vous permet de simuler la croissance de votre plante en fonction de différents paramètres environnementaux :
            <br><br>
                • <span class="font-bold">Type de sol :</span> Composition du sol dans lequel la plante évolue, comprenant le sable, le limon ou l’argile.<br>
                • <span class="font-bold">Humidité :</span> Taux d'humidité de l’air autour de la plante.<br>
                • <span class="font-bold">Température :</span> Niveau de chaleur du sol dans lequel la plante se développe.<br>
                • <span class="font-bold">Exposition au Soleil :</span> Durée et intensité de l’exposition de la plante à la lumière du soleil. <br>
                • <span class="font-bold">Fréquence d’arrosage :</span> Quotidien, semi-hebdomadaire ou hebdomadaire.
            <br><br>
            En fonction des paramètres sélectionnés, la plante pourra être en pleine croissance ou, au contraire, présenter une croissance insuffisante.
        </div>
    </div>

</div>