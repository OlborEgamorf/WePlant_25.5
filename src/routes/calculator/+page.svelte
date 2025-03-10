<script lang="ts">
    import Results from "$lib/components/ui/results.svelte";
    import Search from "$lib/components/ui/search.svelte";

    import Tree from "$lib/assets/tree.svg"

</script>


<div class="bg-[#FFFFF6] h-screen">
    <div class="bg-[#ACE1AF] h-[150px] flex items-center">
        <div class="text-center w-full text-3xl">Calculateur</div>
    </div>

    <img class="fixed bottom-0 z-0 right-100 w-[100px]" src={Tree}>

    <div class="grid mx-10 my-5">
        <div>
            <Search></Search>
        </div>

        <div>
            <Results></Results>
        </div>
    </div>

    

</div>