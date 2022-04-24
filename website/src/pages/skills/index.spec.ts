import {render, waitFor} from "@testing-library/svelte";
import skills_index from "./index.svelte";
import {mocked} from "jest-mock";
import SkillService from "../../services/skill-service";
import {Skill} from "../../types/api/skill";


// start mock skill service
const mockGetAll = jest.fn(() => {
  let skill = new Skill().createDefaultInstance();
  skill.id = "123";
  skill.name = "Airflow";

  return [skill];
});

jest.mock("../../services/skill-service", jest.fn(() => {
  return {
    __esModule: true,
    default: jest.fn().mockImplementation(() => {
      return {
        getAll: mockGetAll
      }
    })
  }
}));
const mockedSkillService = mocked(new SkillService());

// invoke test
it.skip("is currently broken because of routify/store", async () => {
  const results = render(skills_index);

  await waitFor(() => {
    expect(results.getByText("Airflow")).toBeInTheDocument();
  })
});
