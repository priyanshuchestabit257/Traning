import express from "express";
import { addEmailJob } from "../controllers/email.controller.js";

const router = express.Router();

router.post("/", addEmailJob);

export default router;
