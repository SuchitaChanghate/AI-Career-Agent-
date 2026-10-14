import { useState } from "react";
import axios from "axios";

function CareerChat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim() || loading) {
      return;
    }

    const userMessage = message.trim();

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/chat/",
        {
          message: userMessage,
        }
      );

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: response.data.response,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content:
            "I couldn't connect to the AI Career Agent. Please check that the backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const useSuggestion = (text) => {
    setMessage(text);
  };

  return (
    <section className="chat-section">

      <div className="chat-app">

        {/* HEADER */}

        <div className="chat-header">

          <div className="chat-profile">

            <div className="chat-avatar">
              🤖
            </div>

            <div>
              <h3>AI Career Agent</h3>

              <div className="online">
                <span className="online-dot"></span>
                Online
              </div>
            </div>

          </div>

          <div className="header-status">
            AI Assistant
          </div>

        </div>


        {/* CHAT BODY */}

        <div className="chat-body">

          {messages.length === 0 ? (

            <div className="chat-welcome">

              <div className="welcome-avatar">
                🤖
              </div>

              <h2>
                Hi! I'm your AI Career Agent
              </h2>

              <p>
                I can analyze your resume, find your skills,
                compare jobs and help you prepare for interviews.
              </p>

              <div className="chat-suggestions">

                <button
                  onClick={() =>
                    useSuggestion(
                      "What skills do I have on my resume?"
                    )
                  }
                >
                  💡 What skills do I have?
                </button>

                <button
                  onClick={() =>
                    useSuggestion(
                      "What projects are on my resume?"
                    )
                  }
                >
                  📁 What projects do I have?
                </button>

                <button
                  onClick={() =>
                    useSuggestion(
                      "What are my strongest technical skills?"
                    )
                  }
                >
                  🎯 What are my strongest skills?
                </button>

                <button
                  onClick={() =>
                    useSuggestion(
                      "What should I improve to become an AI Engineer?"
                    )
                  }
                >
                  🚀 What should I improve?
                </button>

              </div>

            </div>

          ) : (

            <div className="messages-list">

              {messages.map((item, index) => (

                <div
                  key={index}
                  className={`chat-message ${item.role}`}
                >

                  {item.role === "assistant" && (
                    <div className="small-avatar">
                      🤖
                    </div>
                  )}

                  <div className="message-content-wrapper">

                    <div className="message-sender">
                      {item.role === "user"
                        ? "You"
                        : "AI Career Agent"}
                    </div>

                    <div className="message-bubble">
                      {item.content}
                    </div>

                  </div>

                </div>

              ))}


              {loading && (

                <div className="chat-message assistant">

                  <div className="small-avatar">
                    🤖
                  </div>

                  <div className="message-content-wrapper">

                    <div className="message-sender">
                      AI Career Agent
                    </div>

                    <div className="message-bubble typing">

                      <span></span>
                      <span></span>
                      <span></span>

                    </div>

                  </div>

                </div>

              )}

            </div>

          )}

        </div>


        {/* INPUT */}

        <div className="chat-footer">

          <div className="chat-input-box">

            <textarea
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Message AI Career Agent..."
              rows="1"
            />

            <button
              onClick={sendMessage}
              disabled={loading || !message.trim()}
              className="send-btn"
            >
              ➤
            </button>

          </div>

          <p className="input-hint">
            AI Career Agent can make mistakes. Verify important information.
          </p>

        </div>

      </div>

    </section>
  );
}

export default CareerChat;