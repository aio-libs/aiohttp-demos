import React from 'react';
import { compose, withState, withHandlers } from 'recompose';
import ChatMessages from './ChatMessages';

function ChatroomRow({
  closeMessages,
  openMessages,
  isActive,
  id,
  title,
}) {
  if (!isActive) {
    return (
      <button className="chatroom" key={id} onClick={openMessages}>
        {title}
      </button>
    );
  }

  return <ChatMessages closeMessages={closeMessages} title={title} id={id} />;
};

export default compose(
  withState('isActive', 'setActive', false),
  withHandlers({
    openMessages: ({setActive}) => {
      return () => {
        return setActive(true);
      };
    },
    closeMessages: ({setActive}) => {
      return () => {
        return setActive(false);
      };
    },
  })
)(ChatroomRow);
