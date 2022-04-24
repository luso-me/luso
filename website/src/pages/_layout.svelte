<style>
  main {
    flex-grow: 1;
    flex-shrink: 0;
  }
</style>

<script>
  import Header from "../components/Header.svelte";
  import Footer from "../components/Footer.svelte";
</script>

<Header />
<main>
  <slot>
    <!-- pages in this folder and subfolders
     will be rendered here -->
  </slot>
</main>
<Footer />
