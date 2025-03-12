<script lang="ts">
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
    let SunNeed:string = $state("Mi-Ombre")
    let Maintenance:string = $state("Moyen")    
    let saison:Selected = $state({value:"Printemps", label:"Printemps",disabled:false})
    let categorie:Selected = $state({value:"Vivaces", label:"Vivaces",disabled:false})

    let minHeight:number = $state(20)
    let maxHeight:number = $state(60)

    let soils:Selects[] = [
        {value:"Limon", label:"Terre"},
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
        fetch(`http://127.0.0.1:8000/recommend?sun_needs=${SunNeed}&water_needs=${WaterNeed}&maintenance=${Maintenance}&soil=${soil}&season=${saison}&plant_category=${categorie}&min_height=${minHeight}&max_height=${maxHeight}`)
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

</script>

<div class="grid mx-10 my-10 lg:mx-75  grid-cols-2 gap-x-10">
    <div class="col-start-1">
        <div class="w-[450px]">
            <div class="mb-5">
                <div class="font-bold text-xl">Recommandation</div>
                <div>Notre système vous recommandera 5 plantes correspondants à vos envies ...</div>
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
        <div class="w-full mx-10">
            <div class="grid grid-cols-5 gap-x-4 gap-y-10">
                {#each dataAPI.recommendations as plant, i}
                    <!-- svelte-ignore a11y_click_events_have_key_events -->
                    <!-- svelte-ignore a11y_no_static_element_interactions -->
                    <div class="w-full aspect-[1/1] h-20 bg-red-500 rounded-md" id={i.toString()} onclick={onclickRecom}>{plant}</div>
                {/each}    
                
                <div class="col-span-3 w-full h-60 bg-red-500 rounded-md"></div>

                {#each dataAPI.recommendations as plant, i}
                    <div class="col-span-2 text-lg text-black {i.toString() != recomID ? 'hidden' : ''}">
                        <p>{plant}</p>
                    </div>
                {/each}
            </div>
        </div>
    </div>
    
    

</div>
    
    
    

