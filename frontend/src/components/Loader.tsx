import React from "react";
import { CircularProgress, Box } from "@mui/material";

const Loader: React.FC<{ message?: string }> = ({ message }) => (
  <Box sx={{
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    minHeight: 200,
    width: "100%",
    py: 4,
  }}>
    <CircularProgress color="primary" size={60} thickness={5} />
    {message && (
      <div style={{ marginTop: 16, color: "#1976d2", fontWeight: 500 }}>{message}</div>
    )}
  </Box>
);

export default Loader;
