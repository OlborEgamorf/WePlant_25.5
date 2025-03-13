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
                <div class="font-bold text-xl">Recommandation</div>
                <div>Découvrez nos recommandations personnalisées de 5 plantes pour sublimer vos bureaux selon vos critères !</div>
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

            <div class = "mb-3">
                <div class="mb-1 font-semibold">Taille (cm)</div>
                <div class = "flex">
                    <Input type="number" min="0" max="1000" step="1" bind:value={minHeight} class="w-[100px]"></Input>
                    <Input type="number" min="0" max="1000" step="1" bind:value={maxHeight} class="w-[100px]"></Input>
                </div>
            </div>  
        </div>
    </div>

    <div class="col-start-2 flex flex-col items-start">
        {#if dataAPI.hasFailed}
            <div class="text-red-500 text-sm mt-2 m-5 bg-red-100 p-2 rounded-md">
                <p>Attention, tous les filtres n'ont pas été appliqués !</p>
                <p class="mt-2">{dataAPI.failed_criteria.join(', ')}</p>
            </div>
        {/if}
        
        <div class="w-full mx-10">
            <div class="grid grid-cols-5 gap-x-4 gap-y-10 text-zinc-700 ">
                {#each dataAPI.recommendations as plant, i}
                    <!-- svelte-ignore a11y_click_events_have_key_events -->
                    <!-- svelte-ignore a11y_no_static_element_interactions -->
                    <Tooltip.Root>
                        <Tooltip.Trigger><div class="w-full aspect-[1/1] h-20 bg-red-500 rounded-md" id={i.toString()} onclick={onclickRecom}></div></Tooltip.Trigger>
                        <Tooltip.Content>
                          <p>{getPlantName(plant.Name)}</p>
                        </Tooltip.Content>
                      </Tooltip.Root>
                {/each}    
                
                <div class="col-span-3 w-60 h-60 bg-red-500 row-start-2 rounded-md text-zinc-700"></div>
                {#each dataAPI.recommendations as plant, i}

                    <div class="col-span-2 row-start-2 text-lg text-zinc-700 {i.toString() != recomID ? 'hidden' : ''}">
                        <div class="mb-3">
                            <p class="font-bold">{getPlantName(plant.Name)}</p>
                            <div class="font-semibold text-sm mt-2">Caractéristiques:</div>
                            <div class="grid grid-cols-2 gap-2 text-sm mt-1">
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
                    <div class="col-span-5 row-start-3 text-lg text-zinc-700 pb-10 {i.toString() != recomID ? 'hidden' : ''}">
                        <div class="text-sm">{plant.Desc}</div>
                    </div>  
                {/each}
            </div>
        </div>
    </div>
    
    

</div>
    
    
    

