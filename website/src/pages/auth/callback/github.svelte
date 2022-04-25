<script lang="ts">
  import {goto, params} from "@roxi/routify";
  import AuthService from "../../../services/github-auth-service";
  import {authStore} from "../../../stores";

  new AuthService().callback($params.code, $params.state)
  .then((res) => {
    $authStore = res;
    $goto("/skills");
  });
</script>

<h1 class="ml-4">Busy logging you in...</h1>
