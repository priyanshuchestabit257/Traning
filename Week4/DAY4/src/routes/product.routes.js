import express from "express";
import {
  getProducts,
  deleteProduct,
  getProduct,
  createProduct
} from "../controllers/product.controller.js";
import { validate, productSchema } from "../middlewares/validate.js";

const router = express.Router();

router.get("/:id", getProduct);
router.get("/", getProducts);

router.post(
  "/",
  validate(productSchema),
  createProduct
);

router.delete("/:id", deleteProduct);

export default router;
