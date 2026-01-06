# Product API Query Engine Documentation

This API supports advanced querying features including dynamic search, complex filtering, sorting, pagination, and soft-delete management.

## Base URL
`GET /products`

---

## 1. Filtering & Search Parameters

| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `search` | String | Performs a partial regex match (case-insensitive) on `name` or `description`. | `?search=phone` |
| `minPrice` | Number | Filters products with price greater than or equal to this value. | `?minPrice=100` |
| `maxPrice` | Number | Filters products with price less than or equal to this value. | `?maxPrice=1000` |
| `tags` | String | Comma-separated list of tags. Returns products containing *any* of the tags. | `?tags=apple,samsung` |

---

## 2. Sorting & Pagination

| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `sort` | String | Sorts results by field. Format: `field:order` (`asc` or `desc`). | `?sort=price:desc` |
| `page` | Number | The page number for pagination (default: 1). | `?page=2` |
| `limit` | Number | Number of items per page (default: 10). | `?limit=5` |

---

## 3. Soft Delete Management

| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `includeDeleted`| Boolean | If set to `true`, the response includes items that have been soft-deleted (where `deletedAt` is not null). | `?includeDeleted=true` |

---

## Example Scenarios

### 1. Complex Search
**Goal:** Find phones between $500 and $1000, sorted by newest first.
`GET /products?search=phone&minPrice=500&maxPrice=1000&sort=createdAt:desc`

### 2. Tag Filtering
**Goal:** Find all Apple or Dell products.
`GET /products?tags=apple,dell`

### 3. Data Recovery (Soft Delete)
**Goal:** View all products, including those that were deleted.
`GET /products?includeDeleted=true`

---

## Error Responses
All errors follow the unified error contract:
```json
{
  "success": false,
  "message": "Product not found",
  "code": 404,
  "timestamp": "2025-12-31T10:00:00.000Z",
  "path": "/products/123"
}