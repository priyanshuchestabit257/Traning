import mongoose from "mongoose";
import bcrypt from "bcrypt";

const accountSchema = new mongoose.Schema(
  {
    firstName: {
      type: String,
      required: true,
      trim: true
    },
    lastName: {
      type: String,
      required: true,
      trim: true
    },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      trim: true,
      match: /.+@.+\..+/
    },
    password: {
      type: String,
      required: true,
      minlength: 8,
      select: false
    },
    status: {
      type: String,
      enum: ["ACTIVE", "INACTIVE"],
      default: "ACTIVE"
    }
  },
  { timestamps: true }
);

/* 🔹 Compound Index */
accountSchema.index({ status: 1, createdAt: -1 });

/* 🔹 Virtual Field */
accountSchema.virtual("fullName").get(function () {
  return `${this.firstName} ${this.lastName}`;
});

/* 🔹 Pre-save Hook */
accountSchema.pre("save", async function () {
  if (!this.isModified("password")) return;

  this.password = await bcrypt.hash(this.password, 10);
});


export default mongoose.model("Account", accountSchema);
