<style>
  .hero-logo {
    max-width: 100%;
    height: auto;
    fill: #f4f4f4;
  }
</style>

<script lang="ts">
  import Button, {Icon as ButtonIcon, Label} from "@smui/button";
  import {goto} from "@roxi/routify";
  import {Cell} from "@smui/layout-grid";
</script>

<Cell class="hero" spanDevices={{desktop: 3, tablet: 4, phone: 2}}>
  <h1>Take charge of your IT skill progression</h1>
  <p>
    A community driven Skills Manager that allows you to find, plan & track your skill
    progression in a fun and engaging way.
  </p>

  <Button
    on:click={() => $goto("/auth/github")}
    variant="raised"
    data-test="home-index-github-login"
    class="luso-social-login-github-button"
  >
    <ButtonIcon>
      <svg aria-hidden="true" width="18" height="18" viewBox="0 0 18 18">
        <path
          d="M9 1a8 8 0 0 0-2.53 15.59c.4.07.55-.17.55-.38l-.01-1.49c-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.42 7.42 0 0 1 4 0c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48l-.01 2.2c0 .21.15.46.55.38A8.01 8.01 0 0 0 9 1Z"
          fill="#fff"
        />
      </svg>
    </ButtonIcon>
    <Label>Login with GitHub</Label>
  </Button>
</Cell>

<Cell spanDevices={{desktop: 3, tablet: 4, phone: 2}}>
  <img class="hero-logo" src="/assets/oc-growing.svg" alt="logo" />
</Cell>
