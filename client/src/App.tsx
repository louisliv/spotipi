import React from 'react';

import { Container } from 'react-bootstrap';
import { Routes, Route } from 'react-router-dom';

import Home from './pages/Home';
import Scanner from './pages/Scanner';
import RfidModify from './pages/rfids/Modify';
import Settings from './pages/Settings';

import SiteNavbar from './components/Navbar';

import './App.scss';

function App() {
  return (
    <div>
      <SiteNavbar />
      <Container>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/scanner" element={<Scanner />} />
          <Route path="/rfids/modify" element={<RfidModify />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Container>
    </div>
  );
}

export default App;
