import React from 'react';

const ResultPanel = ({ results }) => {
  if (!results) {
    return (
      <div className="p-4 text-gray-500">
        <p>No analysis results available.</p>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <h3 className="text-lg font-semibold">Analysis Results</h3>
      
      {results.algorithm && (
        <div className="bg-blue-50 p-3 rounded">
          <h4 className="font-medium text-blue-900">Detected Algorithm</h4>
          <p className="text-blue-700">{results.algorithm}</p>
        </div>
      )}

      {results.complexity && (
        <div className="bg-green-50 p-3 rounded">
          <h4 className="font-medium text-green-900">Time Complexity</h4>
          <p className="text-green-700">{results.complexity}</p>
        </div>
      )}

      {results.bugs && results.bugs.length > 0 && (
        <div className="bg-red-50 p-3 rounded">
          <h4 className="font-medium text-red-900">Detected Issues</h4>
          <ul className="list-disc list-inside text-red-700">
            {results.bugs.map((bug, index) => (
              <li key={index}>{bug}</li>
            ))}
          </ul>
        </div>
      )}

      {results.score && (
        <div className="bg-purple-50 p-3 rounded">
          <h4 className="font-medium text-purple-900">Quality Score</h4>
          <p className="text-purple-700">{results.score}/100</p>
        </div>
      )}
    </div>
  );
};

export default ResultPanel;
