import React from 'react';

const BugList = ({ bugs }) => {
  if (!bugs || bugs.length === 0) {
    return (
      <div className="p-4 text-gray-500">
        <p>No bugs detected.</p>
      </div>
    );
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-50';
      case 'warning': return 'text-yellow-600 bg-yellow-50';
      case 'info': return 'text-blue-600 bg-blue-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="p-4 space-y-3">
      <h3 className="text-lg font-semibold">Detected Issues ({bugs.length})</h3>
      
      {bugs.map((bug, index) => (
        <div key={index} className="border rounded-lg p-4">
          <div className="flex justify-between items-start mb-2">
            <h4 className="font-medium">{bug.title}</h4>
            <span className={`px-2 py-1 rounded text-xs font-medium ${getSeverityColor(bug.severity)}`}>
              {bug.severity}
            </span>
          </div>
          
          <p className="text-gray-600 text-sm mb-2">{bug.description}</p>
          
          {bug.line && (
            <p className="text-sm text-gray-500">
              Line {bug.line}: {bug.codeSnippet}
            </p>
          )}
          
          {bug.suggestion && (
            <div className="mt-3 p-3 bg-blue-50 rounded">
              <p className="text-sm font-medium text-blue-900">Suggestion:</p>
              <p className="text-sm text-blue-700">{bug.suggestion}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default BugList;
