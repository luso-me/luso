import API from "../api";
import {Skill} from "../types/api/skill";

class SkillService {
  getAll(): Promise<Skill[]> {
    return API.get("/skills?limit=1000");
  }

  get(id: any): Promise<Skill> {
    return API.get(`/skills/${id}`);
  }

  create(data: any): Promise<any> {
    return API.post("/skills", data);
  }

  update(id: any, data: any): Promise<any> {
    return API.put(`/skills/${id}`, data);
  }

  delete(id: any): Promise<any> {
    return API.delete(`/skills/${id}`);
  }
}

export default SkillService;
