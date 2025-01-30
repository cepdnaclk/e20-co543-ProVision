import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import TodoCard from "../Components/TodoCard";
import CreateNew from "../Components/NewTodo";
import { addData, deleteData, getData } from "../Api/Api";
import { useNavigate } from "react-router-dom";

interface TODOProps {
  id: string;
  title: string;
  content: string;
  dueDate: string;
}

function Todo() {
  const navigate = useNavigate();
  const [todos, setTodos] = useState<TODOProps[]>();

  // Load Todo List
  useEffect(() => {
    getEvent();
  }, []);

  const getEvent = async () => {
    try {
      const serverResposnse = await getData("todos");
      //console.log("Todo List: ", serverResposnse.data);
      setTodos(serverResposnse.data);
    } catch (error) {
      //console.log("Error occured");
      console.log("Error in fetching todo list!", error);
    }
  };

  const addEvent = async (event: object) => {
    try {
      const serverResposnse = await addData(event, "todos");
      console.log("Adding New Event: ", serverResposnse.data);
    } catch (error) {
      console.log("Error in adding event!", error);
    } finally {
      refresh();
    }
  };

  const removeEvent = async (event: object) => {
    try {
      const serverResposnse = await deleteData(event, "todos");
      console.log("Delete Event: ", serverResposnse.data);
    } catch (error) {
      console.log("Error in deleting event!", error);
    } finally {
      refresh();
    }
  };

  const handleAdd = (todo: Omit<TODOProps, "id">) => {
    console.log("Adding new event:" + todo);
    addEvent(todo);
  };

  const handleDelete = (id: string) => {
    console.log("Deleting " + id);
    removeEvent({ id });
  };

  const refresh = () => {
    navigate(0);
  };

  const priorityList = todos?.sort((item1, item2) => {
    return item1.dueDate < item2.dueDate ? -1 : 1;
  });

  return (
    <Box
      display={"flex"}
      flexDirection={"column"}
      alignItems={"center"}
      py={3}
      gap={3}
    >
      {/* Create New */}
      <CreateNew onAdd={handleAdd} />

      {/* My TODO List */}
      <Paper
        data-testid="cypress-TodoListSection"
        elevation={3}
        sx={{
          padding: "15px",
          width: "90%",
          gap: "15px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Typography variant="h4" textAlign={"center"} mb={2}>
          My Todo List
        </Typography>
        {priorityList &&
          priorityList.map((todo) => (
            <TodoCard
              key={todo.id}
              id={todo.id}
              title={todo.title}
              content={todo.content}
              dueDate={todo.dueDate}
              onDelete={handleDelete}
            />
          ))}
      </Paper>
    </Box>
  );
}

export default Todo;
