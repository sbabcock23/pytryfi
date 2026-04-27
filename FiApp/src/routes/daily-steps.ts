import { Router } from "express";
import {  DailySteps } from "../models/daily-steps";

const router = Router();

// Get all daily steps
router.get("/", async (req, res) => {
  try {
    const dailySteps = await DailySteps.findAll();
    res.json(dailySteps);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch daily steps" });
  }
});

// Get a single daily step by ID
router.get("/:id", async (req, res) => {
  try {
    const dailyStep = await DailySteps.findByPk(req.params.id);
    if (dailyStep) {
      res.json(dailyStep);
    } else {
      res.status(404).json({ error: "Daily step not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch daily step" });
  }
});

// Create a new daily step
router.post("/", async (req, res) => {
  try {
    // TODO: Replace raw request-body creates with an explicit field allowlist.
    const dailyStep = await DailySteps.create(req.body);
    res.status(201).json(dailyStep);
  } catch (error) {
    res.status(500).json({ error: "Failed to create daily step" });
  }
});

// Update a daily step
router.put("/:id", async (req, res) => {
  try {
    // TODO: Replace raw request-body updates with an explicit field allowlist.
    const [updated] = await DailySteps.update(req.body, {
      where: { id: req.params.id },
    });
    if (updated) {
      const updatedDailyStep = await DailySteps.findByPk(req.params.id);
      res.json(updatedDailyStep);
    } else {
      res.status(404).json({ error: "Daily step not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to update daily step" });
  }
});

// Delete a daily step
router.delete("/:id", async (req, res) => {
  try {
    const deleted = await DailySteps.destroy({ where: { id: req.params.id } });
    if (deleted) {
      res.status(204).json();
    } else {
      res.status(404).json({ error: "Daily step not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to delete daily step" });
  }
});

export default router;
