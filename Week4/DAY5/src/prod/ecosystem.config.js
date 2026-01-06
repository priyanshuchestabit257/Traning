export default {
  apps: [
    {
      name: "backend-api",
      script: "src/index.js",
      instances: 1,
      exec_mode: "fork",
      env: {
        NODE_ENV: "production",
      },
    },
    {
      name: "email-worker",
      script: "src/jobs/email.job.js",
    },
  ],
};
