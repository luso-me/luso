import {DateTime} from "luxon";
import {statuses} from "./const";


export class UserSkillUsed {
  from_date: string = "";
  to_date?: string = "";
  at: string = "";

  createDefaultInstance() {
    this.at = "";
    this.from_date = "";
    this.to_date = "";

    return this;
  }
}

export class UserSkill {
  skill_id: string = "";
  user_rating: string = "";
  score: number = 0;
  confidence: number = 0;
  notes: string = "";
  used: UserSkillUsed[] = [];

  createDefaultInstance() {
    this.notes = "";
    this.used = [];

    return this;
  }
}

export interface UserScore {
  gold: number;
  points: number;
}

export class User {
  id: string = "";
  username: string = "";
  github_user_id: string = "";
  display_name: string = "";
  active!: boolean;
  email?: string;
  password?: string;
  skills?: UserSkill[];
  plans: SkillPlan[] = [];
  score!: UserScore;

  createDefaultInstance() {
    this.plans = [];
    this.display_name = "";
    this.github_user_id = "";
    this.username = "";
    this.skills = [];
    this.active = true;

    return this;
  }

}

export interface UserInfo {
  id: string;
  gold: number;
  points: number;
}

export class SkillPlanObjective {
  id: string = "";
  resource_id: string = "";
  resource_item_id: string = "";
  start_date!: DateTime;
  end_date!: DateTime;
  status: string = "";

  createDefaultInstance() {
    this.id = "";

    return this;
  }
}

export class SkillPlan {

  id: string = "";
  plan_name: string = "";
  skill_id: string = "";
  start_date!: DateTime;
  end_date!: DateTime;
  time_horizon: string = "";
  notes: string = "";
  status: string = "";
  objectives: SkillPlanObjective[] = [];

  createDefaultInstance() {
    this.plan_name = "";
    this.notes = "";
    this.status = statuses[0];
    this.objectives = [];

    return this;
  }

  typeConvert() {
    this.start_date = DateTime.fromISO(this.start_date.toString());
    this.end_date = DateTime.fromISO(this.end_date.toString());

    return this;
  }

}
