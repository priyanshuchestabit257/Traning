import mongoose from "mongoose";

const orderSchema = new mongoose.Schema(
  {
    accountId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Account",
      required: true
    },
    items: [
      {
        productName: String,
        price: Number,
        quantity: Number
      }
    ],
    status: {
      type: String,
      enum: ["PENDING", "PAID", "CANCELLED"],
      default: "PENDING"
    },
    totalAmount: {
      type: Number
    }
  },
  { timestamps: true }
);

/* 🔹 Compound Index */
orderSchema.index({ status: 1, createdAt: -1 });

/* 🔹 Pre-save Hook (compute total) */
orderSchema.pre("save", function (next) {
  this.totalAmount = this.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  next();
});

export default mongoose.model("Order", orderSchema);
