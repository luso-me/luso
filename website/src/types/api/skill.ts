import {DateTime} from "luxon";
import {estimatedEfforts, resourceCategories} from "./const";
import {defaultDuration} from "../web/date";

export class SkillResourceItem {
  id: string = "";
  name: string = "";
  description: string = "";
  web_link?: string = "";
  duration: string = "";

  createDefaultInstance() {
    this.id = "";
    this.name = "";
    this.duration = defaultDuration;
    this.web_link = "";
    this.description = "";

    return this;
  }
}

export interface DurationRange {
  min: string;
  max: string;
  period: string;
}

export class SkillResource {
  id: string = "";
  name: string = "";
  authors: string = "";
  description: string = "";
  web_link: string = "";
  category: string = "";
  resource_authored_date?: DateTime;
  resource_added_date?: DateTime;
  tags: string[] = [];
  community_rating?: number;
  duration: string = "";
  estimated_effort?: DurationRange;
  intended_levels: string[] = [];
  items: SkillResourceItem[] = [];

  createDefaultInstance() {
    this.id = "";
    this.name = "";
    this.authors = "";
    this.description = "";
    this.web_link = "";
    this.duration = defaultDuration;
    this.category = resourceCategories[0];
    this.community_rating = 0.0;
    this.intended_levels = [];

    this.estimated_effort = {
      min: defaultDuration,
      max: defaultDuration,
      period: estimatedEfforts[0]
    };

    this.items = [];

    return this;
  }
}

export class Skill {
  id: string = "";
  name: string = "";
  description: string = "";
  web_link: string = "";
  repo_link?: string = "";
  icon_link: string = "";
  tags: string[] = [];
  category: string = "";
  active?: boolean;
  resources: SkillResource[] = [];

  createDefaultInstance() {
    this.name = "";
    this.description = "";
    this.web_link = "";
    this.repo_link = "";
    this.icon_link = "";
    this.tags = [];
    this.category = "";
    this.resources = [];
    this.active = true;

    return this;
  }

}

