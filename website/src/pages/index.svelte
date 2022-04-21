<script lang="ts">
  import {authStore} from "../stores";
  import LayoutGrid from "@smui/layout-grid";
  import Hero from "../components/Hero.svelte";
  import Features from "../components/Features.svelte";
  import Faq from "../components/Faq.svelte";
  import Drivers from "../components/Drivers.svelte";
  import Mechanics from "../components/Mechanics.svelte";
</script>

{#if $authStore.access_token}
  Dashboard Here
{:else}
  <LayoutGrid>
    <Hero/>
    <Features/>
    <Mechanics/>
    <Drivers/>
    <Faq/>
  </LayoutGrid>
{/if}
