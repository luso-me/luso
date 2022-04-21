import {Skill} from "../api/skill";

export class PortfolioItem extends Skill {

  user_rating: string;

  createDefaultInstance() {
    this.user_rating = "";

    return this;
  }

}
