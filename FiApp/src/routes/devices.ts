import { Router } from "express";
import { Device } from "../models/device";

const router = Router();

// Get all devices
router.get("/", async (req, res) => {
  try {
    const devices = await Device.findAll();
    res.json(devices);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch devices" });
  }
});

// Get a single device by ID
router.get("/:id", async (req, res) => {
  try {
    const device = await Device.findByPk(req.params.id);
    if (device) {
      res.json(device);
    } else {
      res.status(404).json({ error: "Device not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch device" });
  }
});

// Create a new device
router.post("/", async (req, res) => {
  try {
    // TODO: Replace raw request-body creates with an explicit field allowlist.
    const device = await Device.create(req.body);
    res.status(201).json(device);
  } catch (error) {
    res.status(500).json({ error: "Failed to create device" });
  }
});

// Update a device
router.put("/:id", async (req, res) => {
  try {
    // TODO: Replace raw request-body updates with an explicit field allowlist.
    const [updated] = await Device.update(req.body, {
      where: { id: req.params.id },
    });
    if (updated) {
      const updatedDevice = await Device.findByPk(req.params.id);
      res.json(updatedDevice);
    } else {
      res.status(404).json({ error: "Device not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to update device" });
  }
});

// Delete a device
router.delete("/:id", async (req, res) => {
  try {
    const deleted = await Device.destroy({ where: { id: req.params.id } });
    if (deleted) {
      res.status(204).json();
    } else {
      res.status(404).json({ error: "Device not found" });
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to delete device" });
  }
});

export default router;
