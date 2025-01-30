import { Button, Grid2 as Grid, Paper, Stack, TextField } from "@mui/material";
import { useState } from "react";

// Initial State
const INITERR: ErrorTodo = {
  titleErr: false,
  contentErr: false,
  dueDateErr: false,
};

// Interfaces
interface TodoProp {
  title: string;
  content: string;
  dueDate: string;
}

interface NewTodoProps {
  onAdd: (todo: TodoProp) => void;
}

interface ErrorTodo {
  titleErr: boolean;
  contentErr: boolean;
  dueDateErr: boolean;
}

function validateEvent(event: TodoProp) {
  const err: ErrorTodo = { ...INITERR };
  const today = new Date().toISOString().split("T")[0];

  if (!event.title) {
    err.titleErr = true;
  }

  if (!event.content) {
    err.contentErr = true;
  }

  if (!event.dueDate || event.dueDate < today) {
    err.dueDateErr = true;
  }

  console.log(err);
  return err;
}

function CreateNew({ onAdd }: NewTodoProps) {
  const [title, setTitle] = useState<string>("");
  const [dueDate, setDueDate] = useState<string>("");
  const [content, setContent] = useState<string>("");
  const [err, setErr] = useState<ErrorTodo>(INITERR);

  const handleSend = () => {
    const inputErr = validateEvent({ title, content, dueDate });
    console.log("Validation: ", inputErr);

    if (!inputErr.titleErr && !inputErr.dueDateErr && !inputErr.contentErr) {
      onAdd({ title, content, dueDate });
      handleCancel(); // Reset form after adding
    } else {
      setErr(inputErr);
      console.log("All fields are required");
    }
  };

  const handleCancel = () => {
    // Reset form
    setTitle("");
    setContent("");
    setDueDate("");
  };

  return (
    <Paper
      data-testid="cypress-NewTodoSection"
      elevation={3}
      sx={{
        width: "90%",
        padding: "20px",
      }}
    >
      <Grid container spacing={2}>
        <Grid size={{ xs: 12, lg: 10 }}>
          <TextField
            data-testid="cypress-NewTitle"
            fullWidth
            label="Title"
            variant="outlined"
            value={title}
            error={err.titleErr}
            helperText={err.titleErr && "* This field is requred!"}
            onChange={(e) => setTitle(e.target.value)}
          />
        </Grid>

        <Grid size={{ xs: 12, lg: 2 }}>
          <TextField
            data-testid="cypress-NewDate"
            fullWidth
            label="Due Date"
            variant="outlined"
            type="date"
            error={err.dueDateErr}
            helperText={err.dueDateErr && "* Invalid Date!"}
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />
        </Grid>

        <Grid size={{ xs: 12 }}>
          <TextField
            data-testid="cypress-NewContent"
            fullWidth
            label="Content"
            variant="outlined"
            value={content}
            error={err.contentErr}
            helperText={err.contentErr && "* This field is requred!"}
            multiline
            rows={3}
            onChange={(e) => setContent(e.target.value)}
          />
        </Grid>

        <Grid size={{ xs: 12 }}>
          <Stack spacing={2} direction="row" justifyContent="center" gap={10}>
            <Button
              data-testid="cypress-CancelBtn"
              variant="outlined"
              sx={{ width: 150 }}
              onClick={handleCancel}
            >
              Cancel
            </Button>
            <Button
              data-testid="cypress-AddBtn"
              variant="contained"
              sx={{ width: 150 }}
              onClick={handleSend}
            >
              Add New
            </Button>
          </Stack>
        </Grid>
      </Grid>
    </Paper>
  );
}

export default CreateNew;
