import {SkillResource, SkillResourceItem} from "../../../types/api/skill";

const x = new SkillResource().createDefaultInstance();
x.id = "x";

const x1 = new SkillResourceItem().createDefaultInstance();
x1.id = "x1";

const x2 = new SkillResourceItem().createDefaultInstance();
x2.id = "x2";

const x3 = new SkillResourceItem().createDefaultInstance();
x3.id = "x3";

x.items.push(x1, x2, x3);

const y = new SkillResource().createDefaultInstance();
y.id = "y";

const y4 = new SkillResourceItem().createDefaultInstance();
y4.id = "y4";

const y5 = new SkillResourceItem().createDefaultInstance();
y5.id = "y5";

const y6 = new SkillResourceItem().createDefaultInstance();
y6.id = "y6";

y.items.push(y4, y5, y6);


test("test unchecked all", () => {
  let master = [x1, x2, x3];
  let checked = [];
  let added = [x1, x2, x3];
  let expected = [];

  let result = doStuff(master, checked, added)

  expect(result.length).toBe(expected.length);
});

test("test checked none multiple addeds", () => {
  let master = [x1, x2, x3];
  let checked = [x1, x3];
  let added = [x1, x2, x3];
  let expected = [x1, x3];

  let result = doStuff(master, checked, added)

  expect(result.length).toBe(expected.length);
  expect(result[0]).toBe(expected[0]);
  expect(result[1]).toBe(expected[1]);
});

test("test swap multiple addeds", () => {
  let master = [x1, x2, x3];
  let checked = [x1, x3];
  let added = [x2, y4];
  let expected = [x1, x3, y4];

  let result = doStuff(master, checked, added)

  expect(result.length).toBe(expected.length);
  expect(result[0]).toBe(expected[2]);
  expect(result[1]).toBe(expected[0]);
  expect(result[2]).toBe(expected[1]);
});

test("test swap single added", () => {
  let master = [x1, x2, x3];
  let checked = [x1];
  let added = [x2];
  let expected = [x1];

  let result = doStuff(master, checked, added)

  expect(result.length).toBe(1);
  expect(result[0]).toBe(expected[0]);
});

test("test empty added", () => {
  let master = [x1, x2];
  let checked = [x1];
  let added = [];
  let expected = [x1];

  let result = doStuff(master, checked, added)

  expect(result.length).toBe(1);
  expect(result[0]).toBe(expected[0]);
});

function doStuff(master: SkillResourceItem[],
                 checked: SkillResourceItem[],
                 added: SkillResourceItem[]) {

  let masterChecked = master.filter(i => !checked.map(s => s.id).includes(i.id));
  added = added.filter(a => !masterChecked.includes(a));

  checked.forEach(i => {
    if (!added.includes(i)) {
      added.push(i);
    }
  });

  return added;
}

