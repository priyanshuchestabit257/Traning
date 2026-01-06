import { emailQueue } from "../jobs/email.queue.js";

export const addEmailJob = async (req, res, next) => {
  try {
    const { email, subject, message } = req.body;

    if (!email || !subject || !message) {
      return res.status(400).json({
        success: false,
        message: "email, subject and message are required",
        requestId: req.requestId,
      });
    }

    await emailQueue.add(
      "send-email",
      { email, subject, message },
      {
        attempts: 3,
        backoff: {
          type: "exponential",
          delay: 2000,
        },
      }
    );

    res.status(202).json({
      success: true,
      message: "Email job queued",
      requestId: req.requestId,
    });
  } catch (err) {
    next(err);
  }
};
