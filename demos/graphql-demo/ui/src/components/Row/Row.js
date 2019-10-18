import React from 'react';

// styles
import './Row.css'


function ChatRoomRow({
  closeMessages,
  onClick,
  active,
  id,
  title,
}) {
  const className = active === id ? "chat-room chat-room-active": "chat-room";

  return (
    <p className={className} key={id} onClick={onClick}>
      {title}
    </p>
  );
}


export default ChatRoomRow;
