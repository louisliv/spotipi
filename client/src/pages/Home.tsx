import React, { useEffect, useState } from "react";

import { Table, Button } from "react-bootstrap";

import { Link, useNavigate } from "react-router-dom";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPencil, faTrash, faPlay } from "@fortawesome/free-solid-svg-icons";

import { capitalize } from "../utils/utils";

function Home() {
  const [rfids, setRfids] = useState([])
  const navigate = useNavigate();

  useEffect(() => {
    function getRfids() {
      fetch('/api/rfid_numbers/')
        .then(response => response.json())
        .then(data => setRfids(data));
    }
    getRfids();
  }, []);

  const deleteRfid = (event: any, rfid: any) => {
    fetch(`/api/rfid_numbers/${rfid.id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json"
      },
    })
      .then(response => response.json())
      .then(data => {
        const newRfids = rfids.filter((item: any) => item.id !== rfid.id);
        setRfids(newRfids);
      })
      .catch(error => {
        console.log(error)
      });
  }

  const playRfid = async (event: any, rfid: any) => {
    try {
      const response = await fetch(`/api/rfid_numbers/play`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ rfid_number: rfid.number })
      });
      if (!response.ok) throw new Error(`RFID ${rfid.number} could not be played`);
    }
    catch (error) {
      console.log(error);
    }
  }

  const navigateToRfidModify = (event: any, rfid: any) => {
    navigate("/rfids/modify", { state: { rfid: rfid } });
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mt-3">
        <h1>RFIDs</h1>
        <Link to="/scanner">
          <Button variant="success">Scan</Button>
        </Link>
      </div>
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
    </div>
  );
}

export default Home;