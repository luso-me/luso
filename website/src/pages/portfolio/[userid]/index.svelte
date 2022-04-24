<script lang="ts">

  import {Title} from "@smui/dialog";
  import {Skill} from "../../../types/api/skill";
  import {User} from "../../../types/api/user";
  import {UserSkill} from "../../../types/api/user";
  import {onMount} from "svelte";
  import LayoutGrid, {Cell} from "@smui/layout-grid";
  import Card, {Content} from "@smui/card";
  import UserService from "../../../services/user-service";
  import SkillService from "../../../services/skill-service";
  import Button, {Icon, Label} from "@smui/button";
  import {url, goto, params} from "@roxi/routify";
  import {skillCategories} from "../../../types/api/const";
  import Paper from "@smui/paper";
  import {PortfolioItem} from "../../../types/web/skill";
  import Chip, {Set, Text} from "@smui/chips";

  let open = false;
  let user: User = new User().createDefaultInstance();
  let userSkill: UserSkill = new UserSkill().createDefaultInstance();
  let selectedSkill: Skill = new Skill().createDefaultInstance();
  let skills: Skill[] = [];
  let portfolioItems: PortfolioItem[] = [];
  const userService: UserService = new UserService();
  const skillService: SkillService = new SkillService();

  onMount(async () => {
    user = await userService.get($params.userid);
    skills = await skillService.getAll();

    user.skills.forEach(userSkill => {
      const exist = skills.find(s => s.id === userSkill.skill_id);
      if (exist) {
        portfolioItems.push(_createPortfolioItem(exist, userSkill));
      }
    });

    portfolioItems = portfolioItems.sort((a, b) => a.name.localeCompare(b.name));
  });

  function _createPortfolioItem(skill: Skill, userSkill: UserSkill): PortfolioItem {
    let portfolioItem: PortfolioItem = new PortfolioItem().createDefaultInstance();

    portfolioItem.icon_link = skill.icon_link;
    portfolioItem.id = skill.id;
    portfolioItem.name = skill.name;
    portfolioItem.category = skill.category;
    portfolioItem.user_rating = _formatUserRating(userSkill)

    return portfolioItem;
  }

  function _formatUserRating(userSkill: UserSkill): string {
    return userSkill.user_rating.replace(/\(.*\)/g, "");
  }
</script>

<h1 class="ml-4">Portfolio</h1>

<Card variant="outlined" class="luso-background-light">
  <Content>
    <LayoutGrid>
      <Cell span="{12}">
        <Button
            on:click="{() => $goto('/portfolio/:userid/skill/create', {userid: user.id})}"
            variant="raised">
          <Icon class="material-icons">add</Icon>
          <Label>Add My Skill</Label>
        </Button>
      </Cell>

      <Cell span={12}>
        <div class="card-display">
          <div class="card-container">
            {#each skillCategories as category}
              <Paper class="luso-paper-portfolio-category">
                <Title>{category}</Title>
                <div class="column-content">
                  {#each portfolioItems as item}
                    {#if item.category === category}
                      <div class="luso-portfolio-item-wrap">
                        <div class="luso-portfolio-item">
                          <div class="luso-portfolio-item-logo-wrap">
                            <a href="{$url('/portfolio/:userid/skill/:skillid/edit',
                            {userid: user.id, skillid: item.id})}">
                              <img src="{item.icon_link}" alt="{item.name}"
                                   class="luso-portfolio-item-logo">
                            </a>
                          </div>
                          <div class="luso-portfolio-item-info">
                            <div class="luso-portfolio-item-title">
                              {item.name}
                            </div>
                            <div class="luso-portfolio-item-funding">
                                My Rating:
                                <Set chips={[item.user_rating]} let:chip nonInteractive>
                                  <Chip {chip} class="luso-portfolio-item-chip">
                                    <Text>{chip}</Text>
                                  </Chip>
                                </Set>
                            </div>
                          </div>
                        </div>
                      </div>
                    {/if}
                  {/each}
                </div>
              </Paper>
            {/each}
          </div>
        </div>
      </Cell>

    </LayoutGrid>
  </Content>
</Card>
