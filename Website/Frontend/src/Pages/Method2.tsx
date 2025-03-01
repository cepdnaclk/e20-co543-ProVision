import { useState } from "react";
import {
  Button,
  Box,
  Typography,
  useTheme,
  Paper,
  Container,
  Grid2,
} from "@mui/material";
import placeholder from "../assets/placeholder2.jpg";

const IMAGE_SERVER_URL = import.meta.env.VITE_IMAGE_SERVER_URL;

const Method2 = () => {
  const theme = useTheme();
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [enhancedImage, setEnhancedImage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setOriginalImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSendToServer = async () => {
    if (!originalImage) return alert("Please upload an image first!");

    setLoading(true);

    try {
      const response = await fetch(IMAGE_SERVER_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: originalImage }),
      });

      if (!response.ok) throw new Error("Failed to process image");

      const data = await response.json();
      setEnhancedImage(data.enhancedImage); // Assuming API returns { enhancedImage: "image-url" }
    } catch (error) {
      console.error("Error:", error);
      alert("Error processing the image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        textAlign: "center",
        p: 4,
        minHeight: "100vh",
        backgroundColor: theme.palette.background.default,
      }}
    >
      <Typography variant="h4" gutterBottom color="primary" mb={2}>
        Methodology II - Specific Weather Condition Methods
      </Typography>

      {/* Upload Button */}
      <Box my={5}>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
          style={{ display: "none" }}
          id="upload-button"
        />
        <label htmlFor="upload-button">
          <Button variant="contained" component="span">
            Upload Image
          </Button>
        </label>

        {/* Process Button */}
        <Button
          variant="contained"
          color="secondary"
          sx={{ ml: 2 }}
          onClick={handleSendToServer}
          disabled={!originalImage || loading}
        >
          {loading ? "Processing..." : "Enhance Image"}
        </Button>
      </Box>

      {/* Images Display */}
      <Container>
        <Paper
          elevation={5}
          sx={{
            mt: 4,
            padding: 3,
            borderRadius: 3,
            gap: 4,
          }}
        >
          <Grid2 container spacing={3} sx={{ height: "min-content" }}>
            {/* Original Image Slot */}
            <Grid2 size={{ xs: 12, md: 6 }}>
              <Typography color="primary" variant="h6" mb={1}>
                Original Image
              </Typography>
              <img
                src={originalImage || placeholder}
                alt="Original"
                style={{
                  width: "100%",
                  height: "auto",
                  maxWidth: "100%",
                  border: "2px solid black",
                  borderRadius: "8px",
                  objectFit: "contain",
                }}
              />
            </Grid2>

            {/* Enhanced Image Slot */}
            <Grid2 size={{ xs: 12, md: 6 }}>
              <Typography color="primary" variant="h6" mb={1}>
                Enhanced Image
              </Typography>
              <img
                src={enhancedImage || placeholder}
                alt="Enhanced"
                style={{
                  width: "100%",
                  height: "auto",
                  maxWidth: "100%",
                  border: "2px solid green",
                  borderRadius: "8px",
                  objectFit: "contain",
                }}
              />
            </Grid2>
          </Grid2>
        </Paper>
      </Container>
    </Box>
  );
};

export default Method2;
