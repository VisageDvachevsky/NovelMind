import React, { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";

function PasswordDialog({ show, handleClose, onPasswordSubmit }) {
  const [password, setPassword] = useState("");
  const [basePath, setBasePath] = useState("");

  const handleSubmit = () => {
    if (password.length >= 8 && basePath) {
      onPasswordSubmit(password, basePath);
      handleClose();
    } else {
      alert("Password must be at least 8 characters long and path cannot be empty.");
    }
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Deploy File System</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group controlId="formPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Form.Group>
          <Form.Group controlId="formBasePath">
            <Form.Label>Base Path</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter absolute path"
              value={basePath}
              onChange={(e) => setBasePath(e.target.value)}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Cancel
        </Button>
        <Button variant="primary" onClick={handleSubmit}>
          Deploy
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default PasswordDialog;
