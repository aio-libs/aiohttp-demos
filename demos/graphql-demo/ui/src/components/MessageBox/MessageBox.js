import React from 'react';
import {compose, withHandlers, withState} from 'recompose';

import SendMessageButton from '../SendMessageButton/SendMessageButton';
import gql from "graphql-tag";
import {graphql} from 'react-apollo';

import { getUser } from '../../utils'

// styles
import './MessageBox.css'


const addMessage = gql`
  mutation addMessage($body: String!, $ownerId: Int!, $roomId: Int!) {
    addMessage(body: $body, ownerId: $ownerId, roomId: $roomId) {
      isCreated
    }
  }
`;

const startTyping = gql`
  mutation startTyping($roomId: Int!, $userId: Int!) {
    startTyping(roomId: $roomId, userId: $userId) {
      isSuccess
    }
  }
`;


function MessageBox({
  onChange,
  message,
  setMessage,
  sendMessage,
  onKeyPress,
  addMessage,
  id,
}) {
  return (
    <section className="message-box-wrapper">
      <input
        placeholder="Enter your message"
        className="message-box"
        value={message}
        onChange={onChange}
        onKeyPress={
          (e) => {
            if (e.key === 'Enter') {
              sendMessage({setMessage, id, message, addMessage})
            }
          }
        }
      />
      <div className="button-wrapper">
        <SendMessageButton
          id={id}
          message={message}
          sendMessage={sendMessage}
        />
      </div>
    </section>
  );
}

export default compose(
  graphql(addMessage, {name: 'addMessage'}),
  graphql(startTyping, {name: 'startTyping'}),
  withState('message', 'setMessage', ''),
  withState('sendMessage', 'sendMessage', ''),
  withHandlers({
    onChange: ({setMessage, startTyping, id}) => {
      let user_id = getUser();

      return e => {
        startTyping({
          variables: {
            userId: user_id,
            roomId: id,
          },
        }).then(data => {})
          .catch(e => {console.error(e)});

        return setMessage(e.target.value);
      };
    },
    sendMessage: ({setMessage, id, message, addMessage}) => {
      // get random user
      let user_id = getUser();

      return e => {
        addMessage({
          variables: {
            body: message,
            ownerId: user_id,
            roomId: id,
          },
        })
          .then(data => {
            return setMessage('');
          })
          .catch(e => {
            console.error(e);
          });
      };
    },
  })
)(MessageBox);
