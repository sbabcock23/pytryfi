import { Router } from "express";
import { ActivitySummary } from "../models/activity-summary";
import { DailySteps } from "../models/daily-steps";
import sequelize from "../config/database";

const router = Router();

// Get all activity summaries
router.get("/", async (req, res) => {
  try {
    const summaries = await ActivitySummary.findAll();
    res.json(summaries);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch activity summaries" });
  }
});

// Get a single activity summary by ID
router.get("/:id", async (req, res) => {
  try {
    const summary = await ActivitySummary.findByPk(req.params.id, {
      include: [DailySteps],
    });
    if (summary) {
      res.json(summary);
    } else {
      res.status(404).json({ error: "Activity summary not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch activity summary" });
  }
});

// Create a new activity summary
router.post("/", async (req, res) => {
  try {
    // TODO: Replace manual request-body mapping with shared validation/allowlists.
    const {
      start_date,
      end_date,
      period_type,
      total_steps,
      step_goal,
      dailySteps,
      total_distance,
      pet_id
    } = req.body;

    const activitySummary = await ActivitySummary.create({
      start_date,
      end_date,
      period_type,
      total_steps,
      step_goal,
      total_distance,
      pet_id
    } as ActivitySummary);

    if (dailySteps && Array.isArray(dailySteps)) {
      const dailyStepsPromises = dailySteps.map((dailyStep) => {
        return DailySteps.create({
          activity_summary_id: activitySummary.id,
          date: dailyStep.date,
          total_steps: dailyStep.total_steps,
          step_goal: dailyStep.step_goal,
        } as DailySteps);
      });

      await Promise.all(dailyStepsPromises);
    }

    res.status(201).json(activitySummary);
  } catch (error: any) {
    console.error("Error creating activity summary:", error);
    res.status(500).json({
      error: "Failed to create activity summary",
      details: error.message,
    });
  }
});

router.post("/bulk", async (req, res) => {
  const { activitySummaries } = req.body;

  // Start a transaction
  const transaction = await sequelize.transaction();

  try {
    // Loop through each activity summary
    for (const summary of activitySummaries) {
      // Create the ActivitySummary
      const activitySummary = await ActivitySummary.create(
        {
          start_date: summary.start_date,
          end_date: summary.end_date,
          period_type: summary.period_type,
          total_steps: summary.total_steps,
          step_goal: summary.step_goal,
          total_distance: summary.total_distance,
          pet_id: summary.pet_id,
        } as ActivitySummary,
        { transaction },
      );

      // Create the associated DailySteps entries
      if (summary.dailySteps && Array.isArray(summary.dailySteps)) {
        const dailyStepsData = summary.dailySteps.map(
          (dailyStep: DailySteps) => ({
            activity_summary_id: activitySummary.id,
            date: dailyStep.date,
            total_steps: dailyStep.total_steps,
            step_goal: dailyStep.step_goal,
          }),
        );

        await DailySteps.bulkCreate(dailyStepsData, { transaction });
      }
    }

    // Commit the transaction if all goes well
    await transaction.commit();
    res.status(201).json({
      message: "Activity summaries and daily steps created successfully.",
    });
  } catch (error: any) {
    // Rollback the transaction in case of any error
    await transaction.rollback();
    res.status(500).json({
      error: "Failed to create activity summaries",
      details: error.message,
    });
  }
});


// Update an activity summary
router.put("/:id", async (req, res) => {
  try {
    // TODO: Replace raw request-body updates with an explicit field allowlist.
    const [updated] = await ActivitySummary.update(req.body, {
      where: { id: req.params.id },
    });
    if (updated) {
      const updatedSummary = await ActivitySummary.findByPk(req.params.id);
      res.json(updatedSummary);
    } else {
      res.status(404).json({ error: "Activity summary not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to update activity summary" });
  }
});

// Delete an activity summary
router.delete("/:id", async (req, res) => {
  try {
    const deleted = await ActivitySummary.destroy({
      where: { id: req.params.id },
    });
    if (deleted) {
      res.status(204).json();
    } else {
      res.status(404).json({ error: "Activity summary not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to delete activity summary" });
  }
});

export default router;
