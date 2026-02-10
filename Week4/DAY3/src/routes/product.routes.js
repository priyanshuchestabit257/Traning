import express from "express";
import { getProducts, deleteProduct,getProduct } from "../controllers/product.controller.js";

const router = express.Router();
// router.get("/:id", getProduct);
router.get("/", getProducts);
router.delete("/:id", deleteProduct);

export default router;
