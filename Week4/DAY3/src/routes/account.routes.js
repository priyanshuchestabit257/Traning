import express from "express";
import accountRepository from "../repositories/account.repository.js";

const router = express.Router();

/* CREATE ACCOUNT */
router.post("/", async (req, res) => {
  try {
    const account = await accountRepository.create(req.body);
    res.status(201).json(account);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

/* GET ACCOUNT BY ID */
router.get("/:id", async (req, res) => {
  try {
    const account = await accountRepository.findById(req.params.id);
    if (!account) return res.status(404).json({ message: "Not found" });
    res.json(account);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

export default router;
