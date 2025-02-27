import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const TryButton = ({ page }: { page: string }) => {
  const navigate = useNavigate();

  return (
    <Button
      variant="contained"
      sx={{
        my: "20px",
        textTransform: "none",
        whiteSpace: "nowrap",
        backgroundColor: "#007BFF",
        color: "white",
        fontWeight: "bold",
        padding: "10px 20px",
        borderRadius: "8px",
        boxShadow: "0 4px 8px rgba(0, 123, 255, 0.3)",
        "&:hover": {
          backgroundColor: "#0056b3",
          boxShadow: "0 6px 12px rgba(0, 123, 255, 0.4)",
        },
        transition: "background-color 0.3s ease, box-shadow 0.3s ease",
      }}
      onClick={() => navigate(`/${page}`)}
    >
      {"Try It Out >>>"}
    </Button>
  );
};

export default TryButton;
