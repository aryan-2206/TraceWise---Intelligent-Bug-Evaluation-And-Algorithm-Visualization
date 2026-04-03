import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PlayCircle, ChevronLeft, ChevronRight, Hash, Layers } from 'lucide-react';

const VisualizationPanel = ({ visualizationData }) => {
  const [currentStep, setCurrentStep] = useState(0);

  if (!visualizationData) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-center bg-surface-lighter/20 rounded-2xl border border-white/5 h-full">
        <PlayCircle size={48} className="text-slate-600 mb-4" />
        <p className="text-slate-400 font-medium">No execution trace data available.</p>
      </div>
    );
  }

  const renderStepVisualization = () => {
    if (!visualizationData.steps || visualizationData.steps.length === 0) {
      return (
        <div className="p-8 text-center bg-surface/50 rounded-xl border border-white/5">
           <Layers size={32} className="mx-auto mt-2 text-slate-600 mb-3" />
           <p className="text-slate-400">No step execution data available.</p>
        </div>
      );
    }
    
    const step = visualizationData.steps[currentStep];
    
    switch (visualizationData.type) {
      case 'binary_search':
        const searchArray = step.array || visualizationData.array || [];
        return (
          <div className="space-y-8 mt-4">
            <div className="flex flex-wrap justify-center gap-2 md:gap-3 perspective-1000">
              <AnimatePresence mode="popLayout">
                {searchArray.map((value, index) => {
                  let status = 'default';
                  let bgStyle = 'bg-surface-lighter border-white/10 text-slate-300';
                  let yOffset = 0;
                  
                  if (index === step.mid) {
                    status = 'mid';
                    bgStyle = 'bg-accent-500 text-white border-accent-400 shadow-[0_0_20px_rgba(139,92,246,0.6)]';
                    yOffset = -10;
                  } else if (index === step.left || index === step.right) {
                    status = 'bound';
                    bgStyle = 'bg-primary-500 text-white border-primary-400 shadow-[0_0_15px_rgba(14,165,233,0.4)]';
                  } else if (index < step.left || index > step.right) {
                    status = 'eliminated';
                    bgStyle = 'bg-surface border-white/5 text-slate-600 opacity-50';
                  }

                  if (step.found && index === step.mid) {
                     bgStyle = 'bg-green-500 text-white border-green-400 shadow-[0_0_25px_rgba(34,197,94,0.6)]';
                     yOffset = -15;
                  }

                  return (
                    <motion.div
                      layout
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1, y: yOffset }}
                      key={index}
                      className={`w-12 h-14 md:w-16 md:h-16 flex items-center justify-center rounded-xl border-2 font-mono text-lg font-bold transition-all duration-300 ${bgStyle}`}
                    >
                      {value}
                    </motion.div>
                  );
                })}
              </AnimatePresence>
            </div>
            
            <motion.div 
              key={`desc-${currentStep}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-surface/50 border border-white/5 p-4 rounded-xl flex flex-wrap gap-4 justify-center text-sm font-medium"
            >
              <div className="flex items-center gap-2 text-primary-400"><Hash size={16}/> L: {step.left}</div>
              <div className="flex items-center gap-2 text-accent-400"><Hash size={16}/> M: {step.mid}</div>
              <div className="flex items-center gap-2 text-primary-400"><Hash size={16}/> R: {step.right}</div>
              <div className="w-px h-5 bg-white/10 mx-2"></div>
              <div className="flex items-center gap-2 text-slate-300">Target: <span className="font-bold text-white">{step.target}</span></div>
              <div className={`flex items-center gap-2 ${step.found ? 'text-green-400 font-bold' : 'text-slate-400'}`}>
                Status: {step.found ? 'FOUND' : 'Searching...'}
              </div>
            </motion.div>
          </div>
        );
      
      case 'sorting':
        case 'bubble_sort':
        case 'merge_sort':
        case 'quick_sort':
        case 'insertion_sort':
        case 'selection_sort':
        const sortArray = step.array || visualizationData.initial_array || [];
        // prevent divide by zero bounds
        const maxVal = Math.max(...sortArray, 1);
        return (
          <div className="space-y-8 mt-4">
            <div className="h-48 flex items-end justify-center gap-1.5 md:gap-2">
              <AnimatePresence>
                {sortArray.map((value, index) => {
                  const heightPercentage = Math.max(10, (value / maxVal) * 100);
                  
                  let bgStyle = 'bg-primary-500/50 hover:bg-primary-500/80';
                  
                  if (step.comparing?.includes(index)) {
                     bgStyle = 'bg-accent-500 shadow-[0_0_15px_rgba(139,92,246,0.5)]';
                  } else if (step.swapped?.includes(index) || step.placed_index === index) {
                     bgStyle = 'bg-green-500 shadow-[0_0_15px_rgba(34,197,94,0.5)]';
                  }

                  return (
                    <motion.div
                      layout
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: `${heightPercentage}%` }}
                      transition={{ type: "spring", stiffness: 300, damping: 20 }}
                      key={index} // normally should use value if non repeating but index works for visual block shifting if we change state fully
                      className={`w-6 md:w-8 rounded-t-lg relative group transition-colors duration-200 ${bgStyle}`}
                    >
                      <div className="absolute -top-8 left-1/2 -translate-x-1/2 font-mono text-xs text-white opacity-0 group-hover:opacity-100 transition-opacity">
                        {value}
                      </div>
                    </motion.div>
                  );
                })}
              </AnimatePresence>
            </div>
            <motion.div 
              key={`desc-${currentStep}`}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-surface/50 border border-white/5 p-4 rounded-xl text-center text-slate-300 min-h-[4rem] flex items-center justify-center font-medium"
            >
              Step {currentStep + 1}: {step.description || "Executing sort operation..."}
            </motion.div>
          </div>
        );
      
      case 'dfs':
      case 'bfs':
      case 'dijkstra':
        const graphData = visualizationData.graph_data?.data;
        if (!graphData || !graphData.nodes) {
          return (
            <div className="p-8 text-center bg-surface/50 rounded-xl border border-white/5">
              <Layers size={32} className="mx-auto mt-2 text-slate-600 mb-3" />
              <p className="text-slate-400">Invalid graph data payload.</p>
            </div>
          );
        }

        return (
          <div className="space-y-4 mt-2 max-w-full overflow-x-auto hide-scrollbar">
            <div className="relative w-full h-64 sm:h-72 flex justify-center perspective-1000">
              <svg className="absolute inset-0 w-full h-full overflow-visible" viewBox="0 0 500 250">
                <defs>
                  <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="22" refY="3" orient="auto">
                    <polygon points="0 0, 8 3, 0 6" fill="rgba(255,255,255,0.2)"/>
                  </marker>
                </defs>
                
                {/* Edges */}
                <AnimatePresence>
                  {graphData.edges.map((edge, idx) => {
                    const fromNode = graphData.nodes.find(n => n.id === edge.from);
                    const toNode = graphData.nodes.find(n => n.id === edge.to);
                    if (!fromNode || !toNode) return null;
                    
                    // Check if this edge is active (the "previous" array could track it, but we can animate active transitions if the current visited path implies it).
                    const isVisited = step.visited_nodes?.includes(edge.from) && step.visited_nodes?.includes(edge.to);
                    
                    return (
                      <motion.line
                        key={`edge-${idx}`}
                        initial={{ pathLength: 0, opacity: 0 }}
                        animate={{ pathLength: 1, opacity: isVisited ? 0.8 : 0.2 }}
                        x1={fromNode.x}
                        y1={fromNode.y}
                        x2={toNode.x}
                        y2={toNode.y}
                        stroke={isVisited ? '#0ea5e9' : 'currentColor'}
                        strokeWidth={isVisited ? 3 : 2}
                        className={isVisited ? 'text-primary-500' : 'text-slate-600'}
                        markerEnd="url(#arrowhead)"
                      />
                    );
                  })}
                </AnimatePresence>

                {/* Nodes */}
                {graphData.nodes.map((node) => {
                  let status = 'unvisited';
                  let bgStyle = 'fill-[#1a1a24] stroke-[#334155]';
                  let textStyle = '#94a3b8';
                  let shadow = '';
                  
                  const stateNode = step.node_states?.find(n => n.id === node.id);
                  if (stateNode) status = stateNode.status;

                  if (status === 'visited') {
                    bgStyle = 'fill-[#0ea5e9]/20 stroke-[#0ea5e9]';
                    textStyle = '#bae6fd';
                  } else if (status === 'current') {
                    bgStyle = 'fill-[#a855f7] stroke-[#c084fc]';
                    textStyle = '#ffffff';
                    shadow = 'drop-shadow(0 0 12px rgba(168,85,247,0.8))';
                  } else if (status === 'highlighted') {
                    bgStyle = 'fill-[#38bdf8] stroke-[#7dd3fc]';
                    textStyle = '#ffffff';
                    shadow = 'drop-shadow(0 0 8px rgba(56,189,248,0.6))';
                  }

                  return (
                    <g key={`node-${node.id}`} className="transition-all duration-300 transform-gpu" style={{ filter: shadow }}>
                      <motion.circle
                        initial={{ scale: 0 }}
                        animate={{ scale: status === 'current' ? 1.1 : 1 }}
                        cx={node.x}
                        cy={node.y}
                        r="20"
                        className={`${bgStyle} stroke-2 transition-colors duration-300`}
                      />
                      <text
                        x={node.x}
                        y={node.y}
                        dy=".3em"
                        textAnchor="middle"
                        fill={textStyle}
                        className="font-mono text-sm font-bold transition-colors duration-300 pointer-events-none"
                      >
                        {node.label}
                      </text>
                      
                      {stateNode?.distance !== undefined && (
                        <text
                          x={node.x}
                          y={node.y - 25}
                          textAnchor="middle"
                          fill="#c084fc"
                          className="font-mono text-xs font-semibold"
                        >
                          {stateNode.distance === Infinity ? '∞' : stateNode.distance}
                        </text>
                      )}
                    </g>
                  );
                })}
              </svg>
            </div>

            {/* Step Description */}
            <motion.div 
              key={`desc-${currentStep}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-surface/50 border border-white/5 p-4 rounded-xl text-center text-slate-300 min-h-[4rem] flex flex-col items-center justify-center font-medium gap-2"
            >
              <div>{step.description || "Processing graph..."}</div>
              
              {/* Optional data structures context */}
              <div className="flex gap-4 text-xs font-mono mt-2">
                {step.stack && (
                  <div className="bg-white/5 px-3 py-1 rounded text-primary-300">
                    Stack: [{step.stack.join(', ')}]
                  </div>
                )}
                {step.queue && (
                  <div className="bg-white/5 px-3 py-1 rounded text-accent-300">
                    Queue: [{step.queue.join(', ')}]
                  </div>
                )}
              </div>
            </motion.div>
          </div>
        );
      
      default:
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold text-slate-200 flex items-center gap-2">
           <PlayCircle className="text-primary-400" size={24} />
           Execution Trace
        </h3>
        <div className="px-3 py-1 rounded-full bg-surface-lighter border border-white/10 text-slate-300 text-sm font-medium font-mono">
           Step {currentStep + 1} / {visualizationData.steps.length}
        </div>
      </div>
      
      <div className="glass-panel p-6 rounded-3xl min-h-[400px] flex flex-col justify-between relative overflow-hidden">
        {/* Background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-primary-500/5 rounded-full blur-[100px] pointer-events-none" />
        
        <div className="relative z-10 flex-1">
          {renderStepVisualization()}
        </div>
        
        <div className="relative z-10 mt-8 flex justify-center items-center gap-4 border-t border-white/5 pt-6">
          <button
            onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
            disabled={currentStep === 0}
            className="flex items-center gap-1.5 px-4 py-2 bg-surface-lighter hover:bg-white/10 border border-white/5 text-slate-300 rounded-lg disabled:opacity-30 disabled:hover:bg-surface-lighter transition-all"
          >
            <ChevronLeft size={18} /> Previous
          </button>
          
          <div className="flex flex-wrap justify-center gap-1.5 max-w-[150px] sm:max-w-[250px] md:max-w-[400px] max-h-[3rem] overflow-y-auto hide-scrollbar">
             {visualizationData.steps.map((_, i) => (
                <div 
                   key={i} 
                   className={`h-2 rounded-full transition-all duration-300 flex-shrink-0 ${
                      i === currentStep ? 'w-6 bg-primary-500 shadow-[0_0_8px_rgba(14,165,233,0.8)]' : 
                      i < currentStep ? 'w-2 bg-primary-500/50' : 'w-2 bg-white/10'
                   }`}
                />
             ))}
          </div>
          
          <button
            onClick={() => setCurrentStep(Math.min(visualizationData.steps.length - 1, currentStep + 1))}
            disabled={currentStep === visualizationData.steps.length - 1}
            className="flex items-center gap-1.5 px-4 py-2 bg-primary-600 hover:bg-primary-500 border border-primary-500/50 text-white rounded-lg disabled:opacity-30 disabled:hover:bg-primary-600 transition-all shadow-[0_0_15px_rgba(2,132,199,0.3)] disabled:shadow-none"
          >
            Next <ChevronRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default VisualizationPanel;
