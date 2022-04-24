<script lang="ts">
  import {onMount} from "svelte";
  import {User, UserSkill, UserSkillUsed} from "../../../../types/api/user";
  import Card, {Actions as CardActions, Content} from "@smui/card";
  import {Skill} from "../../../../types/api/skill";
  import DataTable, {Body, Cell as TableCell, Head, Row} from "@smui/data-table";
  import IconButton from "@smui/icon-button";
  import Textfield from "@smui/textfield";
  import Dialog, {Actions, Content as DialogContent, Header, Title} from "@smui/dialog";
  import Select, {Option} from "@smui/select";
  import HelperText from "@smui/textfield/helper-text";
  import Button, {Icon, Label} from "@smui/button";
  import UserService from "../../../../services/user-service";
  import {goto} from "@roxi/routify";
  import {userInfoStore} from "../../../../stores";
  import SkillService from "../../../../services/skill-service";
  import {userSkillRatings} from "../../../../types/api/const";

  let open = false;

  let skills: Skill[] = [];
  let user: User = new User().createDefaultInstance();
  let selectedSkill: Skill = new Skill().createDefaultInstance();
  let userSkill: UserSkill = new UserSkill().createDefaultInstance();
  let userSkillUsed: UserSkillUsed = new UserSkillUsed().createDefaultInstance();
  const userService: UserService = new UserService();
  const skillService: SkillService = new SkillService();

  onMount(async () => {
    user = await userService.get($userInfoStore.id);
    skills = await skillService.getAll();
    skills.sort((a, b) => a.name.localeCompare(b.name));

    if (user.skills.length > 0) {
      skills = _filterUsedSkills();
    }
  });

  const onSubmit = async () => {
    user.skills.push(userSkill);
    user = user;

    await userService.update(user.id, user);
    await $goto('/portfolio/:userid', {userid: user.id});
  }

  function handleClick(event) {
    userSkill.skill_id = selectedSkill.id;
  }

  function onSubmitUserSkillUsed() {
    const exist = userSkill.used.find(u =>
        (u.at === userSkillUsed.at && u.from_date === userSkillUsed.from_date)
    );

    if (!exist) {
      // this doesn't currently cater for the scenario where the user is update an item to
      // the same name as an existing item
      userSkill.used.push(userSkillUsed);
    }

    userSkill = userSkill;
    userSkillUsed = new UserSkillUsed().createDefaultInstance();
    open = false;
  }

  function onUserSkillUsedEdit(used: UserSkillUsed) {
    userSkillUsed = used;
    open = true;
  }

  function onUserSkillUsedDelete(used: UserSkillUsed) {
    userSkill.used = userSkill.used.filter(u => !(u.at === used.at && u.from_date === used.from_date));
  }

  function onUserSkillUsedAdd() {
    userSkillUsed = new UserSkillUsed().createDefaultInstance();
    open = true;
  }

  function _filterUsedSkills() {
    return skills.filter((s) => {
      for (let i = 0; i < user.skills.length; i++) {
        if (s.id === user.skills[i].skill_id) {
          return false;
        }
      }
      return true;
    });
  }
</script>

<h1 class="ml-4">Add User Skill</h1>

<Card variant="outlined" class="luso-background-light">
  <Content>
    <form on:submit|preventDefault={onSubmit}>

      <Card>
        <Content>
          <h4>Details</h4>
          <div>
            <Select bind:value={selectedSkill} label="Select Skill"
                    class="luso-dialog-field" on:SMUISelect:change={handleClick}
                    key={(selectedSkill) => (selectedSkill && selectedSkill.id) || ''}>
              {#each skills as skill}
                <Option value={skill}>{skill.name} ({skill.category})</Option>
              {/each}
            </Select>
          </div>
          <div>
            <Select bind:value={userSkill.user_rating} label="Select My Rating"
                    class="luso-dialog-field">
              {#each userSkillRatings as rating}
                <Option value={rating}>{rating}</Option>
              {/each}
            </Select>
          </div>
          <div class="margins">
            <Textfield
                style="width: 100%; height: 200px"
                helperLine$style="width: 100%;"
                textarea
                bind:value={userSkill.notes}
                label="Notes">
              <HelperText slot="helper">Helper Text</HelperText>
            </Textfield>
          </div>
        </Content>
      </Card>

      <Card class="mt-4">
        <Content>
          <h4>History</h4>
          <div>
            <Button on:click$preventDefault={onUserSkillUsedAdd} variant="raised">
              <Icon class="material-icons">add</Icon>
              <Label>Add History</Label>
            </Button>
          </div>
          <div>
            <DataTable class="luso-width-100-percent">
              <Head>
                <Row>
                  <TableCell>From</TableCell>
                  <TableCell>To</TableCell>
                  <TableCell>At</TableCell>
                  <TableCell>Actions</TableCell>
                </Row>
              </Head>
              <Body>
              {#each userSkill.used || [] as used}
                <Row>
                  <TableCell>{used.from_date}</TableCell>
                  <TableCell>{used.to_date}</TableCell>
                  <TableCell>{used.at}</TableCell>
                  <TableCell>
                    <IconButton class="material-icons"
                                on:click$preventDefault={onUserSkillUsedEdit(used)}>
                      edit
                    </IconButton>
                    <IconButton class="material-icons"
                                on:click$preventDefault={onUserSkillUsedDelete(used)}>
                      delete
                    </IconButton>
                  </TableCell>
                </Row>
              {:else}
                Add your history with this skill
              {/each}
              </Body>
            </DataTable>
          </div>
        </Content>
      </Card>

      <CardActions>
        <Button variant="raised">
          <Icon class="material-icons">save</Icon>
          <Label>Save</Label>
        </Button>
      </CardActions>

    </form>
  </Content>
</Card>

<Dialog bind:open
        fullscreen
        aria-labelledby="mandatory-title"
        aria-describedby="mandatory-content">

  <Header>
    <Title id="title">Add Skill Used</Title>
    <IconButton action="close" class="material-icons">close</IconButton>
  </Header>

  <DialogContent id="content">
    <div>
      <Textfield bind:value={userSkillUsed.from_date} label="From" required input$maxlength={100}
                 class="luso-dialog-field-with-helper" type="date">
        <svelte:fragment slot="helper">
          <HelperText>When did you start using this skill?</HelperText>
        </svelte:fragment>
      </Textfield>
    </div>

    <div>
      <Textfield bind:value={userSkillUsed.to_date} label="To" input$maxlength={100}
                 class="luso-dialog-field-with-helper" type="date">
        <svelte:fragment slot="helper">
          <HelperText>When did you stop using this skill? If you are still using it, just leave this
            blank.
          </HelperText>
        </svelte:fragment>
      </Textfield>
    </div>

    <div>
      <Textfield bind:value={userSkillUsed.at} label="At" required input$maxlength={100}
                 class="luso-dialog-field-with-helper">
        <svelte:fragment slot="helper">
          <HelperText>Where did you use this skill?</HelperText>
        </svelte:fragment>
      </Textfield>
    </div>

  </DialogContent>

  <Actions>
    <Button on:click$preventDefault={onSubmitUserSkillUsed} variant="raised">
      <Icon class="material-icons">save</Icon>
      <Label>Save</Label>
    </Button>
  </Actions>
</Dialog>
