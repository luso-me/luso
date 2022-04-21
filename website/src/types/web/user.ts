import {SkillPlan, SkillPlanObjective} from "../api/user";

export class MissionObjective extends SkillPlanObjective {

  resource_name: string;
  resource_web_link;
  resource_item_name: string;
  resource_item_web_link: string;
  duration: string;

}

export class MissionPlan extends SkillPlan {

  skill_name: string;
  progress: number;
  objectives: MissionObjective[];

  createDefaultInstance() {
    this.objectives = [];

    return this;
  }

}
