<style>
  footer {
    border-top: black solid 1px;
    flex-shrink: 0;
  }

  .copyright {
    grid-column-start: 1;
  }
</style>

<script lang="ts">
  import LayoutGrid, {Cell} from "@smui/layout-grid";
</script>

<footer>
  <LayoutGrid>
    <Cell
      class="discord-footer text-center"
      spanDevices={{desktop: 4, tablet: 4, phone: 2}}
    >
      <div class="luso-flex-column">
        <a href="https://discord.gg/ddgdhWPQFC" target="_blank">
          <img class="luso-footer-icon" src="/assets/discord.svg" alt="discord" /><br />
          Discord
        </a>
        <div class="luso-footer-icon-support">Luso community on Discord</div>
      </div>
    </Cell>

    <Cell class="text-center" spanDevices={{desktop: 4, tablet: 4, phone: 2}}>
      <div class="luso-flex-column">
        <a href="https://github.com/luso-me" target="_blank">
          <img class="luso-footer-icon" src="/assets/github.svg" alt="github" /><br />
          GitHub
        </a>
        <div class="luso-footer-icon-support">Luso community on GitHub</div>
      </div>
    </Cell>

    <Cell
      class="copyright text-center"
      spanDevices={{desktop: 12, tablet: 8, phone: 4}}
    >
      © Luso.me 2022. All rights reserved.
    </Cell>
  </LayoutGrid>
</footer>
