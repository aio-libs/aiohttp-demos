import React from 'react';

import AppProvider from './client/Provider';
import ChatRoom from './components/index';
import Header from './components/Header/Header';
import ChatMessages from './components/ChatMessages/ChatMessages';

// styles
import './App.css';


export default class extends React.Component {
  state = {
    activeRoom: 1,
  };

  changeRoom = (item) => {
    this.setState({activeRoom: item});
  };

  render () {
    return (
      <AppProvider>
        <div className="App">
          <div className="content">
            <Header />
            <div className="main">
              <ChatRoom clickHandler={this.changeRoom}/>
              <ChatMessages id={this.state.activeRoom} />
            </div>
          </div>
        </div>
      </AppProvider>
    );
  }
};
