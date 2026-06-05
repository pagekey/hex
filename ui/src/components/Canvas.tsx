// Copyright 2026 PageKey Solutions, LLC

import { Background, Controls, ReactFlow } from "@xyflow/react";
import type { DataNode, Edge, ProcessNode } from "../lib/models";

// Helper to determine node styles based on status and selection
const getNodeStyle = (node: DataNode | ProcessNode, isSelected: boolean, isInput: boolean) => {
    let borderColor = isInput ? '#ddd' : '#777';
    let bgColor = '#fff';

    // Status-based coloring
    if (node.status === 'completed' || node.status === 'valid') {
        borderColor = 'green';
        bgColor = '#e8f5e9';
    } else if (node.status === 'failed' || node.status === 'invalid') {
        borderColor = 'red';
        bgColor = '#ffebee';
    } else if (node.status === 'pending') {
        borderColor = 'gray';
        bgColor = '#f5f5f5';
    }

    // Selection-based coloring (overrides status)
    if (isSelected) {
        borderColor = '#007bff';
        bgColor = '#e3f2fd';
    }

    return {
        width: isInput ? 80 : 70,
        height: isInput ? 80 : 70,
        borderRadius: '50%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        border: `2px solid ${borderColor}`,
        background: bgColor,
        fontSize: isInput ? 'inherit' : '12px'
    };
};

const convertToGraphElements = (
    dataNodes: DataNode[],
    processNodes: (ProcessNode & { id: string })[],
    edges: Edge[],
    selectedNodeId?: string
) => {
    // Mapping Data Nodes (Inputs/Outputs)
    const mappedDataNodes = dataNodes.map((node, index) => {
        const isInput = node.id.includes('in');
        const isSelected = selectedNodeId === node.id;

        return {
            id: node.id,
            type: isInput ? 'input' : undefined,
            position: isInput
                ? { x: 150 + (index * 110), y: 0 }
                : { x: 205, y: 220 },
            data: {
                label: (
                    <div style={{ display: 'flex', flexDirection: 'column', lineHeight: '1.2' }}>
                        <span style={{ fontSize: '10px', fontWeight: 'bold', textTransform: 'uppercase', color: '#888' }}>
                            {node.title}
                        </span>
                        <span style={{ fontSize: '16px', fontWeight: '500' }}>
                            {node.value || "(empty)"}
                        </span>
                    </div>
                )
            },
            style: getNodeStyle(node, isSelected, isInput)
        };
    });

    // Mapping Process Nodes
    const mappedProcessNodes = processNodes.map((node) => {
        const isEcho = node.id === 'echo';
        const isSelected = selectedNodeId === node.id;

        return {
            id: node.id,
            type: isEcho ? 'output' : undefined,
            data: { label: node.title },
            position: isEcho ? { x: 185, y: 340 } : { x: 195, y: 120 },
            style: getNodeStyle(node, isSelected, false)
        };
    });

    // Mapping Edges
    const mappedEdges = edges.map((edge) => ({
        id: `e-${edge.start}-${edge.end}`,
        source: edge.start,
        target: edge.end,
        markerEnd: { type: 'arrowclosed' }
    }));

    return {
        nodes: [...mappedDataNodes, ...mappedProcessNodes],
        edges: mappedEdges
    };
};

interface GraphCanvasProps {
    dataNodes: DataNode[]
    processNodes: ProcessNode[]
    edges: Edge[]
    onNodeClick: any
    setSelectedNode: Function
    selectedNode?: any // Added to track selection state
}

export default function GraphCanvas(props: GraphCanvasProps) {
    // We compute the elements directly during render. 
    // React Flow handles the efficient updating.
    const { nodes, edges } = convertToGraphElements(
        props.dataNodes,
        props.processNodes,
        props.edges,
        props.selectedNode?.id
    );

    return (
        <div style={{ flex: 1, backgroundColor: '#fdfdfd', position: 'relative', height: '100%' }}>
            <ReactFlow
                nodes={nodes as any}
                edges={edges as any}
                onNodeClick={props.onNodeClick}
                onPaneClick={() => props.setSelectedNode(null)}
                fitView
                nodesDraggable={false}
                nodesConnectable={false}
                elementsSelectable={true}
            >
                <Background gap={12} size={1} />
                <Controls />
            </ReactFlow>
        </div>
    );
}
