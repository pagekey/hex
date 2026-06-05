// Copyright 2026 PageKey Solutions, LLC

import { useState, useCallback } from 'react';
import '@xyflow/react/dist/style.css';
import './App.css';
import GraphCanvas from './components/Canvas';
import ControlPanel from './components/ControlPanel';
import type { DataNode, Edge, Execution, ProcessNode } from './lib/models';

// --- MOCK DATA ---
const dummyExecutions: Execution[] = [
  {
    id: 'exec-001',
    timestamp: '2026-04-20 10:00:00',
    status: 'completed',
    dataNodes: [
      { id: '1', title: 'Trigger', value: 'manual', status: 'valid' }
    ],
    processNodes: [
      {
        id: '2',
        title: 'Logger',
        code: 'print()',
        inputs: { timestamp: '1679000000' },
        outputs: { stdout: 'Hello World printed' },
        status: 'completed'
      }
    ],
    edges: [{ start: '1', end: '2' }]
  },
  {
    id: 'exec-002',
    timestamp: '2026-04-20 10:05:30',
    status: 'failed',
    dataNodes: [
      {
        id: '1',
        title: 'Webhook Trigger',
        value: 'null',
        status: 'invalid'
      }
    ],
    processNodes: [
      {
        id: '2',
        title: 'Payload Processor',
        code: 'process(payload)',
        inputs: { timestamp: '1679000330', payload: 'null' },
        outputs: { error: 'Crash: Null pointer' },
        status: 'failed'
      },
      {
        id: '3',
        title: 'Data Archiver',
        code: 'save()',
        inputs: {},
        outputs: {},
        status: 'pending'
      }
    ],
    edges: [
      { start: '1', end: '2' },
      { start: '2', end: '3' }
    ]
  },
];

const dataNodes: DataNode[] = [
  { id: 'name-in', title: 'Name', value: '', status: 'valid' },
  { id: 'age-in', title: 'Age', value: '', status: 'valid' },
  { id: 'message-out', title: 'Message', value: '', status: 'pending' }
];

const processNodes: ProcessNode[] = [
  {
    id: 'greeter',
    title: 'Greeter',
    code: 'def greet(inputs: dict):\n    return None',
    inputs: { name: 'name-in', age: 'age-in' },
    outputs: { out: 'message-out' },
    status: 'pending'
  },
  {
    id: 'echo',
    title: 'Echo',
    code: 'echo()',
    inputs: { msg: 'message-out' },
    outputs: {},
    status: 'pending'
  }
];

const edges: Edge[] = [
  { start: 'name-in', end: 'greeter' },
  { start: 'age-in', end: 'greeter' },
  { start: 'greeter', end: 'message-out' },
  { start: 'message-out', end: 'echo' }
];

// --- MAIN APP COMPONENT ---
function App() {

  const [activeTab, setActiveTab] = useState('run'); // 'run' | 'executions'
  const [executions, setExecutions] = useState(dummyExecutions);
  const [activeExecution, setActiveExecution] = useState<any>(null);
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [currentDataNodes, setCurrentDataNodes] = useState<DataNode[]>(dataNodes);

  const onNodeClick = useCallback((_: any, node: any) => {
    setSelectedNode(node);
  }, []);

  const updateDataNodeValue = (id: string, newValue: string) => {
    setCurrentDataNodes(prev => prev.map(n => n.id === id ? { ...n, value: newValue } : n));
  };


  const handleRunGraph = () => {

    // Mocking a new execution run
    const newExec: Execution = {
      id: `exec-00${executions.length + 1}`,
      timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
      status: 'completed', // 'completed' matches the interface, 'success' was the dummy format
      dataNodes: [
        {
          id: '1',
          title: 'Manual Trigger',
          value: 'manual_run',
          status: 'valid'
        }
      ],
      processNodes: [
        {
          id: '2',
          title: 'Task Processor',
          code: 'process()',
          inputs: { ok: 'true' },
          outputs: { ran: 'true' },
          status: 'completed'
        },
        {
          id: '3',
          title: 'System Exit',
          code: 'exit()',
          inputs: { ran: 'true' },
          outputs: { exitCode: '0' },
          status: 'completed'
        }
      ],
      edges: [
        { start: '1', end: '2' },
        { start: '2', end: '3' }
      ]
    };
    setExecutions([newExec as any, ...executions]);
    setActiveExecution(newExec);
    setActiveTab('executions');
    setSelectedNode(null);
  };

  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh', fontFamily: 'sans-serif' }}>

      {/* LEFT PANEL: ReactFlow Canvas */}
      <GraphCanvas
        dataNodes={currentDataNodes}
        processNodes={processNodes}
        edges={edges}
        onNodeClick={onNodeClick}
        setSelectedNode={setSelectedNode}
      />

      {/* RIGHT PANEL: Controls and State Inspection */}
      <ControlPanel
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        activeExecution={activeExecution}
        setActiveExecution={setActiveExecution}
        selectedNode={selectedNode}
        setSelectedNode={setSelectedNode}
        handleRunGraph={handleRunGraph}
        executions={executions}
        dataNodes={currentDataNodes}
        processNodes={processNodes}
        updateDataNodeValue={updateDataNodeValue}
      />
    </div>
  );
}

export default App;
