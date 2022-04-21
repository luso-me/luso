import {Duration} from "luxon";
import {durations} from "../api/const";

export const defaultDuration: string = "PT0M";

export class LusoDuration {
  value: number;
  unit: string;

  createDefaultInstance() {
    this.value = 0;
    this.unit = durations[0];

    return this;
  }

  calculateDuration() {
    if (!this.value) {
      this.value = 0;
    }

    return this.getDuration();
  }

  private getDuration() {
    if (this.unit === "Minutes") {
      return Duration.fromObject({minutes: this.value}).toISO();
    }

    if (this.unit === "Hours") {
      return Duration.fromObject({hours: this.value}).toISO();
    }

    if (this.unit === "Days") {
      return Duration.fromObject({days: this.value}).toISO();
    }

    if (this.unit === "Weeks") {
      return Duration.fromObject({weeks: this.value}).toISO();
    }

    if (this.unit === "Months") {
      return Duration.fromObject({months: this.value}).toISO();
    }
  }

  createInstance(duration: string): LusoDuration {
    this.value = parseInt(duration.replace(/[^0-9]/g, ''));

    if (duration.startsWith("PT") && duration.endsWith("M")) {
      this.unit = durations[0];
      return this;
    }

    if (duration.endsWith("H")) {
      this.unit = durations[1];
      return this;
    }

    if (duration.endsWith("D")) {
      this.unit = durations[2];
      return this;
    }

    if (duration.endsWith("W")) {
      this.unit = durations[3];
      return this;
    }

    if (duration.startsWith("P") && duration.endsWith("M")) {
      this.unit = durations[4];
      return this;
    }

    return this;
  }

}
