import React, { useState } from 'react';
import CodeEditor from '../components/CodeEditor';
import ResultPanel from '../components/ResultPanel';
import ScoreCard from '../components/ScoreCard';
import VisualizationPanel from '../components/VisualizationPanel';
import BugList from '../components/BugList';
import AlgorithmInfo from '../components/AlgorithmInfo';
import { analyzeCode } from '../services/api';

const Analyzer = () => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [activeTab, setActiveTab] = useState('results');

  const handleAnalyze = async () => {
    if (!code.trim()) {
      alert('Please enter some code to analyze');
      return;
    }

    setLoading(true);
    try {
      const analysisResults = await analyzeCode(code, language);
      setResults(analysisResults);
      setActiveTab('results');
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const sampleCode = {
    python: `def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1`,
    
    javascript: `function binarySearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;
    
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (arr[mid] === target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}`,
    
    cpp: `int binarySearch(const vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}`
  };

  const loadSample = () => {
    setCode(sampleCode[language] || '');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Code Analyzer</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Code Editor Section */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="p-4 border-b">
              <div className="flex justify-between items-center">
                <div className="flex items-center space-x-4">
                  <label className="text-sm font-medium">Language:</label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="border rounded px-3 py-1 text-sm"
                  >
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="cpp">C++</option>
                  </select>
                </div>
                <button
                  onClick={loadSample}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Load Sample
                </button>
              </div>
            </div>
            
            <div className="h-96">
              <CodeEditor code={code} setCode={setCode} language={language} />
            </div>
            
            <div className="p-4 border-t">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400"
              >
                {loading ? 'Analyzing...' : 'Analyze Code'}
              </button>
            </div>
          </div>
          
          {/* Results Section */}
          <div className="bg-white rounded-lg shadow-md">
            {results ? (
              <div>
                <div className="border-b">
                  <nav className="flex space-x-8 px-4">
                    {['results', 'score', 'bugs', 'visualization', 'info'].map((tab) => (
                      <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`py-4 px-1 border-b-2 font-medium text-sm capitalize ${
                          activeTab === tab
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700'
                        }`}
                      >
                        {tab}
                      </button>
                    ))}
                  </nav>
                </div>
                
                <div className="h-96 overflow-y-auto">
                  {activeTab === 'results' && <ResultPanel results={results} />}
                  {activeTab === 'score' && <ScoreCard score={results.score} details={results.scoreDetails} />}
                  {activeTab === 'bugs' && <BugList bugs={results.bugs} />}
                  {activeTab === 'visualization' && <VisualizationPanel visualizationData={results.visualization} />}
                  {activeTab === 'info' && <AlgorithmInfo algorithmInfo={results.algorithmInfo} />}
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-96 text-gray-500">
                <div className="text-center">
                  <p className="mb-4">Enter code and click "Analyze Code" to see results</p>
                  <button onClick={loadSample} className="text-blue-600 hover:text-blue-800">
                    Load Sample Code
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analyzer;
