import React from 'react';

// styles
import './SendMessageButton.css'


function SendMessageButton({sendMessage}) {
  return (
    <button className="button-item" onClick={sendMessage}>
      &#9654;
    </button>
  );
}

export default SendMessageButton;
