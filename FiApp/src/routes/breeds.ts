import { Router } from "express";
import { Breed } from "../models/breed";

const router = Router();

// Get all breeds
router.get("/", async (req, res) => {
  try {
    const breeds = await Breed.findAll();
    res.json(breeds);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch breeds" });
  }
});

// Get a single breed by ID
router.get("/:id", async (req, res) => {
  try {
    const breed = await Breed.findByPk(req.params.id);
    if (breed) {
      res.json(breed);
    } else {
      res.status(404).json({ error: "Breed not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch breed" });
  }
});

// Create a new breed
router.post("/", async (req, res) => {
  try {
    // TODO: Replace raw request-body creates with an explicit field allowlist.
    const breed = await Breed.create(req.body);
    res.status(201).json(breed);
  } catch (error:any) {

    console.error("Error creating breed:", error);
    res
      .status(500)
      .json({ error: "Failed to create breed", details: error.message });
  }
});

// Update a breed
router.put("/:id", async (req, res) => {
  try {
    // TODO: Replace raw request-body updates with an explicit field allowlist.
    const [updated] = await Breed.update(req.body, {
      where: { id: req.params.id },
    });
    if (updated) {
      const updatedBreed = await Breed.findByPk(req.params.id);
      res.json(updatedBreed);
    } else {
      res.status(404).json({ error: "Breed not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to update breed" });
  }
});

// Delete a breed
router.delete("/:id", async (req, res) => {
  try {
    const deleted = await Breed.destroy({ where: { id: req.params.id } });
    if (deleted) {
      res.status(204).json();
    } else {
      res.status(404).json({ error: "Breed not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to delete breed" });
  }
});

export default router;
