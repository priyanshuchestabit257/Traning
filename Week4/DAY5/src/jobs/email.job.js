import { Worker } from "bullmq";
import { redisConnection } from "../utils/redis.js";
import { logger } from "../utils/logger.js";

const emailWorker = new Worker(
  "email-queue",
  async (job) => {
    const { to, subject, requestId } = job.data;

    logger.info("Email job started", {
      jobId: job.id,
      to,
      requestId,
    });

   
    await new Promise((resolve) => setTimeout(resolve, 2000));

    
    if (Math.random() < 0.4) {
      throw new Error("SMTP server error");
    }

    logger.info("Email job sent successfully", {
      jobId: job.id,
      to,
      requestId,
    });

    return { success: true };
  },
  {
    connection: redisConnection,
  }
);

// Job lifecycle logs
emailWorker.on("completed", (job) => {
  logger.info("Email job completed", {
    jobId: job.id,
    requestId: job.data.requestId,
  });
});

emailWorker.on("failed", (job, err) => {
  logger.error("Email job failed", {
    jobId: job?.id,
    error: err.message,
    requestId: job?.data?.requestId,
  });
});

console.log(" Email worker is running...");
