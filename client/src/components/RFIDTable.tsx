import React from "react";

import { Table } from "react-bootstrap";

import RFID from "../types/RFID";

interface RFIDTableProps {
  data: RFID[];
}

const RFIDTable = ({data}: RFIDTableProps) => {
  return (
    <Table>
      <thead>
        <tr>
          <th>ID</th>
          <th>RFID</th>
          <th>Spotify Token</th>
          <th>Token Type</th>
          <th>Spotify Name</th>
        </tr>
      </thead>
      <tbody>
        {data.map((rfid) => (
          <tr key={rfid.id}>
            <td>{rfid.id}</td>
            <td>{rfid.number}</td>
            <td>{rfid.spotify_token}</td>
            <td>{rfid.spotify_token_type}</td>
            <td>{rfid.spotify_name}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default RFIDTable;
