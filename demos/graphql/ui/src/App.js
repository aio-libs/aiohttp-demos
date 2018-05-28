import React from 'react';
import AppProvider from './client/Provider';
import Chatroom from './components';
import './App.css';


export default function App() {
  return (
    <AppProvider>
      <div className="App">
        <Chatroom />
      </div>
    </AppProvider>
  );
};
