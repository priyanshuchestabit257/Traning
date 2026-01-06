import Account from "../models/Account.js";

class AccountRepository {
  create(data) {
    return Account.create(data);
  }

  findById(id) {
    return Account.findById(id);
  }

  findPaginated({ status, limit = 10, cursor }) {
    const query = {};
    if (status) query.status = status;
    if (cursor) query._id = { $lt: cursor };

    return Account.find(query)
      .sort({ createdAt: -1 })
      .limit(limit);
  }

  update(id, data) {
    return Account.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true
    });
  }

  delete(id) {
    return Account.findByIdAndDelete(id);
  }
}

export default new AccountRepository();
