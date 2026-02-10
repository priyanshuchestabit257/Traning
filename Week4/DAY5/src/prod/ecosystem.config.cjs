module.exports = {
  apps: [
    {
      name: "backend-api",
      script: "../index.js",        
      instances: 1,
      autorestart: true,
      watch: false,
      env: {
        NODE_ENV: "production",
        PORT: 3000
      }
    },
    {
      name: "email-worker",
      script: "../jobs/email.job.js", 
      instances: 1,
      autorestart: true,
      watch: false,
      env: {
        NODE_ENV: "production"
      }
    }
  ]
};
