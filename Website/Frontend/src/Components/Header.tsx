import { Box, Stack } from "@mui/system";
import ContrastIcon from "@mui/icons-material/Contrast";
import { IconButton, Tooltip, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import { useState } from "react";

interface HeaderProps {
  isDarkThemeOn: boolean;
  toggleTheme: () => void;
}

function Header({ isDarkThemeOn, toggleTheme }: HeaderProps) {
  const navigate = useNavigate();
  const currentPath = window.location.pathname;
  console.log(currentPath);

  const [value, setValue] = useState<string>(currentPath);

  const handleChange = (_: React.SyntheticEvent, newValue: string) => {
    console.log("New tab: ", newValue);
    navigate(newValue);
    setValue(newValue);
  };

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
        ProVision
      </Typography>

      <Stack direction="row">
        <TabContext value={value}>
          <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
            <TabList onChange={handleChange} aria-label="lab API tabs example">
              <Tab label="home" value="/home" />
              <Tab label="tab2" value="/tab2" />
              <Tab label="tab3" value="/tab3" />
            </TabList>
          </Box>
        </TabContext>

        <IconButton data-testid="cypress-theme-toggle" onClick={toggleTheme}>
          <Tooltip title="Change Theme">
            <ContrastIcon />
          </Tooltip>
        </IconButton>
      </Stack>
    </Box>
  );
}

export default Header;
