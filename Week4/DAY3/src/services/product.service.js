import * as productRepo from "../repositories/product.repository.js";

/**
 * GET PRODUCTS (with soft delete support)
 */
export const getProducts = async (queryParams) => {
  const {
    search,
    minPrice,
    maxPrice,
    sort,
    page = 1,
    limit = 10,
    includeDeleted
  } = queryParams;

  const includeDeletedBool =
    includeDeleted === "true" || includeDeleted === true;

  const query = {};

  // ✅ IMPORTANT: filter soft-deleted records
  if (!includeDeletedBool) {
    query.deletedAt = null;
  }

  if (search) {
    query.name = { $regex: search, $options: "i" };
  }

  if (minPrice || maxPrice) {
    query.price = {};
    if (minPrice) query.price.$gte = Number(minPrice);
    if (maxPrice) query.price.$lte = Number(maxPrice);
  }

  let sortObj = {};
  if (sort) {
    const [field, order] = sort.split(":");
    sortObj[field] = order === "desc" ? -1 : 1;
  } else {
    sortObj = { createdAt: -1 };
  }

  const skip = (page - 1) * limit;

  return productRepo.findProducts(query, {
    sort: sortObj,
    skip,
    limit: Number(limit)
  });
};

/**
 * SOFT DELETE PRODUCT
 */
export const deleteProduct = async (id) => {
  const product = await productRepo.findById(id);

  if (!product || product.deletedAt) {
    const error = new Error("Product not found");
    error.statusCode = 404;
    error.code = "PRODUCT_NOT_FOUND";
    throw error;
  }

  return productRepo.softDeleteById(id);
};

/**
 * GET PRODUCT BY ID
 */
export const getProductById = async (id) => {
  const product = await productRepo.findById(id);

  if (!product || product.deletedAt) {
    const error = new Error("Product not found");
    error.statusCode = 404;
    error.code = "PRODUCT_NOT_FOUND";
    throw error;
  }

  return product;
};
