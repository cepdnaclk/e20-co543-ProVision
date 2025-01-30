import { Box, Typography } from "@mui/material";

function Footer() {
  return (
    <Box
      width={"fit-parent"}
      height={"30px"}
      textAlign={"center"}
      alignContent={"center"}
      padding={1}
    >
      <Typography
        data-testid="cypress-footer"
        variant="caption"
        color="primary.dark"
      >
        All rights reserved © 2025 PeraBytes
      </Typography>
    </Box>
  );
}

export default Footer;
