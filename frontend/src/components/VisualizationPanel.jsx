import React, { useState } from 'react';

const VisualizationPanel = ({ visualizationData }) => {
  const [currentStep, setCurrentStep] = useState(0);

  if (!visualizationData) {
    return (
      <div className="p-4 text-gray-500">
        <p>No visualization data available.</p>
      </div>
    );
  }

  const renderStepVisualization = () => {
    const step = visualizationData.steps[currentStep];
    
    switch (visualizationData.type) {
      case 'binary_search':
        return (
          <div className="space-y-4">
            <div className="flex justify-center space-x-2">
              {step.array.map((value, index) => (
                <div
                  key={index}
                  className={`w-12 h-12 flex items-center justify-center rounded ${
                    index === step.left ? 'bg-green-200' :
                    index === step.right ? 'bg-red-200' :
                    index === step.mid ? 'bg-yellow-200' :
                    'bg-gray-100'
                  }`}
                >
                  {value}
                </div>
              ))}
            </div>
            <div className="text-center text-sm">
              <p>Left: {step.left}, Right: {step.right}, Mid: {step.mid}</p>
              <p>Target: {step.target}, Found: {step.found ? 'Yes' : 'No'}</p>
            </div>
          </div>
        );
      
      case 'sorting':
        return (
          <div className="space-y-4">
            <div className="flex justify-center space-x-2">
              {step.array.map((value, index) => (
                <div
                  key={index}
                  className={`w-12 h-12 flex items-center justify-center rounded ${
                    step.comparing?.includes(index) ? 'bg-yellow-200' :
                    step.swapped?.includes(index) ? 'bg-green-200' :
                    'bg-gray-100'
                  }`}
                >
                  {value}
                </div>
              ))}
            </div>
            <div className="text-center text-sm">
              <p>Step {currentStep + 1}: {step.description}</p>
            </div>
          </div>
        );
      
      default:
        return <div>Visualization not available for this algorithm type.</div>;
    }
  };

  return (
    <div className="p-4 space-y-4">
      <h3 className="text-lg font-semibold">Algorithm Visualization</h3>
      
      <div className="bg-white rounded-lg p-4">
        {renderStepVisualization()}
      </div>
      
      <div className="flex justify-between items-center">
        <button
          onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
          disabled={currentStep === 0}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
        >
          Previous
        </button>
        
        <span className="text-sm text-gray-600">
          Step {currentStep + 1} of {visualizationData.steps.length}
        </span>
        
        <button
          onClick={() => setCurrentStep(Math.min(visualizationData.steps.length - 1, currentStep + 1))}
          disabled={currentStep === visualizationData.steps.length - 1}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default VisualizationPanel;
