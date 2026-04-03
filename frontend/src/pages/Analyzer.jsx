import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Code, FileCode2, LayoutTemplate, Activity, AlertTriangle, Info, PlayCircle } from 'lucide-react';
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

  const loadSample = () => setCode(sampleCode[language] || '');

  const tabs = [
    { id: 'results', label: 'Results', icon: Activity },
    { id: 'score', label: 'Score', icon: LayoutTemplate },
    { id: 'bugs', label: 'Bugs', icon: AlertTriangle },
    { id: 'visualization', label: 'Visual', icon: PlayCircle },
    { id: 'info', label: 'Info', icon: Info },
  ];

  return (
    <div className="min-h-screen bg-background p-6 pt-12 relative overflow-hidden">
      {/* Background Orbs */}
      <div className="absolute -top-20 -left-20 w-[30rem] h-[30rem] bg-indigo-600/10 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute top-1/3 -right-20 w-[20rem] h-[20rem] bg-accent-500/10 rounded-full blur-[100px] pointer-events-none" />

      <div className="container mx-auto max-w-7xl relative z-10">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-4 mb-8"
        >
          <div className="p-3 rounded-2xl border border-white/10 shadow-lg" style={{ background: 'rgba(14,165,233,0.12)' }}>
            <Code className="text-primary-400" size={28} />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-white" style={{ textShadow: '0 0 40px rgba(14,165,233,0.5)' }}>
              TraceWise <span className="text-gradient">Workspace</span>
            </h1>
            <p className="text-slate-400 text-sm mt-1">Select logic, analyze complexity, and visualize execution.</p>
          </div>
        </motion.div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8 min-h-[75vh]">
          {/* Editor Panel */}
          <motion.div 
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass-panel flex flex-col rounded-3xl overflow-hidden shadow-2xl"
          >
            {/* Toolbar */}
            <div className="px-6 py-4 border-b border-white/5 bg-surface-lighter/50 flex justify-between items-center backdrop-blur-md">
              <div className="flex items-center gap-3">
                <FileCode2 size={18} className="text-slate-400" />
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="bg-surface border border-white/10 text-slate-200 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block px-3 py-1.5 outline-none transition-all"
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="cpp">C++</option>
                </select>
              </div>
              <button
                onClick={loadSample}
                className="text-xs font-medium text-slate-400 hover:text-primary-400 transition-colors px-3 py-1.5 rounded-lg hover:bg-primary-400/10"
              >
                Load Example
              </button>
            </div>
            
            {/* Editor Container */}
            <div className="flex-1 relative bg-[#1e1e1e]/60">
              <CodeEditor code={code} setCode={setCode} language={language} />
            </div>
            
            {/* Footer Action */}
            <div className="p-4 border-t border-white/5 bg-surface-lighter/50 backdrop-blur-md">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full relative group overflow-hidden bg-primary-600 text-white py-3.5 px-6 rounded-xl font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-[0_0_20px_rgba(2,132,199,0.4)]"
              >
                <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-primary-400 to-primary-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                <div className="relative flex items-center justify-center gap-2">
                  {loading ? (
                    <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }}>
                      <Activity size={20} />
                    </motion.div>
                  ) : (
                    <Play size={20} className="group-hover:translate-x-1 transition-transform" />
                  )}
                  <span>{loading ? 'Analyzing Source Code...' : 'Execute Analysis'}</span>
                </div>
              </button>
            </div>
          </motion.div>
          
          {/* Results Panel */}
          <motion.div 
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass-panel flex flex-col rounded-3xl overflow-hidden shadow-2xl relative"
          >
            {results ? (
              <div className="flex flex-col h-full">
                {/* Navigation */}
                <div className="border-b border-white/5 bg-surface-lighter/50 px-2 pt-2">
                  <nav className="flex overflow-x-auto hide-scrollbar">
                    {tabs.map((tab) => {
                      const Icon = tab.icon;
                      const isActive = activeTab === tab.id;
                      return (
                        <button
                          key={tab.id}
                          onClick={() => setActiveTab(tab.id)}
                          className={`relative px-5 py-3.5 text-sm font-medium transition-colors flex items-center gap-2 whitespace-nowrap ${
                            isActive ? 'text-primary-400' : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                          }`}
                        >
                          <Icon size={16} />
                          {tab.label}
                          {isActive && (
                            <motion.div
                              layoutId="activeTabIndicator"
                              className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-500 shadow-[0_0_8px_rgba(14,165,233,0.8)]"
                              initial={false}
                              transition={{ type: "spring", stiffness: 500, damping: 30 }}
                            />
                          )}
                        </button>
                      );
                    })}
                  </nav>
                </div>
                
                {/* Content Area */}
                <div className="flex-1 overflow-y-auto p-6 scroll-smooth">
                  <AnimatePresence mode="wait">
                    <motion.div
                      key={activeTab}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      transition={{ duration: 0.2 }}
                      className="h-full"
                    >
                      {activeTab === 'results' && <ResultPanel results={results} />}
                      {activeTab === 'score' && <ScoreCard score={results.score} details={results.score_details || results.scoreDetails} />}
                      {activeTab === 'bugs' && <BugList bugs={results.bugs} />}
                      {activeTab === 'visualization' && <VisualizationPanel visualizationData={results.visualization} />}
                      {activeTab === 'info' && <AlgorithmInfo algorithmInfo={results.algorithm_info || results.algorithmInfo} />}
                    </motion.div>
                  </AnimatePresence>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-gradient-to-b from-transparent to-surface-lighter/20">
                <div className="w-24 h-24 mb-6 rounded-full border border-white/10 flex items-center justify-center bg-surface-lighter shadow-[0_0_30px_rgba(255,255,255,0.02)]">
                  <Activity size={40} className="text-slate-600" />
                </div>
                <h3 className="text-2xl font-semibold text-slate-300 mb-3">Awaiting Payload</h3>
                <p className="text-slate-500 max-w-sm leading-relaxed mb-6">
                  Input your code and execute analysis to see performance metrics, bugs, and visual traces here.
                </p>
                <button onClick={loadSample} className="text-primary-500 hover:text-primary-400 text-sm font-medium flex items-center gap-2 group">
                  <Code size={16} className="group-hover:rotate-12 transition-transform" />
                  Try example code
                </button>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Analyzer;
