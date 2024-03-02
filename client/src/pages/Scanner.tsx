import React, {useState} from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faNfcSymbol } from "@fortawesome/free-brands-svg-icons";

import { useNavigate } from "react-router-dom";
import useWebSocket from "react-use-websocket";

import { Button } from "react-bootstrap";

import { baseWSUrl } from "../utils/utils";
import RFID from "../types/RFID";

const WS_URL = `ws://${baseWSUrl}/api/rfid_numbers/ws/rfid_number`;

function Scanner() {
  const [scannedRfid, setScannedRfid] = useState<RFID | null>(null);
  const [scanning, setScanning] = useState(true);
  const [scanSuccessful, setScanSuccessful] = useState(false);
  const [beatClass, setBeatClass] = useState("fa-beat-fade");
  const navigate = useNavigate();
  
  useWebSocket(WS_URL, {
    onMessage: (event: any) => {
      console.log(event.data);
      var data = JSON.parse(event.data)

      if (data?.type === "rfid_number") {
        setScannedRfid(data?.rfid_number)
        setBeatClass("")
        setScanSuccessful(true)
        setScanning(false)
      }
    }
  });

  const tryAgain = (event: any) => {
    setScanning(true)
    setBeatClass("fa-beat-fade")
  }

  const navigateToRfidModify = (event: any) => {
    navigate("/rfids/modify", {state: {rfid: scannedRfid}});
  }

  return (
    <div className="d-flex flex-column align-items-center">
      <h1 className="mt-5">Please scan RFID tag...</h1>
      <FontAwesomeIcon icon={faNfcSymbol} className={`${beatClass} mt-5`} size="10x" />
      {!scanning && scanSuccessful &&
        (
          <>
            <div className="mt-5"><h2>RFID scanned successfully!</h2></div>
            <div className="mt-5"><h3>RFID: {scannedRfid?.number}</h3></div>
            <Button variant="success" className="mt-5" onClick={navigateToRfidModify}>Link Spotify Token</Button>
          </>
        )
      }
      {!scanning && !scanSuccessful &&
        (
          <>
            <div className="mt-5"><h2>RFID scan failed!</h2></div>
            <Button variant="primary" className="mt-5" onClick={tryAgain}>Try Again</Button>
          </>
        )
      }
    </div>
  );
}

export default Scanner;
