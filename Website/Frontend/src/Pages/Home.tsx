import {
  alpha,
  Box,
  Button,
  Container,
  Divider,
  List,
  ListItem,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import heroImage from "../assets/Homepage_bg.jpg";
import { useTheme } from "@mui/material/styles";

function Home() {
  const handleClick = () => {
    window.open("https://github.com/cepdnaclk/e20-co543-ProVision", "_blank");
  };

  const theme = useTheme();

  return (
    <Box
      width="100%"
      display="flex"
      flexDirection="column"
      alignItems={"center"}
      sx={{
        overflowX: "hidden",
      }}
    >
      {/* Hero Section */}
      <Box
        height="calc(100vh - 100px)"
        width="100%"
        mb={5}
        sx={{
          backgroundImage: `url(${heroImage})`,
          backgroundRepeat: "no-repeat",
          backgroundPosition: "bottom",
          backgroundSize: "cover",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
          padding: "0 5%",
          color: "white",
          "@media (max-width: 600px)": {
            height: "400px",
            padding: "20px 0",
          },
        }}
      >
        <Container
          sx={{
            border: "5px solid rgba(255, 255, 255, 0.9)",
            padding: "20px",
            mx: "50px",
            textAlign: "center",
            bgcolor: "rgba(0, 0, 0, 0.2)",
          }}
        >
          <Typography variant="h2" component="h1" gutterBottom>
            ProVision
          </Typography>
          <Typography variant="h4" component="h1" gutterBottom>
            Restoring Clarity in Adverse Weather Conditions
          </Typography>
          <Typography variant="h5" mb={2}>
            CO543 - Image Processing
          </Typography>
          <Button
            variant="outlined"
            onClick={handleClick}
            sx={{
              textWrap: "nowrap",
              textDecoration: "bold",
              borderRadius: "25px",
              border: "3px solid rgba(255, 255, 255, 0.6)",
              width: "150px",
              color: "white",
              "&:hover": {
                border: "3px solid rgba(255, 255, 255, 1)",
              },
            }}
          >
            Git Repository
          </Button>
        </Container>
      </Box>

      {/* About Section */}
      <Container
        sx={{
          display: "flex",
          flexDirection: { xs: "column", md: "row" },
          gap: 5,
          alignItems: "center",
        }}
      >
        <Box
          component="img"
          src={heroImage}
          alt="About"
          sx={{
            width: { xs: "100%", md: "35%" },
            borderRadius: "25px",
          }}
        />
        <Stack>
          <Typography variant="h4" mb={1} color="primary">
            About
          </Typography>
          <Typography textAlign="justify" fontFamily="arial" color="primary">
            ProVision is a project focused on removing weather effects like
            rain, fog, haze, and snow from images to restore their quality and
            detail. Traditional image processing methods fall short, making this
            enhancement crucial for applications such as autonomous driving,
            surveillance systems, outdoor vision-dependent systems, and
            satellite imaging. The goal of this project is to restore the image
            quality by removing the weather effects.
          </Typography>
        </Stack>
      </Container>

      <Divider
        orientation="horizontal"
        sx={{
          borderColor: alpha(theme.palette.primary.main, 0.5),
          borderWidth: 2,
          borderStyle: "solid",
          width: "80%",
          my: 5,
        }}
      />

      {/* Problem Statement Section */}
      <Container
        sx={{
          display: "flex",
          flexDirection: { xs: "column", md: "row" },
          gap: 5,
          alignItems: "center",
        }}
      >
        <Stack>
          <Typography variant="h4" mb={1} color="primary">
            Problem Statement
          </Typography>
          <Typography textAlign="justify" fontFamily="arial" color="primary">
            Due to bad weather conditions obscuring key details in images,
            reducing the contrast and clarity and also adding noise and
            artifacts, the visual and logical output from the image is poor.
            Hence, the reliability is not ensured; analysis is therefore
            redundant in many cases. The purpose of this project is to address
            this problem domain and enhance the quality of images affected by
            adverse weather conditions.
          </Typography>
        </Stack>

        <Box
          component="img"
          src={heroImage}
          alt="Problem Statement"
          sx={{
            width: { xs: "100%", md: "35%" },
            borderRadius: "25px",
          }}
        />
      </Container>

      <Divider
        orientation="horizontal"
        sx={{
          borderColor: alpha(theme.palette.primary.main, 0.5),
          borderWidth: 2,
          borderStyle: "solid",
          width: "80%",
          my: 5,
        }}
      />

      {/* Objectives Section */}
      <Container
        sx={{
          display: "flex",
          flexDirection: { xs: "column", md: "row" },
          gap: 5,
          alignItems: "center",
        }}
      >
        <Box
          component="img"
          src={heroImage}
          alt="About"
          sx={{
            width: { xs: "100%", md: "35%" },
            borderRadius: "25px",
          }}
        />
        <Stack>
          <Typography variant="h4" mb={1} color="primary">
            Objectives
          </Typography>
          <Typography textAlign="justify" fontFamily="arial" color="primary">
            Main Goal of this project is to produce clean and clear images by
            removing weather effects which degrade the image quality in the
            means of a robust method.
          </Typography>
          <List
            sx={{
              listStyleType: "disc",
              pl: 4,
              "& li::marker": {
                color: "primary.main",
              },
            }}
          >
            <ListItem
              sx={{
                display: "list-item",
                p: 0,
              }}
            >
              <Typography
                textAlign="justify"
                fontFamily="arial"
                color="primary"
              >
                Ensure solutions work for multiple weather conditions. (general
                method)
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography
                textAlign="justify"
                fontFamily="arial"
                color="primary"
              >
                Create an efficient system for real-time and large-scale
                applications.
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography
                textAlign="justify"
                fontFamily="arial"
                color="primary"
              >
                Integrate advanced algorithms for optimal results.
              </Typography>
            </ListItem>
          </List>
        </Stack>
      </Container>

      <Divider
        orientation="horizontal"
        sx={{
          borderColor: alpha(theme.palette.primary.main, 0.5),
          borderWidth: 2,
          borderStyle: "solid",
          width: "80%",
          my: 5,
        }}
      />

      {/* Methadology 1 Section */}
      <Container
        sx={{
          display: "flex",
          flexDirection: { xs: "column", md: "row" },
          gap: 5,
          alignItems: "center",
        }}
      >
        <Stack>
          <Typography variant="h4" mb={1} color="primary">
            Methodology I - Physics Based Approach
          </Typography>

          <Typography fontFamily="arial" color="primary" variant="h5" mb={1}>
            Overview
          </Typography>
          <Typography
            textAlign="justify"
            fontFamily="arial"
            color="primary"
            mb={2}
          >
            Involves modeling and estimating physical parameters like
            transmission maps, atmospheric light, and scene radiance to restore
            weather-degraded images.
          </Typography>

          <Typography fontFamily="arial" color="primary" variant="h5">
            Key Parameters
          </Typography>
          <List
            sx={{
              listStyleType: "disc",
              mb: 2,
              pl: 4,
              "& li::marker": {
                color: "primary.main",
              },
            }}
          >
            <ListItem
              sx={{
                display: "list-item",
                p: 0,
              }}
            >
              <Typography fontFamily="arial" color="primary">
                Observed image
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography fontFamily="arial" color="primary">
                Transmission map (light attenuation due to weather)
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography fontFamily="arial" color="primary">
                Integrate advanced algorithms for optimal results.
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography fontFamily="arial" color="primary">
                Atmospheric light (scattered light from the medium)
              </Typography>
            </ListItem>
          </List>

          <Typography fontFamily="arial" color="primary" variant="h5">
            Steps
          </Typography>
          <List
            sx={{
              listStyleType: "disc",
              mb: 2,
              pl: 4,
              "& li::marker": {
                color: "primary.main",
              },
            }}
          >
            <ListItem
              sx={{
                display: "list-item",
                p: 0,
              }}
            >
              <Typography fontFamily="arial" color="primary">
                Estimate transmission map using DCP (Dark Channel Prior).
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography fontFamily="arial" color="primary">
                Estimate atmospheric light.
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography fontFamily="arial" color="primary">
                Restore image using a predefined formula.
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography fontFamily="arial" color="primary">
                Apply post-processing for contrast enhancement.
              </Typography>
            </ListItem>
          </List>

          <Typography fontFamily="arial" color="primary" variant="h5">
            Challanges
          </Typography>
          <List
            sx={{
              listStyleType: "disc",
              pl: 4,
              "& li::marker": {
                color: "primary.main",
              },
            }}
          >
            <ListItem
              sx={{
                display: "list-item",
                p: 0,
              }}
            >
              <Typography fontFamily="arial" color="primary">
                Estimation Accuracy: Requires precise estimation of transmission
                maps and atmospheric light.
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography fontFamily="arial" color="primary">
                Severe Weather Limitations: Struggles with extreme conditions
                without advanced techniques.
              </Typography>
            </ListItem>
          </List>
        </Stack>

        <Box
          component="img"
          src={heroImage}
          alt="Problem Statement"
          sx={{
            width: { xs: "100%", md: "35%" },
            borderRadius: "25px",
          }}
        />
      </Container>

      <Divider
        orientation="horizontal"
        sx={{
          borderColor: alpha(theme.palette.primary.main, 0.5),
          borderWidth: 2,
          borderStyle: "solid",
          width: "80%",
          my: 5,
        }}
      />

      {/* Methadology 2 Section */}
      <Container
        sx={{
          display: "flex",
          flexDirection: { xs: "column", md: "row" },
          gap: 5,
          alignItems: "center",
        }}
      >
        <Box
          component="img"
          src={heroImage}
          alt="Problem Statement"
          sx={{
            width: { xs: "100%", md: "35%" },
            borderRadius: "25px",
          }}
        />
        <Stack>
          <Typography variant="h4" mb={1} color="primary">
            Methodology II - Specific Weather Condition Methods
          </Typography>
          <Typography fontFamily="arial" color="primary" variant="h5" mb={1}>
            Overview
          </Typography>
          <Typography
            textAlign="justify"
            fontFamily="arial"
            color="primary"
            mb={2}
          >
            Tailored implementations for specific weather effects, optimizing
            results for unique conditions.
          </Typography>

          <Typography fontFamily="arial" color="primary" variant="h5">
            Characteristics
          </Typography>
          <List
            sx={{
              listStyleType: "disc",
              mb: 2,
              pl: 4,
              "& li::marker": {
                color: "primary.main",
              },
            }}
          >
            <ListItem
              sx={{
                display: "list-item",
                p: 0,
              }}
            >
              <Typography fontFamily="arial" color="primary">
                Provides more efficient outputs.
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography fontFamily="arial" color="primary">
                Optimized for intended weather conditions.
              </Typography>
            </ListItem>
            <ListItem sx={{ display: "list-item", p: 0 }}>
              <Typography fontFamily="arial" color="primary">
                Requires more computational power.
              </Typography>
            </ListItem>
          </List>
        </Stack>
      </Container>

      <TableContainer
        component={Paper}
        sx={{
          bgcolor: theme.palette.secondary.main,
          width: "90%",
          mx: "auto",
          my: 2,
          p: 2,
          overflowX: "auto",
        }}
      >
        <Table sx={{ minWidth: 650 }} aria-label="weather condition table">
          <TableHead>
            <TableRow>
              <TableCell sx={{ textWrap: "noWrap" }}>
                <b>Weather Condition</b>
              </TableCell>
              <TableCell align="center">
                <b>Proposed Approaches</b>
              </TableCell>
              <TableCell align="center">
                <b>Challenges</b>
              </TableCell>
              <TableCell align="center">
                <b>Potential Solutions</b>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell align="center" component="th" scope="row">
                Rain
              </TableCell>
              <TableCell align="center">
                CNN, GAN, Image Decomposition
              </TableCell>
              <TableCell align="center">
                High data needs, model complexity, real-time issues
              </TableCell>
              <TableCell align="center">
                Data augmentation, lightweight models, edge computing
              </TableCell>
            </TableRow>

            <TableRow
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell component="th" align="center" scope="row">
                Haze
              </TableCell>
              <TableCell align="center">
                L0 Gradient, Dictionary Learning, Guided Filtering
              </TableCell>
              <TableCell align="center">
                Sparse representation, training complexity, scalability
              </TableCell>
              <TableCell align="center">
                Pre-trained models, adaptive filtering, cloud computing
              </TableCell>
            </TableRow>

            <TableRow
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell component="th" align="center" scope="row">
                Snow
              </TableCell>
              <TableCell align="center">
                Contrast Restoration, Multi-Scale CNN, Histogram Stretching
              </TableCell>
              <TableCell align="center">
                Physical models, parameter sensitivity, computational load
              </TableCell>
              <TableCell align="center">
                Hybrid models, feature engineering, GPU acceleration
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      <Divider
        orientation="horizontal"
        sx={{
          borderColor: alpha(theme.palette.primary.main, 0.5),
          borderWidth: 2,
          borderStyle: "solid",
          width: "80%",
          my: 5,
        }}
      />
    </Box>
  );
}

export default Home;
