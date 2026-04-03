import React from 'react';

const ScoreCard = ({ score, details }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="text-center">
        <div className={`text-4xl font-bold ${getScoreColor(score)}`}>
          {score}/100
        </div>
        <div className="text-gray-600 mt-2">
          {getScoreLabel(score)}
        </div>
      </div>
      
      {details && (
        <div className="mt-6 space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-600">Readability:</span>
            <span className="font-medium">{details.component_scores?.readability ?? 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Efficiency:</span>
            <span className="font-medium">{details.component_scores?.efficiency ?? 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Correctness:</span>
            <span className="font-medium">{details.component_scores?.correctness ?? 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Best Practices:</span>
            <span className="font-medium">{details.component_scores?.best_practices ?? 'N/A'}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ScoreCard;
