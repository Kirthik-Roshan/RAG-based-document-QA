"use client";

import { useState } from "react";

import Sidebar from "@/components/Sidebar";
import ChatInput from "@/components/ChatInput";
import ChatMessage from "@/components/ChatMessage";

import { askQuestion } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSend() {
    if (!question.trim()) return;

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");

    setLoading(true);

    try {
      const data = await askQuestion(userQuestion);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong while contacting the server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="batman-bg">
      <Sidebar />

      <section className="chat-container">
        <div className="messages">
          {messages.map((message, index) => (
            <ChatMessage
              key={index}
              role={message.role}
              content={message.content}
            />
          ))}

          {loading && (
            <ChatMessage
              role="assistant"
              content="Alfred is thinking..."
            />
          )}
        </div>

        <ChatInput
          question={question}
          setQuestion={setQuestion}
          handleSend={handleSend}
        />
      </section>
    </main>
  );
}