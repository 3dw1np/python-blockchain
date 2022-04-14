import React, { useState, useEffect } from 'react';
import logo from '../assets/logo.png'
import { API_BASE_URL } from '../config'
import Blockchain from './Blockchain';

function App() {
   const [walletInfo, setWalletInfo] = useState({});

   useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/info`)
      .then(r => r.json())
      .then(json => setWalletInfo(json))
   }, [])

   const { address, balance } = walletInfo;

  return (
    <div className="App"> 
      <img className="logo" src={logo} alt="app-logo" />
      <h3>Welcome to pychain</h3>
      <hr />
      <div className='WalletInfo'>
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
      <br />
      <Blockchain />
    </div>
  );
}

export default App;
