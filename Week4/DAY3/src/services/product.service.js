import * as productRepo from "../repositories/product.repository.js";

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
  }

  const skip = (page - 1) * limit;

  return productRepo.findProducts(query, {
    sort: sortObj,
    skip,
    limit: Number(limit)
  });
};

export const deleteProduct = async (id) => {
  const product = await productRepo.findById(id);

  if (!product) {
    const error = new Error("Product not found");
    error.statusCode = 404;
    error.code = "PRODUCT_NOT_FOUND";
    throw error;
  }

  return productRepo.softDeleteById(id);
};

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


 const getAllProducts = async (queryParams) => {
  const filter = buildQuery(queryParams);

  // Sorting Logic (e.g., sort=price:desc)
  let sort = {};
  if (queryParams.sort) {
    const [field, order] = queryParams.sort.split(':');
    sort[field] = order === 'desc' ? -1 : 1;
  } else {
    sort = { createdAt: -1 }; // Default sort
  }

  // Pagination Logic
  const page = Number(queryParams.page) || 1;
  const limit = Number(queryParams.limit) || 10;
  const skip = (page - 1) * limit;

  // Execute Query
  const products = await Product.find(filter)
    .sort(sort)
    .skip(skip)
    .limit(limit);
    
  const total = await Product.countDocuments(filter);

  return { products, total, page, totalPages: Math.ceil(total / limit) };
};

const softDeleteProduct = async (id) => {
  // Instead of remove(), we update the deletedAt timestamp
  return await Product.findByIdAndUpdate(
    id, 
    { deletedAt: new Date() }, 
    { new: true }
  );
};