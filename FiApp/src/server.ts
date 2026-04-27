import express from "express";
import sequelize from "./config/database";
import routes from "./routes";

const app = express();

app.use(express.json());
app.use("/api", routes);

const startServer = async () => {
  try {
    await sequelize.sync({ force: false });
    console.log("Database connected successfully.");

    app.listen(3000, () => {
      console.log("Server is running on port 3000");
    });
  } catch (error) {
    console.error("Unable to connect to the database:", error);
  }
};

startServer();
