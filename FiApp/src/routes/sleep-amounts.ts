import { Router } from "express";
import {  SleepAmounts } from "../models/sleep-amount";

const router = Router();

// Get all sleep amounts
router.get("/", async (req, res) => {
  try {
    const sleepAmounts = await SleepAmounts.findAll();
    res.json(sleepAmounts);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch sleep amounts" });
  }
});

// Get a single sleep amount by ID
router.get("/:id", async (req, res) => {
  try {
    const sleepAmount = await SleepAmounts.findByPk(req.params.id);
    if (sleepAmount) {
      res.json(sleepAmount);
    } else {
      res.status(404).json({ error: "Sleep amount not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch sleep amount" });
  }
});

// Create a new sleep amount
router.post("/", async (req, res) => {
  try {
    // TODO: Replace raw request-body creates with an explicit field allowlist.
    const sleepAmount = await SleepAmounts.create(req.body);
    res.status(201).json(sleepAmount);
  } catch (error) {
    res.status(500).json({ error: "Failed to create sleep amount" });
  }
});

// Update a sleep amount
router.put("/:id", async (req, res) => {
  try {
    // TODO: Replace raw request-body updates with an explicit field allowlist.
    const [updated] = await SleepAmounts.update(req.body, {
      where: { id: req.params.id },
    });
    if (updated) {
      const updatedSleepAmount = await SleepAmounts.findByPk(req.params.id);
      res.json(updatedSleepAmount);
    } else {
      res.status(404).json({ error: "Sleep amount not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to update sleep amount" });
  }
});

// Delete a sleep amount
router.delete("/:id", async (req, res) => {
  try {
    const deleted = await SleepAmounts.destroy({ where: { id: req.params.id } });
    if (deleted) {
      res.status(204).json();
    } else {
      res.status(404).json({ error: "Sleep amount not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to delete sleep amount" });
  }
});

export default router;
