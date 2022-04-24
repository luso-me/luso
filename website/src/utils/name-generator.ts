export class NameGenerator {
  static capitalizeFirst(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  static getRandomInt(max: number) {
    return Math.floor(Math.random() * max);
  }

  static generateName() {
    const name1 = ["operation", "mission", "tour"];
    const name2 = ["eagle", "success", "light", "conquest", "bear", "night", "day"];

    const randomName1 = this.capitalizeFirst(name1[this.getRandomInt(name1.length)]);
    const randomName2 = this.capitalizeFirst(name2[this.getRandomInt(name2.length)]);

    return randomName1 + " " + randomName2;
  }
}
