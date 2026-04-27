import { Sequelize } from "sequelize-typescript";
import { User } from "../models/user";
import { Breed } from "../models/breed";
import { Pet } from "../models/pet";
import { Photo } from "../models/photo";
import { Device } from "../models/device";
import { ActivitySummary } from "../models/activity-summary";
import { DailySteps } from "../models/daily-steps";
import { RestSummary } from "../models/rest-summary";
import { SleepAmounts } from "../models/sleep-amount";

const sequelize = new Sequelize({
  database: "Fi_Collar_Data",
  dialect: "postgres",
  username: "postgres",
  port: 5433,
  password:
    "RDF6*KUD.BRQrbJ!k8tTR-FDEJ*!DxhEu99fR@@KYGKDcvbRqjxcJtiq*Kn!tvjx-Y.gDL8raLZZ2",
  models: [
    User,
    Breed,
    Pet,
    Photo,
    Device,
    ActivitySummary,
    DailySteps,
    RestSummary,
    SleepAmounts,
  ],
});

export default sequelize;
