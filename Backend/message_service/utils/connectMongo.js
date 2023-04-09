const { dbUri } = require("../env.js");
const mongoose = require("mongoose");
const logger = require("./logger");

async function connectMongo() {

  try {
    await mongoose.connect(process.env.dbUri || dbUri);
    logger.info("DB connected");
  } catch (error) {
    logger.error("Could not connect to db");
    process.exit(1);
  }
}

module.exports = connectMongo;
