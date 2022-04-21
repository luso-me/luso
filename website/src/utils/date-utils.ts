import humanizeDuration from "humanize-duration";
import {DateTime} from "luxon";

export const shortHumanizer = humanizeDuration.humanizer({
  largest: 1,
  round: false,
  language: "shortEn",
  languages: {
    shortEn: {
      y: () => "y",
      mo: () => "mo",
      w: () => "w",
      d: () => "d",
      h: () => "h",
      m: () => "m",
      s: () => "s",
      ms: () => "ms",
    },
  },
});

export const longHumanizer = humanizeDuration.humanizer({
  largest: 1,
  round: false,
});

export class DateUtils {

  static determineEndDateForTimeHorizon(time_horizon: string, now: DateTime) {
    // because we get a string back from the server and not doing any forced conversion
    // into DateTime type
    if (typeof now === 'string') {
      now = DateTime.fromISO(now);
    }

    if (time_horizon.endsWith("3 months")) {
      return now.plus({months: 3});
    }

    if (time_horizon.endsWith("6 months")) {
      return now.plus({months: 6});
    }

    if (time_horizon.endsWith("1 year")) {
      return now.plus({year: 1});
    }

    if (time_horizon.endsWith("3 years")) {
      return now.plus({year: 3});
    }

    if (time_horizon.endsWith("3+ years")) {
      return now.plus({year: 5});
    }
  }
}
