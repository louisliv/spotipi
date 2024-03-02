import React, { useEffect, useState } from "react";

import { useLocation, useNavigate } from "react-router-dom";

import { Form, Button } from 'react-bootstrap';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSpinner } from "@fortawesome/free-solid-svg-icons";

import { capitalize } from "../../utils/utils";

const RfidModify = () => {
  const { state } = useLocation();
  const [fetchingFromSpotify, setFetchingFromSpotify] = useState(false);
  const [modifiedRfid, setModifiedRfid] = useState<any>({});
  const navigate = useNavigate();
  const rfid = state?.rfid;
  const [modifyType, setModifyType] = useState("Create");
  const [formIsValid, setFormIsValid] = useState(false)

  useEffect(() => {
    if (!rfid) {
      navigate("/");
    }

    setModifiedRfid(rfid);

    if (rfid?.id) {
      setModifyType("Update");
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (
      modifiedRfid.number &&
      modifiedRfid.spotify_token_type &&
      modifiedRfid.spotify_token &&
      modifiedRfid.spotify_name
    ) {
      setFormIsValid(true);
    } else {
      setFormIsValid(false);
    }
  }, [modifiedRfid])

  const tokenTypeOptions = [
    "artist",
    "album",
    "playlist",
    "track"
  ]

  const submit = async (event: any) => {
    if (rfid?.id) {
      try {
        var request = await fetch(`/api/rfid_numbers/${rfid.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(modifiedRfid)
        })
        var response = await request.json();
        if (request.status >= 400) throw new Error(response);
        navigate("/");
      } catch (error) {
        console.log(error)
      }
    } else {
      try {
        var req = await fetch("/api/rfid_numbers/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(modifiedRfid)
        })
        var res = await req.json();
        if (req.status >= 400) throw new Error(res);
        navigate("/");
      } catch (error) {
        console.log(error)
      }
    }
  }

  const onChange = (event: any, name: string) => {
    let value = event.target.value;
    setModifiedRfid({...modifiedRfid, [name]: value});
  }

  const onTokenChange = async (event: any) => {
    let value = event.target.value;
    
    if (!value) {
      console.log("here")
      setModifiedRfid({...modifiedRfid, spotify_name: value, spotify_token: value})
      return;
    }

    setFetchingFromSpotify(true);

    try {
      var request = await fetch("/api/spotify/item_info", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          item_id: value,
          item_type: modifiedRfid.spotify_token_type
        })
      })

      var response = await request.json();

      if (request.status >= 400) throw new Error(response);
    } catch (error) {
      console.log(error)
      setModifiedRfid({...modifiedRfid, spotify_name: "", spotify_token: value})
      setFetchingFromSpotify(false);
      return;
    }
    setModifiedRfid({...modifiedRfid, spotify_name: response.name, spotify_token: value});
    setFetchingFromSpotify(false);
  }

  return (
    <div>
      <h1 className="mt-3">{modifyType} RFID</h1>
      <Form>
        <Form.Group className="mb-3" controlId="formRFIDNumber">
          <Form.Label>RFID Number</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter RFID Number"
            value={modifiedRfid.number} 
            onChange={(event) => onChange(event, "number")}
            />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formSpotifyTokenType">
          <Form.Label>Spotify Token Type</Form.Label>
          <Form.Select
            aria-label="Select Spotify Token Type"
            value={modifiedRfid.spotify_token_type}
            onChange={(event) => onChange(event, "spotify_token_type")}
            >
            <option value="" />
            {tokenTypeOptions.map((option: string) => {
              return <option key={option} value={option}>{capitalize(option)}</option>
            })}
          </Form.Select>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formSpotifyToken">
          <Form.Label>Spotify Token</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter Spotify Token"
            value={modifiedRfid.spotify_token} 
            onChange={(event) => onTokenChange(event)}
            disabled={!modifiedRfid.spotify_token_type}
            />
          <FontAwesomeIcon icon={faSpinner} spin visibility={fetchingFromSpotify ? "visible" : "hidden"} />
        </Form.Group>
        <Form.Group className="mb-5" controlId="formSpotifyName">
          <Form.Label>Spotify Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter Spotify Name"
            value={modifiedRfid.spotify_name}
            disabled
            />
        </Form.Group>
        <Form.Group className="mb-3 d-flex justify-content-end" controlId="formSpotifySubmit">
          <Button variant="success" onClick={submit} disabled={!formIsValid}>
            Submit
          </Button>
        </Form.Group>
      </Form>
    </div>
  );
}

export default RfidModify;