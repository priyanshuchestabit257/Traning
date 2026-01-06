import mongoose from "mongoose";

const productSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    price: { type: Number, required: true },
    tags: [{ type: String }],
    deletedAt: { type: Date, default: null }
  },
  { timestamps: true }
);

export default mongoose.model("Product", productSchema);
