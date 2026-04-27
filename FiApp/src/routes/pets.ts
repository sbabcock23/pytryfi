import { Router } from "express";
import { Pet } from "../models/pet";

const router = Router();

// Get all pets
router.get("/", async (req, res) => {
  try {
    const pets = await Pet.findAll();
    res.json(pets);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch pets" });
  }
});

// Get a single pet by ID
router.get("/:id", async (req, res) => {
  try {
    const pet = await Pet.findByPk(req.params.id);
    if (pet) {
      res.json(pet);
    } else {
      res.status(404).json({ error: "Pet not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch pet" });
  }
});

// Create a new pet
router.post("/", async (req, res) => {
  try {
    // TODO: Replace raw request-body creates with an explicit field allowlist.
    const pet = await Pet.create(req.body);
    res.status(201).json(pet);
  } catch (error: any) {
    console.error("Error creating pet:", error);
    res
      .status(500)
      .json({ error: "Failed to create pet", details: error.message });

  }
});

// Update a pet
router.put("/:id", async (req, res) => {
  try {
    // TODO: Replace raw request-body updates with an explicit field allowlist.
    const [updated] = await Pet.update(req.body, {
      where: { id: req.params.id },
    });
    if (updated) {
      const updatedPet = await Pet.findByPk(req.params.id);
      res.json(updatedPet);
    } else {
      res.status(404).json({ error: "Pet not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to update pet" });
  }
});

// Delete a pet
router.delete("/:id", async (req, res) => {
  try {
    const deleted = await Pet.destroy({ where: { id: req.params.id } });
    if (deleted) {
      res.status(204).json();
    } else {
      res.status(404).json({ error: "Pet not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to delete pet" });
  }
});

export default router;
