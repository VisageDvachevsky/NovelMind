import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import PasswordDialog from "./PasswordDialog";
import FileActions from "./FileActions";
import { deployFileSystem } from '../services/systemOperations';
import { getCurrentDirectory, listFiles } from '../services/fileOperations';
import FileList from './FileList';

function FileManager() {
  const [showPasswordDialog, setShowPasswordDialog] = useState(false);
  const [currentDir, setCurrentDir] = useState("Not deployed");
  const [fileList, setFileList] = useState([]);

  const handleDeploy = async (password, basePath) => {
    try {
      await deployFileSystem(basePath, password);
      const dir = await getCurrentDirectory();
      const files = await listFiles();
      setFileList(files);
      setCurrentDir(dir);
    } catch (error) {
      alert("Failed to deploy file system");
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const dir = await getCurrentDirectory();
        const files = await listFiles();
        setFileList(files);
        setCurrentDir(dir);
      } catch (error) {
        console.log("Error fetching files", error);
      }
    };
    fetchData();
  }, []);

  return (
    <Container>
      <Row className="mt-3">
        <Col>
          <h4>Current Directory: {currentDir}</h4>
        </Col>
        <Col className="text-right">
          <Button onClick={() => setShowPasswordDialog(true)}>
            Deploy File System
          </Button>
        </Col>
      </Row>
      <Row>
        <Col>
          {/* Используем компонент FileList для отображения файлов */}
          <FileList files={fileList} />
        </Col>
      </Row>
      <Row>
        <Col>
          <FileActions onActionComplete={async () => {
            const files = await listFiles();
            setFileList(files);
          }} />
        </Col>
      </Row>

      <PasswordDialog
        show={showPasswordDialog}
        handleClose={() => setShowPasswordDialog(false)}
        onPasswordSubmit={handleDeploy}
      />
    </Container>
  );
}

export default FileManager;
