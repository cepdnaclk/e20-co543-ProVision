// CORS connection policy
import cors from "cors";

// Express connection
import express, { NextFunction, Request, Response } from "express";

// Http Errors
import createHttpError, { isHttpError } from "http-errors";

// Routes
import todoRoutes from "./routes";

const app = express();

app.use(
  cors({
    origin: "*", // Allow requests from any origin
    methods: ["GET", "POST", "PATCH", "DELETE"], // Restrict allowed methods to GET (you can modify if needed)
  })
);

// Middleware to handle URL-encoded data
app.use(
  express.urlencoded({
    extended: true,
  })
);

// Middleware to parse incoming JSON data
app.use(express.json());

// Root (Welcome Message)
app.get("/", (req, res) => {
  console.log("Check end point connection");
  res.send("Hello, World! I'm Node App. I can hear you!");
});

// Routes
app.use("/api/todos", todoRoutes);

// End point not found error
app.use((req, res, next) => {
  next(createHttpError(404, "Endpoint not found!"));
});

// Error Function Middleware
app.use((err: unknown, req: Request, res: Response, next: NextFunction) => {
  console.error(err);

  // Default case error
  let errMsg = "An unknown error occured!";
  let statusCode = 500;

  // Unique error
  if (isHttpError(err)) {
    errMsg = err.message;
    statusCode = err.status;
  }

  res.status(statusCode).json({ error: errMsg });
});

// Export the app
export default app;
