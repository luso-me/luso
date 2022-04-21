import API from "../api";
import {SkillPlan, SkillPlanObjective, User} from "../types/api/user";
import {Skill, SkillResource} from "../types/api/skill";
import {MissionObjective, MissionPlan} from "../types/web/user";
import {userInfoStore} from "../stores";

class UserService {

  updateUserInfoStore() {
    this.me().then(user=>{
      userInfoStore.update(u => {
        u.id = user.id;
        u.gold = user.score.gold;
        u.points = user.score.points;
        return u;
      })
    }).catch((err)=>{
        console.log("failed to update user", err)
    })
  }

  getAll(): Promise<any> {
    return API.get("/users");
  }

  get(id: any): Promise<any> {
    return API.get(`/users/${id}`);
  }

  me(): Promise<any> {
    return API.get(`/users/me`);
  }

  create(data: any): Promise<any> {
    return API.post("/users", data);
  }

  update(id: any, data: any): Promise<any> {
    return API.put(`/users/${id}`, data);
  }

  delete(id: any): Promise<any> {
    return API.delete(`/users/${id}`);
  }

  calculateProgress(spos: SkillPlanObjective[]): number {
    if (spos.length === 0) {
      return 0;
    }

    const done = spos.filter(c => c.status === "Done").length;

    return Math.trunc((done / spos.length) * 100) / 100;
  }

  createMissionPlan(skills: Skill[], sp: SkillPlan) {
    const skill: Skill[] = skills.filter(s => s.id === sp.skill_id);

    if (skill.length === 0) {
      throw new Error("Skill could not be found");
    }

    let mp = new MissionPlan().createDefaultInstance();

    mp.id = sp.id;
    mp.plan_name = sp.plan_name;
    mp.skill_name = skill[0].name;
    mp.progress = this.calculateProgress(sp.objectives);
    mp.status = sp.status;
    mp.start_date = sp.start_date;
    mp.end_date = sp.end_date;

    sp.objectives.forEach(skillPlanObjective => {
      mp.objectives.push(this.createMissionObjective(skill[0], skillPlanObjective));
    });

    return mp;
  }

  createMissionObjective(skill: Skill, spo: SkillPlanObjective) {
    let mo = new MissionObjective();

    const resource: SkillResource[] = skill.resources.filter(r => r.id === spo.resource_id);
    const resourceItem = resource[0].items.filter(ri => ri.id === spo.resource_item_id);

    mo.id = spo.id;
    mo.resource_id = spo.resource_id;
    mo.resource_item_id = spo.resource_item_id;
    mo.start_date = spo.start_date;
    mo.end_date = spo.end_date;
    mo.status = spo.status;

    mo.resource_name = resource[0].name;
    mo.resource_web_link = resource[0].web_link;
    mo.resource_item_name = resourceItem[0].name;
    mo.resource_item_web_link = resourceItem[0].web_link;
    mo.duration = resourceItem[0].duration;

    return mo;
  }
}

export default UserService;
