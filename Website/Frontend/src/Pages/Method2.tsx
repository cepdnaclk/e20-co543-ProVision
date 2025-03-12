import { useState } from "react";
import {
  Button,
  Box,
  Typography,
  useTheme,
  Paper,
  Container,
  Grid2,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import placeholder from "../assets/placeholder2.jpg";
import { sendData } from "../Api/Api";

const Method2 = () => {
  const theme = useTheme();
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [enhancedImage, setEnhancedImage] = useState<string | null>(null);
  const [selectedEffect, setSelectedEffect] = useState<string>("");
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

  const convertImage = (image: string) => {
    // Convert base64 to a File object
    const byteCharacters = atob(image.split(",")[1]);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const file = new File([byteArray], "image.png", { type: "image/png" });

    // Create FormData and append the file
    const formData = new FormData();
    formData.append("file", file);

    return formData;
  };

  const handleSendToServer = async () => {
    if (!originalImage) return alert("Please upload an image first!");
    if (selectedEffect === "") return alert("Please select an effect first!");

    setLoading(true);

    try {
      const obj = convertImage(originalImage);

      const serverResponse = await sendData(obj, selectedEffect);

      if (serverResponse.status !== 200) {
        throw new Error("Failed to process image");
      }

      // Create a URL for the processed image
      const imageUrl = URL.createObjectURL(new Blob([serverResponse.data]));

      setEnhancedImage(imageUrl);
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
        Methodology - Specific Weather Condition Methods
      </Typography>

      {/* Upload Button */}
      <Box
        my={5}
        display={"flex"}
        gap={3}
        alignItems={"center"}
        justifyContent={"center"}
      >
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

        {/* Method Selector */}
        <FormControl sx={{ mx: 1, width: 160 }} margin="normal">
          <InputLabel>Choose Effect</InputLabel>
          <Select
            value={selectedEffect}
            onChange={(e) => setSelectedEffect(e.target.value)}
            label="Choose Effect"
          >
            <MenuItem value="haze">Haze</MenuItem>
            <MenuItem value="rain">Rain</MenuItem>
            <MenuItem value="snow">Snow</MenuItem>
          </Select>
        </FormControl>
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
