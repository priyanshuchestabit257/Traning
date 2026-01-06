// src/middlewares/error.middleware.js

class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;

    Error.captureStackTrace(this, this.constructor);
  }
}

const errorMiddleware = (err, req, res, next) => {
  // Default values
  const statusCode = err.statusCode || 500;
  const message =
    err.isOperational
      ? err.message
      : "Internal Server Error";

  res.status(statusCode).json({
    success: false,
    message,
    code: statusCode,
    timestamp: new Date().toISOString(),
    path: req.originalUrl,
  });
};

export { errorMiddleware, AppError };
