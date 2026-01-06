// middlewares/error.middleware.js

class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
  }
}

const errorMiddleware = (err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';

  // Requirement: Global error formats
  res.status(statusCode).json({
    success: false,
    message: message,
    code: statusCode,
    timestamp: new Date().toISOString(),
    path: req.originalUrl, 
  });
};

export { errorMiddleware, AppError };
