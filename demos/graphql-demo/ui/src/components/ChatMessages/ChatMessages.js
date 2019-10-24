import React from 'react';
import gql from 'graphql-tag';
import update from 'immutability-helper';
import { graphql } from 'react-apollo';
import { get } from 'lodash';
import { compose, mapProps, lifecycle, withState } from 'recompose';

import MessageBox from '../MessageBox/MessageBox';

// styles
import './ChatMessages.css'


// queries
const roomQuery = gql`
  query room($id: Int!) {
    room(id: $id) {
      messages {
        id
        body
        owner {
          username
          id
        }
      }
    }
  }
`;

const messageAdded = gql`
  subscription onMessageAdded($roomId: Int!){
    messageAdded(roomId: $roomId){
      id
      body
      owner {
        username
        id
      }
    }
  }
`;


const typingStart = gql`
  subscription typingStart($roomId: Int!){
    typingStart(roomId: $roomId){
      user {
        username
        id
      }
    }
  }
`;


let subscribeRooms = [];
let subscribeTypingRooms = [];


class ChatMessages extends React.Component {
  componentDidMount() {
    this.scrollToBottom();

    // hiding typing user
    setInterval(
      () => this.props.updateTyping(false),
      2000,
    );
  }

  componentWillReceiveProps() {
    this.props.subscribeToMessages();
    this.props.subscribeToTyping(this.props.updateTyping);
  }

  componentDidUpdate() {
    this.scrollToBottom();
  }

  scrollToBottom() {
    this.el.scrollTop = this.el.scrollHeight - this.el.clientHeight;
  }

  message = (message) => {
    const userId = Number(window.localStorage.getItem('id'));
    const classWrapper = message.owner.id === userId ?
      "message-wrapper-right": "message-wrapper-left";

    return (
      <div key={message.id} className={classWrapper}>
        <div className="message">
          <span className="message-username">
            {message.owner.username}
          </span>
          <p>{message.body}</p>
        </div>
      </div>
    );
  };

  render() {
    const { ready, id, messages, typing } = this.props;
    const userId = Number(window.localStorage.getItem('id'));

    return (
      <section className="message-block" ref={el => { this.el = el; }}>
        {ready ? messages.map((message) => this.message(message)) : null}
          {typing ? typing.user.id !== userId ? (
            <p className="typing-block">
              {typing.user.username} is typing...
            </p>
          ): null: null}
        <MessageBox id={id} />
      </section>
    );
  }
}


export default compose(
  graphql(roomQuery, {
    options: ({id}) => {
      return {
        variables: {
          id,
        },
      };
    },
  }),
  withState('typing', 'updateTyping', false),
  mapProps(({data, id, ...rest}) => {
    const subscribeToMore = data && data.subscribeToMore;
    const messages = data && data.room && data.room.messages;
    return {
      id,
      ready: !data.loading,
      messages,
      subscribeToMessages: () => {
        if (subscribeRooms.includes(id)) return;

        subscribeRooms.push(id);

        return subscribeToMore({
          document: messageAdded,
          variables: {
            roomId: id,
          },
          onError: (e) => {
            return console.error('APOLLO-CHAT', e);
          },
          updateQuery: (
            previousResult,
            {subscriptionData}
          ) => {
            if (!subscriptionData.data) {
              return previousResult;
            }

            const messageToAdd = get(subscriptionData, 'data.messageAdded');

            const newResult = update(previousResult, {
              room: {
                messages: {
                  $push: [messageToAdd],
                },
              },
            });
            return newResult;
          },
        });
      },
      subscribeToTyping: (updateTyping) => {
        if (subscribeTypingRooms.includes(id)) return;

        subscribeTypingRooms.push(id);

        return subscribeToMore({
          document: typingStart,
          variables: {
            roomId: id,
          },
          onError: (e) => {
            return console.error('APOLLO-CHAT', e);
          },
          updateQuery: (
            previousResult,
            {subscriptionData}
          ) => {
            if (!subscriptionData.data) {
              return previousResult;
            }

            const messageTyping = get(subscriptionData, 'data.typingStart');
            updateTyping(messageTyping)
          },
        });
      },
      ...rest,
    };
  }),
  lifecycle({
    componentWillMount() {
      const {
        subscribeToMessages,
        subscribeToTyping,
        updateTyping,
      } = this.props;

      subscribeToMessages();
      subscribeToTyping(updateTyping);
    },
  })
)(ChatMessages);
