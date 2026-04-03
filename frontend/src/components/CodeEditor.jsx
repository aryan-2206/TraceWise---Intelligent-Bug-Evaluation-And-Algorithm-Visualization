import React, { useState } from 'react';
import { Editor } from '@monaco-editor/react';

const CodeEditor = ({ code, setCode, language }) => {
  const handleEditorChange = (value) => {
    setCode(value);
  };

  return (
    <div className="h-full">
      <Editor
        height="100%"
        language={language}
        value={code}
        onChange={handleEditorChange}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          wordWrap: 'on',
          automaticLayout: true,
        }}
      />
    </div>
  );
};

export default CodeEditor;
