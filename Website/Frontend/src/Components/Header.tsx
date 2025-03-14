import { Box, Stack } from "@mui/system";
import ContrastIcon from "@mui/icons-material/Contrast";
import { IconButton, Tooltip, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import { useEffect, useState } from "react";

interface HeaderProps {
  isDarkThemeOn: boolean;
  toggleTheme: () => void;
}

const SUB_TOPICS = [
  "home",
  "about",
  "problem",
  "objectives",
  "method1",
  "method2",
  "team",
];

function Header({ isDarkThemeOn, toggleTheme }: HeaderProps) {
  const navigate = useNavigate();
  const currentPage = window.location.pathname;
  const currentTab = sessionStorage.getItem("tabName");

  const [value, setValue] = useState<string>(currentTab || "home");

  useEffect(() => {
    navigation(value);
  }, [value]);

  useEffect(() => {
    const page = currentPage.split("/")[1];
    if (page !== "home") {
      setValue(page);
    }
  }, [currentPage]);

  const navigation = (newValue: string) => {
    //console.log("Navigate to section");
    const section = document.getElementById(newValue);

    if (section) {
      section.scrollIntoView({ behavior: "smooth" });
    }
  };

  const handleChange = (_: React.SyntheticEvent, newValue: string) => {
    //console.log("New tab: ", newValue);
    sessionStorage.setItem("tabName", newValue);
    sessionStorage.setItem("flag", "true");

    if (currentPage !== "/home") {
      window.location.href = "/home";
    } else {
      setValue(newValue);
    }
  };

  const handleClick = () => {
    navigate("/"); // Redirect to the home page
  };

  // Function to update tab when scrolling
  useEffect(() => {
    const sections = document.querySelectorAll("[id]"); // Select all sections
    //console.log("Sections: ", sections);

    const observer = new IntersectionObserver(
      (entries) => {
        const visibleSection = entries.find((entry) => entry.isIntersecting);

        if (visibleSection) {
          const section = visibleSection.target.id;
          //console.log("Section: ", section);

          if (SUB_TOPICS.includes(section)) {
            let flag = sessionStorage.getItem("flag") === "true";
            const tab = sessionStorage.getItem("tabName");

            //console.log("Flag: " + flag + "\tvalue: " + value);

            if (flag && section === tab) {
              flag = false;
              sessionStorage.setItem("flag", "false");
            }

            //console.log("New Flag: ", flag);

            if (!flag) {
              setValue(section);
            }
          }
        }
      },
      {
        rootMargin: "7% 0px -60% 0px", // Focus on the top 20% of the viewport
        threshold: 0.7, // Fires when a small part of the section is visible
      }
    );

    sections.forEach((section) => observer.observe(section));

    return () => observer.disconnect(); // Cleanup observer
  }, []);

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
              <Tab label="home" value="home" />
              <Tab label="about" value="about" />
              <Tab label="problem Statement" value="problem" />
              <Tab label="objectives" value="objectives" />
              {/* <Tab label="methodology I" value="method1" /> */}
              <Tab label="methodology" value="method2" />
              <Tab label="team" value="team" />
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
