<script lang="ts">
  import Card, {Content} from "@smui/card";
  import DataTable, {Body, Cell as TableCell, Head, Row} from "@smui/data-table";
  import IconButton from "@smui/icon-button";
  import {Skill, SkillResource} from "../../types/api/skill";
  import SkillService from "../../services/skill-service"
  import {onMount} from "svelte";
  import {params} from "@roxi/routify";
  import StarRating from "svelte-star-rating/src/StarRating.svelte";
  import {longHumanizer, shortHumanizer} from "../../utils/date-utils";
  import {Duration} from "luxon";
  import Button, {Icon, Label} from "@smui/button";
  import Dialog, {Actions, Content as DialogContent, Header, Title} from "@smui/dialog";

  let skillResourceOpen = false;

  let skill: Skill = new Skill().createDefaultInstance();
  let selectedSkillResource: SkillResource = new SkillResource().createDefaultInstance();
  const skillService: SkillService = new SkillService();

  onMount(async () => {
    skill = await skillService.get($params.skillid);
  });

  function openSkillResourceDialog(resource: SkillResource) {
    skillResourceOpen = true;
    selectedSkillResource = resource;
  }
</script>

<h1 class="ml-4">Show Skill</h1>

<Card variant="outlined">
  <Content>
    <div>
      Name: {skill.name}
    </div>

    <div>
      Description: {skill.description}
    </div>

    <div>
      Web Link: <a href="{skill.web_link}" target="_blank">{skill.web_link}</a>
    </div>

    <div>
      Repo Link: <a href="{skill.repo_link}" target="_blank">{skill.repo_link}</a>
    </div>

    <div>
      Category: {skill.category}
    </div>

    <div>
      <DataTable class="luso-width-100-percent">
        <Head>
          <Row>
            <TableCell>Name</TableCell>
            <TableCell>Authors</TableCell>
            <TableCell>Rating</TableCell>
            <TableCell>Type</TableCell>
            <TableCell>Duration</TableCell>
            <TableCell>Est. Effort</TableCell>
          </Row>
        </Head>
        <Body>
        {#if skill.resources}
          {#each skill.resources as resource (resource.name)}
            <Row>
              <TableCell>
                <a on:click={() => openSkillResourceDialog(resource)}>
                  {resource.name}
                </a>
              </TableCell>
              <TableCell>
                {resource.authors}
              </TableCell>
              <TableCell>
                <StarRating rating={resource.community_rating}/>
              </TableCell>
              <TableCell>{resource.category}</TableCell>
              <TableCell>
                {longHumanizer(Duration.fromISO(resource.duration))}
              </TableCell>
              <TableCell>
                {shortHumanizer(Duration.fromISO(resource.estimated_effort?.min))}
                -
                {shortHumanizer(Duration.fromISO(resource.estimated_effort?.max))}
                /
                {resource.estimated_effort?.period}
              </TableCell>
            </Row>
          {/each}
        {/if}
        </Body>
      </DataTable>
    </div>
  </Content>
</Card>

<Dialog bind:open={skillResourceOpen}
        fullscreen
        aria-labelledby="fullscreen-title"
        aria-describedby="fullscreen-content"
        bind:selectedSkillResource
        surface$style="width: 850px; max-width: calc(100vw - 32px);">

  <Header>
    <Title id="title">Skill Resource</Title>
    <IconButton action="close" class="material-icons">close</IconButton>
  </Header>

  <DialogContent id="content">
    <div>
      Name: {selectedSkillResource.name}
    </div>
    <div>
      Authors: {selectedSkillResource.authors}
    </div>
    <div>
      Category: {selectedSkillResource.category}
    </div>
    <div>
      Web Link:
      <a href="{selectedSkillResource.web_link}" target="_blank">
        {selectedSkillResource.web_link}
      </a>
    </div>
    <div class="luso-flex">
      Overall Rating:
      <StarRating style="margin-bottom: 0;" rating={selectedSkillResource.community_rating}/>
    </div>
    <div>
      Duration: {shortHumanizer(Duration.fromISO(selectedSkillResource.duration).toMillis())}
    </div>
    <div>
      Estimated Effort:
      {shortHumanizer(Duration.fromISO(selectedSkillResource.estimated_effort?.min).toMillis())} -
      {shortHumanizer(Duration.fromISO(selectedSkillResource.estimated_effort?.max).toMillis())}
      {selectedSkillResource.estimated_effort?.period}
    </div>
    <div>
      Description: {selectedSkillResource.description}
    </div>
    <div>
      <h4>Items</h4>
      <DataTable class="luso-width-100-percent">
        <Head>
          <Row>
            <TableCell>Name</TableCell>
            <TableCell>Duration</TableCell>
          </Row>
        </Head>
        <Body>
        {#each selectedSkillResource.items || [] as item (item.name)}
          <Row>
            <TableCell>
              <a href="{item.web_link}" target="_blank">
                {item.name}
              </a>
            </TableCell>
            <TableCell>
              {shortHumanizer(Duration.fromISO(item.duration).toMillis())}
            </TableCell>
          </Row>
        {:else}
          whoops - no modules found
        {/each}
        </Body>
      </DataTable>
    </div>
  </DialogContent>

  <Actions>
    <Button action=close variant="raised">
      <Icon class="material-icons">close</Icon>
      <Label>Close</Label>
    </Button>
  </Actions>
</Dialog>

