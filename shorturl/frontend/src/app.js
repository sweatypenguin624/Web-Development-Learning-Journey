import React, { useState } from "react";
import styled from "styled-components";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #121212;
  color: #ffffff;
  font-family: Arial, sans-serif;
`;

const Title = styled.h1`
  font-size: 2rem;
  margin-bottom: 20px;
`;

const Input = styled.input`
  padding: 10px;
  font-size: 1rem;
  width: 300px;
  border: none;
  border-radius: 5px;
  margin-bottom: 10px;
  background-color: #1e1e1e;
  color: white;
`;

const Button = styled.button`
  padding: 10px 20px;
  font-size: 1rem;
  background-color: #6200ea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
  &:hover {
    background-color: #3700b3;
  }
`;

const ShortUrl = styled.p`
  margin-top: 20px;
  font-size: 1.2rem;
  word-break: break-all;
`;

const ErrorMessage = styled.p`
  margin-top: 10px;
  font-size: 1rem;
  color: red;
`;

const App = () => {
  const [inputUrl, setInputUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [error, setError] = useState(null);

  const handleShorten = async () => {
    if (!inputUrl) {
      setError("Please enter a valid URL.");
      return;
    }

    setError(null); // Clear previous errors

    try {
      const response = await fetch("http://192.168.38.135:5002/shorten", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: inputUrl }),
      });

      const data = await response.json();

      if (!response.ok) {
        console.error("Server Error:", data);
        setError(data.error || "Failed to shorten URL.");
        return;
      }

      console.log("Shortened URL:", data.shortUrl);
      setShortUrl(data.shortUrl);
    } catch (error) {
      console.error("Network Error:", error);
      setError("Network error. Check your connection.");
    }
  };

  return (
    <Container>
      <Title>🔗 URL Shortener</Title>
      <Input
        type="text"
        placeholder="Enter a URL"
        value={inputUrl}
        onChange={(e) => setInputUrl(e.target.value)}
      />
      <Button onClick={handleShorten}>Shorten URL</Button>
      {shortUrl && <ShortUrl>Shortened URL: <a href={shortUrl} target="_blank" rel="noopener noreferrer">{shortUrl}</a></ShortUrl>}
      {error && <ErrorMessage>{error}</ErrorMessage>}
    </Container>
  );
};

export default App;
