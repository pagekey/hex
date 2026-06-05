// Copyright 2026 PageKey Solutions, LLC

import type { DataNode, ProcessNode, Execution } from "../lib/models"
import Prism from 'prismjs';
import 'prismjs/themes/prism.css';
import 'prismjs/components/prism-python';


interface ControlPanelProps {
    activeTab: string
    setActiveTab: Function
    activeExecution: Execution | null // Using the Execution interface
    setActiveExecution: Function
    selectedNode: any
    setSelectedNode: Function
    handleRunGraph: any
    executions: Execution[]
    dataNodes: DataNode[]
    processNodes: ProcessNode[]
    updateDataNodeValue?: (id: string, value: string) => void
}

export default function ControlPanel(props: ControlPanelProps) {
    // Helper to find node data within the structured Execution model
    const getSelectedNodeData = () => {
        if (!props.selectedNode) return null;

        if (props.activeExecution) {
            // Check both dataNodes and processNodes for the ID within an execution
            return props.activeExecution.dataNodes.find(n => n.id === props.selectedNode.id) ||
                props.activeExecution.processNodes.find(n => n.id === props.selectedNode.id);
        }

        // Check base dataNodes and processNodes if no active execution
        return props.dataNodes.find(n => n.id === props.selectedNode.id) ||
            props.processNodes.find(n => n.id === props.selectedNode.id);
    };

    const nodeData = getSelectedNodeData();
    const isRunDisabled = props.dataNodes.some(n => !n.value);

    return (
        <div style={{ width: '350px', borderLeft: '1px solid #ddd', display: 'flex', flexDirection: 'column', backgroundColor: '#fff' }}>

            {/* TABS */}
            <div style={{ display: 'flex', borderBottom: '1px solid #ddd' }}>
                <button
                    style={{ flex: 1, padding: '15px', cursor: 'pointer', border: 'none', background: props.activeTab === 'run' ? '#f0f0f0' : 'transparent', fontWeight: props.activeTab === 'run' ? 'bold' : 'normal' }}
                    onClick={() => { props.setActiveTab('run'); props.setActiveExecution(null); props.setSelectedNode(null); }}
                >
                    Run Graph
                </button>
                <button
                    style={{ flex: 1, padding: '15px', cursor: 'pointer', border: 'none', background: props.activeTab === 'executions' ? '#f0f0f0' : 'transparent', fontWeight: props.activeTab === 'executions' ? 'bold' : 'normal' }}
                    onClick={() => props.setActiveTab('executions')}
                >
                    Executions
                </button>
            </div>

            {/* TAB CONTENT */}
            <div style={{ flex: 1, overflowY: 'auto', padding: '20px' }}>

                {/* RUN TAB */}
                {props.activeTab === 'run' && (
                    <div>
                        <h3>Node Details</h3>
                        {!props.selectedNode ? (
                            <p style={{ fontSize: '14px', color: '#666' }}>Select a node to view details.</p>
                        ) : (
                            <div>
                                <h4 style={{ margin: '0 0 10px 0' }}>Node: {nodeData?.title || 'Unknown'}</h4>

                                <p style={{ fontSize: '14px', margin: '0 0 5px 0' }}>
                                    <strong>Type:</strong> {'value' in (nodeData || {}) ? 'Data Node' : 'Process Node'}
                                </p>

                                <p style={{ fontSize: '14px', margin: '0 0 5px 0' }}><strong>Status:</strong> {nodeData?.status || 'N/A'}</p>

                                <p style={{ fontSize: '14px', margin: '15px 0 5px 0' }}><strong>Data/Inputs:</strong></p>
                                {nodeData && 'value' in nodeData ? (
                                    <input
                                        type="text"
                                        value={nodeData.value}
                                        onChange={(e) => props.updateDataNodeValue?.(nodeData.id, e.target.value)}
                                        style={{ width: '100%', padding: '8px', boxSizing: 'border-box', border: '1px solid #ccc', borderRadius: '4px' }}
                                        placeholder={nodeData.status == "pending" ? "(upstream node has not run yet)" : `Value for ${nodeData.title}`}
                                        disabled={nodeData.status == "pending"}
                                    />
                                ) : (
                                    <>
                                        <pre style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px', fontSize: '12px', overflowX: 'auto' }}>
                                            {nodeData
                                                ? JSON.stringify(nodeData.inputs, null, 2)
                                                : '"No data available"'}
                                        </pre>
                                        {nodeData && 'code' in nodeData && (
                                            <>
                                                <p style={{ fontSize: '14px', margin: '15px 0 5px 0' }}><strong>Code:</strong></p>
                                                <pre className="language-javascript" style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px', fontSize: '12px', overflowX: 'auto', margin: 0 }}>
                                                    <code dangerouslySetInnerHTML={{
                                                        __html: Prism.highlight(nodeData.code, Prism.languages.python, 'python')
                                                    }} />
                                                </pre>
                                            </>
                                        )}
                                    </>
                                )}
                            </div>
                        )}

                        <hr style={{ margin: '20px 0', border: 'none', borderTop: '1px solid #ddd' }} />

                        <button
                            onClick={props.handleRunGraph}
                            disabled={isRunDisabled}
                            style={{
                                width: '100%',
                                padding: '10px',
                                backgroundColor: isRunDisabled ? '#ccc' : '#007bff',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: isRunDisabled ? 'not-allowed' : 'pointer',
                                fontWeight: 'bold'
                            }}
                        >
                            Execute Graph
                        </button>
                    </div>
                )}

                {/* EXECUTIONS TAB */}
                {props.activeTab === 'executions' && !props.activeExecution && (
                    <div>
                        <h3>Execution History</h3>
                        {props.executions.map(exec => (
                            <div
                                key={exec.id}
                                onClick={() => { props.setActiveExecution(exec); props.setSelectedNode(null); }}
                                style={{ padding: '10px', border: '1px solid #ddd', marginBottom: '10px', borderRadius: '4px', cursor: 'pointer', borderLeft: `5px solid ${exec.status === 'completed' ? 'green' : 'red'}` }}
                            >
                                <div style={{ fontWeight: 'bold' }}>{exec.id}</div>
                                <div style={{ fontSize: '12px', color: '#666' }}>{exec.timestamp}</div>
                            </div>
                        ))}
                    </div>
                )}

                {/* ACTIVE EXECUTION DETAILS */}
                {props.activeTab === 'executions' && props.activeExecution && (
                    <div>
                        <button
                            onClick={() => props.setActiveExecution(null)}
                            style={{ background: 'none', border: 'none', color: '#007bff', cursor: 'pointer', padding: '0 0 15px 0', fontSize: '14px' }}
                        >
                            &larr; Back to History
                        </button>
                        <h3>Run Details: {props.activeExecution.id}</h3>
                        <p><strong>Status:</strong> <span style={{ color: props.activeExecution.status === 'completed' ? 'green' : 'red' }}>{props.activeExecution.status.toUpperCase()}</span></p>

                        <hr style={{ margin: '20px 0', border: 'none', borderTop: '1px solid #ddd' }} />

                        {!props.selectedNode ? (
                            <div>
                                <h4 style={{ margin: '0 0 10px 0' }}>Execution Overview</h4>
                                <p style={{ fontSize: '14px' }}>Nodes: {props.activeExecution.dataNodes.length + props.activeExecution.processNodes.length}</p>
                                <p style={{ fontSize: '14px' }}>Edges: {props.activeExecution.edges.length}</p>

                                <p style={{ fontSize: '12px', color: '#888', marginTop: '20px' }}><em>Click on a node in the graph to see its specific inputs, outputs, and status.</em></p>
                            </div>
                        ) : (
                            <div>
                                <h4 style={{ margin: '0 0 10px 0' }}>Node Detail: {nodeData?.title || 'Unknown'}</h4>

                                <p style={{ fontSize: '14px', margin: '0 0 5px 0' }}><strong>Status:</strong> {nodeData?.status || 'N/A'}</p>

                                <p style={{ fontSize: '14px', margin: '15px 0 5px 0' }}><strong>Data/Inputs:</strong></p>
                                <pre style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px', fontSize: '12px', overflowX: 'auto' }}>
                                    {nodeData
                                        ? JSON.stringify('value' in nodeData ? { value: nodeData.value } : nodeData.inputs, null, 2)
                                        : '"No data available for this execution"'}
                                </pre>

                                {nodeData && 'code' in nodeData && (
                                    <>
                                        <p style={{ fontSize: '14px', margin: '15px 0 5px 0' }}><strong>Code:</strong></p>
                                        <pre className="language-javascript" style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px', fontSize: '12px', overflowX: 'auto', margin: 0 }}>
                                            <code dangerouslySetInnerHTML={{
                                                __html: Prism.highlight(nodeData.code, Prism.languages.javascript, 'javascript')
                                            }} />
                                        </pre>
                                    </>
                                )}

                                {/* Only try to render outputs if nodeData exists AND has an outputs property */}
                                {nodeData && 'outputs' in nodeData && (
                                    <>
                                        <p style={{ fontSize: '14px', margin: '15px 0 5px 0' }}><strong>Outputs generated:</strong></p>
                                        <pre style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px', fontSize: '12px', overflowX: 'auto' }}>
                                            {JSON.stringify(nodeData.outputs, null, 2)}
                                        </pre>
                                    </>
                                )}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}
