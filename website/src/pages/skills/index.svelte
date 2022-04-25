<script lang="ts">

  import ToolTip, {Wrapper} from "@smui/tooltip";
  import {onMount} from "svelte";
  import DataTable, {Body, Cell as TableCell, Head, Row} from "@smui/data-table";
  import IconButton from "@smui/icon-button";
  import Button, {Icon, Label} from "@smui/button";
  import LayoutGrid, {Cell} from "@smui/layout-grid";
  import Card, {Content} from "@smui/card";
  import SkillService from "../../services/skill-service";
  import {goto, url} from "@roxi/routify";
  import {Skill} from "../../types/api/skill";
  import jwtDecode from "jwt-decode";
  import {authStore} from "../../stores";

  let skills: Skill[] = [];
  let skillService: SkillService = new SkillService();

  onMount(async () => {
    skills = await skillService.getAll();
    skills.sort((a, b) => a.name.localeCompare(b.name));
  });

  function canUserWriteSkill() {
    return jwtDecode($authStore.access_token)["scopes"].includes('skill:write:*');
  }
</script>

<h1 class="ml-4">Skills</h1>

<Card variant="outlined" class="luso-background-light">
  <Content>
    <LayoutGrid>
      {#if canUserWriteSkill()}
        <Cell span="{12}">
          <Button on:click={() => $goto('/skills/create')} variant="raised"
                  data-test="skill-index-add-skill">
            <Icon class="material-icons">add</Icon>
            <Label>Add Skill</Label>
          </Button>
        </Cell>
      {:else}
        Don
      {/if}
      <Cell span="{12}">
        <DataTable class="luso-width-100-percent">
          <Head>
            <Row>
              <TableCell>Icon</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>External Link</TableCell>
              <TableCell>Category</TableCell>
              {#if canUserWriteSkill()}
                <TableCell>Actions</TableCell>
              {/if}
            </Row>
          </Head>
          <Body>
          {#each skills as skill (skill.name)}
            <Row>
              <TableCell>
                <img class="luso-skills-list-icon" src="{skill.icon_link}" alt="">
              </TableCell>
              <TableCell data-test="skill-index-skill-name">
                <a href="{$url('/skills/:skillid', {skillid: `${skill.id}`})}"
                   data-test="skill-index-skill-id">
                  {skill.name}
                </a>
              </TableCell>
              <TableCell>
                <Wrapper>
                  <IconButton class="material-icons"
                              href="{skill.web_link}" target="_blank">
                    link
                  </IconButton>
                  <ToolTip>External Link</ToolTip>
                </Wrapper>
              </TableCell>
              <TableCell>
                {skill.category}
              </TableCell>
              {#if canUserWriteSkill()}
                <TableCell>
                  <Wrapper>
                    <IconButton class="material-icons"
                                on:click={() => $goto(`/skills/${skill.id}/edit`)}>
                      edit
                    </IconButton>
                    <ToolTip>Edit Skill</ToolTip>
                  </Wrapper>
                </TableCell>
              {/if}
            </Row>
          {/each}
          </Body>
        </DataTable>
      </Cell>
    </LayoutGrid>
  </Content>
</Card>
