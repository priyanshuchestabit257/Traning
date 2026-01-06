import { logger } from "../utils/logger.js";

export const errorMiddleware = (err, req, res, next) => {
  logger.error("Unhandled error", {
    message: err.message,
    stack: err.stack,
    requestId: req.requestId,
    path: req.originalUrl,
  });

  res.status(err.statusCode || 500).json({
    success: false,
    message: err.message || "Internal Server Error",
    requestId: req.requestId,
  });
};
