import React from "react";

import { Table, Button } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPencil, faTrash, faPlay } from "@fortawesome/free-solid-svg-icons";

import RFID from "../types/RFID";
import { capitalize } from "../utils/utils";

interface RFIDTableProps {
  rfids: RFID[];
  onPlay: (rfid: RFID) => void;
  onDelete: (rfid: RFID) => void;
  onModify: (rfid: RFID) => void;
}

const RFIDTable = ({rfids, onPlay, onDelete, onModify}: RFIDTableProps) => {
  const playRfid = (event: any, rfid: RFID) => {
    onPlay(rfid);
  }

  const deleteRfid = (event: any, rfid: RFID) => {
    onDelete(rfid);
  }

  const navigateToRfidModify = (event: any, rfid: RFID) => {
    onModify(rfid);
  }

  return (
    <Table>
        <thead>
          <tr>
            <th>Id</th>
            <th>RFID</th>
            <th>Spotify Token</th>
            <th>Token Type</th>
            <th>Spotify Name</th>
            <th></th>
          </tr>
          {rfids.map((rfid: any) => {
            return (
              <tr key={rfid.id}>
                <td>{rfid.id}</td>
                <td>{rfid.number}</td>
                <td>{rfid.spotify_token}</td>
                <td>{capitalize(rfid.spotify_token_type)}</td>
                <td>{rfid.spotify_name}</td>
                <td>
                  <div className="d-flex justify-content-end align-items-center" >
                    <Button variant="success" className="me-3" onClick={(event) => playRfid(event, rfid)}>
                      <FontAwesomeIcon icon={faPlay} />
                    </Button>
                    <Button variant="primary" className="me-3" onClick={(event) => navigateToRfidModify(event, rfid)}>
                      <FontAwesomeIcon icon={faPencil} />
                    </Button>
                    <Button variant="danger" onClick={(event) => deleteRfid(event, rfid)}>
                      <FontAwesomeIcon icon={faTrash}/>
                    </Button>
                  </div>
                </td>
              </tr>
            )
          })}
        </thead>
      </Table>
  );
};

export default RFIDTable;
