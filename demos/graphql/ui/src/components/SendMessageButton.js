import React from 'react';
import gql from 'graphql-tag';
import {compose, withHandlers} from 'recompose';
import {graphql} from 'react-apollo';


function SendMessageButton({sendMessage}) {
  return (
    <button className="button-item" onClick={sendMessage}>Send Message</button>
  );
};

const addMessage = gql`
  mutation addMessage($body: String!, $ownerId: Int!, $roomId: Int!) {
    addMessage(body: $body, ownerId: $ownerId, roomId: $roomId) {
      isCreated
    }
  }
`;

export default compose(
  graphql(addMessage),
  withHandlers({
    sendMessage: ({setMessage, id, message, mutate}) => {
      return e => {
        mutate({
          variables: {
            body: message,
            ownerId: 1,
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
)(SendMessageButton);
