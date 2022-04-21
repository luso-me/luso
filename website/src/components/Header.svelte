<script lang="ts">
  import Button, {Icon, Label} from "@smui/button";
  import IconButton from "@smui/icon-button";
  import TopAppBar, {Row, Section,} from '@smui/top-app-bar';
  import {goto, url} from "@roxi/routify";
  import {authStore, userInfoStore} from "../stores";
  import UserService from "../services/user-service";
  import ToolTip, {Wrapper} from "@smui/tooltip";
  import jwtDecode from "jwt-decode";

  const userService: UserService = new UserService();

  $: if ($authStore.access_token && !$userInfoStore.id) {
    userService.updateUserInfoStore();
  }

  function onLogout() {
    $authStore.access_token = "";
    $authStore.token_type = "";
    $userInfoStore.id = null;
    $userInfoStore.points = null;
    $userInfoStore.gold = null;
    $goto('/');
    location.reload();
  }

  function isSuperUser() {
    return jwtDecode($authStore.access_token)["scopes"].includes('user:super:*');
  }
</script>

<header>
  <TopAppBar variant="standard">
    <Row>
      <Section>
        <Button href={$url("/skills")}>Luso.Me</Button>
      </Section>

      {#if !$userInfoStore.id}

        <Section align="end">
          <div class="luso-flex-align-items-center">
            <Button on:click={() => $goto('/auth/github')} variant="raised"
                    data-test="home-index-github-login"
                    class="luso-social-login-github-button mr-5">
              <Icon>
                <svg aria-hidden="true" width="18" height="18" viewBox="0 0 18 18">
                  <path
                      d="M9 1a8 8 0 0 0-2.53 15.59c.4.07.55-.17.55-.38l-.01-1.49c-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.42 7.42 0 0 1 4 0c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48l-.01 2.2c0 .21.15.46.55.38A8.01 8.01 0 0 0 9 1Z"
                      fill="#fff">
                  </path>
                </svg>
              </Icon>
              <Label>Login with GitHub</Label>
            </Button>
            <a href="https://github.com/luso-me" target="_blank">
              <img class="luso-header-icon luso-header-icon-github"
                   src="/assets/github.svg" alt="github"/>
            </a>
          </div>
        </Section>

      {/if}

      {#if $userInfoStore.id}
        <Section class="luso-flex-align-items-center">
          <Button href={$url('/skills')}>Skills</Button>
          <Button href={$url('/plans/:userid', {userid: $userInfoStore.id})}>
            Plans
          </Button>
          <Button href={$url('/portfolio/:userid', {userid: $userInfoStore.id})}>
            Portfolio
          </Button>
          {#if isSuperUser()}
            <Button href={$url('/debug')}>Debug</Button>
          {/if}

          <div class="luso-flex-align-items-center">
            {$userInfoStore.gold}
            <Wrapper>
              <Icon class="material-icons">token</Icon>
              <ToolTip>Tokens</ToolTip>
            </Wrapper>
          </div>

          <div class="luso-flex-align-items-center ml-2">
            {$userInfoStore.points}
            <Wrapper>
              <Icon class="material-icons">star_border</Icon>
              <ToolTip>XP</ToolTip>
            </Wrapper>
          </div>
        </Section>

        <Section align="end">
          <Wrapper>
            <IconButton on:click={onLogout} class="material-icons"
                        data-test="home-index-logout">
              logout
            </IconButton>
            <ToolTip>Logout</ToolTip>
          </Wrapper>

          <Wrapper>
            <a href="https://github.com/luso-me" target="_blank">
              <img class="luso-header-icon luso-header-icon-github"
                   src="/assets/github.svg" alt="github"/>
            </a>
            <ToolTip>GitHub Repo</ToolTip>
          </Wrapper>
        </Section>
      {/if}
    </Row>
  </TopAppBar>
</header>

<style>
  header {
    padding-bottom: 75px;
    flex-shrink: 0;
  }
</style>
