import { Queue } from "bullmq";
import { redisConnection } from "../utils/redis.js";

export const emailQueue = new Queue("email-queue", {
  connection: redisConnection,
});
