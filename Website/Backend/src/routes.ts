import express from "express";
import { getTodos, addTodo, deleteTodo } from "./controller";

const router = express.Router();

router.get("/", getTodos);

router.post("/", addTodo);

router.delete("/", deleteTodo);

export default router;
