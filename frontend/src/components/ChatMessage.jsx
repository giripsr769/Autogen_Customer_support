export default function ChatMessage({ message }) {
  return (
    <div className="chat-row user-row">
      <div className="user-avatar">👤</div>
      <div className="chat-bubble user-bubble">
        <div className="chat-label">You</div>
        <div className="chat-content">{message}</div>
      </div>
    </div>
  );
}
