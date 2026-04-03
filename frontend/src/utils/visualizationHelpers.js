export const generateVisualizationSteps = (algorithmType, array, target = null) => {
  switch (algorithmType) {
    case 'binary_search':
      return generateBinarySearchSteps(array, target);
    case 'bubble_sort':
      return generateBubbleSortSteps(array);
    case 'quick_sort':
      return generateQuickSortSteps(array);
    default:
      return [];
  }
};

export const generateBinarySearchSteps = (array, target) => {
  const steps = [];
  const arr = [...array];
  let left = 0;
  let right = arr.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    
    steps.push({
      array: [...arr],
      left,
      right,
      mid,
      target,
      found: arr[mid] === target,
      description: `Comparing arr[${mid}] = ${arr[mid]} with target ${target}`
    });

    if (arr[mid] === target) {
      break;
    } else if (arr[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return steps;
};

export const generateBubbleSortSteps = (array) => {
  const steps = [];
  const arr = [...array];
  const n = arr.length;

  for (let i = 0; i < n - 1; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      steps.push({
        array: [...arr],
        comparing: [j, j + 1],
        swapped: [],
        description: `Comparing ${arr[j]} and ${arr[j + 1]}`
      });

      if (arr[j] > arr[j + 1]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        
        steps.push({
          array: [...arr],
          comparing: [],
          swapped: [j, j + 1],
          description: `Swapped ${arr[j + 1]} and ${arr[j]}`
        });
      }
    }
  }

  steps.push({
    array: [...arr],
    comparing: [],
    swapped: [],
    description: 'Sorting complete!'
  });

  return steps;
};

export const generateQuickSortSteps = (array) => {
  const steps = [];
  const arr = [...array];

  const quickSort = (low, high) => {
    if (low < high) {
      const pivotIndex = partition(low, high);
      quickSort(low, pivotIndex - 1);
      quickSort(pivotIndex + 1, high);
    }
  };

  const partition = (low, high) => {
    const pivot = arr[high];
    let i = low - 1;

    steps.push({
      array: [...arr],
      comparing: [high],
      swapped: [],
      description: `Pivot selected: ${pivot} at position ${high}`
    });

    for (let j = low; j < high; j++) {
      steps.push({
        array: [...arr],
        comparing: [j, high],
        swapped: [],
        description: `Comparing ${arr[j]} with pivot ${pivot}`
      });

      if (arr[j] < pivot) {
        i++;
        [arr[i], arr[j]] = [arr[j], arr[i]];
        
        if (i !== j) {
          steps.push({
            array: [...arr],
            comparing: [],
            swapped: [i, j],
            description: `Swapped ${arr[i]} and ${arr[j]}`
          });
        }
      }
    }

    [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
    
    steps.push({
      array: [...arr],
      comparing: [],
      swapped: [i + 1, high],
      description: `Placed pivot ${pivot} at correct position ${i + 1}`
    });

    return i + 1;
  };

  quickSort(0, arr.length - 1);

  steps.push({
    array: [...arr],
    comparing: [],
    swapped: [],
    description: 'Quick sort complete!'
  });

  return steps;
};

export const formatComplexity = (complexity) => {
  if (!complexity) return 'Unknown';
  
  const formatted = complexity.replace(/O\((.*?)\)/, 'O($1)');
  return formatted;
};

export const getComplexityColor = (complexity) => {
  if (!complexity) return 'text-gray-600';
  
  if (complexity.includes('n^2') || complexity.includes('2^n')) {
    return 'text-red-600';
  } else if (complexity.includes('n log n')) {
    return 'text-yellow-600';
  } else if (complexity.includes('n') || complexity.includes('log n')) {
    return 'text-green-600';
  } else if (complexity.includes('1')) {
    return 'text-blue-600';
  }
  
  return 'text-gray-600';
};
