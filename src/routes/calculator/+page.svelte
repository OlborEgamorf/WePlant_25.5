<script lang="ts">
    import Results from "$lib/components/ui/results.svelte";
    import Search from "$lib/components/ui/search.svelte";

    type Selection = {
        value:string,
        label:string,
        disabled:false
    }

    let light:number[] = $state([50])
    let moisture:number[] = $state([50])
    let temperture:number[] = $state([20])
    let soil:Selection = $state({value:"loam", label:"Terre", disabled:false})
    
    let soilValue = $derived(soil.value)

</script>


<div class="bg-[#ACE1AF] h-screen">
    <div class="bg-[#ACE1AF] h-[150px] flex items-center">
        <div class="text-center w-full text-3xl">Calculateur</div>
    </div>

    <div class="grid mx-10 my-5 lg:mx-100 items-center">
        <div class="col-start-1">
            <Search bind:light={light} bind:moisture={moisture} bind:temperture={temperture} bind:soil={soil}></Search>
        </div>

        <div class="col-start-2 ">
            <Results {light} {moisture} {temperture} soil={soilValue}></Results>
        </div>
    </div>

    

</div>