import React, { useEffect, useState } from "react";

import { Button } from "react-bootstrap";

import { Link, useNavigate } from "react-router-dom";

import RFID from "../types/RFID";
import RFIDTable from "../components/RFIDTable";

function Home() {
  const [rfids, setRfids] = useState<RFID[]>([])
  const navigate = useNavigate();

  useEffect(() => {
    function getRfids() {
      fetch('/api/rfid_numbers/')
        .then(response => response.json())
        .then(data => setRfids(data));
    }
    getRfids();
  }, []);

  const deleteRfid = (rfid: RFID) => {
    fetch(`/api/rfid_numbers/${rfid.id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json"
      },
    })
      .then(response => response.json())
      .then(data => {
        const newRfids = rfids.filter((item: RFID) => item.id !== rfid.id);
        setRfids(newRfids);
      })
      .catch(error => {
        console.log(error)
      });
  }

  const playRfid = async (rfid: RFID) => {
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

  const navigateToRfidModify = (rfid: RFID) => {
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
      <RFIDTable rfids={rfids} onPlay={playRfid} onDelete={deleteRfid} onModify={navigateToRfidModify} />
    </div>
  );
}

export default Home;