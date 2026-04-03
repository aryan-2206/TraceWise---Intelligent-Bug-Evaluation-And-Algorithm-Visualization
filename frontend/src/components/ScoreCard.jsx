import React from 'react';
import { motion } from 'framer-motion';
import { Activity, Beaker, CheckCircle2, Award } from 'lucide-react';

const ScoreCard = ({ score, details }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-400 border-green-500 bg-green-500/10 shadow-[0_0_20px_rgba(34,197,94,0.2)]';
    if (score >= 60) return 'text-amber-400 border-amber-500 bg-amber-500/10 shadow-[0_0_20px_rgba(245,158,11,0.2)]';
    return 'text-red-400 border-red-500 bg-red-500/10 shadow-[0_0_20px_rgba(239,68,68,0.2)]';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  };

  const metricIcons = {
    readability: <Activity size={16} />,
    efficiency: <Beaker size={16} />,
    correctness: <CheckCircle2 size={16} />,
    bestPractices: <Award size={16} />
  };
  const componentScores = details?.component_scores || details || {};

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel rounded-3xl p-8"
    >
      <div className="flex flex-col md:flex-row gap-8 items-center md:items-start">
        
        {/* Main Score */}
        <div className="flex-1 text-center md:text-left flex flex-col items-center md:items-start">
          <h3 className="text-xl font-semibold text-slate-200 mb-6">Overall Assessment</h3>
          
          <motion.div 
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 200, damping: 20, delay: 0.2 }}
            className={`w-40 h-40 rounded-full border-4 flex flex-col items-center justify-center ${getScoreColor(score)}`}
          >
            <span className="text-5xl font-black">{score}</span>
            <span className="text-sm font-medium uppercase tracking-widest mt-1 opacity-80">
              {getScoreLabel(score)}
            </span>
          </motion.div>
        </div>
        
        {/* Metric Breakdown (combined logic) */}
        {componentScores && (
          <div className="flex-1 w-full space-y-4">
            <h3 className="text-lg font-medium text-slate-300 mb-4 px-2">Metric Breakdown</h3>
            
            <div className="grid gap-3">
              {Object.entries({
                readability: componentScores.readability,
                efficiency: componentScores.efficiency,
                correctness: componentScores.correctness,
                bestPractices: componentScores.bestPractices ?? componentScores.best_practices
              }).map(([key, value], i) => (
                <motion.div 
                  key={key}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 * i }}
                  className="bg-surface p-4 rounded-xl flex items-center justify-between border border-white/5"
                >
                  <div className="flex items-center gap-3 text-slate-400 capitalize">
                    {metricIcons[key] || <Activity size={16} />}
                    <span className="font-medium text-sm">
                      {key.replace(/([A-Z])/g, ' $1').trim()}
                    </span>
                  </div>
                  
                  <span className="font-bold text-white bg-white/10 px-3 py-1 rounded-lg">
                    {value ?? 'N/A'}/100
                  </span>
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default ScoreCard;