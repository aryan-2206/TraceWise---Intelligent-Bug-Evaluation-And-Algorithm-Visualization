import React from 'react';

const AlgorithmInfo = ({ algorithmInfo }) => {
  if (!algorithmInfo) {
    return (
      <div className="p-4 text-gray-500">
        <p>No algorithm information available.</p>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <h3 className="text-lg font-semibold">Algorithm Information</h3>
      
      <div className="bg-white rounded-lg p-4 space-y-3">
        <div>
          <h4 className="font-medium text-gray-900">Algorithm Type</h4>
          <p className="text-gray-700">{algorithmInfo.name}</p>
        </div>
        
        <div>
          <h4 className="font-medium text-gray-900">Description</h4>
          <p className="text-gray-700">{algorithmInfo.description}</p>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <h4 className="font-medium text-gray-900">Time Complexity</h4>
            <p className="text-gray-700">{algorithmInfo.timeComplexity}</p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900">Space Complexity</h4>
            <p className="text-gray-700">{algorithmInfo.spaceComplexity}</p>
          </div>
        </div>
        
        {algorithmInfo.bestCase && (
          <div>
            <h4 className="font-medium text-gray-900">Best Case</h4>
            <p className="text-gray-700">{algorithmInfo.bestCase}</p>
          </div>
        )}
        
        {algorithmInfo.worstCase && (
          <div>
            <h4 className="font-medium text-gray-900">Worst Case</h4>
            <p className="text-gray-700">{algorithmInfo.worstCase}</p>
          </div>
        )}
        
        {algorithmInfo.useCases && algorithmInfo.useCases.length > 0 && (
          <div>
            <h4 className="font-medium text-gray-900">Common Use Cases</h4>
            <ul className="list-disc list-inside text-gray-700">
              {algorithmInfo.useCases.map((useCase, index) => (
                <li key={index}>{useCase}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default AlgorithmInfo;
