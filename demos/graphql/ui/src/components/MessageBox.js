import React from 'react';
import {compose, withHandlers, withState} from 'recompose';
import SendMessageButton from './SendMessageButton';

function MessageBox({
  onChange,
  message,
  closeMessages,
  setMessage,
  id,
}) {
  return (
    <section>
      <textarea
        placeholder="Enter your message"
        className="message-box"
        value={message}
        onChange={onChange}
      />
      <div className="button-wrapper">
        <button className="button-item" onClick={closeMessages}>Cancel</button>
        <SendMessageButton id={id} message={message} setMessage={setMessage} />
      </div>
    </section>
  );
};

export default compose(
  withState('message', 'setMessage', ''),
  withHandlers({
    onChange: ({setMessage}) => {
      return e => {
        return setMessage(e.target.value);
      };
    },
  })
)(MessageBox);
