<script lang="ts">
  import DataTable, {Body, Cell as TableCell, Head, Row} from "@smui/data-table";
  import IconButton from "@smui/icon-button";
  import Textfield from "@smui/textfield";
  import Select, {Option} from "@smui/select";
  import {Skill, SkillResource, SkillResourceItem} from "../../../types/api/skill";
  import HelperText from "@smui/textfield/helper-text";
  import {onMount} from "svelte";
  import LayoutGrid, {Cell} from "@smui/layout-grid";
  import Button, {Icon, Label} from "@smui/button";
  import UserService from "../../../services/user-service";
  import {SkillPlan, SkillPlanObjective, User} from "../../../types/api/user";
  import StarRating from "svelte-star-rating/src/StarRating.svelte";
  import Checkbox from "@smui/checkbox";
  import ToolTip, {Wrapper} from "@smui/tooltip";
  import {DateTime, Duration} from "luxon";
  import {NameGenerator} from "../../../utils/name-generator";
  import {goto} from "@roxi/routify";
  import {userInfoStore} from "../../../stores";
  import SkillService from "../../../services/skill-service";
  import {statuses, timeHorizons} from "../../../types/api/const";
  import {defaultDuration} from "../../../types/web/date";
  import {DateUtils, longHumanizer, shortHumanizer} from "../../../utils/date-utils";
  import Dialog, {Actions, Content as DialogContent, Header, Title} from "@smui/dialog";
  import Card, {Actions as CardActions, Content} from "@smui/card";
  import {MissionObjective} from "../../../types/web/user";

  let skillResourceOpen = false;
  let totalDuration: string = "0";
  let formDisabled = true;

  let user: User;
  let skills: Skill[] = [];
  let skillPlan: SkillPlan = new SkillPlan().createDefaultInstance();
  let selectedSkill: Skill = new Skill().createDefaultInstance();
  let selectedSkillResource: SkillResource = new SkillResource().createDefaultInstance();
  let selectedSkillResourceItemsDialog: SkillResourceItem[] = [];
  let missionObjectives: MissionObjective[] = [];
  let skillPlanObjectives: SkillPlanObjective[] = [];
  const userService: UserService = new UserService();
  const skillService: SkillService = new SkillService();

  onMount(async () => {
    user = await userService.get($userInfoStore.id);
    skills = await skillService.getAll();
    skills.sort((a, b) => a.name.localeCompare(b.name));
  });

  const onSubmit = async () => {
    _populateNewSkillPlan();
    user.plans.push(skillPlan);
    user = user;

    await userService.update(user.id, user);
    $goto('/plans/:userid', {userid: user.id});
  }

  function _populateNewSkillPlan() {
    skillPlan.id = "";
    skillPlan.plan_name = NameGenerator.generateName();
    skillPlan.status = statuses[0];
    skillPlan.time_horizon;

    let now = DateTime.utc();
    skillPlan.start_date = now;
    skillPlan.end_date = DateUtils.determineEndDateForTimeHorizon(skillPlan.time_horizon, now);

    missionObjectives.forEach(mo => {
      skillPlanObjectives.push(_createSkillPlanObjective(mo));
    });

    skillPlan.objectives = skillPlanObjectives;
  }

  async function handleSelectSkill(event) {
    skillPlan.skill_id = selectedSkill.id;
    console.log('skill id: ' + skillPlan.skill_id);
  }

  function openSkillResourceDialog(resource: SkillResource) {
    skillResourceOpen = true;
    selectedSkillResource = resource;
    _preSelectExistingSkillResources();
  }

  function _preSelectExistingSkillResources() {
    missionObjectives.forEach(mo => {
      let existingItem = selectedSkillResource.items.find(i => i.id === mo.resource_item_id);
      if (existingItem) {
        selectedSkillResourceItemsDialog.push(existingItem);
      }
    });
  }

  function saveSkillResourceDialog(sr: SkillResource) {
    skillResourceOpen = false;

    const diff = sr.items.filter(i => !selectedSkillResourceItemsDialog.map(s => s.id).includes(i.id));
    missionObjectives = missionObjectives.filter(i => !diff.map(s => s.id).includes(i.resource_item_id));

    selectedSkillResourceItemsDialog.forEach(i => {
      const exist = missionObjectives.find(mo => i.id === mo.resource_item_id);
      if (!exist) {
        missionObjectives.push(_createMissionObjective(i));
      }
    });

    _resetSkillResourceDialog();
  }

  function _resetSkillResourceDialog() {
    formDisabled = !(missionObjectives.length > 0);
    missionObjectives = missionObjectives;

    selectedSkillResourceItemsDialog = [];
    totalDuration = _calculateTotalDuration();
  }

  function _createMissionObjective(skillResourceItem: SkillResourceItem): MissionObjective {
    let missionObjective: MissionObjective = new MissionObjective().createDefaultInstance();

    missionObjective.resource_id = selectedSkillResource.id;
    missionObjective.resource_web_link = selectedSkillResource.web_link;
    missionObjective.resource_name = selectedSkillResource.name;

    missionObjective.resource_item_id = skillResourceItem.id;
    missionObjective.resource_item_name = skillResourceItem.name;
    missionObjective.resource_item_web_link = skillResourceItem.web_link;

    missionObjective.duration = skillResourceItem.duration;
    missionObjective.status = statuses[0];

    return missionObjective;
  }

  function _createSkillPlanObjective(missionObjective: MissionObjective): SkillPlanObjective {
    let objective: SkillPlanObjective = new SkillPlanObjective().createDefaultInstance();

    objective.resource_id = missionObjective.resource_id;
    objective.resource_item_id = missionObjective.resource_item_id;
    objective.status = missionObjective.status;

    return objective;
  }

  function removeObjective(objective: SkillPlanObjective) {
    missionObjectives = missionObjectives.filter(o =>
        objective.resource_item_id !== o.resource_item_id
    );
    totalDuration = _calculateTotalDuration();
  }

  function _calculateTotalDuration(): string {
    let total: Duration = Duration.fromISO(defaultDuration);

    missionObjectives.forEach(objective => {
      let duration = objective.duration;
      total = total.plus(Duration.fromISO(duration));
    });

    return longHumanizer(total.toMillis(), {largest: 2});
  }
</script>

<h1 class="ml-4">Add Skill Plan</h1>

<Card variant="outlined" class="luso-background-light">
  <Content>
    <LayoutGrid>
      <Cell span="{12}">
        <div>
          <form on:submit|preventDefault={onSubmit}
                data-test="plan-create-form"
          >
            <Card>
              <Content>
                <h4>Details</h4>
                <div>
                  <Select bind:value={selectedSkill}
                          on:SMUISelect:change={handleSelectSkill}
                          label="Select Skill" class="luso-dialog-field" required
                          key={(selectedSkill) => (selectedSkill && selectedSkill.name) || ''}
                          data-test="plan-create-select-skill">
                    {#each skills as skill}
                      <Option value={skill} data-test="plan-create-selected-skill-name">
                        {skill.name}
                      </Option>
                    {/each}
                  </Select>
                </div>
                <div>
                  <Select bind:value={skillPlan.time_horizon} required
                          label="Select Time Horizon" class="luso-dialog-field"
                          data-test="plan-create-select-time-horizon">
                    {#each timeHorizons as horizon}
                      <Option value={horizon}
                              data-test="plan-create-selected-time-horizon-name">
                        {horizon}
                      </Option>
                    {/each}
                  </Select>
                </div>
                <div class="margins">
                  <Textfield
                      style="width: 100%; height: 200px"
                      helperLine$style="width: 100%;"
                      textarea
                      bind:value={skillPlan.notes}
                      label="Goals">
                    <HelperText slot="helper">
                      What goals do you want to achieve by learning this skill?
                    </HelperText>
                  </Textfield>
                </div>
              </Content>
            </Card>

            <Card class="mt-4">
              <Content>
                <h4>Skill Resources</h4>
                <div>
                  <DataTable class="luso-width-100-percent">
                    <Head>
                      <Row>
                        <TableCell>Name</TableCell>
                        <TableCell>Authors</TableCell>
                        <TableCell>Link</TableCell>
                        <TableCell>Rating</TableCell>
                        <TableCell>Duration</TableCell>
                        <TableCell>Est. Effort</TableCell>
                        <TableCell>Type</TableCell>
                      </Row>
                    </Head>
                    <Body>
                    {#each selectedSkill?.resources || [] as resource (resource.name)}
                      <Row>
                        <TableCell>
                          <a on:click={() => openSkillResourceDialog(resource)}
                             data-test="plan-create-select-skill-resource-dialog">
                            {resource.name}
                          </a>
                        </TableCell>
                        <TableCell>
                          {resource.authors}
                        </TableCell>
                        <TableCell>
                          <a href="{resource.web_link}"
                             target="_blank">{resource.web_link}</a>
                        </TableCell>
                        <TableCell>
                          <StarRating rating={resource.community_rating}/>
                        </TableCell>
                        <TableCell>
                          {longHumanizer(Duration.fromISO(resource.duration))}
                        </TableCell>
                        <TableCell>
                          {shortHumanizer(
                              Duration.fromISO(resource.estimated_effort?.min))}
                          -
                          {shortHumanizer(
                              Duration.fromISO(resource.estimated_effort?.max))}
                          /
                          {resource.estimated_effort?.period}
                        </TableCell>
                        <TableCell>
                          {resource.category}
                        </TableCell>
                      </Row>
                    {:else}
                      Select a Skill first
                    {/each}
                    </Body>
                  </DataTable>
                </div>
              </Content>
            </Card>

            <Card class="mt-4">
              <Content>
                <h4>Mission Objectives (*)</h4>
                <div>
                  <DataTable class="luso-width-100-percent">
                    <Head>
                      <Row>
                        <TableCell>Resource Name</TableCell>
                        <TableCell>Objective Name</TableCell>
                        <TableCell>Duration</TableCell>
                        <TableCell>Reward</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Actions</TableCell>
                      </Row>
                    </Head>
                    <Body>
                    {#each missionObjectives as objective}
                      <Row>
                        <TableCell>
                          <a href="{objective.resource_web_link}" target="_blank"
                             data-test="plan-create-mission-objective-resource-name">
                            {objective.resource_name}
                          </a>
                        </TableCell>
                        <TableCell>
                          <a href="{objective.resource_item_web_link}" target="_blank"
                             data-test="plan-create-mission-objective-resource-item-name">
                            {objective.resource_item_name}
                          </a>
                        </TableCell>
                        <TableCell>
                          {shortHumanizer(
                              Duration.fromISO(objective.duration).toMillis())}
                        </TableCell>
                        <TableCell>
                          <div class="luso-flex-align-items-center">
                            1
                            <Wrapper>
                              <Icon class="material-icons">token</Icon>
                              <ToolTip>Token</ToolTip>
                            </Wrapper>
                            <Wrapper>
                              <Icon class="material-icons">star_border</Icon>
                              <ToolTip>XP</ToolTip>
                            </Wrapper>
                          </div>
                        </TableCell>
                        <TableCell>
                          {objective.status}
                        </TableCell>
                        <TableCell>
                          <IconButton class="material-icons"
                                      on:click$preventDefault={() => removeObjective(objective)}>
                            delete
                          </IconButton>
                        </TableCell>
                      </Row>
                    {:else}
                      Click on a Community Skill Resource to add Mission Objectives
                    {/each}
                    </Body>
                  </DataTable>
                </div>
              </Content>
            </Card>

            <Card class="mt-4">
              <Content>
                <h4>Mission Summary</h4>
                <div>
                  Total Modules: {missionObjectives?.length}<br/>
                  Total Duration: {totalDuration} <br/>
                  <div class="luso-flex-align-items-center">
                    Mission Rewards:
                    {missionObjectives?.length}
                    <Wrapper>
                      <Icon class="material-icons">token</Icon>
                      <ToolTip>Token</ToolTip>
                    </Wrapper>
                    &
                    {missionObjectives?.length}
                    <Wrapper>
                      <Icon class="material-icons">star_border</Icon>
                      <ToolTip>XP</ToolTip>
                    </Wrapper>
                  </div>
                </div>
              </Content>
            </Card>

            <CardActions>
              <Button variant="raised" disabled={formDisabled}
                      data-test="plan-create-start-mission">
                <Icon class="material-icons">rocket_launch</Icon>
                <Label>Start Mission!</Label>
              </Button>
            </CardActions>
          </form>
        </div>
      </Cell>
    </LayoutGrid>
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

  <DialogContent id="content" class="luso-background-light">
    <Card class="mt-2">
      <Content>
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
          <StarRating style="margin-bottom: 0;"
                      rating={selectedSkillResource.community_rating}/>
        </div>
        <div>
          Duration: {shortHumanizer(
            Duration.fromISO(selectedSkillResource.duration).toMillis())}
        </div>
        <div>
          Estimated Effort:
          {shortHumanizer(
              Duration.fromISO(selectedSkillResource.estimated_effort?.min).toMillis())}
          -
          {shortHumanizer(
              Duration.fromISO(selectedSkillResource.estimated_effort?.max).toMillis())}
          {selectedSkillResource.estimated_effort?.period}
        </div>
        <div>
          Description: {selectedSkillResource.description}
        </div>
      </Content>
    </Card>

    <Card class="mt-2">
      <Content>
        <h4>Which modules do you want to add to your Mission Plan?</h4>
        <div>
          <DataTable class="luso-width-100-percent">
            <Head>
              <Row>
                <TableCell checkbox>
                  <Checkbox/>
                </TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Duration</TableCell>
              </Row>
            </Head>
            <Body>
            {#each selectedSkillResource.items || [] as item (item.name)}
              <Row data-test="plan-create-skill-resource-dialog-module-item-row">
                <TableCell checkbox>
                  <Checkbox
                      bind:group={selectedSkillResourceItemsDialog}
                      value={item}
                      valueKey={item.id}
                      data-test="plan-create-skill-resource-dialog-module-item-checkbox"
                  />
                </TableCell>
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
      </Content>
    </Card>
  </DialogContent>

  <Actions>
    <Button on:click$preventDefault={() => saveSkillResourceDialog(selectedSkillResource)}
            variant="raised" data-test="plan-create-skill-resource-dialog-save">
      <Icon class="material-icons">save</Icon>
      <Label>Save</Label>
    </Button>
  </Actions>
</Dialog>

