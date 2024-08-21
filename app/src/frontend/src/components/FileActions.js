import React from "react";
import { ButtonGroup, Button } from "react-bootstrap";
import {
  addFile,
  readFile,
  deleteFile,
  createDirectory,
  renameDirectory,
  deleteDirectory,
  moveFile,
  changeDirectory,
} from "../services/fileOperations";

function FileActions({ onActionComplete }) {
  const handleAddFile = async () => {
    const filePath = prompt("Enter file path");
    const fileId = prompt("Enter file ID");
    if (filePath && fileId) {
      await addFile(filePath, fileId);
      onActionComplete();
    }
  };

  const handleReadFile = async () => {
    const fileId = prompt("Enter file ID to read");
    if (fileId) {
      const content = await readFile(fileId);
      alert(`File content: ${content}`);
    }
  };

  const handleDeleteFile = async () => {
    const fileId = prompt("Enter file ID to delete");
    if (fileId) {
      await deleteFile(fileId);
      onActionComplete();
    }
  };

  const handleCreateDirectory = async () => {
    const dirName = prompt("Enter directory name");
    if (dirName) {
      await createDirectory(dirName);
      onActionComplete();
    }
  };

  const handleRenameDirectory = async () => {
    const oldName = prompt("Enter current directory name");
    const newName = prompt("Enter new directory name");
    if (oldName && newName) {
      await renameDirectory(oldName, newName);
      onActionComplete();
    }
  };

  const handleDeleteDirectory = async () => {
    const dirName = prompt("Enter directory name to delete");
    if (dirName) {
      await deleteDirectory(dirName);
      onActionComplete();
    }
  };

  const handleMoveFile = async () => {
    const fileId = prompt("Enter file ID to move");
    const destDir = prompt("Enter destination directory");
    if (fileId && destDir) {
      await moveFile(fileId, destDir);
      onActionComplete();
    }
  };

  const handleChangeDirectory = async () => {
    const dirName = prompt("Enter directory name to change to");
    if (dirName) {
      await changeDirectory(dirName);
      onActionComplete();
    }
  };

  return (
    <ButtonGroup className="mt-3">
      <Button onClick={handleAddFile}>Add File</Button>
      <Button onClick={handleReadFile}>Read File</Button>
      <Button onClick={handleDeleteFile}>Delete File</Button>
      <Button onClick={handleCreateDirectory}>Create Directory</Button>
      <Button onClick={handleRenameDirectory}>Rename Directory</Button>
      <Button onClick={handleDeleteDirectory}>Delete Directory</Button>
      <Button onClick={handleMoveFile}>Move File</Button>
      <Button onClick={handleChangeDirectory}>Change Directory</Button>
    </ButtonGroup>
  );
}

export default FileActions;
