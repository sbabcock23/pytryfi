import { Router } from "express";
import usersRouter from "./users";
import breedsRouter from "./breeds";
import petsRouter from "./pets";
import photosRouter from "./photos";
import devicesRouter from "./devices";
import activitySummariesRouter from "./activitiy-summaries";
import dailyStepsRouter from "./daily-steps";
import restSummariesRouter from "./rest-summaries";
import sleepAmountsRouter from "./sleep-amounts";

const router = Router();

router.use("/users", usersRouter);
router.use("/breeds", breedsRouter);
router.use("/pets", petsRouter);
router.use("/photos", photosRouter);
router.use("/devices", devicesRouter);
router.use("/activitySummaries", activitySummariesRouter);
router.use("/dailySteps", dailyStepsRouter);
router.use("/restSummaries", restSummariesRouter);
router.use("/sleepAmounts", sleepAmountsRouter);

export default router;
