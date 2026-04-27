import { Router } from "express";
import { RestSummary } from "../models/rest-summary";

const router = Router();

// Get all rest summaries
router.get("/", async (req, res) => {
  try {
    const summaries = await RestSummary.findAll();
    res.json(summaries);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch rest summaries" });
  }
});

// Get a single rest summary by ID
router.get("/:id", async (req, res) => {
  try {
    const summary = await RestSummary.findByPk(req.params.id);
    if (summary) {
      res.json(summary);
    } else {
      res.status(404).json({ error: "Rest summary not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch rest summary" });
  }
});

// Create a new rest summary
router.post("/", async (req, res) => {
  try {
    // TODO: Replace raw request-body creates with an explicit field allowlist.
    const summary = await RestSummary.create(req.body);
    res.status(201).json(summary);
  } catch (error) {
    res.status(500).json({ error: "Failed to create rest summary" });
  }
});

// Update a rest summary
router.put("/:id", async (req, res) => {
  try {
    // TODO: Replace raw request-body updates with an explicit field allowlist.
    const [updated] = await RestSummary.update(req.body, {
      where: { id: req.params.id },
    });
    if (updated) {
      const updatedSummary = await RestSummary.findByPk(req.params.id);
      res.json(updatedSummary);
    } else {
      res.status(404).json({ error: "Rest summary not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to update rest summary" });
  }
});

// Delete a rest summary
router.delete("/:id", async (req, res) => {
  try {
    const deleted = await RestSummary.destroy({ where: { id: req.params.id } });
    if (deleted) {
      res.status(204).json();
    } else {
      res.status(404).json({ error: "Rest summary not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to delete rest summary" });
  }
});

export default router;
