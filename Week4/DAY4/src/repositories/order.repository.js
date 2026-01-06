import Order from "../models/Order.js";

class OrderRepository {
  create(data) {
    return Order.create(data);
  }

  findById(id) {
    return Order.findById(id).populate("accountId");
  }

  findPaginated({ status, limit = 10, cursor }) {
    const query = {};
    if (status) query.status = status;
    if (cursor) query._id = { $lt: cursor };

    return Order.find(query)
      .sort({ createdAt: -1 })
      .limit(limit);
  }

  update(id, data) {
    return Order.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true
    });
  }

  delete(id) {
    return Order.findByIdAndDelete(id);
  }
}

export default new OrderRepository();
