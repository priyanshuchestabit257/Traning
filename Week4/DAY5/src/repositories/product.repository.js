import Product from "../models/product.model.js";

export const findProducts = (query, options) => {
  return Product.find(query)
    .sort(options.sort)
    .skip(options.skip)
    .limit(options.limit);
};

export const softDeleteById = (id) => {
  return Product.findByIdAndUpdate(
    id,
    { deletedAt: new Date() },
    { new: true }
  );
};

export const findById = (id) => {
  return Product.findOne({ _id: id, deletedAt: null });
};
