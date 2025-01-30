import { Box } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles"; // Use MUI's ThemeProvider
import { darkTheme, lightTheme } from "./Theme"; // Custom themes
import { useState } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Header from "./Components/Header";
import Footer from "./Components/Footer";
import Home from "./Pages/Home";
import Todo from "./Pages/Todo";

function App() {
  // State to toggle between light and dark themes
  const [isDarkThemeOn, setIsDarkThemeOn] = useState<boolean>(false);

  // Function to toggle the theme
  const toggleTheme = () => {
    setIsDarkThemeOn((prev) => !prev);
  };

  return (
    <ThemeProvider theme={isDarkThemeOn ? darkTheme : lightTheme}>
      <Box
        width="100vw"
        height="100vh"
        bgcolor={isDarkThemeOn ? "grey.900" : "grey.100"}
      >
        <BrowserRouter>
          {/* Header */}
          <Header isDarkThemeOn={isDarkThemeOn} toggleTheme={toggleTheme} />

          {/* Body */}
          <Box
            width={"fit-parent"}
            height={"calc(100% - 120px)"}
            overflow={"auto"}
          >
            <Routes>
              <Route path="/" element={<Navigate to="/home" />} />
              <Route path="/home" element={<Home />} />
              <Route path="/mytodo" element={<Todo />} />
            </Routes>
          </Box>

          {/* Footer */}
          <Footer />
        </BrowserRouter>
      </Box>
    </ThemeProvider>
  );
}

export default App;
