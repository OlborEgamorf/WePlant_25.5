<script lang="ts">
    import Separator from "./separator/separator.svelte";
    import Slider from "./slider/slider.svelte";

    import Banzai from "$lib/assets/banzai.svg"
    import Eclair2 from "$lib/assets/thunder.svg"
    import Fleur from "$lib/assets/flower.svg"
    import Loading from "./loading.svelte";

    import Evapo from "$lib/assets/explore/evapo.png"

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
    let load:boolean = $state(false)

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
        load = true
        fetch(`http://127.0.0.1:8000/stress_hydrique?soil_moisture=${moisture}&soil_temperature=${temperature}&nitrogen_level=${nitro}&phosphorus_level=${phosphore}&potassium_level=${potassisum}`)
        .then(response => response.json())
        .then(data => dataAPI = data);
    })

    $effect(() => {
        dataAPI;
        load = false;
    })

</script>

<div class="grid mx-10 my-10 lg:mx-75 items-center grid-cols-2 gap-x-10">
    <div class="col-start-1 row-start-1 row-span-2">
        <div class="w-[300px]">
            <div class="mb-5">
                <div class="font-bold text-xl">Paramètres obligatoires</div>
                <div>L'humidité et la température sont primordiaux pour les calculs...</div>
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
                <div>...alors que le phosphore, le nitrogène et le potassium ont un impact différent.</div>
            </div>

            <div class="mb-3">
                <div class="mb-2 font-semibold">Taux de phosphore - {phosphoreTemp} mg/kg</div>
                <Slider bind:value={phosphoreTemp} min={minPhosphore} max={maxPhosphore} step={1} class="w-[180px]" />
            </div>

            <div class="mb-3">
                <div class="mb-2 font-semibold">Taux de nitrogène - {nitroTemp} mg/kg</div>
                <Slider bind:value={nitroTemp} min={minNitro} max={maxNitro} step={1} class="w-[180px]" />
            </div>

            <div class="mb-5">
                <div class="mb-2 font-semibold">Taux de potassium - {potassisumTemp} mg/kg</div>
                <Slider bind:value={potassisumTemp} min={minPotassium} max={maxPotassium} step={1} class="w-[180px]" />
            </div>

            <Loading {change} {load}></Loading>
        </div>
    </div>

        
    <div class="col-start-2 row-start-1 row-span-2 relative transition-all">
        <img src={Banzai} class="w-[300px] absolute -top-47 left-15 z-5" alt="">

        <img src={Eclair2} class="w-[40px] absolute -top-32 left-20 z-5 transition-all {health >= 1 ? 'animate-bounce animate-infinite animate-duration-[2000ms] animate-ease-out' : 'opacity-0'}" alt="">
        <img src={Eclair2} class="w-[40px] absolute -top-47 left-70 z-5 transition-all {health >= 1 ? 'animate-bounce animate-infinite animate-duration-[2000ms] animate-ease-out ' : 'opacity-0'}" alt="">

        <img src={Eclair2} class="w-[40px] absolute -top-7 left-72 z-5 transition-all {health == 2 ? 'animate-bounce animate-infinite animate-duration-[2000ms] animate-ease-out ' : 'opacity-0'}" alt="">
        <img src={Eclair2} class="w-[40px] absolute -top-57 left-42 z-5 transition-all {health == 2 ? 'animate-bounce animate-infinite animate-duration-[2000ms] animate-ease-out ' : 'opacity-0'}" alt="">

        <img src={Fleur} class="w-[25px] absolute -top-45 left-45 z-5 transition-all {health <= 1 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
        <img src={Fleur} class="w-[25px] absolute -top-40 left-33 z-5 transition-all {health <= 1 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
        <img src={Fleur} class="w-[25px] absolute -top-36 left-55 z-5 transition-all {health == 0 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">

        <img src={Fleur} class="w-[25px] absolute -top-35 left-72 z-5 transition-all {health <= 1 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
        <img src={Fleur} class="w-[25px] absolute -top-29 left-55 z-5 transition-all {health == 0 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">

        <img src={Fleur} class="w-[25px] absolute -top-12 left-22 z-5 transition-all {health <= 1 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
        <img src={Fleur} class="w-[25px] absolute -top-17 left-43 z-5 transition-all  {health == 0 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
        <img src={Fleur} class="w-[25px] absolute -top-21 left-35 z-5 transition-all  {health == 0 ? 'animate-spin animate-infinite animate-duration-[12000ms]' : 'opacity-0'}" alt="">
    </div>

    <div class="col-start-2 row-start-2 text-start mb-[44px]">
        {#if health == 0}
            <div class="text-xl font-semibold">Etat : En bonne santé !</div>
            La plante est dans des conditions optimales pour son développement.
        {:else if health == 1}
            <div class="text-xl font-semibold">Etat : Stress modéré.</div>
            La plante commence à se restreindre par manque d'eau.
        {:else}
            <div class="text-xl font-semibold">Etat : Stress élevé.</div>
            Le manque d'eau est trop important la plante stoppe sa croissance et limite toutes ses interactions.
        {/if}
    </div>

    <div class="col-start-1 col-span-2 row-start-3 my-5">
        <Separator class="mb-4 bg-gray-950 px-100"></Separator>
    </div>

    <div class="col-start-1 col-span-2 row-start-4 text-justify">

        <div class="text-2xl font-bold mb-3">Introduction</div>
        <div>
            Revenons sur la problématique de notre <span class="font-bold">bougainvillier</span> rachitique vu en introduction du sujet. Celui ci est face à un problème l’empêchant de se développer ; pire, l’empêchant de survivre. Sous <span class="font-bold">la chaleur et la sécheresse</span>, il n’y a pas que vous qui souffrez et qui transpirez, mais les plantes aussi. La différence entre cette plante et vous est que, malgré votre transpiration, vous avez accès à la ressource qui fait la vie depuis la nuit des temps : <span class="font-bold">l’eau</span>. 
            <br><br>
	        Comme les humains, les plantes boivent cette eau, en l’absorbant par leurs <span class="font-bold">racines</span>. Pour cela, il faut qu’elles aient accès à de l’eau présente dans le sol dans lequel elles vivent. Cette eau reste accessible plus ou moins bien en fonction du sol qu’elle traverse : elle restera abondement dans de l’argile et s’écoulera rapidement dans du sable. 
            <br><br>
	        Nos bougainvilliers fleuris et chatoyants ont eux accès à une réserve d’eau satisfaisant leurs besoins et régulant immédiatement la <span class="font-bold">perte d’eau</span> due à la transpiration. En revanche, le bougainvillier esseulé n’a pas cette chance... Il n’a pas accès à assez d’eau pour pouvoir <span class="font-bold">se développer</span> et <span class="font-bold">survivre</span>. Ce concept de régulation entre la transpiration et l’absorption de l’eau se nomme <span class="font-bold italic">le stress hydrique</span>.
        </div>

        <div class="text-2xl font-bold mb-3 mt-5">Le stress hydrique</div>
        <div>
            Le stress hydrique chez les plantes survient lorsque l’eau disponible dans le sol devient insuffisante pour répondre à leurs <span class="font-bold">besoins</span>. Ce manque d’eau perturbe le transport des <span class="font-bold">nutriments</span> et la <span class="font-bold">photosynthèse</span>, entraînant un ralentissement de la croissance. En conséquence, les feuilles se flétrissent et les stomates (petits pores à la surface des feuilles) se ferment pour limiter <span class="font-bold">l’évaporation</span>. Cependant, cette fermeture empêche aussi l’absorption du CO₂ nécessaire à la photosynthèse, ce qui affaiblit encore la plante. Si le stress persiste, il peut causer des <span class="font-bold">dommages irréversibles</span> et même <span class="font-bold underline">la mort</span> de la plante. 
        </div>

        <div class="text-2xl font-bold mb-3 mt-5">Pour aller plus loin : l'évapotranspiration</div>

        <div class="flex">
            <div>
                Pour la régulation de la plante il faut prendre deux paramètres en compte : 
                <br><br>
                • le premier est <span class="font-bold">l’humidité</span> présente dans le sol abritant la plante. Cette humidité va imager la ressource en eau disponible pour la plante en question.<br>
                • le deuxième paramètre se base sur la <span class="font-bold">transpiration</span> de la plante.
                <br><br>
                Le rapport entre ces deux paramètres décrit un phénomène assez impressionnant et intéressant. Ce phénomène permet à la plante de tirer un avantage de sa transpiration, c’est <span class="font-bold italic">l’évapotranspiration</span>. L’évapotranspiration désigne l'ensemble des processus par lesquels l'eau est transférée de la surface de la Terre vers l'atmosphère. Pour faire simple, elle aide les plantes à <span class="font-bold">réguler</span> leur température et à maintenir un <span class="font-bold">équilibre hydrique</span>. La transpiration, qui fait partie de ce processus, permet aux plantes d'absorber de l'eau et des nutriments du sol tout en évacuant l'excès de chaleur. Cela favorise leur croissance et leur développement tout en empêchant un <span class="font-bold">stress thermique ou hydrique</span>. 
            </div>

            <img src={Evapo} alt="" class="w-[375px] h-[375px] rounded-md ml-5">
        </div>

        <div class="text-2xl font-bold mb-3 mt-5">Utilisation de l’outil : Prédiction de stress hydrique</div>

        <div>
            L’outil ci dessus présente le stress hydrique chez une plante. Celui ci dépend des caractéristiques modélisées par nos soins et présentes dans l’environnement de votre plante : <br><br>
            • <span class="font-bold">l’humidité du sol :</span> ce paramètre relève de la proportion d’eau présente dans le sol en pourcentage. <br>
            • <span class="font-bold">la température du sol (°C) :</span> représente la température proche des racines de la plante. <br>
            • <span class="font-bold">le niveau d’azote (mg/kg) :</span> ce paramètre est un nutriment essentiel pour le développement des plantes. <br>
            • <span class="font-bold">le niveau de phosphore (mg/kg) :</span> ce paramètre est un nutriment essentiel pour le développement des racines. <br>
            • <span class="font-bold">le niveau de potassium (mg/kg) :</span> ce paramètre est un nutriment augmentant la résistance des plantes.

    C’est la combinaison de ces paramètres qui nous donne l’état de santé de la plante liée au stress.
        </div>

    </div>
</div>