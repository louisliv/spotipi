import React from "react";

import { Modal } from "react-bootstrap";

interface TokenHelpModalProps {
  show: boolean;
  handleClose: () => void;
}

const TokenHelpModal = ({ show, handleClose }: TokenHelpModalProps) => {
  return (
    <Modal show={show} onHide={handleClose} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>Linking Spotify Token</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div className="mb-3">
          You will need to provide both the Spotify token type and the Spotify token for 
          the RFID tag. These two fields can be found in the url for the media you want to
          connect. Use the image below as a guide.
        </div>
        <img src="/spotify_token_help.png" alt="Spotify Token Help" style={ { maxWidth: "100%" } } />
      </Modal.Body>
    </Modal>
  );
}

export default TokenHelpModal;
