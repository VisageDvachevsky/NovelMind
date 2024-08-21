import React from 'react';
import PropTypes from 'prop-types';

const FileItem = ({ name, type, indentLevel }) => {
  return (
    <div style={{ paddingLeft: `${indentLevel * 20}px` }}>
      {type === 'directory' ? (
        <span role="img" aria-label="folder">
          📁
        </span>
      ) : (
        <span role="img" aria-label="file">
          📄
        </span>
      )}
      <span style={{ marginLeft: '10px' }}>{name}</span>
    </div>
  );
};

FileItem.propTypes = {
  name: PropTypes.string.isRequired,
  type: PropTypes.oneOf(['file', 'directory']).isRequired,
  indentLevel: PropTypes.number.isRequired,
};

const FileList = ({ files, indentLevel = 0 }) => {
  return (
    <div>
      {files.map((file) => (
        <div key={file.name}>
          <FileItem name={file.name} type={file.type} indentLevel={indentLevel} />
          {file.type === 'directory' && file.contents && (
            <FileList files={file.contents} indentLevel={indentLevel + 1} />
          )}
        </div>
      ))}
    </div>
  );
};

FileList.propTypes = {
  files: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      type: PropTypes.oneOf(['file', 'directory']).isRequired,
      contents: PropTypes.array, 
    })
  ).isRequired,
  indentLevel: PropTypes.number,
};

export default FileList;
