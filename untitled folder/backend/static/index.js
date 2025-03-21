document.addEventListener("DOMContentLoaded", () => {
    const voiceButton = document.getElementById("voice-button");
    const statusText = document.getElementById("status");
    const conversation = document.getElementById("conversation");
  
    let mediaRecorder;
    let audioChunks = [];
  
    // Function to start recording audio
    async function startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data);
        };
  
        mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          audioChunks = [];
  
          // Send audio to backend for processing
          sendAudioToBackend(audioBlob);
        };
  
        mediaRecorder.start();
        statusText.textContent = "Listening...";
        voiceButton.classList.add("recording");
      } catch (error) {
        console.error("Error accessing microphone:", error);
        statusText.textContent = "Microphone access denied!";
      }
    }
  
    // Function to stop recording
    function stopRecording() {
      if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        statusText.textContent = "Processing...";
        voiceButton.classList.remove("recording");
      }
    }
  
    // Function to send recorded audio to Flask backend
    async function sendAudioToBackend(audioBlob) {
      const formData = new FormData();
      formData.append("audio", audioBlob, "voice-command.wav");
  
      try {
        const response = await fetch("/process-audio", {
          method: "POST",
          body: formData,
        });
  
        const data = await response.json();
        displayMessage(data.user_text, "user");
        displayMessage(data.bot_response, "bot");
      } catch (error) {
        console.error("Error sending audio:", error);
        displayMessage("Error communicating with the bot.", "bot");
      }
  
      statusText.textContent = "Click to speak";
    }
  
    // Function to display messages in chat UI
    function displayMessage(message, sender) {
      if (!message) return;
  
      const messageDiv = document.createElement("div");
      messageDiv.classList.add("message", sender === "bot" ? "bot-message" : "user-message");
  
      const avatar = document.createElement("div");
      avatar.classList.add("avatar", sender);
  
      avatar.innerHTML = sender === "bot" 
        ? `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 8V4H8"></path>
            <rect width="16" height="12" x="4" y="8" rx="2"></rect>
            <path d="M2 14h2"></path>
            <path d="M20 14h2"></path>
            <path d="M15 13v2"></path>
            <path d="M9 13v2"></path>
          </svg>` 
        : "👤"; // User icon (can be improved)
  
      const bubble = document.createElement("div");
      bubble.classList.add("bubble");
      bubble.textContent = message;
  
      messageDiv.appendChild(avatar);
      messageDiv.appendChild(bubble);
      conversation.appendChild(messageDiv);
  
      // Auto-scroll to latest message
      conversation.scrollTop = conversation.scrollHeight;
    }
  
    // Event Listener: Click to start/stop recording
    voiceButton.addEventListener("mousedown", startRecording);
    voiceButton.addEventListener("mouseup", stopRecording);
    voiceButton.addEventListener("touchstart", startRecording);
    voiceButton.addEventListener("touchend", stopRecording);
  });