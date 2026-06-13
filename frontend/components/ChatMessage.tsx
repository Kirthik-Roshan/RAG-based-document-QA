interface ChatMessageProps {

  role:
    | "user"
    | "assistant";

  content: string;
}

export default function ChatMessage({
  role,
  content,
}: ChatMessageProps) {

  return (

    <div
      className={
        role === "user"
          ? "user-message"
          : "ai-message"
      }
    >

      {content}

    </div>

  );
}