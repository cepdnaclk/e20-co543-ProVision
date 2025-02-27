import {
  Card,
  CardContent,
  Typography,
  Box,
  Avatar,
  IconButton,
  Tooltip,
} from "@mui/material";
import { GitHub, LinkedIn, Web } from "@mui/icons-material";
import { useState } from "react";

interface PhotoCardProps {
  name: string;
  regNumber?: string; // Optional
  imageUrl: string;
  githubUrl?: string; // Optional
  linkedInUrl?: string; // Optional
  portfolioUrl?: string; // Optional
}

const PhotoCard: React.FC<PhotoCardProps> = ({
  name,
  regNumber,
  imageUrl,
  githubUrl,
  linkedInUrl,
  portfolioUrl,
}) => {
  const [hovered, setHovered] = useState(false);

  return (
    <Card
      elevation={5}
      sx={{
        width: 250,
        textAlign: "center",
        overflow: "hidden",
        position: "relative",
        boxShadow: 3,
        borderRadius: 2,
      }}
    >
      {/* Image Section with Hover Effect */}
      <Box
        sx={{
          position: "relative",
          width: "100%",
          height: 200,
          overflow: "hidden",
        }}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        <Avatar
          src={imageUrl}
          alt={name}
          sx={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            borderRadius: 0,
          }}
        />
        {/* Icons appear on hover */}
        {hovered && (githubUrl || linkedInUrl || portfolioUrl) && (
          <Box
            sx={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              backgroundColor: "rgba(0, 0, 0, 0.5)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              gap: 2,
            }}
          >
            {linkedInUrl && (
              <Tooltip title="LinkedIn">
                <IconButton
                  href={linkedInUrl}
                  target="_blank"
                  sx={{ color: "white" }}
                >
                  <LinkedIn fontSize="large" />
                </IconButton>
              </Tooltip>
            )}

            {githubUrl && (
              <Tooltip title="GitHub">
                <IconButton
                  href={githubUrl}
                  target="_blank"
                  sx={{ color: "white" }}
                >
                  <GitHub fontSize="large" />
                </IconButton>
              </Tooltip>
            )}

            {portfolioUrl && (
              <Tooltip title="CN Portfolio">
                <IconButton
                  href={portfolioUrl}
                  target="_blank"
                  sx={{ color: "white" }}
                >
                  <Web fontSize="large" />
                </IconButton>
              </Tooltip>
            )}
          </Box>
        )}
      </Box>

      {/* Name & Registration Number */}
      <CardContent>
        <Typography variant="h6">{name}</Typography>
        {regNumber && (
          <Typography variant="body2" color="text.secondary">
            {regNumber}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default PhotoCard;
