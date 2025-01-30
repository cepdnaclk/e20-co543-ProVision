import { RequestHandler } from "express";
import { Todo } from "./models";
import { todoList } from "./db";

let todos = todoList;

export const getTodos: RequestHandler = async (req, res, next) => {
  try {
    console.log("Readding Todos!");
    res.status(200).json(todos);
  } catch (error) {
    next(error);
  }
};

export const addTodo: RequestHandler = async (req, res, next) => {
  try {
    const { title, content, dueDate } = req.body;
    const len = todos.length;
    const newTodo: Todo = {
      id: todos[len - 1].id + 1,
      title,
      content,
      dueDate,
    };
    todos.push(newTodo);
    console.log("New Todo added successfully!");
    res.status(201).json("Success");
  } catch (error) {
    next(error);
  }
};

export const deleteTodo: RequestHandler = async (req, res, next) => {
  try {
    const { id } = req.body;
    todos = todos.filter((todo) => todo.id !== id);
    console.log("Item " + id + " deleted successfully.");
    res.status(201).json("Success");
  } catch (error) {
    next(error);
  }
};
