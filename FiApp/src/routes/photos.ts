import { Router } from "express";
import { Photo } from "../models/photo";

const router = Router();

// Get all photos
router.get("/", async (req, res) => {
  try {
    const photos = await Photo.findAll();
    res.json(photos);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch photos" });
  }
});

// Get a single photo by ID
router.get("/:id", async (req, res) => {
  try {
    const photo = await Photo.findByPk(req.params.id);
    if (photo) {
      res.json(photo);
    } else {
      res.status(404).json({ error: "Photo not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch photo" });
  }
});

// Create a new photo
router.post("/", async (req, res) => {
  try {
    // TODO: Replace raw request-body creates with an explicit field allowlist.
    const photo = await Photo.create(req.body);
    res.status(201).json(photo);
  } catch (error) {
    res.status(500).json({ error: "Failed to create photo" });
  }
});

// Update a photo
router.put("/:id", async (req, res) => {
  try {
    // TODO: Replace raw request-body updates with an explicit field allowlist.
    const [updated] = await Photo.update(req.body, {
      where: { id: req.params.id },
    });
    if (updated) {
      const updatedPhoto = await Photo.findByPk(req.params.id);
      res.json(updatedPhoto);
    } else {
      res.status(404).json({ error: "Photo not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to update photo" });
  }
});

// Delete a photo
router.delete("/:id", async (req, res) => {
  try {
    const deleted = await Photo.destroy({ where: { id: req.params.id } });
    if (deleted) {
      res.status(204).json();
    } else {
      res.status(404).json({ error: "Photo not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to delete photo" });
  }
});

export default router;
