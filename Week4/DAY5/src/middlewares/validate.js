import Joi from "joi";
import { AppError } from "./error.middleware.js";

// Generic validator
export const validate = (schema, property = "body") => {
  return (req, res, next) => {
    const { error } = schema.validate(req[property], {
      abortEarly: false,
      allowUnknown: false,
    });

    if (error) {
      const message = error.details.map(d => d.message).join(", ");
      return next(new AppError(message, 400));
    }

    next();
  };
};

// Product validation
export const productSchema = Joi.object({
  name: Joi.string().min(3).max(100).required(),
  price: Joi.number().positive().required(),
  description: Joi.string().min(5).max(500).required(),
  tags: Joi.array().items(Joi.string()).min(1).required(),
});

// User validation
export const userSchema = Joi.object({
  name: Joi.string().min(3).max(50).required(),
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
});
