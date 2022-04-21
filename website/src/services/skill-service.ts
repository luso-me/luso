import API from "../api";

class SkillService {

  getAll(): Promise<any> {
    return API.get("/skills?limit=1000");
  }

  get(id: any): Promise<any> {
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
