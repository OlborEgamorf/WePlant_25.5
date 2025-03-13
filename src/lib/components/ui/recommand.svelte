<script lang="ts">
    import * as Tooltip from "$lib/components/ui/tooltip";

    import miOmbre from "$lib/assets/mi_ombre.svg";
    import ombre from "$lib/assets/ombre.svg";
    import soleil from "$lib/assets/soleil.svg";

    import arrosoire_mi_plein from "$lib/assets/Arrosoire_mi_vide.svg";
    import arrosoire_plein from "$lib/assets/Arrosoire_plein.svg";
    import arrosoire_vide from "$lib/assets/Arrosoire_vide.svg";

    import argile from "$lib/assets/argile.svg";
    import sable from "$lib/assets/sable.svg";
    import terre from "$lib/assets/terre.svg";

    import gant from "$lib/assets/gant.svg";
    import rateau from "$lib/assets/rateau.svg";
    import secateur from "$lib/assets/secateur.svg";

    import automne from "$lib/assets/automne.svg";
    import hivers from "$lib/assets/hivers.svg";
    import printemps from "$lib/assets/printemps.svg";

    import annuelles from "$lib/assets/annuelle.svg";
    import bulbes from "$lib/assets/bulbe.svg";
    import cactus from "$lib/assets/cactus.svg";
    import grimpantes from "$lib/assets/climbing.svg";
    import herbes from "$lib/assets/herb.svg";
    import roses from "$lib/assets/rose.svg";
    import arbustes from "$lib/assets/treeRec.svg";
    import vivaces from "$lib/assets/vivaces.svg";

    import Input from "./input/input.svelte";
    import Selection from "./selection.svelte";
    import Separator from "./separator/separator.svelte";
    import Toggle from "./toggle.svelte";



    let soil:string = $state("Limon")
    let WaterNeed:string = $state("Moyen")
    let SunNeed:string = $state("Mi-ombre")
    let Maintenance:string = $state("Moyen")    
    let saison:Selected = $state({value:"Printemps", label:"Printemps",disabled:false})
    let categorie:Selected = $state({value:"Vivaces", label:"Vivaces",disabled:false})

    let minHeight:number = $state(20)
    let maxHeight:number = $state(60)

    let soils:Selects[] = [
        {value:"Limon", label:"Limon"},
        {value:"Argile", label:"Argile"},
        {value:"Sable", label:"Sable"},
    ]

    let WaterNeeds:Selects[] = [
        {value:"Faible", label:"Faible"},
        {value:"Moyen", label:"Moyen"},
        {value:"Elevé", label:"Elevé"},
    ]

    let SunNeeds:Selects[] = [
        {value:"Plein soleil", label:"Plein soleil"},
        {value:"Mi-ombre", label:"Mi-ombre"},
        {value:"Ombre", label:"Ombre"},
    ]

    let Maintenances:Selects[] = [
        {value:"Faible", label:"Faible"},
        {value:"Moyen", label:"Moyen"},
        {value:"Difficile", label:"Difficile"},
    ]

    let saisons:Selects[] = [
        {value:"Printemps", label:"Printemps"},
        {value:"Eté", label:"Eté"},
        {value:"Automne", label:"Automne"},
        {value:"Hiver", label:"Hiver"},
    ]

    let plant_categories:Selects[] = [
        {value:"Vivaces", label:"Vivaces"},
        {value:"Annuelles", label:"Annuelles"},
        {value:"Bulbes", label:"Bulbes"},
        {value:"Arbustes", label:"Arbustes"},
        {value:"Grimpantes", label:"Grimpantes"},
        {value:"Cactus - Succulentes", label:"Cactus"},
        {value:"Herbes", label:"Herbes"},
        {value:"Roses", label:"Roses"},
    ]
    
    let dataAPI:APIRecommandation = $state({recommendations:[], success:true, hasFailed:false, failed_criteria:[]})

    $effect(() => {
        soil;WaterNeed;SunNeed;Maintenance;saison;categorie;minHeight;maxHeight
        fetch(`http://127.0.0.1:8000/recommend?sun_needs=${SunNeed}&water_needs=${WaterNeed}&maintenance=${Maintenance}&soil=${soil}&season=${saison.value}&plant_category=${categorie.value}&min_height=${minHeight}&max_height=${maxHeight}`)
        .then(response => response.json())
        .then(data => dataAPI = data);
    })

    let recomID:string = $state("0")

    function onclickRecom(this : HTMLElement) {
        recomID = this.id
    }

    $effect(() => {
        console.log(dataAPI)
    })

    function getPlantName(name:string) {
        return name.split(" (")[0];
    }

</script>

<div class="grid mx-10 my-10 lg:mx-75  grid-cols-2 gap-x-10">
    <div class="col-start-1">
        <div class="w-[450px]">
            <div class="mb-5">
                <div class="font-bold text-xl text-justify">Recommandation</div>
                <div>Définissez les caractéristiques du futur environnement de la plante et vos critères d’entretien pour obtenir une liste de plantes idéales.</div>
            </div>
        
            <div class="mb-3">
                <div class="mb-1 font-semibold">Choix du sol</div>
                <Toggle bind:selected={soil} params={soils} image={[terre,argile,sable]} styles={"w-5 h-5"}></Toggle>
            </div>
        
            <div class="mb-3">
                <div class="mb-1 font-semibold">Besoin en eau</div>
                <Toggle bind:selected={WaterNeed} params={WaterNeeds} image={[arrosoire_vide,arrosoire_mi_plein,arrosoire_plein]} ></Toggle>
            </div>

            <div class="mb-3">
                <div class="mb-1 font-semibold">Besoin en soleil</div>
                <Toggle bind:selected={SunNeed} params={SunNeeds} image={[soleil,miOmbre,ombre]} styles={"w-5 h-5"}></Toggle>
            </div>

            <div class="mb-3">
                <div class="mb-1 font-semibold">Entretien</div>
                <Toggle bind:selected={Maintenance} params={Maintenances} image={[gant,rateau,secateur]} styles={"w-6 h-6"}></Toggle>
            </div>
            
            <div class="mb-3">
                <div class="flex">
                    <div class="mb-3">
                        <div class="mb-1 font-semibold">Saison</div>
                        <Selection bind:selected={saison} params={saisons} placeholder="Saison" image={[printemps,soleil,automne,hivers]}></Selection>
                    </div>

                    <div class="mb-3">
                        <div class="mb-1 font-semibold">Catégorie de plante</div>
                        <Selection bind:selected={categorie} params={plant_categories} placeholder="Catégorie" image={[vivaces,annuelles,bulbes,arbustes,grimpantes,cactus,herbes,roses]}></Selection>
                    </div>
                </div>
            </div>

            <div class="mb-3">
                <div class="mb-1 font-semibold">Taille (cm)</div>
                <div class="flex">
                  <div class="flex flex-col mr-4">
                    <label class="mb-1 font-medium">Minimale</label>
                    <Input  type="number" min="0" max="1000" step="1" bind:value={minHeight} class="w-[100px]" />
                  </div>
              
                  <div class="flex flex-col">
                    <label class="mb-1 font-medium">Maximale</label>
                    <Input type="number"  min="0"  max="1000" step="1" bind:value={maxHeight} class="w-[100px]"/>
                  </div>
                </div>
              </div>
              
        </div>
    </div>

    <div class="col-start-2 flex flex-col items-start">
        {#if dataAPI.hasFailed}
            <div class="text-white text-sm mt-2 m-5 bg-[#ABAA6C] p-2 rounded-md">
                <p>Attention, tous les filtres n'ont pas été appliqués !  {dataAPI.failed_criteria.join(', ')}</p>
            </div>
        {/if}
        
        <div class="w-full mx-10">
            <div class="grid grid-cols-5 gap-x-4 gap-y-5 text-zinc-700 ">
                {#each dataAPI.recommendations as plant, i}
                    <!-- svelte-ignore a11y_click_events_have_key_events -->
                    <!-- svelte-ignore a11y_no_static_element_interactions -->
                    <Tooltip.Root>
                        <Tooltip.Trigger>
                          <div
                            class="w-full aspect-[1/1] h-20 bg-[#ABAA6C] rounded-md cursor-pointer {i.toString() === recomID ? 'border-4 border-[#ABAA6C]' : ''}" id={i.toString()} on:click={onclickRecom}>
                            <img src="/src/lib/assets/flowers/{plant.id}.jpg" class="rounded-md w-full h-full object-cover"/>
                          </div>
                        </Tooltip.Trigger>
                        <Tooltip.Content>
                          <p>{getPlantName(plant.Name)}</p>
                        </Tooltip.Content>
                      </Tooltip.Root>
                      
                {/each}    
                
                <div class="col-span-3 w-60 h-60 bg-[#ABAA6C] row-start-2 rounded-md text-zinc-700">
                    {#each dataAPI.recommendations as plant, i}
                        <img src="/src/lib/assets/flowers/{plant.id}.jpg" class="rounded-md w-full h-full object-cover {i.toString() != recomID ? 'hidden' : ''}">
                    {/each}
                </div>
                {#each dataAPI.recommendations as plant, i}

                    <div class="col-span-2 row-start-2 text-lg text-zinc-700 {i.toString() != recomID ? 'hidden' : ''}">
                        <div class="mb-3">
                            <p class="font-bold">{getPlantName(plant.Name)}</p>
                            <div class="font-semibold text-sm mt-2">Caractéristiques:</div>
                            <div class="grid grid-cols-2 gap-2 text-sm ">
                                <div><strong>Soleil :</strong> {plant.SunNeeds}</div>
                                <div><strong>Arrosage :</strong> {plant.WaterNeeds}</div>
                                <div><strong>Entretien :</strong> {plant.Maintenance}</div>
                                <div><strong>Sol :</strong> {plant["Type de Sol"]}</div>
                                <div><strong>Saison :</strong> {plant.saison}</div>
                                <div><strong>Catégorie :</strong> {plant.plant_categories}</div>
                                <div class="col-span-2"><strong>Taille :</strong> {plant.min_height_cm} - {plant.max_height_cm} cm</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-span-5 row-start-3 text-justify  text-zinc-700 pb-2 {i.toString() != recomID ? 'hidden' : ''}">
                        <div class="text-base">{plant.Desc}</div>
                    </div>  
                {/each}
            </div>
        </div>
    </div>
    
    <div class="col-start-1 col-span-2 row-start-3 my-5">
        <Separator class="mb-4 bg-gray-950 px-100"></Separator>
    </div>


    <div class="col-start-1 col-span-2 row-start-4 text-justify">
        <div class="text-2xl font-bold mb-3">Un conseiller pour votre choix de plante</div>

        <div>
            Manque d’inspiration ? Peur de choisir une plante non adaptée à votre environnement ? Grâce à cet outil vous pouvez renseigner les caractéristiques futur de votre environnement et vos critères d’entretien pour avoir des bureaux fleuri toute l’année.
        </div>

        <div class="text-2xl font-bold mb-3 mt-5">Les paramètres nécessaires à la prédiction</div>
        <ul class="list-disc list-inside space-y-2">
        <li>
            <strong>Le type de sol :</strong>
            Argileux, limoneux ou sableux, du moins poreux au plus poreux, c’est-à-dire d’une forte capacité à retenir l’eau à une faible capacité à retenir l’eau et à forte capacité à laisser passer l’air.
        </li>
        <li>
            <strong>Besoin en eau :</strong>
            Faible, Moyen ou Élevé représente votre fréquence d’arrosage idéale.
        </li>
        <li>
            <strong>Besoin en soleil :</strong>
            Plein Soleil, Mi-Ombre ou Ombre, le besoin en soleil est défini par l’emplacement de la plante dans votre bureau.
        </li>
        <li>
            <strong>Entretien :</strong>
            Faible, Moyen ou Difficile, choisissez le type d’entretien idéal pour vous.
        </li>
        <li>
            <strong>Saison :</strong>
            Indique la saison de floraison de votre plante.
        </li>
        <li>
            <strong>Catégorie de plante :</strong>
            Désigne la famille ou le groupe auquel appartient votre plante : arbuste, plante vivace, plante d’intérieur...
        </li>
        <li>
            <strong>Taille minimale :</strong>
            Représente la taille adulte minimum de la plante pour la recommandation.
        </li>
        <li>
            <strong>Taille maximale :</strong>
            Représente la taille adulte maximum de la plante pour la recommandation.
        </li>
        </ul>

        <div class="col-start-1 col-span-2 row-start-3 my-5">
            <Separator class="mb-4 bg-gray-950 px-100"></Separator>
        </div>

        <div class="text-2xl font-bold mb-3 mt-5">Détails sur les catégories de plante:</div>
        Désigne la famille ou le groupe auquel appartient votre plante (arbuste, plante vivace, plante d’intérieur, etc.). On distingue notamment :
        <ul class="list-disc list-inside pl-4 mt-1 space-y-1">
        <li><strong>Vivaces</strong> : plantes qui repoussent chaque année.</li>
        <li><strong>Annuelles</strong> : plantes dont le cycle de vie ne dure qu’une saison.</li>
        <li><strong>Bulbes</strong> : plantes poussant à partir d’un bulbe (tulipes, jonquilles...).</li>
        <li><strong>Arbustes</strong> : plantes ligneuses plus petites qu’un arbre.</li>
        <li><strong>Grimpantes</strong> : plantes qui s’accrochent ou s’enroulent sur un support.</li>
        <li><strong>Cactus / Succulentes</strong> : plantes stockant l’eau dans leurs tiges ou feuilles.</li>
        <li><strong>Herbes</strong> : plantes herbacées, souvent aromatiques (basilic, ciboulette...).</li>
        <li><strong>Roses</strong> : rosiers et variétés apparentées.</li>
        </ul>

    </div>


</div>
    


    
    
    

