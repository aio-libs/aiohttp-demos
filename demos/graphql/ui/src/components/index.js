import React from 'react';
import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import {compose, mapProps, withHandlers} from 'recompose';
import { withState } from 'recompose';

import ChatRoomRow from './Row/Row';


const chatRoomsQuery = gql`
{
  rooms {
    id
    name
  }
}
`;


function ChatRoom({chatRooms = [], openMessages, active}) {
  return (
    <section className="bar">
      {chatRooms.map(room => {
        return (
          <ChatRoomRow
            key={room.id}
            title={room.name}
            id={room.id}
            active={active}
            onClick={() => openMessages(room.id)}
          />
        );
      })}
    </section>
  );
}

export default compose(
  withState('active', 'setActive', 1),
  withHandlers({
    openMessages: ({setActive, clickHandler}) => {
      return (id) => {
        clickHandler(id);

        return setActive(id);
      };
    }}),
  graphql(chatRoomsQuery),
  mapProps(({data, ...rest}) => {
    const chatRooms = (data && data.rooms) || [];
    return {
      chatRooms,
      ...rest,
    };
  })
)(ChatRoom);

