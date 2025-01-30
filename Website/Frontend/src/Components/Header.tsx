import { Box } from "@mui/system";
import ContrastIcon from "@mui/icons-material/Contrast";
import { IconButton, Tooltip, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

interface HeaderProps {
  isDarkThemeOn: boolean;
  toggleTheme: () => void;
}

function Header({ isDarkThemeOn, toggleTheme }: HeaderProps) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/"); // Redirect to the home page
  };
  return (
    <Box
      data-testid="cypress-header-background"
      width="fit-parent"
      height="50px"
      bgcolor={isDarkThemeOn ? "black" : "white"}
      padding={1}
      display="flex"
      justifyContent="space-between"
      alignItems="center" // Align items vertically
    >
      <Typography
        variant="h4"
        data-testid="cypress-logo"
        color={isDarkThemeOn ? "white" : "black"}
        sx={{ cursor: "pointer" }}
        onClick={handleClick}
      >
        TODO APP
      </Typography>
      <IconButton data-testid="cypress-theme-toggle" onClick={toggleTheme}>
        <Tooltip title="Change Theme">
          <ContrastIcon />
        </Tooltip>
      </IconButton>
    </Box>
  );
}

export default Header;
