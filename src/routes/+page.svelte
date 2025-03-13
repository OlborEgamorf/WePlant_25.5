<script lang="ts">
    import bambou from "$lib/bambou.png";
    import fleur from "$lib/fleur.png";
    import fleur2 from "$lib/fleur2.jpg";
    import logo from "$lib/weplante.png";
  </script>
  
  <div class="bg-[#EBDC94] relative flex flex-col justify-center items-center min-h-screen">
    <img src={fleur} class="w-auto h-70 absolute top-0 right-0" alt="fleur" />
    <img src={bambou} class="w-auto h-70 absolute bottom-0 left-0" alt="fleur" />
    <img src={logo} class="w-auto h-30 absolute top-0 left-0" alt="logo" />
  
    <div class="flex flex-col items-center text-zinc-700">
      <h1 class="text-4xl text-center py-10 font-[Shikaku_Serif]">
        Le printemps dans vos bureaux avec WePlante
      </h1>
  
      <div class="grid grid-cols-2 gap-4 mt-6 w-full px-4">
        <div class="flex flex-col items-center mt-10">
          <img
            src={fleur2}
            alt="fleur"
            class="w-70 h-70 object-cover rounded-full"
          />
          <p class="font-[Indie_flower] text-center mt-4 text-lg">
            " + 15 à 32 % de bien être au travail<br>grâce aux espaces végétalisés" 
          </p>
        </div>
  
        <div>
            <p class="text-md px-2 mr-60 text-justify text-lg mb-2">
                Imaginez vous dans le sud de la France (le vrai), dans les Pyrénées-Orientales, l'air méditerranéen qui vous soulage des chaleurs de ce début d'été. Devant vous, de magnifiques fleurs grimpantes, parmi elles, vous remarquez <strong class="text-xl font-bold">des bougainvilliers</strong>.
              </p>
              
              <p class="text-md px-2 mr-60  text-justify text-lg mb-2">
                Cette couleur rose chatoyante vous parait irréelle dans un environnement si sec et violent que cette région, dans les périodes de <strong class="text-xl font-bold">pénuries</strong> et de <strong class="text-xl font-bold">sécheresse</strong>. Vous continuez de vous balader et vous remarquez que plus loin, en plein soleil, sur le flanc d’une maison loin de toute source d’eau potentielle, se tient un autre bougainvillier. Celui-ci est rachitique, presque <strong class="text-xl font-bold">fané</strong>, il tiendrait du miracle qu’il survive.
              </p>
              
              <p class="text-md px-2 mr-60  text-justify text-lg">
                Comment peut-il être si dégradé alors que son congénère vivant non loin de lui est au plus haut de sa forme ? De quoi a-t’il besoin pour renaître de ces cendres et revenir à un état de <strong class="text-xl font-bold">croissance</strong> et de bien-être ?
              </p>
              
        </div>
      </div>
    </div>
  
    <a href="/calculator" class="mt-8 px-4 py-2 bg-[#DED08C] rounded-md font-[Futura_Md_BT] text-justify text-xl">
      Découvrez les réponses !
    </a>
  </div>
  