import { v4 as uuidv4 } from "uuid";
import { logger } from "./logger.js";

export const tracingMiddleware = (req, res, next) => {
  const requestId = req.headers["x-request-id"] || uuidv4();
  req.requestId = requestId;

  res.setHeader("X-Request-ID", requestId);

  const start = Date.now();

  res.on("finish", () => {
    logger.info("HTTP request", {
      requestId,
      method: req.method,
      url: req.originalUrl,
      statusCode: res.statusCode,
      responseTimeMs: Date.now() - start,
    });
  });

  next();
};
