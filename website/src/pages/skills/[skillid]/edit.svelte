<script lang="ts">
  import Card, {Content} from "@smui/card";
  import Textfield from "@smui/textfield";
  import IconButton from "@smui/icon-button";
  import HelperText from "@smui/textfield/helper-text";
  import CharacterCounter from "@smui/textfield/character-counter";
  import Button, {Icon, Label} from "@smui/button";
  import DataTable, {Body, Cell as TableCell, Head, Row} from "@smui/data-table";
  import Dialog, {Actions, Content as DialogContent, Header, Title} from "@smui/dialog";
  import Select, {Option} from "@smui/select";
  import {goto, params} from "@roxi/routify";
  import StarRating from "svelte-star-rating/src/StarRating.svelte";
  import Slider from "@smui/slider";
  import FormField from "@smui/form-field";
  import TabBar from "@smui/tab-bar";
  import Tab, {Icon as TabIcon, Label as TabLabel} from "@smui/tab";
  import {longHumanizer, shortHumanizer} from "../../../utils/date-utils";
  import {Duration} from "luxon";
  import LayoutGrid, {Cell} from "@smui/layout-grid";
  import {Skill, SkillResource, SkillResourceItem} from "../../../types/api/skill";
  import SkillService from "../../../services/skill-service";
  import {
    durations,
    estimatedEfforts,
    resourceCategories,
    skillCategories
  } from "../../../types/api/const";
  import {onMount} from "svelte";
  import {LusoDuration} from "../../../types/web/date";

  let skill: Skill = new Skill().createDefaultInstance();
  let skillResource: SkillResource = new SkillResource().createDefaultInstance();
  let skillResourceItem: SkillResourceItem = new SkillResourceItem().createDefaultInstance();
  let openSkillResource = false;
  let skillResourceDuration: LusoDuration = new LusoDuration().createDefaultInstance();
  let skillResourceMinDuration: LusoDuration = new LusoDuration().createDefaultInstance();
  let skillResourceMaxDuration: LusoDuration = new LusoDuration().createDefaultInstance();
  let skillResourceItemDuration: LusoDuration = new LusoDuration().createDefaultInstance();
  const skillService: SkillService = new SkillService();

  let pageTabs = [
    {icon: 'access_time', label: 'Skill Details',},
    {icon: 'near_me', label: 'Resources',},
  ];
  let activePageTab = pageTabs[0];

  let dialogTabs = [
    {icon: 'access_time', label: 'Resource Details',},
    {icon: 'near_me', label: 'Resource Items',},
  ];
  let activeDialogTab = dialogTabs[0];

  onMount(async () => {
    skill = await skillService.get($params.skillid);
  });

  const onSubmit = async () => {
    await skillService.update(skill.id, skill);
    await $goto('/skills');
  }

  function onSubmitSkillResource() {
    const exist = skill.resources.find(s => s.name === skillResource.name);
    if (!exist) {
      // this doesn't currently cater for the scenario where the user is update an item to
      // the same name as an existing item
      skill.resources.push(skillResource);
    }

    skill = skill;
    openSkillResource = false;
  }

  function onSkillResourceEdit(resource: SkillResource) {
    skillResource = resource;
    openSkillResource = true;

    skillResourceDuration = new LusoDuration().createInstance(skillResource.duration);
    skillResourceMinDuration = new LusoDuration().createInstance(skillResource.estimated_effort?.min);
    skillResourceMaxDuration = new LusoDuration().createInstance(skillResource.estimated_effort?.max);
  }

  function onSkillResourceDelete(resource: SkillResource) {
    skill.resources = skill.resources.filter(s => s.name !== resource.name);
  }

  function onSkillResourceAdd() {
    skillResource = new SkillResource().createDefaultInstance();
    openSkillResource = true;

    skillResourceDuration = new LusoDuration().createDefaultInstance();
    skillResourceMinDuration = new LusoDuration().createDefaultInstance();
    skillResourceMaxDuration = new LusoDuration().createDefaultInstance();
    skillResourceItemDuration = new LusoDuration().createDefaultInstance();
  }

  function onSkillResourceItemAdd() {
    const exist = skillResource.items.find(s => s.name === skillResourceItem.name);
    if (!exist) {
      // this doesn't currently cater for the scenario where the user is update an item to
      // the same name as an existing item
      skillResource.items.push(skillResourceItem);
    }

    skillResource = skillResource;
    skillResourceItem = new SkillResourceItem().createDefaultInstance();
    skillResourceItemDuration = new LusoDuration().createDefaultInstance();
  }

  function onSkillResourceItemEdit(item: SkillResourceItem) {
    skillResourceItem = item;
    skillResourceItemDuration = new LusoDuration().createInstance(skillResourceItem.duration);
  }

  function onSkillResourceItemDelete(item: SkillResourceItem) {
    skillResource.items = skillResource.items.filter(s => s.name !== item.name);
  }

  function calculateSkillResourceDuration() {
    skillResource.duration = skillResourceDuration.calculateDuration();
  }

  function calculateSkillResourceMinDuration() {
    skillResource.estimated_effort.min = skillResourceMinDuration.calculateDuration();
  }

  function calculateSkillResourceMaxDuration() {
    skillResource.estimated_effort.max = skillResourceMaxDuration.calculateDuration();
  }

  function calculateSkillResourceItemDuration() {
    skillResourceItem.duration = skillResourceItemDuration.calculateDuration();
  }

</script>

<h1 class="ml-4">Edit Skill</h1>

<Card variant="outlined" class="luso-background-light">
  <Content>

    <div>
      <TabBar tabs={pageTabs} let:tab bind:active={activePageTab} class="luso-tabbar-background">
        <Tab {tab}>
          <TabIcon class="material-icons">{tab.icon}</TabIcon>
          <TabLabel>{tab.label}</TabLabel>
        </Tab>
      </TabBar>
    </div>

    <form on:submit|preventDefault={onSubmit}>
      {#if activePageTab.label === 'Skill Details'}
        <Card>
          <Content>
            <h4>Details</h4>
            <div>
              <Textfield bind:value={skill.name} label="Name" required input$maxlength={100}
                         class="luso-form-field">
                <svelte:fragment slot="helper">
                  <HelperText>Helper Text</HelperText>
                  <CharacterCounter>0 / 100</CharacterCounter>
                </svelte:fragment>
              </Textfield>
            </div>
            <div>
              <Select bind:value={skill.category} label="Select Category" required
                      class="luso-dialog-field-with-helper">
                {#each skillCategories as category}
                  <Option value={category}>{category}</Option>
                {/each}
                <HelperText>Select Category</HelperText>
              </Select>
            </div>
            <div class="mt-5 margins">
              <Textfield
                  style="width: 100%;"
                  helperLine$style="width: 100%;"
                  textarea
                  bind:value={skill.description}
                  label="Description">
                <HelperText slot="helper">Helper Text</HelperText>
              </Textfield>
            </div>
            <div>
              <Textfield bind:value={skill.web_link} label="Web Link" required input$maxlength={100}
                         class="luso-form-field">
                <svelte:fragment slot="helper">
                  <HelperText>Helper Text</HelperText>
                  <CharacterCounter>0 / 100</CharacterCounter>
                </svelte:fragment>
              </Textfield>
            </div>
            <div>
              <Textfield bind:value={skill.repo_link} label="Repository Link" input$maxlength={100}
                         class="luso-form-field">
                <svelte:fragment slot="helper">
                  <HelperText>Helper Text</HelperText>
                  <CharacterCounter>0 / 100</CharacterCounter>
                </svelte:fragment>
              </Textfield>
            </div>
            <div>
              <Button on:click$preventDefault={() => {activePageTab = pageTabs[1]}} variant="raised"
                      class="mt-3">
                <Icon class="material-icons">fast_forward</Icon>
                <Label>NEXT</Label>
              </Button>
            </div>
          </Content>
        </Card>
      {:else if activePageTab.label === 'Resources'}
        <Card>
          <Content>
            <h4>Skill Resources</h4>
            <div>
              <Button on:click$preventDefault={onSkillResourceAdd} variant="raised"
                      class="mb-3">
                <Icon class="material-icons">add</Icon>
                <Label>Add Skill Resource</Label>
              </Button>
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
                    <TableCell>Actions</TableCell>
                  </Row>
                </Head>
                <Body>
                {#each skill.resources || [] as resource (resource.name)}
                  <Row>
                    <TableCell>
                      <a href="{resource.web_link}" target="_blank">
                        {resource.name}
                      </a>
                    </TableCell>
                    <TableCell>
                      {resource.authors}
                    </TableCell>
                    <TableCell>
                      <StarRating rating={resource.community_rating}/>
                    </TableCell>
                    <TableCell>
                      {resource.category}
                    </TableCell>
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
                    <TableCell>
                      <IconButton class="material-icons"
                                  on:click$preventDefault={onSkillResourceEdit(resource)}>
                        edit
                      </IconButton>
                      <IconButton class="material-icons"
                                  on:click$preventDefault={onSkillResourceDelete(resource)}>
                        delete
                      </IconButton>
                    </TableCell>
                  </Row>
                {/each}
                </Body>
              </DataTable>
            </div>
          </Content>
        </Card>
        <div>
          <Button variant="raised" class="mt-3">
            <Icon class="material-icons">save</Icon>
            <Label>SAVE</Label>
          </Button>
        </div>
      {/if}
    </form>
  </Content>
</Card>


<Dialog bind:open={openSkillResource}
        fullscreen
        aria-labelledby="fullscreen-title"
        aria-describedby="fullscreen-content"
        surface$style="width: 850px; max-width: calc(100vw - 32px);">

  <Header>
    <Title id="title">Add Skill Resource</Title>
    <IconButton action="close" class="material-icons">close</IconButton>
  </Header>

  <div>
    <TabBar tabs={dialogTabs} let:tab bind:active={activeDialogTab} class="luso-tabbar-background">
      <Tab {tab}>
        <TabIcon class="material-icons">{tab.icon}</TabIcon>
        <TabLabel>{tab.label}</TabLabel>
      </Tab>
    </TabBar>
  </div>

  <DialogContent class="luso-background-light">
    {#if activeDialogTab.label === 'Resource Details'}
      <Card>
        <Content>
          <h4>Resource</h4>
          <div>
            <Textfield bind:value={skillResource.name} label="Name" required input$maxlength={100}
                       class="luso-dialog-field-with-helper">
              <svelte:fragment slot="helper">
                <HelperText>Helper Text</HelperText>
                <CharacterCounter>0 / 100</CharacterCounter>
              </svelte:fragment>
            </Textfield>
          </div>
          <div class="margins">
            <Textfield
                style="width: 100%; height: 100px"
                helperLine$style="width: 100%;"
                textarea
                bind:value={skillResource.description}
                label="Description">
              <HelperText slot="helper">Helper Text</HelperText>
            </Textfield>
          </div>
          <div>
            <Textfield bind:value={skillResource.authors} label="Authors" required
                       input$maxlength={100}
                       class="luso-dialog-field-with-helper">
              <svelte:fragment slot="helper">
                <HelperText>Helper Text</HelperText>
                <CharacterCounter>0 / 100</CharacterCounter>
              </svelte:fragment>
            </Textfield>
          </div>
          <div>
            <Select bind:value={skillResource.category} label="Select Category"
                    class="luso-dialog-field-with-helper">
              {#each resourceCategories as category}
                <Option value={category}>{category}</Option>
              {/each}
              <HelperText>Helper Text</HelperText>
            </Select>
          </div>
          <div>
            <Textfield bind:value={skillResource.web_link} label="Web Link" required
                       input$maxlength={200}
                       class="luso-dialog-field-with-helper">
              <svelte:fragment slot="helper">
                <HelperText>Helper Text</HelperText>
                <CharacterCounter>0 / 200</CharacterCounter>
              </svelte:fragment>
            </Textfield>
          </div>
          <div>
            <FormField align="end" style="display: flex;">
              <Slider
                  bind:value={skillResource.community_rating}
                  min={0}
                  max={5}
                  step={0.5}
                  input$aria-label="Rating slider"
                  style="flex-grow: 1"
              />
              {skillResource.community_rating}/5
              <span slot="label" style="padding-right: 12px; width: max-content; display: block">
                Rating
              </span>
            </FormField>
          </div>
          <div>
            <LayoutGrid style="padding: 0 !important;">
              <Cell span="{2}">
                <Textfield bind:value={skillResourceDuration.value} label="Duration" required
                           on:focusout={calculateSkillResourceDuration}>
                </Textfield>
              </Cell>
              <Cell span="{2}">
                <Select bind:value={skillResourceDuration.unit} label="Duration Unit"
                        on:SMUISelect:change={calculateSkillResourceDuration}>
                  {#each durations as duration}
                    <Option value={duration}>{duration}</Option>
                  {/each}
                </Select>
              </Cell>
            </LayoutGrid>
          </div>
          <div>
            Estimated Effort
            <div>
              <LayoutGrid style="padding: 0 !important;">
                <Cell span="{2}">
                  <Textfield bind:value={skillResourceMinDuration.value} label="Min" required
                             on:focusout={calculateSkillResourceMinDuration}>
                  </Textfield>
                </Cell>
                <Cell span="{2}">
                  <Select bind:value={skillResourceMinDuration.unit} label="Min Unit"
                          on:SMUISelect:change={calculateSkillResourceMinDuration}>
                    {#each durations as duration}
                      <Option value={duration}>{duration}</Option>
                    {/each}
                  </Select>
                </Cell>
              </LayoutGrid>
            </div>
            <div>
              <LayoutGrid style="padding: 0 !important;">
                <Cell span="{2}">
                  <Textfield bind:value={skillResourceMaxDuration.value} label="Max" required
                             on:focusout={calculateSkillResourceMaxDuration}>
                  </Textfield>
                </Cell>
                <Cell span="{2}">
                  <Select bind:value={skillResourceMaxDuration.unit} label="Max Unit"
                          on:SMUISelect:change={calculateSkillResourceMaxDuration}>
                    {#each durations as duration}
                      <Option value={duration}>{duration}</Option>
                    {/each}
                  </Select>
                </Cell>
              </LayoutGrid>
            </div>
            <Select bind:value={skillResource.estimated_effort.period} label="Select Period">
              {#each estimatedEfforts as effort}
                <Option value={effort}>{effort}</Option>
              {/each}
              <HelperText>Helper Text</HelperText>
            </Select>
          </div>
        </Content>
      </Card>
    {:else if activeDialogTab.label === 'Resource Items'}
      <Card>
        <Content>
          <h4>Item Detail</h4>
          <div>
            <Textfield bind:value={skillResourceItem.name} label="Resource Item Name"
                       input$maxlength={200}
                       class="luso-dialog-field-with-helper">
              <svelte:fragment slot="helper">
                <HelperText>e.g. Chapter 1</HelperText>
                <CharacterCounter>0 / 200</CharacterCounter>
              </svelte:fragment>
            </Textfield>
          </div>
          <div class="margins mt-3">
            <Textfield
                style="width: 100%; height: 100px"
                helperLine$style="width: 100%;"
                textarea
                bind:value={skillResourceItem.description}
                label="Description">
              <HelperText slot="helper">Helper Text</HelperText>
            </Textfield>
          </div>
          <div>
            <Textfield bind:value={skillResourceItem.web_link} label="Web Link"
                       input$maxlength={200}
                       class="luso-dialog-field-with-helper">
              <svelte:fragment slot="helper">
                <HelperText>Helper Text</HelperText>
                <CharacterCounter>0 / 200</CharacterCounter>
              </svelte:fragment>
            </Textfield>
          </div>
          <div>
            <div>
              <LayoutGrid style="padding: 0 !important;">
                <Cell span="{2}">
                  <Textfield bind:value={skillResourceItemDuration.value} label="Duration" required
                             on:focusout={calculateSkillResourceItemDuration}>
                  </Textfield>
                </Cell>
                <Cell span="{2}">
                  <Select bind:value={skillResourceItemDuration.unit} label="Duration Unit"
                          on:SMUISelect:change={calculateSkillResourceItemDuration}>
                    {#each durations as duration}
                      <Option value={duration}>{duration}</Option>
                    {/each}
                  </Select>
                </Cell>
              </LayoutGrid>
            </div>
          </div>
          <div>
            <Button on:click$preventDefault={onSkillResourceItemAdd} variant="raised"
                    class="mt-3">
              <Icon class="material-icons">add</Icon>
              <Label>ADD</Label>
            </Button>
          </div>
        </Content>
      </Card>

      <Card class="mt-4">
        <Content>
          <h4>Items</h4>
          <DataTable class="luso-width-100-percent">
            <Head>
              <Row>
                <TableCell>Name</TableCell>
                <TableCell>Duration</TableCell>
                <TableCell>Actions</TableCell>
              </Row>
            </Head>
            <Body>
            {#each skillResource.items || [] as item (item.name)}
              <Row>
                <TableCell>
                  <a href="{item.web_link}" target="_blank">
                    {item.name}
                  </a>
                </TableCell>
                <TableCell>
                  {shortHumanizer(Duration.fromISO(item.duration).toMillis())}
                </TableCell>
                <TableCell>
                  <IconButton class="material-icons"
                              on:click$preventDefault={onSkillResourceItemEdit(item)}>
                    edit
                  </IconButton>
                  <IconButton class="material-icons"
                              on:click$preventDefault={onSkillResourceItemDelete(item)}>
                    delete
                  </IconButton>
                </TableCell>
              </Row>
            {/each}
            </Body>
          </DataTable>
        </Content>
      </Card>
    {/if}
  </DialogContent>
  <Actions>
    <Button on:click$preventDefault={onSubmitSkillResource} variant="raised">
      <Icon class="material-icons">save</Icon>
      <Label>Save</Label>
    </Button>
  </Actions>
</Dialog>
