interface ChatInputProps {

  question: string;

  setQuestion:
    React.Dispatch<
      React.SetStateAction<string>
    >;

  handleSend: () => void;
}

export default function ChatInput({

  question,
  setQuestion,
  handleSend,

}: ChatInputProps) {

  return (

    <div className="input-area">

      <input
        value={question}
        onChange={(e) =>
          setQuestion(
            e.target.value
          )
        }
        placeholder="Ask Alfred..."
      />

      <button
        onClick={handleSend}
      >
        ➤
      </button>

    </div>

  );
}