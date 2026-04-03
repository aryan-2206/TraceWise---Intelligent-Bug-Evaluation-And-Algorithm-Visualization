import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            TraceWise
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Advanced algorithm analysis and visualization tool. Detect bugs, analyze complexity, 
            and understand your code better with interactive visualizations.
          </p>
          
          <Link
            to="/analyzer"
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Start Analyzing
          </Link>
        </div>
        
        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-blue-600 text-3xl mb-4">🔍</div>
            <h3 className="text-lg font-semibold mb-2">Smart Detection</h3>
            <p className="text-gray-600">
              Automatically identify algorithms and detect potential bugs in your code.
            </p>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-green-600 text-3xl mb-4">📊</div>
            <h3 className="text-lg font-semibold mb-2">Complexity Analysis</h3>
            <p className="text-gray-600">
              Get detailed time and space complexity analysis with scoring.
            </p>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="text-purple-600 text-3xl mb-4">🎯</div>
            <h3 className="text-lg font-semibold mb-2">Interactive Visualization</h3>
            <p className="text-gray-600">
              Step through algorithm execution with interactive visualizations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
