import UserService from "./user-service";
import {SkillPlanObjective} from "../types/api/user";
import {statuses} from "../types/api/const";

test("should calculate progress", () => {
  const userService: UserService = new UserService();

  const sp1 = new SkillPlanObjective().createDefaultInstance();
  sp1.status = statuses[0];

  const sp2 = new SkillPlanObjective().createDefaultInstance();
  sp2.status = statuses[1];

  const sp3 = new SkillPlanObjective().createDefaultInstance();
  sp3.status = statuses[2];

  let result = userService.calculateProgress([sp1, sp2, sp3]);
  expect(result).toBe(0.33);

  // empty array
  result = userService.calculateProgress([]);
  expect(result).toBe(0);

  // all done
  sp1.status = statuses[2];
  sp2.status = statuses[2];
  result = userService.calculateProgress([sp1, sp2, sp3]);
  expect(result).toBe(1);
});
