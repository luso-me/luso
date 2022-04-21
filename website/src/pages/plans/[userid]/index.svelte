<script lang="ts">
  import {SkillPlanObjective, User} from "../../../types/api/user";
  import ToolTip, {Wrapper} from "@smui/tooltip";
  import {onMount} from "svelte";
  import LayoutGrid, {Cell} from '@smui/layout-grid';
  import Card, {Actions, Content} from '@smui/card';
  import UserService from "../../../services/user-service";
  import Button, {Icon, Label} from "@smui/button";
  import DataTable, {Body, Cell as TableCell, Head, Row} from "@smui/data-table";
  import LinearProgress from "@smui/linear-progress";
  import {goto, params, url} from '@roxi/routify';
  import TabBar from "@smui/tab-bar";
  import Tab, {Icon as TabIcon, Label as TabLabel} from "@smui/tab";
  import {DateTime, Duration} from "luxon";
  import {longHumanizer} from "../../../utils/date-utils";
  import {statuses} from "../../../types/api/const";
  import SkillService from "../../../services/skill-service";
  import {Skill} from "../../../types/api/skill";
  import {MissionObjective, MissionPlan} from "../../../types/web/user";

  let tabs = [
    {icon: 'access_time', label: 'Plans',},
    {icon: 'near_me', label: 'Objectives',},
  ];
  let active = tabs[0];
  let user: User = new User().createDefaultInstance();
  let skills: Skill[] = [];
  let missionPlans: MissionPlan[] = [];
  const userService: UserService = new UserService();
  const skillService: SkillService = new SkillService();

  onMount(async () => {
    user = await userService.get($params.userid);
    skills = await skillService.getAll();

    user.plans.forEach(sp => {
      missionPlans.push(userService.createMissionPlan(skills, sp))
      missionPlans = missionPlans;
    });
  });


  async function handleUpdateObjectiveStatus(objective: MissionObjective) {
    for (let up of user.plans) {
      const spo: SkillPlanObjective = up.objectives.find(o => o.id === objective.id);
      if (spo) {
        spo.status = objective.status;
        break;
      }
    }

    await userService.update($params.userid, user);
    await userService.updateUserInfoStore();
  }

</script>

<h1 class="ml-4">Plans</h1>

<Card variant="outlined" class="luso-background-light">
  <Content>
    <LayoutGrid>
      <Cell span={12}>
        <div>
          <TabBar {tabs} let:tab bind:active class="luso-tabbar-background">
            <Tab {tab}>
              <TabIcon class="material-icons">{tab.icon}</TabIcon>
              <TabLabel>{tab.label}</TabLabel>
            </Tab>
          </TabBar>
        </div>
        {#if active.label === 'Plans'}
          <Card class="luso-no-box-shadow">
            <Content>
              <Actions>
                <Button
                    on:click="{() => $goto('/plans/:userid/create', {userid: user.id})}"
                    variant="raised">
                  <Icon class="material-icons">add</Icon>
                  <Label>Add Skill Plan</Label>
                </Button>
              </Actions>
              <DataTable class="luso-width-100-percent">
                <Head>
                  <Row>
                    <TableCell>Name</TableCell>
                    <TableCell>Skill</TableCell>
                    <TableCell>Progress</TableCell>
                    <TableCell>Objectives</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Start Date</TableCell>
                    <TableCell>End Date</TableCell>
                  </Row>
                </Head>
                <Body>
                {#if user.plans}
                  {#each missionPlans as plan}
                    <Row>
                      <TableCell>
                        <a href="{$url(
                                    '/plans/:userid/plan/:planid/edit',
                                    {userid: user.id, planid: plan.id})}">
                          {plan.plan_name}
                        </a>
                      </TableCell>
                      <TableCell>
                        {plan.skill_name}
                      </TableCell>
                      <TableCell>
                        <LinearProgress bind:progress={plan.progress}/>
                      </TableCell>
                      <TableCell>
                        {plan.objectives.length}
                      </TableCell>
                      <TableCell>
                        {plan.status}
                      </TableCell>
                      <TableCell>
                        {DateTime.fromISO(plan.start_date).toISODate()}
                      </TableCell>
                      <TableCell>
                        {DateTime.fromISO(plan.end_date).toISODate()}
                      </TableCell>
                    </Row>
                  {/each}
                {:else}
                  No Skill Plans Found
                {/if}
                </Body>
              </DataTable>
            </Content>
          </Card>
        {:else if active.label === 'Objectives'}
          <Card>
            <Content>
              <div>
                <DataTable class="luso-width-100-percent mb-5">
                  <Head>
                    <Row>
                      <TableCell>Resource Name</TableCell>
                      <TableCell>Objective Name</TableCell>
                      <TableCell>Duration</TableCell>
                      <TableCell>Reward</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Plan Name</TableCell>
                      <TableCell>Skill</TableCell>
                    </Row>
                  </Head>
                  <Body>
                  {#if user.plans}
                    {#each missionPlans as plan}
                      {#each plan.objectives as objective}
                        <Row>
                          <TableCell>
                            {objective.resource_name}
                          </TableCell>
                          <TableCell>
                            {objective.resource_item_name}
                          </TableCell>
                          <TableCell>
                            {longHumanizer(Duration.fromISO(objective.duration))}
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
                            <!-- https://github.com/hperrin/svelte-material-ui/issues/374
                            <Select bind:value={objective.status} label="Current Status"
                                    on:SMUISelect:change={handleUpdateObjectiveStatus}
                                    key={(selectedStatus) => (selectedStatus) || ''}>
                              {#each statuses as status}
                                <Option value={status}>{status}</Option>
                              {/each}
                            </Select>
                            -->
                            <select bind:value={objective.status}
                                    class="luso-select-background"
                                    on:change={handleUpdateObjectiveStatus(objective)}>
                              {#each statuses as status}
                                <option value={status}>{status}</option>
                              {/each}
                            </select>
                          </TableCell>
                          <TableCell>
                            {plan.plan_name}
                          </TableCell>
                          <TableCell>
                            {plan.skill_name}
                          </TableCell>
                        </Row>
                      {/each}
                    {/each}
                  {:else}
                    No Skill Plans Found
                  {/if}
                  </Body>
                </DataTable>
              </div>
            </Content>
          </Card>
        {:else}
        {/if}
      </Cell>
    </LayoutGrid>
  </Content>
</Card>
